#!/usr/bin/env python3
"""
insert_chapter.py — 在教材目录树中按编号插入新的一节（自动重编号后续兄弟节点及子树）

用法:
    python insert_chapter.py "<编号_目录名后缀>" "<题目>" "<介绍>"

示例:
    python insert_chapter.py "05.2.1_新加测试节" "测试节题目" "这是测试节的介绍内容。"

要求:
    - 请在教材根目录下运行（即包含 01_xxx、02_xxx ... 的那一层）
    - 所有目录名必须符合 「数字编号_中文名」 格式，编号按字典序/数字序排列
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)_(.+)$")


def parse_slug(slug: str) -> Tuple[str, str]:
    """把 '05.2.1_新加测试节' 拆成 ('05.2.1', '新加测试节')"""
    m = NUMBER_RE.match(slug)
    if not m:
        raise ValueError(
            f"无法解析编号格式: {slug!r}\n"
            "正确格式示例: 05.2.1_新加测试节"
        )
    return m.group(1), m.group(2)


def number_parts(num: str) -> List[int]:
    return [int(x) for x in num.split(".")]


def format_number(parts: List[int]) -> str:
    """把 [5, 2, 1] 格式化成 '05.2.1'（第一段补零到两位，其余保持原样）"""
    if not parts:
        return ""
    first = f"{parts[0]:02d}"
    rest = [str(p) for p in parts[1:]]
    return ".".join([first] + rest)


def parent_number(num: str) -> Optional[str]:
    """05.2.1 → 05.2 ; 05.2 → 05 ; 05 → None"""
    parts = number_parts(num)
    if len(parts) <= 1:
        return None
    return format_number(parts[:-1])


def increment_last(num: str) -> str:
    """05.2.1 → 05.2.2"""
    parts = number_parts(num)
    parts[-1] += 1
    return format_number(parts)


def is_prefix(prefix: str, full: str) -> bool:
    """判断 full 是否以 prefix. 开头（用于判断子树关系）"""
    return full == prefix or full.startswith(prefix + ".")


def find_dir_by_number(parent: Path, num: str) -> Optional[Path]:
    """在 parent 下找编号精确匹配的目录"""
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        m = NUMBER_RE.match(p.name)
        if m and m.group(1) == num:
            return p
    return None


def list_numbered_dirs(parent: Path) -> List[Tuple[str, Path]]:
    """返回 (编号, Path) 列表，按编号排序"""
    result = []
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        m = NUMBER_RE.match(p.name)
        if m:
            result.append((m.group(1), p))
    # 按数字部分比较
    result.sort(key=lambda x: number_parts(x[0]))
    return result


def compare_numbers(a: str, b: str) -> int:
    """比较两个编号：a < b 返回 -1，a == b 返回 0，a > b 返回 1"""
    pa, pb = number_parts(a), number_parts(b)
    # 补齐长度后逐位比较
    maxlen = max(len(pa), len(pb))
    pa += [0] * (maxlen - len(pa))
    pb += [0] * (maxlen - len(pb))
    if pa < pb:
        return -1
    if pa > pb:
        return 1
    return 0


# ---------------------------------------------------------------------------
# 重命名子树
# ---------------------------------------------------------------------------

def rename_subtree(root: Path, old_prefix: str, new_prefix: str, dry_run: bool = False) -> None:
    """
    把以 old_prefix 开头的目录（含自身）全部改成以 new_prefix 开头。
    必须从最深的节点开始改，避免路径冲突。
    """
    # 收集所有需要改名的目录（深度优先，深的在前）
    to_rename: List[Tuple[Path, str]] = []

    def collect(current: Path):
        for child in sorted(current.iterdir(), key=lambda p: p.name, reverse=True):
            if child.is_dir():
                collect(child)
        m = NUMBER_RE.match(current.name)
        if m and is_prefix(old_prefix, m.group(1)):
            old_num = m.group(1)
            # 替换前缀
            if old_num == old_prefix:
                new_num = new_prefix
            else:
                # old_num = old_prefix + ".xxx" → new_prefix + ".xxx"
                suffix = old_num[len(old_prefix):]
                new_num = new_prefix + suffix
            new_name = f"{new_num}_{m.group(2)}"
            to_rename.append((current, new_name))

    collect(root)

    for old_path, new_name in to_rename:
        new_path = old_path.parent / new_name
        if dry_run:
            print(f"  [DRY] 重命名: {old_path.relative_to(root.parent.parent) if False else old_path.name}")
            print(f"         → {new_name}")
        else:
            print(f"  重命名: {old_path.name}  →  {new_name}")
            old_path.rename(new_path)


# ---------------------------------------------------------------------------
# 主逻辑
# ---------------------------------------------------------------------------

def find_parent_dir(textbook_root: Path, target_num: str) -> Path:
    """
    根据目标编号找到父目录。
    例如 target_num = 05.2.1 → 找 05.2_xxx
         target_num = 05.2   → 找 05_xxx
         target_num = 05     → 返回 textbook_root
    """
    pnum = parent_number(target_num)
    if pnum is None:
        return textbook_root

    # 从根开始逐级向下找
    current = textbook_root
    parts = number_parts(pnum)
    for i in range(1, len(parts) + 1):
        partial = format_number(parts[:i])
        found = find_dir_by_number(current, partial)
        if found is None:
            raise FileNotFoundError(
                f"找不到编号为 {partial} 的目录（在 {current} 下）\n"
                f"请确认教材根目录是否正确，以及目录命名是否符合「编号_名字」格式。"
            )
        current = found
    return current


def insert_chapter(
    textbook_root: Path,
    full_slug: str,
    title: str,
    intro: str,
    dry_run: bool = False,
) -> Path:
    target_num, name_suffix = parse_slug(full_slug)
    new_dir_name = f"{target_num}_{name_suffix}"

    print(f"目标编号 : {target_num}")
    print(f"新目录名 : {new_dir_name}")
    print(f"题目     : {title}")
    print(f"介绍     : {intro[:60]}{'...' if len(intro) > 60 else ''}")
    print()

    parent_dir = find_parent_dir(textbook_root, target_num)
    print(f"父目录   : {parent_dir.relative_to(textbook_root) if parent_dir != textbook_root else '(教材根目录)'}")
    print()

    # 检查目标编号是否已经存在
    existing = find_dir_by_number(parent_dir, target_num)
    if existing is not None:
        print(f"注意: 编号 {target_num} 已存在 → {existing.name}")
        print("将把该节点及之后的所有兄弟节点整体 +1 后，再插入新节点。\n")

    # 收集需要后移的兄弟节点（编号 >= target_num 的同级目录）
    siblings = list_numbered_dirs(parent_dir)
    to_shift = [
        (num, path)
        for num, path in siblings
        if compare_numbers(num, target_num) >= 0
        and len(number_parts(num)) == len(number_parts(target_num))  # 同级
    ]

    if to_shift:
        print(f"需要后移的同级节点（共 {len(to_shift)} 个）:")
        for num, path in to_shift:
            print(f"  {path.name}")
        print()

        # 从大到小重命名，避免冲突
        for num, path in sorted(to_shift, key=lambda x: number_parts(x[0]), reverse=True):
            new_num = increment_last(num)
            print(f"后移子树: {num}  →  {new_num}")
            rename_subtree(path, num, new_num, dry_run=dry_run)
            print()
    else:
        print("没有需要后移的节点，直接插入。\n")

    # 创建新目录
    new_path = parent_dir / new_dir_name
    if new_path.exists():
        raise FileExistsError(f"目录已存在: {new_path}")

    if dry_run:
        print(f"[DRY] 将创建目录: {new_path}")
    else:
        new_path.mkdir(parents=False)
        print(f"已创建目录: {new_path.relative_to(textbook_root)}")

    # 写 index.md
    index_content = build_index_md(
        number=target_num,
        title=title,
        intro=intro,
        parent_num=parent_number(target_num),
    )

    index_path = new_path / "index.md"
    if dry_run:
        print(f"[DRY] 将写入: {index_path}")
        print("--- index.md 预览 ---")
        print(index_content)
        print("---------------------")
    else:
        index_path.write_text(index_content, encoding="utf-8")
        print(f"已写入   : {index_path.relative_to(textbook_root)}")

    print("\n完成。")
    return new_path


def build_index_md(number: str, title: str, intro: str, parent_num: Optional[str]) -> str:
    """生成标准 index.md 内容，链接全部用占位符。"""
    parent_link = f"../index.md" if parent_num else "(教材根目录)"
    # 前后节链接先放占位，后续用扫描脚本补全
    return f"""# {title}

