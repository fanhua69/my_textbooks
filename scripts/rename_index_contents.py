#!/usr/bin/env python3
"""Rename textbook index.md and contents.md files to underscore-prefixed names."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


RENAMES = {
    "index.md": "_index.md",
    "contents.md": "_contents.md",
}


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
        subdirectories[:] = [
            name
            for name in subdirectories
            if not (Path(directory) / name).is_symlink()
        ]
        for filename in filenames:
            target_name = RENAMES.get(filename)
            if target_name is None:
                continue
            source = Path(directory) / filename
            renames.append((source, source.with_name(target_name)))

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

    if dry_run:
        print(f"\n预览完成: {len(renames) - skipped} 个可重命名，{skipped} 个跳过或失败。")
    else:
        print(f"\n重命名完成: {renamed} 个成功，{skipped} 个跳过或失败。")

    return 1 if skipped else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="递归将 index.md 和 contents.md 重命名为 _index.md 和 _contents.md",
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
