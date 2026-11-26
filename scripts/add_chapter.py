#!/usr/bin/env python3
"""在当前目录创建新的一节，并自动使用第一个可用的节号。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from insert_chapter import (
    DIR_NAME_RE,
    build_index_md,
    chapter_to_dir_suffix,
    chapter_to_intro_text,
    list_numbered_dirs,
    number_parts,
)


def first_available_section_num(textbook_root: Path) -> str:
    used_numbers = {
        parts[0]
        for parts, _, _ in list_numbered_dirs(textbook_root)
        if len(parts) == 1
    }
    section_num = 1
    while section_num in used_numbers:
        section_num += 1
    return str(section_num)


def resolve_parent_num_and_section_num(
    current_dir: Path,
) -> tuple[str | None, str]:
    current_match = DIR_NAME_RE.match(current_dir.name)
    if current_match is None:
        return None, first_available_section_num(current_dir)

    parent_parts = number_parts(current_match.group(1))
    parent_num = ".".join(str(part) for part in parent_parts)
    used_numbers = {
        parts[-1]
        for parts, _, _ in list_numbered_dirs(current_dir)
        if len(parts) == len(parent_parts) + 1 and parts[:-1] == parent_parts
    }
    section_num = 1
    while section_num in used_numbers:
        section_num += 1

    return parent_num, f"{parent_num}.{section_num}"


def add_chapter(
    current_dir: Path,
    chapter_name: str,
    dry_run: bool = False,
) -> Path:
    parent_num, section_num = resolve_parent_num_and_section_num(current_dir)
    dir_suffix = chapter_to_dir_suffix(chapter_name)
    clean_chapter = chapter_to_intro_text(chapter_name)
    new_dir = current_dir / f"{section_num}_{dir_suffix}"

    if new_dir.exists():
        raise FileExistsError(f"目录已存在: {new_dir}")

    print(f"自动选择第一个可用节号: {section_num}")
    print(f"新目录名 : {new_dir.name}")
    if dry_run:
        print(f"[DRY] 将创建目录: {new_dir}")
    else:
        new_dir.mkdir()
        print(f"已创建目录: {new_dir.name}")

    index_content = build_index_md(
        number=section_num,
        chapter_name=clean_chapter,
        parent_num=parent_num,
    )
    index_path = new_dir / "_index.md"
    if dry_run:
        print(f"[DRY] 将写入: {index_path}")
        print("--- _index.md 预览 ---")
        print(index_content)
        print("---------------------")
    else:
        index_path.write_text(index_content, encoding="utf-8")
        print(f"已写入   : {index_path}")
    return new_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="在当前目录创建新的一节，自动使用第一个可用节号"
    )
    parser.add_argument("chapter_name", help='章节名，例如 "smart pointers"')
    parser.add_argument("--dry-run", action="store_true", help="仅预览变更，不修改磁盘")
    args = parser.parse_args()

    current_dir = Path.cwd().resolve()
    has_chapter = DIR_NAME_RE.match(current_dir.name) is not None or any(
        path.is_dir() and DIR_NAME_RE.match(path.name) is not None
        for path in current_dir.iterdir()
    )
    if not has_chapter:
        print(f"警告: 当前目录 {current_dir} 下没有发现「数字_名字」格式的章节目录。")
        print("请确认你是在教材根目录下运行本脚本。\n")

    try:
        add_chapter(
            current_dir=current_dir,
            chapter_name=args.chapter_name,
            dry_run=args.dry_run,
        )
    except Exception as error:
        print(f"\n错误: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