> 编号：`{number}`

## 介绍

{intro}

---

## 导航

- **上一层**：[父级]({parent_link})
- **前一节**：[TODO_PREV]
- **后一节**：[TODO_NEXT]

<!-- 
  链接占位说明：
  - TODO_PREV / TODO_NEXT 由后续扫描脚本自动替换为真正的相对路径
  - 父级链接已指向 ../index.md（同级目录的上一层）
-->
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print("\n错误: 参数不足。")
        print('用法: python insert_chapter.py "<编号_目录名后缀>" "<题目>" "<介绍>"')
        print('示例: python insert_chapter.py "05.2.1_新加测试节" "测试节题目" "这是介绍。"')
        sys.exit(1)

    full_slug = sys.argv[1]
    title = sys.argv[2]
    intro = sys.argv[3]
    dry_run = "--dry-run" in sys.argv

    # 教材根目录 = 当前工作目录
    textbook_root = Path.cwd().resolve()

    # 简单校验：根目录下是否有类似 01_ 或 05_ 的目录
    has_chapter = any(
        p.is_dir() and NUMBER_RE.match(p.name)
        for p in textbook_root.iterdir()
    )
    if not has_chapter:
        print(f"警告: 当前目录 {textbook_root} 下没有发现「数字_名字」格式的章节目录。")
        print("请确认你是在教材根目录下运行本脚本。\n")

    try:
        insert_chapter(textbook_root, full_slug, title, intro, dry_run=dry_run)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
