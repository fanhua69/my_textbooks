#!/usr/bin/env python3
"""
insert_chapter.py — 在教材目录树中按编号插入新的一节（自动重编号后续兄弟节点及子树）

数字位宽规则：
    某个节层级的数字位数（如 1、01、001）由“插入后该层级的总节数”决定：
    - 总节数 < 10  → 1 位（如 1, 2, 9）
    - 总节数 10~99 → 2 位（如 01, 02, 13）
    - 总节数 100~999 → 3 位（如 001, 002）
    新插入的节以及被移动的同级节点（及其子树）都会按对应层级的宽度格式化。

用法:
    python insert_chapter.py "<编号_目录名后缀>" "<题目>" "<介绍>" [--dry-run]

示例:
    python insert_chapter.py "05.2.1_新加测试节" "测试节题目" "这是测试节的介绍内容。"
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")


def parse_slug(slug: str) -> Tuple[str, str]:
    """把 '05.2.1_新加测试节' 拆成 ('05.2.1', '新加测试节')"""
    m = NUMBER_RE.match(slug)
    if not m:
        raise ValueError(
            f"无法解析编号格式: {slug!r}\n"
            "正确格式示例: 05.2.1_新加测试节"
        )
    return m.group(1), m.group(2)


def number_parts(num: str) -> List[int]:
    return [int(x) for x in num.split(".")]


def calc_width(total_count: int) -> int:
    """根据该层级的总节数计算数字宽度（如 13 -> 2，即 02、03）"""
    return max(1, len(str(max(0, total_count))))


def format_parts(parts: List[int], widths: Optional[List[int]] = None) -> str:
    """按给定宽度列表格式化编号各段；若未提供宽度，默认使用 len(str(p))"""
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
    """判断 full_parts 是否以 prefix_parts 为前缀（含自身）"""
    if len(full_parts) < len(prefix_parts):
        return False
    return full_parts[: len(prefix_parts)] == prefix_parts


def replace_prefix_parts(
    full_parts: List[int],
    old_prefix_parts: List[int],
    new_prefix_parts: List[int],
) -> List[int]:
    """把 full_parts 中匹配 old_prefix_parts 的前缀替换为 new_prefix_parts"""
    suffix = full_parts[len(old_prefix_parts) :]
    return list(new_prefix_parts) + suffix


def list_numbered_dirs(parent: Path) -> List[Tuple[List[int], str, Path]]:
    """返回 [(数字段列表, 原始编号串, Path), ...]，按数字段排序"""
    result: List[Tuple[List[int], str, Path]] = []
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        m = NUMBER_RE.match(p.name)
        if m:
            raw_num = m.group(1)
            result.append((number_parts(raw_num), raw_num, p))
    result.sort(key=lambda item: item[0])
    return result


def find_dir_by_parts(parent: Path, target_parts: List[int]) -> Optional[Path]:
    """在 parent 下按数字值（而非前导零字符串）查找匹配目录"""
    for parts, _, path in list_numbered_dirs(parent):
        if parts == target_parts:
            return path
    return None


def resolve_level_widths(
    textbook_root: Path,
    target_parts: List[int],
    has_existing_at_target: bool,
) -> List[int]:
    """
    计算编号每一层对应的数字宽度。
    对于目标层级（最后一层）：若插入位置已存在同号节点，插入后总节数为原数量 + 1；
    若插入在末尾新号位，插入后总节数为 max(原数量 + 1, target_parts[-1])。
    """
    widths: List[int] = []
    current = textbook_root

    for depth in range(1, len(target_parts) + 1):
        prefix = target_parts[:depth]
        siblings = list_numbered_dirs(current)
        existing_count = len(siblings)

        if depth < len(target_parts):
            level_total = existing_count
        else:
            if has_existing_at_target:
                level_total = existing_count + 1
            else:
                level_total = max(existing_count + 1, prefix[-1])

        widths.append(calc_width(level_total))

        if depth < len(target_parts):
            next_dir = find_dir_by_parts(current, prefix)
            if next_dir is None:
                partial_str = format_parts(prefix, widths)
                raise FileNotFoundError(
                    f"找不到编号为 {partial_str} 的目录（在 {current} 下）\n"
                    f"请确认教材根目录是否正确，以及目录命名是否符合「编号_名字」格式。"
                )
            current = next_dir

    return widths


# ---------------------------------------------------------------------------
# 重命名子树
# ---------------------------------------------------------------------------

def rename_subtree(
    subtree_root: Path,
    old_prefix_parts: List[int],
    new_prefix_parts: List[int],
    widths: List[int],
    dry_run: bool = False,
) -> None:
    """
    把子树中编号以 old_prefix_parts 开头的目录（含自身）全部重命名为 new_prefix_parts 开头。
    必须从最深的节点开始改，避免路径冲突。
    """
    to_rename: List[Tuple[Path, str]] = []

    def collect(current: Path) -> None:
        for child in sorted(current.iterdir(), key=lambda p: p.name, reverse=True):
            if child.is_dir():
                collect(child)
        m = NUMBER_RE.match(current.name)
        if m:
            cur_parts = number_parts(m.group(1))
            if is_same_or_descendant_parts(old_prefix_parts, cur_parts):
                updated_parts = replace_prefix_parts(
                    cur_parts, old_prefix_parts, new_prefix_parts
                )
                new_num_str = format_parts(updated_parts, widths)
                new_name = f"{new_num_str}_{m.group(2)}"
                to_rename.append((current, new_name))

    collect(subtree_root)

    for old_path, new_name in to_rename:
        new_path = old_path.parent / new_name
        if dry_run:
            print(f"  [DRY] 重命名: {old_path.name}")
            print(f"         → {new_name}")
        else:
            print(f"  重命名: {old_path.name}  →  {new_name}")
            old_path.rename(new_path)


# ---------------------------------------------------------------------------
# 主逻辑
# ---------------------------------------------------------------------------

def find_parent_dir(
    textbook_root: Path, target_parts: List[int], widths: List[int]
) -> Path:
    """
    根据目标编号找到父目录。
    例如 target_parts = [5, 2, 1] → 找 05.2_xxx
         target_parts = [5, 2]    → 找 05_xxx
         target_parts = [5]       → 返回 textbook_root
    """
    p_parts = parent_number_parts(target_parts)
    if p_parts is None:
        return textbook_root

    current = textbook_root
    for depth in range(1, len(p_parts) + 1):
        partial_parts = p_parts[:depth]
        found = find_dir_by_parts(current, partial_parts)
        if found is None:
            partial_str = format_parts(partial_parts, widths[:depth])
            raise FileNotFoundError(
                f"找不到编号为 {partial_str} 的目录（在 {current} 下）\n"
                f"请确认教材根目录是否正确，以及目录命名是否符合「编号_名字」格式。"
            )
        current = found
    return current


def insert_chapter(
    textbook_root: Path,
    full_slug: str,
    title: str,
    intro: str,
    dry_run: bool = False,
) -> Path:
    raw_num, name_suffix = parse_slug(full_slug)
    target_parts = number_parts(raw_num)

    parent_dir_probe = find_parent_dir(
        textbook_root, target_parts, [calc_width(999)] * len(target_parts)
    )
    existing = find_dir_by_parts(parent_dir_probe, target_parts)
    widths = resolve_level_widths(
        textbook_root, target_parts, has_existing_at_target=(existing is not None)
    )

    formatted_target_num = format_parts(target_parts, widths)
    new_dir_name = f"{formatted_target_num}_{name_suffix}"
    level_count = (
        len(list_numbered_dirs(parent_dir_probe)) + 1
        if existing is not None
        else max(len(list_numbered_dirs(parent_dir_probe)) + 1, target_parts[-1])
    )

    print(f"目标编号 : {formatted_target_num} (输入: {raw_num})")
    print(f"当前层总节数(插入后): {level_count} → 该层数字位宽: {widths[-1]}")
    print(f"新目录名 : {new_dir_name}")
    print(f"题目     : {title}")
    print(f"介绍     : {intro[:60]}{'...' if len(intro) > 60 else ''}")
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

        # 从大到小重命名，避免冲突
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
        title=title,
        intro=intro,
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


def build_index_md(
    number: str, title: str, intro: str, parent_num: Optional[str]
) -> str:
    """生成标准 index.md 内容，链接全部用占位符。"""
    parent_link = "../index.md" if parent_num else "(教材根目录)"
    return f"""# {title}

