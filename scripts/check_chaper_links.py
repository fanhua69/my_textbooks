#!/usr/bin/env python3
"""Check and fill textbook section navigation links and child directory TOCs.

Each non-hidden subdirectory under the textbook root is treated as a section.
If the root or any section directory lacks index.md, a new one is created
(unless --check is passed) with title and intro set to the directory name
with spaces removed, followed by child TOC (when applicable) and
prev/next/parent navigation links.

Sibling sections are ordered by the numeric prefix of the directory name
(07 < 07.1 < 07.2 < 07.10).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, unquote

ROLE_LABELS = {
    "prev": ("前一节", "上一节"),
    "next": ("后一节", "下一节"),
    "parent": ("上一层", "返回上级"),
}
PREFERRED = {"prev": "前一节", "next": "后一节", "parent": "上一层"}
LABEL_TO_ROLE = {
    label: role for role, labels in ROLE_LABELS.items() for label in labels
}

NUMBER_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)")
NAV_LINE = re.compile(
    r"^(?P<prefix>\s*(?:[-*+]|\d+\.)?\s*(?:←\s*|↑\s*)?"
    r"(?:\*\*)?(?P<label>前一节|上一节|后一节|下一节|上一层|返回上级)(?:\*\*)?"
    r"\s*[：:]\s*)(?P<body>.*)$"
)
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
NONE_MARKER = re.compile(r"无(?:（[^）]*）|\([^)]*\))?")
H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_HEADING = re.compile(r"^##\s+(.+?)\s*$")
TOC_HEADING_NAMES = {"目录", "本节目录", "本章目录", "子目录", "子章节"}
NAV_HEADING_NAMES = {"导航"}


@dataclass
class Section:
    directory: Path
    name: str
    parent: Section | None = None
    children: list[Section] = field(default_factory=list)
    existed_before: bool = True

    @property
    def index_path(self) -> Path:
        return self.directory / "index.md"

    @property
    def clean_name(self) -> str:
        return "".join(self.name.split())


def sort_key(name: str) -> tuple:
    match = NUMBER_PREFIX.match(name)
    if not match:
        return (1, (), name)
    parts = tuple(int(part) for part in match.group(1).split("."))
    return (0, parts, name)


def discover(root: Path) -> Section:
    root_section = Section(
        directory=root,
        name=root.name,
        existed_before=(root / "index.md").is_file(),
    )

    def walk(section: Section) -> None:
        children: list[Section] = []
        for child in section.directory.iterdir():
            if not child.is_dir() or child.name.startswith("."):
                continue
            has_index = (child / "index.md").is_file()
            children.append(
                Section(
                    directory=child,
                    name=child.name,
                    parent=section,
                    existed_before=has_index,
                )
            )
        children.sort(key=lambda item: sort_key(item.name))
        section.children = children
        for child in children:
            walk(child)

    walk(root_section)
    return root_section


def title_of(section: Section) -> str:
    if section.index_path.is_file():
        text = section.index_path.read_text(encoding="utf-8")
        match = H1.search(text)
        if match:
            return match.group(1).strip()
    return section.clean_name


def render_new_index_base(section: Section) -> str:
    label = section.clean_name
    return f"# {label}\n\n{label}\n"


def relative_link(source: Section, target: Section) -> str:
    rel = Path(os.path.relpath(target.index_path, source.directory)).as_posix()
    if any(char in rel for char in " ()"):
        return quote(rel, safe="/-._~")
    return rel


def previous_section(section: Section, root: Section) -> Section | None:
    if section is root:
        return None
    assert section.parent is not None
    siblings = section.parent.children
    index = siblings.index(section)
    if index > 0:
        return siblings[index - 1]
    found = previous_section(section.parent, root)
    if found is not None:
        return found
    return root


def next_section(section: Section, root: Section) -> Section | None:
    if section is root:
        return root.children[0] if root.children else None
    assert section.parent is not None
    siblings = section.parent.children
    index = siblings.index(section)
    if index + 1 < len(siblings):
        return siblings[index + 1]
    if section.parent is root:
        return None
    return next_section(section.parent, root)


def expected_targets(section: Section, root: Section) -> dict[str, Section | None]:
    parent = None if section is root else section.parent
    return {
        "parent": parent,
        "prev": previous_section(section, root),
        "next": next_section(section, root),
    }


@dataclass
class NavHit:
    role: str
    line_index: int
    prefix: str
    body: str
    href: str | None


def parse_nav(lines: list[str]) -> list[NavHit]:
    hits: list[NavHit] = []
    for index, line in enumerate(lines):
        match = NAV_LINE.match(line)
        if not match:
            continue
        body = match.group("body")
        link = MD_LINK.search(body)
        href = unquote(link.group(2).strip()) if link else None
        if href is not None:
            href = href.split("#", 1)[0].split("?", 1)[0]
            if href == "":
                href = None
        hits.append(
            NavHit(
                role=LABEL_TO_ROLE[match.group("label")],
                line_index=index,
                prefix=match.group("prefix"),
                body=body,
                href=href,
            )
        )
    return hits


def resolves_to(source: Section, href: str, target: Section) -> bool:
    destination = (source.directory / href).resolve()
    return destination == target.index_path.resolve()


def render_body(body: str, target_md: str) -> str:
    if MD_LINK.search(body):
        return MD_LINK.sub(target_md, body, count=1)
    if "无" in body:
        return NONE_MARKER.sub(target_md, body, count=1)
    suffix = ""
    stripped = body.rstrip()
    if stripped.endswith("→"):
        suffix = " →"
    return target_md + suffix


def target_markdown(
    source: Section, target: Section | None, titles: dict[Path, str]
) -> str:
    if target is None:
        return "无"
    return f"[{titles[target.directory]}]({relative_link(source, target)})"


def iter_sections(section: Section):
    yield section
    for child in section.children:
        yield from iter_sections(child)


def find_h2_section_range(
    lines: list[str], heading_names: set[str]
) -> tuple[int, int] | None:
    start: int | None = None
    for idx, line in enumerate(lines):
        match = H2_HEADING.match(line)
        if match:
            title = match.group(1).strip()
            if start is None and title in heading_names:
                start = idx
            elif start is not None:
                return (start, idx)
    if start is not None:
        return (start, len(lines))
    return None


def find_nav_insert_index(lines: list[str]) -> int:
    nav_h2 = find_h2_section_range(lines, NAV_HEADING_NAMES)
    if nav_h2 is not None:
        idx = nav_h2[0]
        probe = idx - 1
        while probe >= 0 and lines[probe].strip() == "":
            probe -= 1
        if probe >= 0 and lines[probe].strip() == "---":
            return probe
        return idx

    nav_hits = parse_nav(lines)
    if nav_hits:
        idx = nav_hits[0].line_index
        probe = idx - 1
        while probe >= 0 and lines[probe].strip() == "":
            probe -= 1
        if probe >= 0 and lines[probe].strip() == "---":
            return probe
        return idx

    return len(lines)


def build_children_toc_lines(
    section: Section, titles: dict[Path, str]
) -> list[str]:
    items = [
        f"- {target_markdown(section, child, titles)}"
        for child in section.children
    ]
    return ["## 目录", "", *items]


def check_and_update_children_toc(
    section: Section,
    lines: list[str],
    titles: dict[Path, str],
    details: list[str],
) -> tuple[list[str], bool]:
    if not section.children:
        return lines, False

    expected_toc = build_children_toc_lines(section, titles)
    toc_range = find_h2_section_range(lines, TOC_HEADING_NAMES)

    if toc_range is not None:
        start, end = toc_range
        content_end = end
        while content_end > start and lines[content_end - 1].strip() == "":
            content_end -= 1
        existing_block = lines[start:content_end]
        if existing_block == expected_toc:
            return lines, False

        details.append(f"更新子目录列表（共 {len(section.children)} 个子节）")
        replacement = [*expected_toc, ""]
        updated = lines[:start] + replacement + lines[end:]
        return updated, True

    existing_hrefs: list[str] = []
    for line in lines:
        if NAV_LINE.match(line):
            continue
        for match in MD_LINK.finditer(line):
            href = unquote(match.group(2).strip()).split("#", 1)[0].split("?", 1)[0]
            if href:
                existing_hrefs.append(href)

    missing_children = [
        child
        for child in section.children
        if not any(resolves_to(section, href, child) for href in existing_hrefs)
    ]
    if not missing_children:
        return lines, False

    if len(missing_children) == len(section.children):
        details.append(f"缺少子目录列表（共 {len(section.children)} 个子节）")
    else:
        missing_names = ", ".join(child.name for child in missing_children)
        details.append(f"缺少部分子目录链接：{missing_names}")

    insert_at = find_nav_insert_index(lines)
    prefix_lines = lines[:insert_at]
    suffix_lines = lines[insert_at:]

    while prefix_lines and prefix_lines[-1].strip() == "":
        prefix_lines.pop()

    inserted: list[str] = []
    if prefix_lines:
        inserted.extend(["", "---", ""])
    inserted.extend(expected_toc)
    if suffix_lines:
        inserted.append("")

    return prefix_lines + inserted + suffix_lines, True


@dataclass
class FileResult:
    section: Section
    status: str
    details: list[str]
    new_text: str | None = None
    created: bool = False


def check_section(
    section: Section, root: Section, titles: dict[Path, str]
) -> FileResult:
    created = not section.existed_before and not section.index_path.is_file()
    if created:
        original = render_new_index_base(section)
    else:
        original = section.index_path.read_text(encoding="utf-8")

    lines = original.splitlines()
    details: list[str] = []
    changed = created

    if created:
        details.append(f"新建 index.md（题目与介绍：{section.clean_name}）")

    lines, toc_changed = check_and_update_children_toc(
        section, lines, titles, details
    )
    if toc_changed:
        changed = True

    hits = parse_nav(lines)
    expected = expected_targets(section, root)
    seen: dict[str, list[NavHit]] = {"prev": [], "next": [], "parent": []}
    for hit in hits:
        seen[hit.role].append(hit)

    for role, target in expected.items():
        role_hits = seen[role]
        if target is None:
            for hit in role_hits:
                if hit.href is not None:
                    details.append(f"{PREFERRED[role]} 应为空，实际指向 {hit.href}")
                    lines[hit.line_index] = hit.prefix + render_body(hit.body, "无")
                    changed = True
            continue

        if not role_hits:
            details.append(f"缺少{PREFERRED[role]}")
            continue

        for hit in role_hits:
            if hit.href is not None and resolves_to(section, hit.href, target):
                continue
            shown = hit.href or hit.body.strip() or "(空)"
            details.append(
                f"{PREFERRED[role]} 不正确：{shown} → {relative_link(section, target)}"
            )
            lines[hit.line_index] = hit.prefix + render_body(
                hit.body, target_markdown(section, target, titles)
            )
            changed = True

    missing_roles = [
        role
        for role, target in expected.items()
        if target is not None and not seen[role]
    ]
    if missing_roles:
        block = ["", "---", "", "## 导航", ""]
        if "## 导航" in "\n".join(lines):
            block = [""]
        for role in ("parent", "prev", "next"):
            if role not in missing_roles:
                continue
            target = expected[role]
            block.append(
                f"- **{PREFERRED[role]}**：{target_markdown(section, target, titles)}"
            )
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend(block)
        changed = True

    if not details:
        return FileResult(section, "ok", [], created=created)

    new_text = "\n".join(lines)
    if original.endswith("\n"):
        new_text += "\n"
    status = "missing" if any(item.startswith("缺少") or item.startswith("新建") for item in details) else "wrong"
    return FileResult(
        section,
        status,
        details,
        new_text if changed else None,
        created=created,
    )


def display_path(section: Section, root: Path) -> str:
    if section.directory == root:
        return "index.md"
    return (section.directory.relative_to(root) / "index.md").as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="核对并补齐教材 index.md、子目录列表与三向导航链接"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="教材根目录，默认当前目录",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="只报告，不改文件",
    )
    args = parser.parse_args()
    root_path = Path(args.root).resolve()
    root = discover(root_path)
    titles = {
        section.directory: title_of(section)
        for section in iter_sections(root)
    }

    results = [check_section(section, root, titles) for section in iter_sections(root)]
    counts = {"ok": 0, "wrong": 0, "missing": 0}
    created_count = 0
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
        if result.created:
            created_count += 1
        if result.status == "ok":
            continue
        print(f"{display_path(result.section, root_path)}")
        for detail in result.details:
            print(f"  - {detail}")
        if not args.check and result.new_text is not None:
            result.section.index_path.write_text(result.new_text, encoding="utf-8")

    print(
        f"\n共 {len(results)} 个 index.md（新建 {created_count} 个）："
        f"正确 {counts['ok']}，需要更新 {counts['wrong']}，缺少链接/文件 {counts['missing']}"
    )
    if args.check:
        print("未修改文件（--check）")
    else:
        print("已写回新建、错误或缺失的文件")
    return 1 if counts["wrong"] or counts["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())