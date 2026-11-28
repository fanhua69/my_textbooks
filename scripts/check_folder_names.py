#!/usr/bin/env python3
"""Recursively normalize numbered directories and centralize indexes under .meta.

每个教材根目录的索引文件集中存放于 .meta，并以节号命名为 1_index.md、
1.1_index.md 等。迁移时只调整旧索引中的相对链接，不改正文内容。
目录及文件中的链接由 check_chapter_links.py 负责更新。
整理完成后，会把无子项且只有目录索引的叶子目录转换为同名 Markdown 文件。

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

from book_paths import discover_book_roots
from change_folder_to_file import change_folders_to_files
from index_paths import (
    index_filename,
    is_index_marker_name,
    metadata_directory,
    migrate_indexes_to_metadata,
)


NUMBERED_NAME_RE = re.compile(r"^(\d+(?:\.\d+)*)[_\s]+(.+)$")
CONTAINER_FILES = {
    "目录.md",
    "contents.md",
    "0_CONTENTS.md",
    "0_大纲.md",
}


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
                and not is_index_marker_name(path.name)
                and not path.name.startswith(".")
            )
        ]
        ordered = sort_siblings(entries)
        number_width = len(str(len(ordered)))

        for index, entry in enumerate(ordered, start=1):
            _, suffix = parse_directory(entry)
            suffix = suffix.replace(" ", "_")
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


def normalize_index_files(
    root: Path,
    dry_run: bool,
    directory_targets: dict[Path, Path] | None = None,
) -> None:
    directory_targets = directory_targets or {}
    meta = metadata_directory(root)
    rename_pairs = [
        (meta / index_filename(old), meta / index_filename(target))
        for old, target in directory_targets.items()
        if old != target
    ]
    rename_pairs = [(old, new) for old, new in rename_pairs if old.is_file() and old != new]

    if dry_run:
        for old, new in rename_pairs:
            print(f"  [预览重命名] {old.name} -> {new.name}")
        for directory, subdirectories, files in os.walk(root):
            subdirectories[:] = [
                name for name in subdirectories if name not in {".meta", ".removed"}
            ]
            for filename in files:
                if is_index_marker_name(filename):
                    print(f"  [预览迁移] {Path(directory) / filename} -> {meta}")
        return

    sources = {old for old, _ in rename_pairs}
    for _, target in rename_pairs:
        if target.exists() and target not in sources:
            raise FileExistsError(f"元数据索引目标已存在: {target}")

    temporary_pairs: list[tuple[Path, Path]] = []
    for index, (old, new) in enumerate(rename_pairs):
        temporary = meta / f".__index_rename_{index}.tmp"
        old.rename(temporary)
        temporary_pairs.append((temporary, new))
    for temporary, target in temporary_pairs:
        temporary.rename(target)

    moved = migrate_indexes_to_metadata(root)
    print(f"已将 {moved} 个目录索引迁移到 {meta}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="递归整理章节编号并将索引集中存放到教材根目录的 .meta",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不修改",
    )
    parser.add_argument(
        "--root",
        help="指定检查根目录；省略时自动根据教材目录标记文件查找书籍根目录",
    )
    args = parser.parse_args()

    if args.root is not None:
        roots = [Path(args.root).resolve()]
    else:
        try:
            roots = discover_book_roots(Path.cwd())
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
            f"错误: 当前目录及其上级目录、当前目录的子目录中均未找到教材目录标记文件",
            file=sys.stderr,
        )
        return 1

    for root in roots:
        print(f"检查书籍根目录: {root}")
        try:
            renames = collect_renames(root)
            directory_targets = {
                old: target for old, target in renames if old.is_dir()
            }
            rename_safely(renames, args.dry_run)
            normalize_index_files(root, args.dry_run, directory_targets)
            result = change_folders_to_files(root, dry_run=args.dry_run)
            if result:
                return result
        except OSError as exc:
            print(f"错误: 处理书籍根目录失败: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
