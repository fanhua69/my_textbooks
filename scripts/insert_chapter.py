#!/usr/bin/env python3
"""
insert_chapter.py — 在教材目录树中按编号插入新的一节（自动重编号后续兄弟节点及子树）

用法:
    python insert_chapter.py "<节编号>" "<章节名>" [--dry-run]

示例:
    python insert_chapter.py "1.1" "smart pointers"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

NUMBER_ONLY_RE = re.compile(r"^\d+(?:\.\d+)*$")
DIR_NAME_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")


def validate_section_num(num: str) -> str:
    cleaned = num.strip()
    if not NUMBER_ONLY_RE.match(cleaned):
        raise ValueError(f"无法解析节编号: {num!r}\n正确格式示例: 2.1.3")
    return cleaned


def chapter_to_dir_suffix(chapter_name: str) -> str:
    words = chapter_name.strip().split()
    if not words:
        raise ValueError("章节名不能为空")
    return "_".join(words)


def chapter_to_intro_text(chapter_name: str) -> str:
    words = chapter_name.strip().split()
    if not words:
        raise ValueError("章节名不能为空")
    return " ".join(words)


def number_parts(num: str) -> List[int]:
    return [int(x) for x in num.split(".")]


def calc_width(total_count: int) -> int:
    return max(1, len(str(max(0, total_count))))


def format_parts(parts: List[int], widths: Optional[List[int]] = None) -> str:
    if not parts:
        return ""
    formatted: List[str] = []
    for idx, val in enumerate(parts):
        w = widths[idx] if widths and idx < len(widths) else 1
        formatted.append(f"{val:0{w}d}")
    return ".".join(formatted)


def parent_number_parts(parts: List[int]) -> Optional[List[int]]:
    if len(parts) <= 1:
        return None
    return parts[:-1]


def is_same_or_descendant_parts(prefix_parts: List[int], full_parts: List[int]) -> bool:
    if len(full_parts) < len(prefix_parts):
        return False
    return full_parts[: len(prefix_parts)] == prefix_parts


def replace_prefix_parts(
    full_parts: List[int],
    old_prefix_parts: List[int],
    new_prefix_parts: List[int],
) -> List[int]:
    suffix = full_parts[len(old_prefix_parts) :]
    return list(new_prefix_parts) + suffix


def list_numbered_dirs(parent: Path) -> List[Tuple[List[int], str, Path]]:
    result: List[Tuple[List[int], str, Path]] = []
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        m = DIR_NAME_RE.match(p.name)
        if m:
            raw_num = m.group(1)
            result.append((number_parts(raw_num), raw_num, p))
    result.sort(key=lambda item: item[0])
    return result


def find_dir_by_parts(parent: Path, target_parts: List[int]) -> Optional[Path]:
    for parts, _, path in list_numbered_dirs(parent):
        if parts == target_parts:
            return path
    return None


def has_prefix_in_children(parent: Path, prefix_parts: List[int]) -> bool:
    for parts, _, _ in list_numbered_dirs(parent):
        if is_same_or_descendant_parts(prefix_parts, parts):
            return True
    return False


def resolve_level_widths(
    textbook_root: Path,
    target_parts: List[int],
    has_existing_at_target: bool,
) -> List[int]:
    widths: List[int] = []
    current = textbook_root

    for depth in range(1, len(target_parts) + 1):
        prefix = target_parts[:depth]
        parent_prefix = prefix[:-1]
        siblings = [
            item
            for item in list_numbered_dirs(current)
            if len(item[0]) == depth and item[0][:-1] == parent_prefix
        ]
        existing_count = len(siblings)

        if depth < len(target_parts):
            level_total = existing_count
        else:
            if has_existing_at_target:
                level_total = existing_count + 1
            else:
                level_total = max(existing_count + 1, prefix[-1])

        widths.append(calc_width(max(level_total, prefix[-1])))

        if depth < len(target_parts):
            next_dir = find_dir_by_parts(current, prefix)
            if next_dir is not None:
                current = next_dir
            elif not has_prefix_in_children(current, prefix):
                partial_str = format_parts(prefix, widths)
                raise FileNotFoundError(
                    f"找不到编号为 {partial_str} 的目录（在 {current} 下）\n"
                    f"请确认教材根目录是否正确，以及目录命名是否符合「编号_名字」格式。"
                )

    return widths


def rename_subtree(
    subtree_root: Path,
    old_prefix_parts: List[int],
    new_prefix_parts: List[int],
    widths: List[int],
    dry_run: bool = False,
) -> None:
    to_rename: List[Tuple[Path, str]] = []

    def collect(current: Path) -> None:
        for child in sorted(current.iterdir(), key=lambda p: p.name, reverse=True):
            if child.is_dir():
                collect(child)
        m = DIR_NAME_RE.match(current.name)
        if m:
            raw_number = m.group(1)
            raw_components = raw_number.split(".")
            cur_parts = number_parts(raw_number)
            if is_same_or_descendant_parts(old_prefix_parts, cur_parts):
                updated_parts = replace_prefix_parts(
                    cur_parts, old_prefix_parts, new_prefix_parts
                )
                formatted_prefix = format_parts(
                    updated_parts[: len(new_prefix_parts)], widths
                )
                suffix_components = raw_components[len(old_prefix_parts) :]
                new_num_str = ".".join(
                    [formatted_prefix, *suffix_components]
                )
                new_name = f"{new_num_str}_{m.group(2)}"
                to_rename.append((current, new_name))

    collect(subtree_root)

    for old_path, new_name in to_rename:
        new_path = old_path.parent / new_name
        if dry_run:
            print(f"  [DRY] 重命名: {old_path.name}  →  {new_name}")
        else:
            print(f"  重命名: {old_path.name}  →  {new_name}")
            old_path.rename(new_path)


def find_parent_dir(
    textbook_root: Path, target_parts: List[int], widths: List[int]
) -> Path:
    p_parts = parent_number_parts(target_parts)
    if p_parts is None:
        return textbook_root

    current = textbook_root
    for depth in range(1, len(p_parts) + 1):
        partial_parts = p_parts[:depth]
        found = find_dir_by_parts(current, partial_parts)
        if found is not None:
            current = found
        elif not has_prefix_in_children(current, partial_parts):
            partial_str = format_parts(partial_parts, widths[:depth])
            raise FileNotFoundError(
                f"找不到编号为 {partial_str} 的目录（在 {current} 下）\n"
                f"请确认教材根目录是否正确，以及目录命名是否符合「编号_名字」格式。"
            )
    return current


def build_index_md(
    number: str,
    chapter_name: str,
    parent_num: Optional[str],
) -> str:
    heading_title = f"{number} {chapter_name}"
    intro_line = f"介绍：{chapter_name}"
    parent_link = "../index.md" if parent_num else "(教材根目录)"
    return f"""# {heading_title}

