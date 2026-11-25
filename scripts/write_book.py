#!/usr/bin/env python3
"""
Generate a nested Markdown textbook directory from a JSON outline.
Supports arbitrary depth (Parts, Sections, Subsections, Sub-subsections, etc.).

Usage:
  python3 gemini-code-1794576208405.py modern_cpp_learning.json
  python3 gemini-code-1794576208405.py 0_software_engineering.json
  python3 gemini-code-1794576208405.py 0_software_engineering.json --output-dir ~/Documents/books
  python3 gemini-code-1794576208405.py 0_software_engineering.json --force
  python3 gemini-code-1794576208405.py 0_software_engineering.json --update-nav

Options:
  --force       允许覆盖已存在的 contents.md / index.md（会重置为初始模板，谨慎使用）
  --update-nav  仅更新已存在 contents.md / index.md 中的导航栏，保留手写正文内容

Navigation logic:
  - 上一节：指向前一节（同级前驱兄弟）。若本节为第一节，则指向上一级目录的兄弟的前一个 index.md（递归回溯）。
  - 下一节：指向后一节（同级后继兄弟）。若本节为最后一节，则指向上一级目录的兄弟的后一个 index.md（递归回溯）。
  - 返回上级：指向直接父级的 contents.md 或 index.md。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


def safe_component(value: str) -> str:
    """Return a filesystem-safe directory component."""
    value = value.strip()
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" ._")
    return value or "untitled"


def node_slug(node: dict[str, Any], fallback: str) -> str:
    slug = node.get("slug")
    return safe_component(str(slug)) if slug else fallback


def pretty_title(raw: str) -> str:
    """'1.1.3_互斥锁、读写锁与自旋锁_mutex_rwlock_and_spinlock'
    -> '互斥锁、读写锁与自旋锁  mutex rwlock and spinlock'"""
    t = raw.strip()
    t = re.sub(r"^\d+(?:\.\d+)*[_\s]+", "", t)  # 去掉 JSON 标题自带的编号前缀
    m = re.match(r"^(.*?)_([\x00-\x7f]+)$", t)  # 第一个 "_" 之后若全是 ASCII，视为英文部分
    if m:
        cn, en = m.groups()
        return f"{cn}  {en.replace('_', ' ')}"
    return t.replace("_", " ")


def get_raw_children(node: dict[str, Any]) -> list[dict[str, Any]]:
    """Retrieve child nodes using common outline keys."""
    for key in ("parts", "sections", "subsections", "children", "topics"):
        val = node.get(key)
        if isinstance(val, list):
            return val
    return []


def validate_outline(data: dict[str, Any]) -> None:
    """Recursively validate JSON outline structure."""
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError('JSON 顶层必须包含非空字符串字段 "title"')

    top_children = get_raw_children(data)
    if not top_children:
        raise ValueError('JSON 顶层必须包含非空子节点列表（如 "parts" 或 "sections"）')

    def check_node(node: Any, path_str: str) -> None:
        if not isinstance(node, dict):
            raise ValueError(f"{path_str} 节点必须是 JSON 对象")
        if not isinstance(node.get("title"), str) or not node["title"].strip():
            raise ValueError(f'{path_str} 缺少非空 "title"')
        children = get_raw_children(node)
        for ci, child in enumerate(children, 1):
            check_node(child, f"{path_str} > [{ci}] {child.get('title', 'untitled')}")

    for pi, child in enumerate(top_children, 1):
        check_node(child, f"Part [{pi}] {child.get('title', 'untitled')}")


class OutlineNode:
    """Represents a node in the textbook outline tree."""

    def __init__(
        self,
        raw: dict[str, Any],
        title: str,
        intro: str,
        dir_path: Path,
        index_path: Path,
        level: int = 1,
        parent: OutlineNode | None = None,
        idx: int = 0,
    ):
        self.raw = raw
        self.title = title
        self.intro = intro
        self.dir_path = dir_path
        self.index_path = index_path
        self.level = level
        self.parent = parent
        self.idx = idx
        self.children: list[OutlineNode] = []

    def get_prev_target(self, root_node: OutlineNode) -> tuple[str, Path] | None:
        """
        前一节链接逻辑：
        指向前一节（同级前驱兄弟）。如果本节为第一节，则指向上一级 index.md 的兄弟的前一个 index.md。
        若所有祖先均为第一节，则指向根目录 contents.md。
        """
        if self.parent is None:
            return None

        # 如果不是同级第一节，指向同级前驱
        if self.idx > 0:
            prev_sibling = self.parent.children[self.idx - 1]
            return (prev_sibling.title, prev_sibling.index_path)

        # 本节为第一节：向上回溯寻找“上一级 index.md 的兄弟的前一个 index.md”
        curr = self.parent
        while curr is not None:
            if curr.parent is not None and curr.idx > 0:
                parent_prev_sibling = curr.parent.children[curr.idx - 1]
                return (parent_prev_sibling.title, parent_prev_sibling.index_path)
            curr = curr.parent

        # 向上回溯到底，若本节点非根节点，则指向教材首页
        if self != root_node:
            return (root_node.title, root_node.index_path)
        return None

    def get_next_target(self) -> tuple[str, Path] | None:
        """
        后一节链接逻辑：
        指向后一节（同级后继兄弟）。如果本节为最后一节，则指向上一级 index.md 的兄弟的后一个 index.md。
        若所有祖先均为最后一节，则无下一节。
        """
        if self.parent is None:
            # 根节点的下一节为第一个子节点
            if self.children:
                return (self.children[0].title, self.children[0].index_path)
            return None

        # 如果不是同级最后一节，指向同级后继
        if self.idx < len(self.parent.children) - 1:
            next_sibling = self.parent.children[self.idx + 1]
            return (next_sibling.title, next_sibling.index_path)

        # 本节为最后一节：向上回溯寻找“上一级 index.md 的兄弟的后一个 index.md”
        curr = self.parent
        while curr is not None:
            if curr.parent is not None and curr.idx < len(curr.parent.children) - 1:
                parent_next_sibling = curr.parent.children[curr.idx + 1]
                return (parent_next_sibling.title, parent_next_sibling.index_path)
            curr = curr.parent

        return None

    def get_parent_target(self) -> tuple[str, Path] | None:
        """返回上级链接逻辑：指向直接父节点的 index.md。"""
        if self.parent is not None:
            return (self.parent.title, self.parent.index_path)
        return None


def build_outline_tree(
    raw_children: list[dict[str, Any]],
    parent_node: OutlineNode,
    current_dir: Path,
    num_prefix: str,
    level_depth: int,
) -> None:
    """Recursively build OutlineNode objects for arbitrary depth."""
    for idx, child in enumerate(raw_children):
        child_num = f"{num_prefix}.{idx + 1}" if num_prefix else f"{idx + 1}"
        child_title = f"{child_num} {pretty_title(child['title'])}"
        child_slug = node_slug(child, f"{idx + 1:02d}_section")
        child_dir = current_dir / child_slug
        child_index = child_dir / "index.md"
        child_intro = child.get("intro", "")

        node = OutlineNode(
            raw=child,
            title=child_title,
            intro=child_intro,
            dir_path=child_dir,
            index_path=child_index,
            level=1,
            parent=parent_node,
            idx=idx,
        )
        parent_node.children.append(node)

        next_children = get_raw_children(child)
        if next_children:
            build_outline_tree(
                raw_children=next_children,
                parent_node=node,
                current_dir=child_dir,
                num_prefix=child_num,
                level_depth=level_depth + 1,
            )


def collect_all_nodes(node: OutlineNode) -> list[OutlineNode]:
    """Collect all nodes in depth-first order."""
    nodes = [node]
    for child in node.children:
        nodes.extend(collect_all_nodes(child))
    return nodes


def relative_link(source_dir: Path, target_index: Path, label: str) -> str:
    rel = Path(os.path.relpath(target_index, source_dir)).as_posix()
    rel = rel.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
    return f"[{label}]({rel})"


def render_nav_lines(
    previous: tuple[str, Path] | None,
    parent: tuple[str, Path] | None,
    following: tuple[str, Path] | None,
    current_dir: Path,
) -> list[str]:
    nav = []
    if previous:
        nav.append(f"← 上一节：{relative_link(current_dir, previous[1], previous[0])}")
    else:
        nav.append("← 上一节：无（这是教材的第一页）")
    if parent:
        nav.append(f"↑ 返回上级：{relative_link(current_dir, parent[1], parent[0])}")
    if following:
        nav.append(f"下一节：{relative_link(current_dir, following[1], following[0])} →")
    else:
        nav.append("下一节：无（这是教材的最后一页）")
    return nav


def render_index(
    title: str,
    intro: str,
    children: list[tuple[str, Path]],
    previous: tuple[str, Path] | None,
    following: tuple[str, Path] | None,
    current_dir: Path,
    level: int = 1,
    parent: tuple[str, Path] | None = None,
) -> str:
    lines = [f'{"#" * level} {title}', "", intro.strip() if intro else "本节内容待补充。", ""]
    if children:
        lines.extend(["## 本节目录", ""])
        for child_title, child_index in children:
            lines.append(f"- {relative_link(current_dir, child_index, child_title)}")
        lines.append("")

    lines.extend(["---", "", "## 导航", ""])
    lines.extend(render_nav_lines(previous, parent, following, current_dir))
    lines.append("")
    return "\n".join(lines)


def update_nav_in_markdown(text: str, nav_lines: list[str]) -> str:
    new_nav_block = "## 导航\n\n" + "\n".join(nav_lines) + "\n"
    pattern = r"## 导航\s*\n+(?:[ \t]*(?:[←↑]|下一节|[-*]\s*[←↑]|[-*]\s*下一节)[^\n]*\n*)+"
    if re.search(pattern, text):
        return re.sub(pattern, new_nav_block + "\n", text)
    else:
        return text.rstrip() + "\n\n---\n\n" + new_nav_block


def update_heading(text: str, title: str, level: int) -> str:
    new_head = f'{"#" * level} {title}'
    if re.match(r"#+ ", text):
        return re.sub(r"\A#+ .*", lambda m: new_head, text, count=1)
    return new_head + "\n\n" + text


def update_toc(text: str, children: list[tuple[str, Path]], current_dir: Path) -> str:
    if not children:
        return text
    block = "## 本节目录\n\n" + "\n".join(
        f"- {relative_link(current_dir, p, t)}" for t, p in children
    ) + "\n\n"
    pattern = r"## 本节目录[ \t]*\n+(?:- [^\n]*\n*)+"
    if re.search(pattern, text):
        return re.sub(pattern, lambda m: block, text, count=1)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="根据 JSON 大纲生成教材 Markdown 目录（支持任意深度）")
    parser.add_argument("json_file", type=Path, help="教材大纲 JSON 文件")
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=Path.cwd(),
        help="输出父目录；省略时使用当前工作目录",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="允许覆盖已存在的 contents.md / index.md（会重置为初始模板，请谨慎使用）",
    )
    parser.add_argument(
        "--update-nav", action="store_true",
        help="仅更新已存在 contents.md / index.md 的导航栏，保留手写正文内容；缺失文件则新建",
    )
    args = parser.parse_args()

    json_file = args.json_file.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    try:
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        validate_outline(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"读取或验证 JSON 失败：{exc}", file=sys.stderr)
        return 1

    root_dir = output_dir / safe_component(data["title"])
    if root_dir.exists() and not root_dir.is_dir():
        print(f"目标路径已存在且不是目录：{root_dir}", file=sys.stderr)
        return 1

    root_index_path = root_dir / "contents.md"
    root_intro = data.get("intro") or data.get("description") or f"欢迎阅读《{data['title']}》教程。"

    root_node = OutlineNode(
        raw=data,
        title=data["title"],
        intro=root_intro,
        dir_path=root_dir,
        index_path=root_index_path,
        level=1,
        parent=None,
        idx=0,
    )

    # 递归建立整棵大纲树
    top_raw_children = get_raw_children(data)
    build_outline_tree(
        raw_children=top_raw_children,
        parent_node=root_node,
        current_dir=root_dir,
        num_prefix="",
        level_depth=1,
    )

    all_nodes = collect_all_nodes(root_node)

    # 检查已存在文件，防止意外覆盖
    existing = [n.index_path for n in all_nodes if n.index_path.exists()]
    if existing and not args.force and not args.update_nav:
        print(
            f"发现 {len(existing)} 个已存在的 contents.md / index.md。\n"
            f"- 如需仅更新导航栏并保留手写正文内容，请使用：--update-nav\n"
            f"- 如需全量覆盖重置为初始模板，请备份后使用：--force",
            file=sys.stderr,
        )
        return 2

    # 生成或更新根目录 contents.md 及各级目录的 index.md
    for node in all_nodes:
        node.dir_path.mkdir(parents=True, exist_ok=True)

        prev_target = node.get_prev_target(root_node)
        parent_target = node.get_parent_target()
        next_target = node.get_next_target()
        children_targets = [(c.title, c.index_path) for c in node.children]

        if args.update_nav and node.index_path.exists():
            existing_text = node.index_path.read_text(encoding="utf-8")
            nav_lines = render_nav_lines(prev_target, parent_target, next_target, node.dir_path)
            updated_text = update_nav_in_markdown(existing_text, nav_lines)
            updated_text = update_heading(updated_text, node.title, node.level)
            updated_text = update_toc(updated_text, children_targets, node.dir_path)
            node.index_path.write_text(updated_text, encoding="utf-8")
        else:
            content = render_index(
                title=node.title,
                intro=node.intro,
                children=children_targets,
                previous=prev_target,
                following=next_target,
                current_dir=node.dir_path,
                level=node.level,
                parent=parent_target,
            )
            node.index_path.write_text(content, encoding="utf-8")

    mode_str = "更新导航栏" if args.update_nav else "生成/覆盖"
    print(f"完成：{root_dir}（模式：{mode_str}）")
    print(f"成功处理 {len(all_nodes)} 个文件（根目录 contents.md 及各级 index.md）")
    print("导航结构：上一节（兄弟或回溯上一级兄弟的前一个） / 返回上级（直接父级） / 下一节（兄弟或回溯上一级兄弟的后一个）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())