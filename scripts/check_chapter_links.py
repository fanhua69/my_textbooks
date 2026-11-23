#!/usr/bin/env python3
"""Check and fill textbook section navigation links.

Each directory that contains an index.md is one section. Sibling sections are
ordered by the numeric prefix of the directory name (07 < 07.1 < 07.2 < 07.10).

For every section except the textbook root:

- 上一层 / 返回上级: the parent directory's index.md
- 前一节 / 上一节: the previous sibling. If this section is first, walk up
  until an ancestor has a previous sibling and link to that sibling's
  index.md. If the walk reaches the textbook root, link to the root index.md.
- 后一节 / 下一节: the next sibling. If this section is last, walk up and
  link to the next sibling of the nearest ancestor that has one.

The root index.md has no parent and no previous section. Its next section is
the first top-level chapter.

Existing lines that use either label set are checked. Missing roles are
appended. Wrong targets are rewritten. Pass --check to report only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

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


@dataclass
class Section:
    directory: Path
    name: str
    parent: Section | None = None
    children: list[Section] = field(default_factory=list)

    @property
    def index_path(self) -> Path:
        return self.directory / "index.md"


def sort_key(name: str) -> tuple:
    match = NUMBER_PREFIX.match(name)
    if not match:
        return (1, (), name)
    parts = tuple(int(part) for part in match.group(1).split("."))
    return (0, parts, name)


def discover(root: Path) -> Section:
    root_section = Section(directory=root, name=root.name)

    def walk(section: Section) -> None:
        children: list[Section] = []
        for child in section.directory.iterdir():
            if not child.is_dir() or child.name.startswith("."):
                continue
            if not (child / "index.md").is_file():
                continue
            children.append(Section(directory=child, name=child.name, parent=section))
        children.sort(key=lambda item: sort_key(item.name))
        section.children = children
        for child in children:
            walk(child)

    if not root_section.index_path.is_file():
        raise SystemExit(f"root has no index.md: {root}")
    walk(root_section)
    return root_section


def title_of(path: Path, fallback: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = H1.search(text)
    if match:
        return match.group(1).strip()
    return fallback


def relative_link(source: Section, target: Section) -> str:
    rel = Path(
        __import__("os").path.relpath(target.index_path, source.directory)
    ).as_posix()
    if any(char in rel for char in " ()"):
        from urllib.parse import quote

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


def parse_nav(text: str) -> list[NavHit]:
    hits: list[NavHit] = []
    for index, line in enumerate(text.splitlines()):
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


def target_markdown(source: Section, target: Section | None, titles: dict[Path, str]) -> str:
    if target is None:
        return "无"
    return f"[{titles[target.directory]}]({relative_link(source, target)})"


def iter_sections(section: Section):
    yield section
    for child in section.children:
        yield from iter_sections(child)


@dataclass
class FileResult:
    section: Section
    status: str
    details: list[str]
    new_text: str | None = None


def check_section(
    section: Section, root: Section, titles: dict[Path, str]
) -> FileResult:
    original = section.index_path.read_text(encoding="utf-8")
    lines = original.splitlines()
    hits = parse_nav(original)
    expected = expected_targets(section, root)
    details: list[str] = []
    changed = False
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
        if "## 导航" in original and not changed:
            block = [""]
        elif "## 导航" in original:
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
        return FileResult(section, "ok", [])
    new_text = "\n".join(lines)
    if original.endswith("\n"):
        new_text += "\n"
    status = "missing" if any(item.startswith("缺少") for item in details) else "wrong"
    if any(item.startswith("缺少") for item in details) and any(
        not item.startswith("缺少") for item in details
    ):
        status = "missing"
    return FileResult(section, status, details, new_text if changed else None)


def display_path(section: Section, root: Path) -> str:
    if section.directory == root:
        return "index.md"
    return (section.directory.relative_to(root) / "index.md").as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="核对并补齐教材 index.md 的三向导航链接")
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
        section.directory: title_of(section.index_path, section.name)
        for section in iter_sections(root)
    }

    results = [check_section(section, root, titles) for section in iter_sections(root)]
    counts = {"ok": 0, "wrong": 0, "missing": 0}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
        if result.status == "ok":
            continue
        print(f"{display_path(result.section, root_path)}")
        for detail in result.details:
            print(f"  - {detail}")
        if not args.check and result.new_text is not None:
            result.section.index_path.write_text(result.new_text, encoding="utf-8")

    print(
        f"\n共 {len(results)} 个 index.md：正确 {counts['ok']}，"
        f"链接错误 {counts['wrong']}，缺少链接 {counts['missing']}"
    )
    if args.check:
        print("未修改文件（--check）")
    else:
        print("已写回错误或缺失的文件")
    return 1 if counts["wrong"] or counts["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
