#!/usr/bin/env python3
"""Generate a textbook by running structure and Markdown maintenance phases."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_phase(script: Path, arguments: list[str]) -> None:
    subprocess.run(
        [sys.executable, str(script), *arguments],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="创建教材目录，统一节名，并重建 Markdown 目录和导航"
    )
    parser.add_argument("json_file", type=Path, help="教材大纲 JSON 文件")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="输出父目录；省略时使用当前工作目录",
    )
    args = parser.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    create_script = scripts_dir / "create_folder_and_files.py"
    folder_names_script = scripts_dir / "check_folder_names.py"
    chapter_links_script = scripts_dir / "check_chapter_links.py"

    create_result = subprocess.run(
        [
            sys.executable,
            str(create_script),
            str(args.json_file),
            "--output-dir",
            str(args.output_dir.expanduser().resolve()),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    root_dir = Path(create_result.stdout.strip()).resolve()

    run_phase(
        folder_names_script,
        ["--root", str(root_dir)],
    )
    run_phase(
        chapter_links_script,
        [str(root_dir)],
    )

    print(f"完成：{root_dir}")
    print(
        "已依次执行 create_folder_and_files.py、"
        "check_folder_names.py、check_chapter_links.py"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
