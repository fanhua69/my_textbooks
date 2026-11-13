#!/usr/bin/env python3
"""
Generate a nested Markdown textbook directory from a JSON outline.

Usage:
  python3 generate_textbook.py modern_cpp_learning.json
  python3 generate_textbook.py modern_cpp_learning.json --output-dir ~/Documents/books
  python3 generate_textbook.py modern_cpp_learning.json --output-dir .
  python3 generate_textbook.py modern_cpp_learning.json --force

If --output-dir is omitted, the current working directory is used.
The generated root directory is named after the JSON "title".
Navigation links connect every index.md in depth-first reading order.
"""

from __future__ import annotations

import argparse
import json
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


def validate_outline(data: dict[str, Any]) -> None:
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError('JSON 顶层必须包含非空字符串字段 "title"')
    if not isinstance(data.get("parts"), list) or not data["parts"]:
        raise ValueError('JSON 顶层必须包含非空数组字段 "parts"')

    for pi, part in enumerate(data["parts"], 1):
        if not isinstance(part, dict) or not part.get("title"):
            raise ValueError(f"parts[{pi-1}] 缺少 title")
        if not isinstance(part.get("sections"), list):
            raise ValueError(f'部分 "{part["title"]}" 缺少 sections 数组')
        for si, section in enumerate(part["sections"], 1):
            if not isinstance(section, dict) or not section.get("title"):
                raise ValueError(f"parts[{pi-1}].sections[{si-1}] 缺少 title")
            if not isinstance(section.get("subsections"), list):
                raise ValueError(f'二级节 "{section["title"]}" 缺少 subsections 数组')
            for ui, subsection in enumerate(section["subsections"], 1):
                if not isinstance(subsection, dict) or not subsection.get("title"):
                    raise ValueError(
                        f"parts[{pi-1}].sections[{si-1}].subsections[{ui-1}] 缺少 title"
                    )


def node_slug(node: dict[str, Any], fallback: str) -> str:
    slug = node.get("slug")
    return safe_component(str(slug)) if slug else fallback


def relative_link(source_dir: Path, target_index: Path, label: str) -> str:
    rel = Path(__import__("os").path.relpath(target_index, source_dir))
    return f"[{label}]({rel.as_posix()})"


def render_index(
    title: str,
    intro: str,
    children: list[tuple[str, Path]],
    previous: tuple[str, Path] | None,
    following: tuple[str, Path] | None,
    current_dir: Path,
    level: int,
) -> str:
    lines = [f'{"#" * level} {title}', "", intro.strip() if intro else "本节内容待补充。", ""]
    if children:
        lines.extend(["## 本节目录", ""])
        for child_title, child_index in children:
            lines.append(f"- {relative_link(current_dir, child_index, child_title)}")
        lines.append("")

    lines.extend(["---", "", "## 导航", ""])
    nav = []
    if previous:
        nav.append(f"← 上一节：{relative_link(current_dir, previous[1], previous[0])}")
    else:
        nav.append("← 上一节：无（这是教材的第一页）")
    if following:
        nav.append(f"下一节：{relative_link(current_dir, following[1], following[0])} →")
    else:
        nav.append("下一节：无（这是教材的最后一页）")
    lines.extend(nav)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="根据 JSON 大纲生成教材 Markdown 目录")
    parser.add_argument("json_file", type=Path, help="教材大纲 JSON 文件")
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=Path.cwd(),
        help="输出父目录；省略时使用当前工作目录",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="目标教材目录已存在时允许覆盖同名 index.md（不会删除其他文件）",
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

    root = output_dir / safe_component(data["title"])
    if root.exists() and not root.is_dir():
        print(f"目标路径已存在且不是目录：{root}", file=sys.stderr)
        return 1

    # Build the tree first. Each page record contains its index path and child links.
    pages: list[dict[str, Any]] = []
    part_records = []

    for pi, part in enumerate(data["parts"], 1):
        part_dir = root / node_slug(part, f"{pi:02d}_part")
        part_index = part_dir / "index.md"
        section_records = []
        for si, section in enumerate(part["sections"], 1):
            section_dir = part_dir / node_slug(section, f"{si:02d}_section")
            section_index = section_dir / "index.md"
            subsection_records = []
            for ui, subsection in enumerate(section["subsections"], 1):
                subsection_dir = section_dir / node_slug(subsection, f"{ui:02d}_topic")
                subsection_index = subsection_dir / "index.md"
                subsection_records.append({
                    "title": subsection["title"],
                    "intro": subsection.get("intro", ""),
                    "dir": subsection_dir,
                    "index": subsection_index,
                })
            section_records.append({
                "title": section["title"],
                "intro": section.get("intro", ""),
                "dir": section_dir,
                "index": section_index,
                "subsections": subsection_records,
            })
        part_records.append({
            "title": part["title"],
            "intro": part.get("intro", ""),
            "dir": part_dir,
            "index": part_index,
            "sections": section_records,
        })

    # Depth-first order: part page -> its section pages -> its topic pages -> next part.
    for part in part_records:
        pages.append({"title": part["title"], "intro": part["intro"],
                      "dir": part["dir"], "index": part["index"],
                      "children": [(s["title"], s["index"]) for s in part["sections"]],
                      "level": 1})
        for section in part["sections"]:
            pages.append({"title": section["title"], "intro": section["intro"],
                          "dir": section["dir"], "index": section["index"],
                          "children": [(u["title"], u["index"]) for u in section["subsections"]],
                          "level": 1})
            for topic in section["subsections"]:
                pages.append({"title": topic["title"], "intro": topic["intro"],
                              "dir": topic["dir"], "index": topic["index"],
                              "children": [], "level": 1})

    # Refuse accidental overwrite unless --force. Existing non-index files are preserved.
    existing = [p["index"] for p in pages if p["index"].exists()]
    if existing and not args.force:
        print(
            f"发现 {len(existing)} 个已存在的 index.md。为避免覆盖，请备份后加 --force。",
            file=sys.stderr,
        )
        return 2

    for i, page in enumerate(pages):
        previous = (pages[i - 1]["title"], pages[i - 1]["index"]) if i > 0 else None
        following = (pages[i + 1]["title"], pages[i + 1]["index"]) if i + 1 < len(pages) else None
        page["dir"].mkdir(parents=True, exist_ok=True)
        content = render_index(
            page["title"], page["intro"], page["children"],
            previous, following, page["dir"], page["level"],
        )
        page["index"].write_text(content, encoding="utf-8")

    print(f"完成：{root}")
    print(f"创建/更新 {len(pages)} 个 index.md 文件")
    print("导航顺序：按 JSON 大纲深度优先排列（部分 → 二级节 → 三级节）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
