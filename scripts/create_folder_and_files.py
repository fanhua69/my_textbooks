#!/usr/bin/env python3
"""Create textbook directories and Markdown files from a JSON outline."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


def safe_component(value: str) -> str:
    value = value.strip()
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" ._")
    return value or "untitled"


def resolve_json_file(raw_path: Path) -> Path:
    requested = raw_path.expanduser()
    if not requested.suffix:
        requested = requested.with_name(requested.name + ".json")

    if requested.is_absolute():
        return requested.resolve()

    current = (Path.cwd() / requested).resolve()
    if current.is_file():
        return current

    textbook_path = os.environ.get("TEXTBOOKPATH")
    if textbook_path:
        jsons_dir = (Path(textbook_path).expanduser() / "jsons").resolve()
        for candidate in (jsons_dir / requested, jsons_dir / requested.name):
            if candidate.is_file():
                return candidate.resolve()

    return current


def get_children(node: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("parts", "sections", "subsections", "children", "topics"):
        value = node.get(key)
        if isinstance(value, list):
            return value
    return []


def get_markdown_files(node: dict[str, Any]) -> list[Any]:
    for key in ("files", "markdown_files", "md_files", "documents"):
        value = node.get(key)
        if isinstance(value, list):
            return value
    return []


def validate(data: dict[str, Any]) -> None:
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError('JSON 顶层必须包含非空字符串字段 "title"')

    def walk(node: Any, path: str) -> None:
        if not isinstance(node, dict):
            raise ValueError(f"{path} 节点必须是 JSON 对象")
        if not isinstance(node.get("title"), str) or not node["title"].strip():
            raise ValueError(f'{path} 缺少非空 "title"')
        for index, child in enumerate(get_children(node), 1):
            walk(child, f"{path} > [{index}]")

    walk(data, "Root")


def node_slug(node: dict[str, Any], fallback: str) -> str:
    slug = node.get("slug")
    return safe_component(str(slug)) if slug else fallback


def numbered_slug(node: dict[str, Any], number: str) -> str:
    raw = node_slug(node, f"{number}_section")
    suffix = re.sub(r"^\d+(?:\.\d+)*[_\s]+", "", raw)
    return safe_component(f"{number}_{suffix}")


def pretty_title(raw: str) -> str:
    title = raw.strip()
    title = re.sub(r"^\d+(?:\.\d+)*[_\s]+", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.replace("_", " ")


def create_markdown_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


def create_json_markdown_files(raw_node: dict[str, Any], parent: Path) -> None:
    for raw_file in get_markdown_files(raw_node):
        if isinstance(raw_file, str):
            filename = raw_file
        elif isinstance(raw_file, dict):
            filename = str(
                raw_file.get("file")
                or raw_file.get("filename")
                or raw_file.get("path")
                or raw_file.get("name")
                or ""
            )
        else:
            continue

        filename = Path(filename).name
        if filename and filename.lower().endswith(".md"):
            if filename.lower() not in {"_index.md", "_contents.md"}:
                create_markdown_file(parent / filename)


def create_outline(
    raw_children: list[dict[str, Any]],
    parent: Path,
    number_prefix: str,
) -> None:
    for index, child in enumerate(raw_children, 1):
        number = f"{number_prefix}.{index}" if number_prefix else str(index)
        slug = numbered_slug(child, number)
        children = get_children(child)

        if children:
            child_dir = parent / slug
            child_dir.mkdir(parents=True, exist_ok=True)
            create_markdown_file(child_dir / "_index.md")
            create_json_markdown_files(child, child_dir)
            create_outline(children, child_dir, number)
        else:
            filename = f"{number}_{re.sub(r'^\d+(?:\.\d+)*[_\s]+', '', slug)}.md"
            create_markdown_file(parent / filename)


def create_folder_and_files(json_file: Path, output_dir: Path) -> Path:
    with json_file.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    validate(data)

    root_dir = output_dir / safe_component(data["title"])
    root_dir.mkdir(parents=True, exist_ok=True)
    create_markdown_file(root_dir / "_contents.md")
    create_json_markdown_files(data, root_dir)
    create_outline(get_children(data), root_dir, "")
    return root_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="根据 JSON 大纲创建目录结构和 Markdown 文件骨架"
    )
    parser.add_argument("json_file", type=Path)
    parser.add_argument("-o", "--output-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()

    json_file = resolve_json_file(args.json_file)
    output_dir = args.output_dir.expanduser().resolve()

    try:
        root_dir = create_folder_and_files(json_file, output_dir)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"读取或创建失败：{exc}", file=sys.stderr)
        return 1

    print(root_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
