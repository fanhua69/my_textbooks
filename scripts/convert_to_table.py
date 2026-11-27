#!/usr/bin/env python3
"""
convert_to_table.py - 将连续的制表符分隔行转换为 Markdown 表格。

用法:
    python3 convert_to_table.py "<节号>" [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from book_paths import find_book_root, find_section_entries
from index_paths import index_filename


def find_chapter_markdown(start: Path, section_num: str) -> Path:
    entries = find_section_entries(start, section_num)
    matches: list[tuple[Path, str]] = []

    for path, kind in entries:
        if kind == "directory":
            index_path = path / index_filename(path)
            if index_path.is_file():
                matches.append((index_path, kind))
        else:
            matches.append((path, kind))

    matches.sort(key=lambda item: (item[1], str(item[0])))
    if not matches:
        book_root = find_book_root(start)
        raise FileNotFoundError(
            f"在书籍根目录 '{book_root}' 下未找到节号为 '{section_num}' 的 Markdown 文件"
        )
    if len(matches) > 1:
        locations = "\n".join(f"  {path}" for path, _ in matches)
        raise FileExistsError(
            f"节号 '{section_num}' 对应多个 Markdown 文件:\n{locations}"
        )
    return matches[0][0]


def split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def convert_tab_tables(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    converted: list[str] = []
    table_count = 0
    i = 0

    while i < len(lines):
        content, newline = split_line_ending(lines[i])
        tab_count = content.count("\t")

        if tab_count == 0:
            converted.append(lines[i])
            i += 1
            continue

        run_end = i
        while run_end < len(lines):
            run_content, _ = split_line_ending(lines[run_end])
            if run_content.count("\t") != tab_count:
                break
            run_end += 1

        run_length = run_end - i
        if run_length < 2:
            converted.append(lines[i])
            i += 1
            continue

        separator = "-|" * tab_count + "-"
        for index, line in enumerate(lines[i:run_end]):
            row, row_newline = split_line_ending(line)
            converted.append(row.replace("\t", "|") + row_newline)
            if index == 0:
                separator_newline = row_newline or ("\r\n" if "\r\n" in text else "\n")
                converted.append(separator + separator_newline)

        table_count += 1
        i = run_end

    return "".join(converted), table_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="把指定节中的连续制表符表格转换为 Markdown 表格"
    )
    parser.add_argument("section_num", help="节号，例如 2.1.3")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不修改文件")
    args = parser.parse_args()

    try:
        markdown_path = find_chapter_markdown(Path.cwd(), args.section_num)
        with markdown_path.open("r", encoding="utf-8", newline="") as source:
            original = source.read()
        converted, table_count = convert_tab_tables(original)

        print(f"Markdown 文件: {markdown_path}")
        print(f"找到制表符表格: {table_count} 个")

        if table_count == 0:
            print("没有符合条件的连续制表符表格，无需修改。")
            return

        if args.dry_run:
            print("[DRY-RUN] 将修改文件")
            print(converted)
        else:
            with markdown_path.open("w", encoding="utf-8", newline="") as target:
                target.write(converted)
            print("已转换制表符表格。")
    except Exception as error:
        print(f"错误: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
