#!/usr/bin/env python3
"""Flatten leaf textbook directories containing only a numbered index file."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from book_paths import discover_book_roots
from index_paths import index_filename


def find_leaf_index_directories(root: Path) -> list[Path]:
    """Return directories whose only entry is the expected numbered index file."""
    candidates: list[Path] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for directory, subdirectories, _ in os.walk(root, onerror=raise_walk_error):
        directory_path = Path(directory)
        subdirectories[:] = [
            name
            for name in subdirectories
            if not (directory_path / name).is_symlink()
        ]
        if directory_path == root:
            continue

        entries = list(directory_path.iterdir())
        if (
            len(entries) == 1
            and entries[0].name == index_filename(directory_path)
            and entries[0].is_file()
            and not entries[0].is_symlink()
        ):
            candidates.append(directory_path)

    return sorted(candidates)


def change_folders_to_files(root: Path, dry_run: bool = False) -> int:
    """Move eligible numbered index files to their parent and remove their directories."""
    root = root.resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Book root not found: {root}")

    candidates = find_leaf_index_directories(root)
    blocked = 0
    moved = 0

    print(f"书籍根目录: {root}")
    print(f"符合条件的叶子目录: {len(candidates)}\n")

    for directory in candidates:
        source = directory / index_filename(directory)
        destination = directory.parent / f"{directory.name}.md"

        if destination.exists() or destination.is_symlink():
            print(f"[跳过] 目标文件已存在: {destination}", file=sys.stderr)
            blocked += 1
            continue

        if dry_run:
            print(f"[预览] {source} -> {destination}，删除目录 {directory}")
            continue

        try:
            source.rename(destination)
        except OSError as exc:
            print(f"[失败] {directory}: {exc}", file=sys.stderr)
            blocked += 1
            continue

        moved += 1
        try:
            directory.rmdir()
        except OSError as exc:
            print(
                f"[部分完成] 文件已移动到 {destination}，"
                f"但无法删除目录 {directory}: {exc}",
                file=sys.stderr,
            )
            blocked += 1
            continue

        print(f"[完成] {source} -> {destination}")

    if dry_run:
        print(f"\n预览完成: {len(candidates) - blocked} 个目录可处理，{blocked} 个跳过。")
    else:
        print(f"\n处理完成: 移动 {moved} 个目录，{blocked} 个跳过或失败。")

    return 1 if blocked else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="将仅含编号索引文件的叶子目录转换为同名 Markdown 文件"
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="指定书籍根目录；省略时根据教材目录标记文件自动查找",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不修改",
    )
    args = parser.parse_args()

    if args.root is not None:
        roots = [args.root.expanduser().resolve()]
    else:
        try:
            roots = discover_book_roots(Path.cwd())
        except OSError as exc:
            print(f"搜索书籍根目录失败: {exc}", file=sys.stderr)
            return 1

    if len(roots) != 1:
        if not roots:
            print(
                "未找到书籍根目录（包含教材目录标记文件的目录）；请使用 --root 指定。",
                file=sys.stderr,
            )
        else:
            print(
                "找到多个书籍根目录，请使用 --root 指定其中一个:\n"
                + "\n".join(str(root) for root in roots),
                file=sys.stderr,
            )
        return 1

    try:
        return change_folders_to_files(roots[0], args.dry_run)
    except OSError as exc:
        print(f"处理书籍目录失败: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