> 编号：`{number}`

## 介绍

{intro}

---

## 导航

- **上一层**：[父级]({parent_link})
- **前一节**：[TODO_PREV]
- **后一节**：[TODO_NEXT]

<!-- 
  链接占位说明：
  - TODO_PREV / TODO_NEXT 由后续扫描脚本自动替换为真正的相对路径
  - 父级链接已指向 ../index.md（同级目录的上一层）
-->
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 4:
        print(__doc__)
        print("\n错误: 参数不足。")
        print('用法: python insert_chapter.py "<编号_目录名后缀>" "<题目>" "<介绍>" [--dry-run]')
        print('示例: python insert_chapter.py "05.2.1_新加测试节" "测试节题目" "这是介绍。"')
        sys.exit(1)

    full_slug = sys.argv[1]
    title = sys.argv[2]
    intro = sys.argv[3]
    dry_run = "--dry-run" in sys.argv

    textbook_root = Path.cwd().resolve()

    has_chapter = any(
        p.is_dir() and NUMBER_RE.match(p.name)
        for p in textbook_root.iterdir()
    )
    if not has_chapter:
        print(f"警告: 当前目录 {textbook_root} 下没有发现「数字_名字」格式的章节目录。")
        print("请确认你是在教材根目录下运行本脚本。\n")

    try:
        insert_chapter(textbook_root, full_slug, title, intro, dry_run=dry_run)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()