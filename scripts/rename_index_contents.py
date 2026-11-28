#!/usr/bin/env python3
"""Move legacy numbered index files into the textbook's .meta directory."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from book_paths import discover_book_roots
from index_paths import index_filename, migrate_indexes_to_metadata

INDEX_SOURCE = re.compile(r"^(?:~|_)?index(\d*)\.md$", re.IGNORECASE)
NUMBERED_INDEX_SOURCE = re.compile(
    r"^(?P<identifier>\d+(?:\.\d+)*)(?:\.0)?_index(?P<duplicate>\d*)\.md$",
    re.IGNORECASE,
)
NUMBERED_CHINESE_INDEX_SOURCE = re.compile(
    r"^(?P<identifier>\d+(?:\.\d+)*)(?:\.0)?_简介(?P<duplicate>\d*)\.md$",
    re.IGNORECASE,
)
CONTENTS_SOURCES = {"~contents.md", "_contents.md", "contents.md", "目录.md"}


def collect_renames(root: Path) -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for directory, subdirectories, filenames in os.walk(
        root,
        topdown=True,
        onerror=raise_walk_error,
        followlinks=False,
    ):
        if Path(directory).name in {".meta", ".removed"}:
            subdirectories[:] = []
            continue
        subdirectories[:] = [
            name
            for name in subdirectories
            if not (Path(directory) / name).is_symlink()
        ]
        for filename in filenames:
            index_match = INDEX_SOURCE.fullmatch(filename)
            if index_match is not None:
                duplicate = int(index_match.group(1) or 1)
                target_name = index_filename(Path(directory), duplicate)
            else:
                numbered_match = NUMBERED_INDEX_SOURCE.fullmatch(filename)
                if numbered_match is not None:
                    duplicate = int(numbered_match.group("duplicate") or 1)
                    target_name = index_filename(Path(directory), duplicate)
                else:
                    chinese_match = NUMBERED_CHINESE_INDEX_SOURCE.fullmatch(filename)
                    if chinese_match is not None:
                        duplicate = int(chinese_match.group("duplicate") or 1)
                        target_name = index_filename(Path(directory), duplicate)
                    elif filename in CONTENTS_SOURCES:
                        target_name = (
                            "contents.md"
                            if filename in {"~contents.md", "_contents.md"}
                            else filename
                        )
                    else:
                        continue
            source = Path(directory) / filename
            target = source.with_name(target_name)
            if source != target:
                renames.append((source, target))

    return sorted(renames, key=lambda item: item[0].as_posix())


def rename_index_contents(root: Path, dry_run: bool = False) -> int:
    root = root.resolve()
    if not root.is_dir():
        print(f"错误: 根目录不存在: {root}", file=sys.stderr)
        return 1

    renames = collect_renames(root)
    skipped = 0
    renamed = 0

    print(f"搜索根目录: {root}")
    print(f"找到待重命名文件: {len(renames)}\n")

    for source, target in renames:
        if target.exists() or target.is_symlink():
            print(f"[跳过] 目标文件已存在: {target}", file=sys.stderr)
            skipped += 1
            continue

        if dry_run:
            print(f"[预览] {source.relative_to(root)} -> {target.relative_to(root)}")
            continue

        try:
            source.rename(target)
        except OSError as error:
            print(f"[失败] {source}: {error}", file=sys.stderr)
            skipped += 1
            continue

        renamed += 1
        print(f"[完成] {source.relative_to(root)} -> {target.relative_to(root)}")

    if not dry_run:
        try:
            roots = discover_book_roots(root)
            for book_root in roots:
                moved = migrate_indexes_to_metadata(book_root)
                print(f"[完成] 已迁移 {moved} 个索引文件到 {book_root / '.meta'}")
        except OSError as error:
            print(f"[失败] 无法迁移索引到 .meta: {error}", file=sys.stderr)
            return 1

    if dry_run:
        print(f"\n预览完成: {len(renames) - skipped} 个可重命名，{skipped} 个跳过或失败。")
    else:
        print(f"\n重命名完成: {renamed} 个成功，{skipped} 个跳过或失败。")

    return 1 if skipped else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="递归将索引文件集中迁移到各教材根目录的 .meta 中",
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="搜索根目录，默认当前目录",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不修改",
    )
    args = parser.parse_args()

    return rename_index_contents(args.root, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
