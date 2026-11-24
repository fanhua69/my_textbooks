#!/usr/bin/env python3
"""
check_folder_names.py - Recursively normalize numbered directory names.

Examples:
    1.01_Alpha
    1.02_Beta
        1.02.1_First
        1.02.2_Second

Usage:
    python3 check_folder_names.py --dry-run
    python3 check_folder_names.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NUMBERED_NAME_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")


def number_parts(number: str) -> list[int]:
    return [int(part) for part in number.split(".")]


def parse_directory(directory: Path) -> tuple[str | None, str]:
    match = NUMBERED_NAME_RE.match(directory.name)
    if not match:
        return None, directory.name
    return match.group(1), match.group(2)


def sort_siblings(directories: list[Path]) -> list[Path]:
    def key(directory: Path) -> tuple:
        number, suffix = parse_directory(directory)
        if number:
            return (0, number_parts(number), suffix, directory.name)
        return (1, directory.name.casefold(), directory.name)

    return sorted(directories, key=key)


def collect_renames(root: Path) -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []

    def visit(
        parent: Path,
        target_parent: Path,
        parent_number: str | None,
    ) -> None:
        directories = [
            path
            for path in parent.iterdir()
            if path.is_dir()
            and not path.is_symlink()
            and not path.name.startswith(".")
        ]
        ordered = sort_siblings(directories)
        number_width = len(str(len(ordered)))

        for index, directory in enumerate(ordered, start=1):
            _, suffix = parse_directory(directory)
            if parent_number:
                target_number = f"{parent_number}.{index:0{number_width}d}"
            else:
                target_number = str(index)

            target_name = f"{target_number}_{suffix}"
            target = target_parent / target_name
            renames.append((directory, target))
            visit(directory, target, target_number)

    visit(root, root, None)
    return renames


def rename_safely(
    renames: list[tuple[Path, Path]],
    dry_run: bool,
) -> None:
    actual = [
        (old, target)
        for old, target in renames
        if old != target
    ]

    if not actual:
        print("所有子目录编号已经正确，无需修改。")
        return

    print(f"共发现 {len(actual)} 个目录需要重命名:\n")
    for old, target in actual:
        print(f"  {old}  ->  {target}")

    if dry_run:
        print("\n预览完成，未修改磁盘。")
        return

    # Use temporary names so swaps and conflicts cannot overwrite one another.
    temp_paths: dict[Path, Path] = {}
    counter = 1

    for old, _ in sorted(actual, key=lambda item: len(item[0].parts), reverse=True):
        while True:
            temp = old.parent / f".__check_folder_names_tmp_{counter}"
            counter += 1
            if not temp.exists():
                break
        old.rename(temp)
        temp_paths[old] = temp

    # Restore in hierarchy order: parents first, then their descendants.
    for old, target in sorted(actual, key=lambda item: len(item[0].parts)):
        temp = temp_paths[old]
        target.parent.mkdir(parents=True, exist_ok=True)
        temp_source = target.parent / temp.name
        if not temp_source.exists():
            temp_source = temp
        temp_source.rename(target)
        print(f"  已重命名: {old.name}  ->  {target.name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="递归检查并统一所有子目录的编号",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不修改",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="要检查的根目录（默认：当前目录）",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"错误: 根目录不存在: {root}", file=sys.stderr)
        return 1

    renames = collect_renames(root)
    rename_safely(renames, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
