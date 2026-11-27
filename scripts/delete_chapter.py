#!/usr/bin/env python3
"""Delete one section directory, then delegate numbering and link maintenance.

用法:
    python delete_chapter.py "05.2.1"
    python delete_chapter.py "05.2.1" --force          # 跳过确认
    python delete_chapter.py "05.2.1" --dry-run        # 只预览

说明:
    - 可在教材目录内任意位置运行；脚本会向上查找 contents.md
    - 参数可以是纯编号 "05.2.1"，也可以是完整目录名 "05.2.1_xxx"
    - 删除后由 check_folder_names.py 整理编号，再由 check_chapter_links.py 更新导航
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from book_paths import find_book_root


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")
NUMBER_ONLY_RE = re.compile(r"^\d+(?:\.\d+)*$")


def parse_slug(slug: str) -> Tuple[str, str]:
    """把 '05.2.1_新加测试节' 拆成 ('05.2.1', '新加测试节')"""
    m = NUMBER_RE.match(slug)
    if not m:
        raise ValueError(
            f"无法解析编号格式: {slug!r}\n"
            "正确格式示例: 05.2.1 或 05.2.1_新加测试节"
        )
    return m.group(1), m.group(2)


def number_parts(num: str) -> List[int]:
    return [int(x) for x in num.split(".")]


def find_section_dir(textbook_root: Path, target_num: str) -> Path:
    target_parts = number_parts(target_num)
    matches: List[Path] = []

    def visit(parent: Path, depth: int) -> None:
        expected_parts = target_parts[: depth + 1]
        for child in parent.iterdir():
            if not child.is_dir() or child.is_symlink():
                continue
            match = NUMBER_RE.match(child.name)
            if match is None or number_parts(match.group(1)) != expected_parts:
                continue
            if depth == len(target_parts) - 1:
                matches.append(child)
            else:
                visit(child, depth + 1)

    visit(textbook_root, 0)
    if not matches:
        raise FileNotFoundError(
            f"在教材根目录 {textbook_root} 下找不到编号为 {target_num} 的目录。"
        )
    if len(matches) > 1:
        paths = "\n".join(f"  {path}" for path in matches)
        raise ValueError(f"编号 {target_num} 对应多个目录，无法确定目标:\n{paths}")
    return matches[0]


# ---------------------------------------------------------------------------
# 删除主逻辑
# ---------------------------------------------------------------------------

def delete_chapter(
    textbook_root: Path,
    target_num: str,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    """Delete the requested section directory; return whether deletion occurred."""
    # 允许传入 "05.2.1" 或 "05.2.1_xxx"
    if "_" in target_num:
        target_num, _ = parse_slug(target_num)
    if not NUMBER_ONLY_RE.fullmatch(target_num):
        raise ValueError(f"无法解析节编号: {target_num!r}")

    print(f"【删除】")
    print(f"  目标编号 : {target_num}")
    print()

    target_dir = find_section_dir(textbook_root, target_num)
    parent_dir = target_dir.parent
    rel_parent = (
        parent_dir.relative_to(textbook_root)
        if parent_dir != textbook_root
        else "(教材根目录)"
    )
    print(f"  父目录   : {rel_parent}")

    print(f"  将删除   : {target_dir.name}")
    print(f"  完整路径 : {target_dir}")

    file_count = sum(1 for _ in target_dir.rglob("*") if _.is_file())
    dir_count = sum(1 for _ in target_dir.rglob("*") if _.is_dir())
    print(f"  包含     : {dir_count} 个子目录, {file_count} 个文件")
    print()

    if not force and not dry_run:
        confirm = input("确认删除？输入 yes 继续: ").strip().lower()
        if confirm != "yes":
            print("已取消。")
            return False

    if dry_run:
        print(f"  [DRY] 将删除目录树: {target_dir.name}")
        return False

    shutil.rmtree(target_dir)
    print(f"  已删除: {target_dir.name}")
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="删除教材目录树中的某一节，并委托整理编号和链接",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "number",
        help='要删除的编号，如 "05.2.1" 或 "05.2.1_xxx"',
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="跳过确认提示",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不实际修改",
    )
    args = parser.parse_args()

    try:
        textbook_root = find_book_root(Path.cwd())
        deleted = delete_chapter(
            textbook_root,
            args.number,
            dry_run=args.dry_run,
            force=args.force,
        )
        if not deleted:
            return 0

        scripts_dir = Path(__file__).resolve().parent
        subprocess.run(
            [
                sys.executable,
                str(scripts_dir / "check_folder_names.py"),
                "--root",
                str(textbook_root),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(scripts_dir / "check_chapter_links.py"),
                str(textbook_root),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\n错误: 目录已删除，但后续整理脚本执行失败 "
            f"(退出码 {e.returncode})。",
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError) as e:
        print(f"\n错误: {e}", file=sys.stderr)
        return 1

    print("删除和后续整理完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
