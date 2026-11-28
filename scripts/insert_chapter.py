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

from book_paths import find_direct_section_entries, list_section_entries
from index_paths import (
    index_filename,
    metadata_directory,
    metadata_index_path,
    migrate_indexes_to_metadata,
)

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
    for p, kind in list_section_entries(parent):
        if kind != "directory":
            continue
        m = DIR_NAME_RE.match(p.name)
        if m:
            raw_num = m.group(1)
            result.append((number_parts(raw_num), raw_num, p))
    result.sort(key=lambda item: item[0])
    return result


def list_numbered_markdown_files(parent: Path) -> List[Tuple[List[int], str, Path]]:
    result: List[Tuple[List[int], str, Path]] = []
    for p, kind in list_section_entries(parent):
        if kind != "file":
            continue
        m = DIR_NAME_RE.match(p.stem)
        if m:
            raw_num = m.group(1)
            result.append((number_parts(raw_num), raw_num, p))
    result.sort(key=lambda item: item[0])
    return result


def list_numbered_entries(parent: Path) -> List[Tuple[List[int], str, Path]]:
    result = list_numbered_dirs(parent) + list_numbered_markdown_files(parent)
    result.sort(key=lambda item: item[0])
    return result


def find_entry_by_parts(parent: Path, target_parts: List[int]) -> Optional[Path]:
    matches = find_direct_section_entries(parent, format_parts(target_parts))
    return matches[0][0] if matches else None


def parent_prefers_markdown(parent: Path) -> bool:
    """目标节所在目录以 Markdown 文件为主时，插入同类型 Markdown 节。"""
    md_count = len(list_numbered_markdown_files(parent))
    dir_count = len(list_numbered_dirs(parent))
    return md_count > dir_count


def find_dir_by_parts(parent: Path, target_parts: List[int]) -> Optional[Path]:
    matches = find_direct_section_entries(
        parent,
        format_parts(target_parts),
        kind="directory",
    )
    return matches[0][0] if matches else None


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
            for item in list_numbered_entries(current)
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
    existing = find_entry_by_parts(parent_dir_probe, target_parts)
    prefer_markdown = parent_prefers_markdown(parent_dir_probe)
    widths = resolve_level_widths(
        textbook_root, target_parts, has_existing_at_target=(existing is not None)
    )

    formatted_target_num = format_parts(target_parts, widths)
    new_dir_name = f"{formatted_target_num}_{dir_suffix}"
    level_count = (
        len(list_numbered_entries(parent_dir_probe)) + 1
        if existing is not None
        else max(len(list_numbered_entries(parent_dir_probe)) + 1, target_parts[-1])
    )

    print(f"目标编号 : {formatted_target_num} (输入: {raw_num})")
    print(f"当前层总节数(插入后): {level_count} → 该层数字位宽: {widths[-1]}")
    new_markdown_name = f"{formatted_target_num}_{dir_suffix}.md"
    print(f"新节点名 : {new_markdown_name if prefer_markdown else new_dir_name}")
    print(f"题目     : {formatted_target_num} {clean_chapter}")
    print(f"介绍     : 介绍：{clean_chapter}")
    print()

    parent_dir = find_parent_dir(textbook_root, target_parts, widths)
    print(
        f"父目录   : "
        f"{parent_dir.relative_to(textbook_root) if parent_dir != textbook_root else '(教材根目录)'}"
    )
    print()
    insert_path = (
        parent_dir / new_markdown_name
        if prefer_markdown
        else parent_dir / new_dir_name
    )
    if existing is not None:
        print(f"注意: 编号 {formatted_target_num} 已存在 → {existing.name}")
        print("将把该节点及之后的所有兄弟节点整体 +1（并按新位宽格式化）后，再插入新节点。\n")

    siblings = list_numbered_entries(parent_dir)
    to_shift = [
        (parts, num_str, path)
        for parts, num_str, path in siblings
        if len(parts) == len(target_parts) and parts >= target_parts
    ]
    if insert_path.exists() and all(path != insert_path for _, _, path in to_shift):
        raise FileExistsError(f"节点已存在: {insert_path}")
    if not dry_run:
        migrate_indexes_to_metadata(textbook_root)

    if to_shift:
        print(f"需要重编号/后移的同级节点（共 {len(to_shift)} 个）:")
        for _, _, path in to_shift:
            print(f"  {path.name}")
        print()

        metadata_renames: list[tuple[Path, Path]] = []
        meta_dir = metadata_directory(textbook_root)
        for parts, _, path in sorted(to_shift, key=lambda item: item[0], reverse=True):
            shifted_parts = list(parts)
            shifted_parts[-1] += 1
            old_formatted = format_parts(parts, widths)
            new_formatted = format_parts(shifted_parts, widths)
            print(f"后移子树: {old_formatted}  →  {new_formatted}")
            if path.is_dir():
                match = DIR_NAME_RE.match(path.name)
                if match is not None:
                    new_name = f"{new_formatted}_{match.group(2)}"
                    new_path = path.parent / new_name
                    if dry_run:
                        print(f"  [DRY] 重命名: {path.name}  →  {new_name}")
                    else:
                        metadata_renames.append(
                            (
                                meta_dir / index_filename(path),
                                meta_dir / index_filename(new_path),
                            )
                        )
                        print(f"  重命名: {path.name}  →  {new_name}")
                        path.rename(new_path)
            else:
                match = DIR_NAME_RE.match(path.stem)
                if match is not None:
                    new_name = f"{new_formatted}_{match.group(2)}.md"
                    new_path = path.parent / new_name
                    if dry_run:
                        print(f"  [DRY] 重命名: {path.name}  →  {new_name}")
                    else:
                        print(f"  重命名: {path.name}  →  {new_name}")
                        path.rename(new_path)
            print()
        if not dry_run:
            sources = {old for old, _ in metadata_renames if old.is_file()}
            for _, target in metadata_renames:
                if target.exists() and target not in sources:
                    raise FileExistsError(f"元数据索引目标已存在: {target}")
            temporary_renames: list[tuple[Path, Path]] = []
            for index, (old, new) in enumerate(metadata_renames):
                if not old.is_file() or old == new:
                    continue
                temporary = meta_dir / f".__insert_index_{index}.tmp"
                old.rename(temporary)
                temporary_renames.append((temporary, new))
            for temporary, target in temporary_renames:
                temporary.rename(target)
    else:
        print("没有需要后移的同级节点，直接插入。\n")

    if dry_run:
        print(f"[DRY] 将创建{'Markdown 文件' if prefer_markdown else '目录'}: {insert_path}")
    elif prefer_markdown:
        insert_path.touch()
        print(f"已创建Markdown文件: {insert_path.relative_to(textbook_root)}")
    else:
        insert_path.mkdir(parents=False)
        index_path = metadata_index_path(textbook_root, insert_path)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.touch()
        print(f"已创建目录: {insert_path.relative_to(textbook_root)}")

    print("\n完成。")
    return insert_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="在教材目录树中按编号插入新的一节（两个参数：节编号、章节名）"
    )
    parser.add_argument("section_num", help="节编号，例如 2.1.3")
    parser.add_argument("chapter_name", help='章节名，例如 "name of the chapter"')
    parser.add_argument("--dry-run", action="store_true", help="仅预览变更，不修改磁盘")
    args = parser.parse_args()

    textbook_root = Path.cwd().resolve()

    has_chapter = bool(list_section_entries(textbook_root))
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
