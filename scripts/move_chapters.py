#!/usr/bin/env python3
"""
move_chapters.py - Move one or a range of numbered chapter directories.

Usage:
    python3 move_chapters.py 1.10 1.2
    python3 move_chapters.py 1.01-1.20 1.60
    python3 move_chapters.py 1.01-1.20 1.60 --dry-run

Directories keep their existing names; section numbers are not changed.
Run the script from the textbook root or another directory that contains
all source and target chapter directories.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from book_paths import find_book_root, find_section_entries
from index_paths import migrate_indexes_to_metadata


NUMBERED_DIR_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")
NUMBER_RE = re.compile(r"^\d+(?:\.\d+)*$")


def parse_number(value: str) -> str:
    value = value.strip()
    if "_" in value:
        match = NUMBERED_DIR_RE.match(value)
        if not match:
            raise ValueError(f"无法解析章节目录名: {value!r}")
        value = match.group(1)
    if not NUMBER_RE.match(value):
        raise ValueError(
            f"无法解析章节编号: {value!r}\n"
            "正确格式例如: 1.10 或 1.60_xxx"
        )
    return value


def parse_source(value: str) -> list[str]:
    value = value.strip()
    if "-" not in value:
        return [parse_number(value)]

    parts = value.split("-")
    if len(parts) != 2:
        raise ValueError(
            f"无法解析编号范围: {value!r}（例如: 1.01-1.20）"
        )

    start = parse_number(parts[0])
    end = parse_number(parts[1])
    start_parts = [int(part) for part in start.split(".")]
    end_parts = [int(part) for part in end.split(".")]

    if len(start_parts) != len(end_parts):
        raise ValueError("范围的起止编号层级必须相同")

    prefix = start_parts[:-1]
    if prefix != end_parts[:-1]:
        raise ValueError("编号范围必须在同一个父章节下")

    first = start_parts[-1]
    last = end_parts[-1]
    if first > last:
        raise ValueError("编号范围的起始编号不能大于结束编号")

    numbers = prefix + [first]
    width = max(
        len(start.split(".")[-1]),
        len(end.split(".")[-1]),
    )

    result = []
    for number in range(first, last + 1):
        parts_out = prefix + [number]
        text_parts = [str(part) for part in parts_out[:-1]]
        text_parts.append(str(parts_out[-1]).zfill(width))
        result.append(".".join(text_parts))
    return result


def number_parts(number: str) -> list[int]:
    return [int(part) for part in number.split(".")]


def find_chapter(root: Path, number: str) -> Path:
    matches = [
        path
        for path, kind in find_section_entries(root, number)
        if kind == "directory"
    ]
    if not matches:
        raise FileNotFoundError(f"找不到编号为 {number} 的章节目录")
    if len(matches) > 1:
        locations = "\n".join(f"  {path}" for path in matches)
        raise RuntimeError(
            f"编号 {number} 对应多个章节目录:\n{locations}"
        )
    return matches[0]


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def move_chapters(
    root: Path,
    source_spec: str,
    target_spec: str,
    dry_run: bool = False,
    force: bool = False,
) -> None:
    root = root.resolve()
    source_numbers = parse_source(source_spec)
    target_number = parse_number(target_spec)

    sources = [find_chapter(root, number) for number in source_numbers]
    target = find_chapter(root, target_number)

    source_parents = {path.parent.resolve() for path in sources}
    if len(source_parents) != 1:
        raise ValueError("源章节必须位于同一个父目录下")

    for source in sources:
        if target.resolve() == source.resolve():
            raise ValueError("不能把章节移动到自身")
        if is_within(target.resolve(), source.resolve()):
            raise ValueError("不能把章节移动到自己的子目录中")

    target_children = {
        child.name: child
        for child in target.iterdir()
        if child.is_dir()
    }
    collisions = [
        source.name
        for source in sources
        if source.name in target_children
    ]
    if collisions:
        names = ", ".join(collisions)
        raise FileExistsError(f"目标目录中已存在同名章节: {names}")

    print(f"源范围  : {source_spec}")
    print(f"目标章节: {target.name}")
    print(f"目标目录: {target}")
    print(f"移动节数: {len(sources)}")
    print()

    for source in sources:
        print(f"  {source.name}  ->  {target.name}/{source.name}")
    print()

    if not dry_run and not force:
        answer = input("确认移动？输入 yes 继续: ").strip().lower()
        if answer != "yes":
            print("已取消。")
            return

    if not dry_run:
        migrate_indexes_to_metadata(find_book_root(root))

    for source in sources:
        destination = target / source.name
        if dry_run:
            print(f"[DRY] 移动: {source}  ->  {destination}")
            continue
        shutil.move(str(source), str(destination))
        print(f"已移动: {source}  ->  {destination}")

    if dry_run:
        print("\n预览完成，未修改磁盘。")
    else:
        print("\n移动完成。")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="移动一个或一串编号章节到指定章节目录下",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "source",
        help='源编号或编号范围，例如 "1.10" 或 "1.01-1.20"',
    )
    parser.add_argument(
        "target",
        help='目标编号或完整目录名，例如 "1.60" 或 "1.60_xxx"',
    )
    parser.add_argument("--dry-run", action="store_true", help="只预览，不修改")
    parser.add_argument("--force", action="store_true", help="跳过确认")

    args = parser.parse_args()

    try:
        move_chapters(
            root=Path.cwd(),
            source_spec=args.source,
            target_spec=args.target,
            dry_run=args.dry_run,
            force=args.force,
        )
    except (ValueError, OSError, RuntimeError) as error:
        print(f"\n错误: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
