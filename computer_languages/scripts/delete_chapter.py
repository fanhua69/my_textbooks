#!/usr/bin/env python3
"""
delete_chapter.py — 删除教材目录树中的某一节（后续同级节点自动 -1 补齐编号）

用法:
    python delete_chapter.py "05.2.1"
    python delete_chapter.py "05.2.1" --force          # 跳过确认
    python delete_chapter.py "05.2.1" --dry-run        # 只预览

说明:
    - 请在教材根目录下运行（即包含 01_xxx、02_xxx ... 的那一层）
    - 参数可以是纯编号 "05.2.1"，也可以是完整目录名 "05.2.1_xxx"
    - 删除后，所有编号更大的同级节点及其子树会整体编号 -1，保持连续
"""

from __future__ import annotations

import argparse
import re
import shutil
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
            "正确格式示例: 05.2.1 或 05.2.1_新加测试节"
        )
    return m.group(1), m.group(2)


def number_parts(num: str) -> List[int]:
    return [int(x) for x in num.split(".")]


def format_number(parts: List[int]) -> str:
    """把 [5, 2, 1] 格式化成 '05.2.1'（第一段补零到两位）"""
    if not parts:
        return ""
    first = f"{parts[0]:02d}"
    rest = [str(p) for p in parts[1:]]
    return ".".join([first] + rest)


def parent_number(num: str) -> Optional[str]:
    """05.2.1 → 05.2 ; 05.2 → 05 ; 05 → None"""
    parts = number_parts(num)
    if len(parts) <= 1:
        return None
    return format_number(parts[:-1])


def decrement_last(num: str) -> str:
    """05.2.2 → 05.2.1"""
    parts = number_parts(num)
    parts[-1] -= 1
    return format_number(parts)


def is_prefix(prefix: str, full: str) -> bool:
    return full == prefix or full.startswith(prefix + ".")


def find_dir_by_number(parent: Path, num: str) -> Optional[Path]:
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        m = NUMBER_RE.match(p.name)
        if m and m.group(1) == num:
            return p
    return None


def list_numbered_dirs(parent: Path) -> List[Tuple[str, Path]]:
    result = []
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        m = NUMBER_RE.match(p.name)
        if m:
            result.append((m.group(1), p))
    result.sort(key=lambda x: number_parts(x[0]))
    return result


def compare_numbers(a: str, b: str) -> int:
    pa, pb = number_parts(a), number_parts(b)
    maxlen = max(len(pa), len(pb))
    pa = pa + [0] * (maxlen - len(pa))
    pb = pb + [0] * (maxlen - len(pb))
    if pa < pb:
        return -1
    if pa > pb:
        return 1
    return 0


def same_level(a: str, b: str) -> bool:
    return len(number_parts(a)) == len(number_parts(b))


# ---------------------------------------------------------------------------
# 子树重命名
# ---------------------------------------------------------------------------

def rename_subtree(root: Path, old_prefix: str, new_prefix: str, dry_run: bool = False) -> None:
    """把以 old_prefix 开头的目录（含自身）全部改成以 new_prefix 开头。从最深节点开始改。"""
    to_rename: List[Tuple[Path, str]] = []

    def collect(current: Path):
        for child in sorted(current.iterdir(), key=lambda p: p.name, reverse=True):
            if child.is_dir():
                collect(child)
        m = NUMBER_RE.match(current.name)
        if m and is_prefix(old_prefix, m.group(1)):
            old_num = m.group(1)
            if old_num == old_prefix:
                new_num = new_prefix
            else:
                suffix = old_num[len(old_prefix):]
                new_num = new_prefix + suffix
            new_name = f"{new_num}_{m.group(2)}"
            to_rename.append((current, new_name))

    collect(root)

    for old_path, new_name in to_rename:
        if dry_run:
            print(f"  [DRY] 重命名: {old_path.name}  →  {new_name}")
        else:
            print(f"  重命名: {old_path.name}  →  {new_name}")
            old_path.rename(old_path.parent / new_name)


# ---------------------------------------------------------------------------
# 定位父目录
# ---------------------------------------------------------------------------

