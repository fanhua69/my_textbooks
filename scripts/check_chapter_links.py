#!/usr/bin/env python3
"""Rebuild textbook Markdown directory sections and navigation links."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote


NUMBER_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)(?:[\s._-]+(.*))?$")
H1 = re.compile(r"^#\s+(.+?)\s*$")
H2 = re.compile(r"^##\s+(.+?)\s*$")
INTRO_LINE = re.compile(
    r"^\s*(?:\*\*)?介绍(?:\*\*)?\s*[：:]\s*(.*?)\s*$"
)
TOC_HEADINGS = {"小节索引", "目录", "本节目录", "本章目录", "子目录", "子章节"}
NAV_HEADINGS = {"导航"}
NAV_LINE = re.compile(
    r"^\s*(?:[-*+]\s*)?(?:⬅️|➡️|⬆️|⏺️|<span[^>]*>\s*(?:⟵|⟶)\s*</span>|⟵|⟶|⤴|←|→|↑|•)?\s*"
    r"(?:前一节|上一节|当前节|后一节|下一节|上一层|返回上级)\s*[：:]"
)


@dataclass
class Section:
    directory: Path
    name: str
    parent: Section | None = None
    children: list[Section] = field(default_factory=list)
    markdown_path: Path | None = None

    @property
    def index_path(self) -> Path:
        if self.markdown_path is not None:
            return self.markdown_path
        index = self.directory / "_index.md"
        if index.is_file():
            return index
        contents = self.directory / "_contents.md"
        if contents.is_file():
            return contents
        return self.directory / "_index.md"

    @property
    def clean_name(self) -> str:
        return " ".join(self.name.split()).strip()

    @property
    def section_number(self) -> str | None:
        match = NUMBER_PREFIX.match(self.clean_name)
        return match.group(1) if match else None

    @property
    def section_title_text(self) -> str:
        match = NUMBER_PREFIX.match(self.clean_name)
        if match and match.group(2):
            return match.group(2).strip()
        return self.clean_name


def parse_num_tuple(number: str) -> tuple[int, ...]:
    return tuple(int(part) for part in number.split("."))


def sort_key(name: str) -> tuple:
    match = NUMBER_PREFIX.match(name.strip())
    if not match:
        return (1, (), name.lower(), name)
    return (0, parse_num_tuple(match.group(1)), name.lower(), name)


def discover(root_path: Path) -> Section:
    root = Section(
        directory=root_path,
        name=root_path.name,
    )

    def walk(section: Section) -> None:
        entries = [
            entry
            for entry in section.directory.iterdir()
            if not entry.name.startswith(".")
            and not (
                section.directory == root_path
                and entry.is_dir()
                and entry.name == "removed"
            )
        ]
        for entry in entries:
            if entry.is_dir():
                children = Section(
                    directory=entry,
                    name=entry.name,
                    parent=section,
                )
                section.children.append(children)
            elif (
                entry.is_file()
                and entry.suffix.lower() == ".md"
                and entry.name.lower() not in {"_index.md", "_contents.md"}
            ):
                section.children.append(
                    Section(
                        directory=section.directory,
                        name=entry.stem,
                        parent=section,
                        markdown_path=entry,
                    )
                )

        section.children.sort(key=lambda child: sort_key(child.name))
        for child in section.children:
            if child.markdown_path is None:
                walk(child)

    walk(root)
    return root


def iter_sections(section: Section):
    yield section
    for child in section.children:
        yield from iter_sections(child)


def title_of(section: Section) -> str:
    raw_title = ""
    if section.index_path.is_file():
        for line in section.index_path.read_text(encoding="utf-8").splitlines():
            match = H1.match(line)
            if match:
                raw_title = match.group(1).strip()
                break

    if not raw_title:
        raw_title = section.section_title_text or section.clean_name

    raw_title = re.sub(r"^\d+(?:\.\d+)*(?:[\s._-]+)?", "", raw_title).strip()
    if section.section_number and raw_title:
        return f"{section.section_number} {raw_title}"
    if section.section_number:
        return section.section_number
    return raw_title or section.clean_name


def normalized_title(section: Section) -> str:
    title = title_of(section)
    number = section.section_number
    if number:
        title = re.sub(r"^\d+(?:\.\d+)*[\s._-]+", "", title).strip()
        return f"{number} {title}".strip()

    title = re.sub(r"^\d+(?:\.\d+)*[\s._-]+", "", title).strip()
    return title


def normalized_intro(text: str) -> str:
    intro = re.sub(r"^\d+(?:\.\d+)*(?:[\s._-]+)?", "", text.strip()).strip()
    return intro


def relative_link(source: Section, target: Section) -> str:
    rel = Path(os.path.relpath(target.index_path, source.directory)).as_posix()
    if any(char in rel for char in " ()"):
        return quote(rel, safe="/-._~")
    return rel


def sibling_section(section: Section, offset: int) -> Section | None:
    current = section
    while current.parent is not None:
        siblings = sorted(
            current.parent.children,
            key=lambda sibling: sort_key(sibling.name),
        )
        position = next(
            (index for index, sibling in enumerate(siblings) if sibling is current),
            -1,
        )
        if position >= 0:
            target_position = position + offset
            if 0 <= target_position < len(siblings):
                return siblings[target_position]
        current = current.parent
    return None


def strip_generated_sections(text: str) -> str:
    lines = text.splitlines()
    result: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        heading = H2.match(line)

        if heading and (
            heading.group(1).strip() in TOC_HEADINGS
            or heading.group(1).strip() in NAV_HEADINGS
        ):
            index += 1
            while index < len(lines):
                next_heading = H2.match(lines[index])
                if next_heading:
                    break
                index += 1
            continue

        if NAV_LINE.match(line):
            index += 1
            continue

        result.append(line)
        index += 1

    while result and not result[-1].strip():
        result.pop()
    while result and result[-1].strip() == "---":
        result.pop()
        while result and not result[-1].strip():
            result.pop()

    return "\n".join(result).rstrip() + "\n"


def rebuild_markdown(section: Section, root: Section) -> tuple[str, bool]:
    original = (
        section.index_path.read_text(encoding="utf-8")
        if section.index_path.is_file()
        else ""
    )
    base = strip_generated_sections(original)
    base_lines = base.splitlines()

    existing_intro: str | None = None
    content_lines: list[str] = []
    h1_removed = False
    for line in base_lines:
        h1_match = H1.match(line)
        if h1_match and not h1_removed:
            h1_removed = True
            continue
        intro_match = INTRO_LINE.match(line)
        if intro_match:
            if existing_intro is None:
                existing_intro = intro_match.group(1).strip()
            continue
        content_lines.append(line)

    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)
    while content_lines and not content_lines[-1].strip():
        content_lines.pop()

    title = normalized_title(section)
    intro = existing_intro
    if intro is None or not intro:
        intro = title
    intro = normalized_intro(intro)

    lines = [f"# {title}", "", f"**介绍**: {intro}", ""]
    if content_lines:
        lines.extend(content_lines)
        lines.append("")

    flat = list(iter_sections(root))
    previous = sibling_section(section, -1)
    following = sibling_section(section, 1)
    parent = section.parent

    titles = {id(node): normalized_title(node) for node in flat}

    if section.children:
        lines.extend(["", "## 目录", ""])
        for child in section.children:
            label = titles[id(child)]
            lines.append(
                f"- [{label}]({relative_link(section, child)})"
            )

    lines.extend(["", "---", "", "## 导航", ""])
    if previous is not None:
        lines.append(
            f"⬅️ 上一节：[{titles[id(previous)]}]"
            f"({relative_link(section, previous)})"
        )
    else:
        lines.append("⬅️ 上一节：无（这是本目录的第一页）")

    lines.append(f"⏺️ 当前节：[{titles[id(section)]}]({relative_link(section, section)})")

    if following is not None:
        lines.append(
            f"➡️ 下一节：[{titles[id(following)]}]"
            f"({relative_link(section, following)})"
        )
    else:
        lines.append("➡️ 下一节：无（这是本目录的最后一页）")

    if parent is not None:
        lines.append(
            f"⬆️ 返回上级：[{titles[id(parent)]}]"
            f"({relative_link(section, parent)})"
        )

    rebuilt = "\n".join(lines).rstrip() + "\n"
    return rebuilt, rebuilt != original


def all_markdown_sections(root: Section):
    for section in iter_sections(root):
        if not section.index_path.exists():
            section.index_path.parent.mkdir(parents=True, exist_ok=True)
            section.index_path.touch()
        yield section


def main() -> int:
    parser = argparse.ArgumentParser(
        description="统一重建教材 Markdown 的目录和前后上级导航"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="教材根目录，默认当前目录",
    )
    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    if not root_path.is_dir():
        print(f"错误: 根目录不存在: {root_path}", file=sys.stderr)
        return 1

    root = discover(root_path)
    sections = list(all_markdown_sections(root))
    changed_count = 0

    for section in sections:
        rebuilt, changed = rebuild_markdown(section, root)
        display = section.index_path.relative_to(root_path).as_posix()
        if not changed:
            continue
        changed_count += 1
        print(display)
        section.index_path.write_text(rebuilt, encoding="utf-8")

    print(
        f"\n共检查 {len(sections)} 个 Markdown 文件："
        f"需要重建 {changed_count} 个"
    )
    print("已统一重建目录和前后上级导航")
    return 0


if __name__ == "__main__":
    sys.exit(main())
