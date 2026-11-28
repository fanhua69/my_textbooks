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

from index_paths import (
    is_index_marker_name,
    metadata_index_path,
)


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


def get_children(node: dict[str, Any]) -> list[Any]:
    for key in (
        "parts",
        "chapters",
        "sections",
        "subsections",
        "children",
        "curriculum_modules",
        "modules",
        "units",
        "lessons",
        "topics",
        "items",
    ):
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


def normalize_outline(data: dict[str, Any]) -> None:
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        for key in ("outline_title", "course_title", "book_title", "name"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                data["title"] = value
                break

    normalize_outline_node(data)


def normalize_outline_node(node: dict[str, Any]) -> None:
    if not isinstance(node.get("title"), str):
        for key in ("name", "label", "outline_title", "course_title"):
            value = node.get(key)
            if isinstance(value, str) and value.strip():
                node["title"] = value
                break

    child_keys = (
        "parts",
        "chapters",
        "sections",
        "subsections",
        "children",
        "curriculum_modules",
        "modules",
        "units",
        "lessons",
        "topics",
        "items",
    )
    for key in child_keys:
        children = node.get(key)
        if not isinstance(children, list):
            continue
        for index, child in enumerate(children):
            if isinstance(child, str) and key in child_keys:
                children[index] = {"title": child}
            elif isinstance(child, dict):
                normalize_outline_node(child)


def node_number(node: dict[str, Any], fallback: str) -> str:
    for key in (
        "chapter_id",
        "section_id",
        "subsection_id",
        "part_id",
        "module_id",
        "unit_id",
        "lesson_id",
        "topic_id",
        "item_id",
    ):
        value = node.get(key)
        if isinstance(value, (str, int)) and re.fullmatch(
            r"\d+(?:\.\d+)*", str(value).strip()
        ):
            return str(value).strip()
    return fallback


def node_slug(node: dict[str, Any], fallback: str) -> str:
    slug = node.get("slug")
    return safe_component(str(slug or node.get("title") or fallback))


def numbered_slug(node: dict[str, Any], number: str) -> str:
    raw = node_slug(node, f"{number}_section")
    suffix = re.sub(r"^\d+(?:\.\d+)*[_\s]+", "", raw)
    return safe_component(f"{number}_{suffix}")


def pretty_title(raw: str) -> str:
    title = raw.strip()
    title = re.sub(r"^\d+(?:\.\d+)*[_\s]+", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.replace("_", " ")


def has_chinese_text(data: dict[str, Any]) -> bool:
    language = str(data.get("language") or "").lower()
    if language.startswith(("zh", "cn")):
        return True
    text = " ".join(
        str(data.get(key) or "")
        for key in ("title", "outline_title", "course_title", "book_title")
    )
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))


def contents_index_path(book_root: Path, chinese: bool) -> Path:
    return book_root / ("0_大纲.md" if chinese else "0_CONTENTS.md")


def create_markdown_file(path: Path, title: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or (title and not path.read_text(encoding="utf-8").strip()):
        content = f"# {title}\n\n" if title else ""
        path.write_text(content, encoding="utf-8")


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
            if (
                filename.lower() not in {
                    "目录.md",
                    "contents.md",
                    "0_contents.md",
                    "0_大纲.md",
                }
                and not is_index_marker_name(filename)
            ):
                create_markdown_file(parent / filename)


def create_outline(
    raw_children: list[dict[str, Any]],
    parent: Path,
    number_prefix: str,
    book_root: Path,
    chinese: bool,
) -> None:
    for index, child in enumerate(raw_children, 1):
        fallback = f"{number_prefix}.{index}" if number_prefix else str(index)
        number = node_number(child, fallback)
        slug = numbered_slug(child, number)
        children = get_children(child)

        if children:
            child_dir = parent / slug
            child_dir.mkdir(parents=True, exist_ok=True)
            create_markdown_file(metadata_index_path(book_root, child_dir, chinese=chinese))
            create_json_markdown_files(child, child_dir)
            create_outline(children, child_dir, number, book_root, chinese)
        else:
            filename = f"{slug}.md"
            title = f"{number} {pretty_title(child['title'])}"
            create_markdown_file(parent / filename, title)


def create_folder_and_files(json_file: Path, output_dir: Path) -> Path:
    with json_file.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("JSON 顶层必须是对象")
    normalize_outline(data)
    validate(data)

    root_dir = output_dir / safe_component(data["title"])
    root_dir.mkdir(parents=True, exist_ok=True)
    chinese = has_chinese_text(data)
    create_json_markdown_files(data, root_dir)
    create_outline(get_children(data), root_dir, "", root_dir, chinese)
    create_markdown_file(contents_index_path(root_dir, chinese))
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