def find_parent_dir(textbook_root: Path, target_num: str) -> Path:
    pnum = parent_number(target_num)
    if pnum is None:
        return textbook_root

    current = textbook_root
    parts = number_parts(pnum)
    for i in range(1, len(parts) + 1):
        partial = format_number(parts[:i])
        found = find_dir_by_number(current, partial)
        if found is None:
            raise FileNotFoundError(
                f"找不到编号为 {partial} 的目录（在 {current} 下）\n"
                f"请确认当前是否在教材根目录，以及目录命名是否符合「编号_名字」格式。"
            )
        current = found
    return current


# ---------------------------------------------------------------------------
# 删除主逻辑
# ---------------------------------------------------------------------------

def delete_chapter(
    textbook_root: Path,
    target_num: str,
    dry_run: bool = False,
    force: bool = False,
) -> None:
    # 允许传入 "05.2.1" 或 "05.2.1_xxx"
    if "_" in target_num:
        target_num, _ = parse_slug(target_num)

    print(f"【删除】")
    print(f"  目标编号 : {target_num}")
    print()

    parent_dir = find_parent_dir(textbook_root, target_num)
    rel_parent = (
        parent_dir.relative_to(textbook_root)
        if parent_dir != textbook_root
        else "(教材根目录)"
    )
    print(f"  父目录   : {rel_parent}")

    target_dir = find_dir_by_number(parent_dir, target_num)
    if target_dir is None:
        raise FileNotFoundError(
            f"在 {parent_dir} 下找不到编号为 {target_num} 的目录。"
        )

    print(f"  将删除   : {target_dir.name}")
    print(f"  完整路径 : {target_dir}")

    file_count = sum(1 for _ in target_dir.rglob("*") if _.is_file())
    dir_count = sum(1 for _ in target_dir.rglob("*") if _.is_dir())
    print(f"  包含     : {dir_count} 个子目录, {file_count} 个文件")
    print()

    # 需要前移的同级节点（编号 > target_num）
    siblings = list_numbered_dirs(parent_dir)
    to_shift = [
        (num, path)
        for num, path in siblings
        if compare_numbers(num, target_num) > 0 and same_level(num, target_num)
    ]

    if to_shift:
        print(f"  删除后将前移的同级节点（共 {len(to_shift)} 个）:")
        for num, path in to_shift:
            new_num = decrement_last(num)
            print(f"    {path.name}  →  {new_num}_...")
        print()
    else:
        print("  删除后没有需要前移的同级节点。\n")

    if not force and not dry_run:
        confirm = input("确认删除？输入 yes 继续: ").strip().lower()
        if confirm != "yes":
            print("已取消。")
            return

    # 1. 删除目标目录
    if dry_run:
        print(f"  [DRY] 将删除目录树: {target_dir.name}")
    else:
        shutil.rmtree(target_dir)
        print(f"  已删除: {target_dir.name}")

    # 2. 前移后续兄弟（从小到大）
    if to_shift:
        print()
        for num, path in sorted(to_shift, key=lambda x: number_parts(x[0])):
            current_path = find_dir_by_number(parent_dir, num)
            if current_path is None:
                print(f"  警告: 找不到 {num}，跳过")
                continue
            new_num = decrement_last(num)
            print(f"  前移子树: {num}  →  {new_num}")
            rename_subtree(current_path, num, new_num, dry_run=dry_run)
            print()

    print("完成。")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="删除教材目录树中的某一节（后续同级节点自动 -1）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "number",
        help='要删除的编号，如 "05.2.1" 或 "05.2.1_xxx"',
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="跳过确认提示",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不实际修改",
    )
    args = parser.parse_args()

    textbook_root = Path.cwd().resolve()
    has_chapter = any(
        p.is_dir() and NUMBER_RE.match(p.name)
        for p in textbook_root.iterdir()
    )
    if not has_chapter:
        print(f"警告: 当前目录 {textbook_root} 下没有发现「数字_名字」格式的章节目录。")
        print("请确认你是在教材根目录下运行本脚本。\n")

    try:
        delete_chapter(
            textbook_root,
            args.number,
            dry_run=args.dry_run,
            force=args.force,
        )
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
