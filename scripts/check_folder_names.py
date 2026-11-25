#!/usr/bin/env python3
"""
check_folder_names.py - Recursively normalize numbered directory names.

此脚本只重命名目录和 Markdown 文件，不读取或修改任何 Markdown 文件内容。
目录及文件中的链接由 check_chapter_links.py 负责更新。

Examples:
    1.01_Alpha
    1.02_Beta
        1.02.1_First
        1.02.2_Second
    Direct Markdown files are also sections:
        1.03_Notes.md
        1.04_Exercises.md

Usage:
    python3 check_folder_names.py --dry-run
    python3 check_folder_names.py
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


NUMBERED_NAME_RE = re.compile(r"^(\d+(?:\.\d+)*)[_\s]+(.+)$")
CONTAINER_FILES = {"index.md", "contents.md"}


def number_parts(number: str) -> list[int]:
    return [int(part) for part in number.split(".")]


def parse_directory(directory: Path) -> tuple[str | None, str]:
    name = directory.name
    if directory.is_file() and name.lower().endswith(".md"):
        name = name[:-3]
    match = NUMBERED_NAME_RE.match(name)
    if not match:
        return None, name
    return match.group(1), match.group(2)


def sort_siblings(entries: list[Path]) -> list[Path]:
    def key(entry: Path) -> tuple:
        number, suffix = parse_directory(entry)
        if number:
            return (0, number_parts(number), suffix, entry.name.casefold(), entry.name)
        return (1, suffix.casefold(), entry.name.casefold(), entry.name)

    return sorted(entries, key=key)


def discover_book_roots(current_dir: Path, home_dir: Path) -> list[Path]:
    """Find the nearest book root, or all book roots below the current directory."""
    current_dir = current_dir.resolve()
    home_dir = home_dir.resolve()

    if (current_dir / "contents.md").is_file():
        return [current_dir]

    if current_dir == home_dir or home_dir in current_dir.parents:
        for ancestor in current_dir.parents:
            if (ancestor / "contents.md").is_file():
                return [ancestor]
            if ancestor == home_dir:
                break

    def raise_walk_error(error: OSError) -> None:
        raise error

    roots: list[Path] = []
    for directory, subdirectories, files in os.walk(current_dir, onerror=raise_walk_error):
        directory_path = Path(directory)
        subdirectories[:] = [
            name
            for name in subdirectories
            if not (directory_path / name).is_symlink()
        ]
        if "contents.md" in files and (directory_path / "contents.md").is_file():
            roots.append(directory_path)

    return sorted(roots)


def collect_renames(root: Path) -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []

    def visit(
        parent: Path,
        target_parent: Path,
        parent_number: str | None,
    ) -> None:
        entries = [
            path
            for path in parent.iterdir()
            if (
                path.is_dir()
                and not path.is_symlink()
                and not path.name.startswith(".")
                and not (parent == root and path.name == "removed")
            )
            or (
                path.is_file()
                and path.suffix.lower() == ".md"
                and path.name not in CONTAINER_FILES
                and not path.name.startswith(".")
            )
        ]
        ordered = sort_siblings(entries)
        number_width = len(str(len(ordered)))

        for index, entry in enumerate(ordered, start=1):
            _, suffix = parse_directory(entry)
            if parent_number:
                target_number = f"{parent_number}.{index:0{number_width}d}"
            else:
                target_number = str(index)

            if entry.is_dir():
                target_name = f"{target_number}_{suffix}"
                target = target_parent / target_name
                renames.append((entry, target))
                visit(entry, target, target_number)
            else:
                target_name = f"{target_number}_{suffix}.md"
                target = target_parent / target_name
                renames.append((entry, target))

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
        description="递归统一目录下子目录与 Markdown 文件的节号、节名和排序",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不修改",
    )
    parser.add_argument(
        "--root",
        help="指定检查根目录；省略时自动根据 contents.md 查找书籍根目录",
    )
    args = parser.parse_args()

    if args.root is not None:
        roots = [Path(args.root).resolve()]
    else:
        try:
            roots = discover_book_roots(Path.cwd(), Path.home())
        except OSError as exc:
            print(f"错误: 搜索书籍根目录失败: {exc}", file=sys.stderr)
            return 1

    invalid_roots = [root for root in roots if not root.is_dir()]
    if invalid_roots:
        for root in invalid_roots:
            print(f"错误: 根目录不存在: {root}", file=sys.stderr)
        return 1

    if not roots:
        print(
            f"错误: 当前目录及其上级目录、当前目录的子目录中均未找到 contents.md",
            file=sys.stderr,
        )
        return 1

    for root in roots:
        print(f"检查书籍根目录: {root}")
        renames = collect_renames(root)
        rename_safely(renames, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