{intro_line}

---

## 导航

- **上一层**：[父级]({parent_link})
- **前一节**：[TODO_PREV]
- **后一节**：[TODO_NEXT]
"""


def insert_chapter(
    textbook_root: Path,
    section_num: str,
    chapter_name: str,
    dry_run: bool = False,
) -> Path:
    raw_num = validate_section_num(section_num)
    target_parts = number_parts(raw_num)
    dir_suffix = chapter_to_dir_suffix(chapter_name)
    clean_chapter = chapter_to_intro_text(chapter_name)

    parent_dir_probe = find_parent_dir(
        textbook_root, target_parts, [calc_width(999)] * len(target_parts)
    )
    existing = find_dir_by_parts(parent_dir_probe, target_parts)
    widths = resolve_level_widths(
        textbook_root, target_parts, has_existing_at_target=(existing is not None)
    )

    formatted_target_num = format_parts(target_parts, widths)
    new_dir_name = f"{formatted_target_num}_{dir_suffix}"
    level_count = (
        len(list_numbered_dirs(parent_dir_probe)) + 1
        if existing is not None
        else max(len(list_numbered_dirs(parent_dir_probe)) + 1, target_parts[-1])
    )

    print(f"目标编号 : {formatted_target_num} (输入: {raw_num})")
    print(f"当前层总节数(插入后): {level_count} → 该层数字位宽: {widths[-1]}")
    print(f"新目录名 : {new_dir_name}")
    print(f"题目     : {formatted_target_num} {clean_chapter}")
    print(f"介绍     : 介绍：{clean_chapter}")
    print()

    parent_dir = find_parent_dir(textbook_root, target_parts, widths)
    print(
        f"父目录   : "
        f"{parent_dir.relative_to(textbook_root) if parent_dir != textbook_root else '(教材根目录)'}"
    )
    print()

    if existing is not None:
        print(f"注意: 编号 {formatted_target_num} 已存在 → {existing.name}")
        print("将把该节点及之后的所有兄弟节点整体 +1（并按新位宽格式化）后，再插入新节点。\n")

    siblings = list_numbered_dirs(parent_dir)
    to_shift = [
        (parts, num_str, path)
        for parts, num_str, path in siblings
        if len(parts) == len(target_parts) and parts >= target_parts
    ]

    if to_shift:
        print(f"需要重编号/后移的同级节点（共 {len(to_shift)} 个）:")
        for _, _, path in to_shift:
            print(f"  {path.name}")
        print()

        for parts, _, path in sorted(to_shift, key=lambda item: item[0], reverse=True):
            shifted_parts = list(parts)
            shifted_parts[-1] += 1
            old_formatted = format_parts(parts, widths)
            new_formatted = format_parts(shifted_parts, widths)
            print(f"后移子树: {old_formatted}  →  {new_formatted}")
            rename_subtree(path, parts, shifted_parts, widths, dry_run=dry_run)
            print()
    else:
        print("没有需要后移的同级节点，直接插入。\n")

    new_path = parent_dir / new_dir_name
    if new_path.exists():
        raise FileExistsError(f"目录已存在: {new_path}")

    if dry_run:
        print(f"[DRY] 将创建目录: {new_path}")
    else:
        new_path.mkdir(parents=False)
        print(f"已创建目录: {new_path.relative_to(textbook_root)}")

    p_parts = parent_number_parts(target_parts)
    p_formatted = format_parts(p_parts, widths[:-1]) if p_parts is not None else None
    index_content = build_index_md(
        number=formatted_target_num,
        chapter_name=clean_chapter,
        parent_num=p_formatted,
    )

    index_path = new_path / "index.md"
    if dry_run:
        print(f"[DRY] 将写入: {index_path}")
        print("--- index.md 预览 ---")
        print(index_content)
        print("---------------------")
    else:
        index_path.write_text(index_content, encoding="utf-8")
        print(f"已写入   : {index_path.relative_to(textbook_root)}")

    print("\n完成。")
    return new_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="在教材目录树中按编号插入新的一节（两个参数：节编号、章节名）"
    )
    parser.add_argument("section_num", help="节编号，例如 2.1.3")
    parser.add_argument("chapter_name", help='章节名，例如 "name of the chapter"')
    parser.add_argument("--dry-run", action="store_true", help="仅预览变更，不修改磁盘")
    args = parser.parse_args()

    textbook_root = Path.cwd().resolve()

    has_chapter = any(
        p.is_dir() and DIR_NAME_RE.match(p.name)
        for p in textbook_root.iterdir()
    )
    if not has_chapter:
        print(f"警告: 当前目录 {textbook_root} 下没有发现「数字_名字」格式的章节目录。")
        print("请确认你是在教材根目录下运行本脚本。\n")

    try:
        insert_chapter(
            textbook_root=textbook_root,
            section_num=args.section_num,
            chapter_name=args.chapter_name,
            dry_run=args.dry_run,
        )
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
