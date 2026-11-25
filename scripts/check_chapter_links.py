#!/usr/bin/env python3
"""Check and fill textbook section titles, intros, links, and child TOCs."""

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

NUMBER_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)(?:[\s._-]+(.*))?$")
LEADING_SECTION_NUM = re.compile(r"^\d+(?:\.\d+)*\s*")
NAV_LINE = re.compile(
    r"^(?P<prefix>\s*(?:[-*+]|\d+\.)?\s*(?:←\s*|↑\s*)?"
    r"(?:\*\*)?(?P<label>前一节|上一节|后一节|下一节|上一层|返回上级)(?:\*\*)?"
    r"\s*[：:]\s*)(?P<body>.*)$"
)
INTRO_LINE = re.compile(r"^\s*(?:\*\*)?介绍(?:\*\*)?\s*[：:]\s*(?P<val>.*?)\s*$")
NONE_MARKER = re.compile(r"无(?:（[^）]*）|\([^)]*\))?")
H1 = re.compile(r"^#\s+(.+?)\s*$")
H2_HEADING = re.compile(r"^##\s+(.+?)\s*$")
TOC_HEADING_NAMES = {"目录", "本节目录", "本章目录", "子目录", "子章节"}
NAV_HEADING_NAMES = {"导航"}


def extract_md_link(text: str, pos: int = 0) -> tuple[str, str, int, int] | None:
    """Return (label, href, start, end) for the first [label](href) from pos."""
    idx = pos
    n = len(text)
    while idx < n:
        open_bracket = text.find("[", idx)
        if open_bracket == -1:
            return None
        depth = 0
        close_bracket = -1
        for i in range(open_bracket, n):
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
                if depth == 0:
                    close_bracket = i
                    break
        if (
            close_bracket == -1
            or close_bracket + 1 >= n
            or text[close_bracket + 1] != "("
        ):
            idx = open_bracket + 1
            continue
        close_paren = text.find(")", close_bracket + 2)
        if close_paren == -1:
            return None
        label = text[open_bracket + 1 : close_bracket]
        href = text[close_bracket + 2 : close_paren].strip()
        return label, href, open_bracket, close_paren + 1
    return None


def iter_md_links(text: str):
    """Yield (label, href, start, end) for all Markdown links in text."""
    pos = 0
    while True:
        hit = extract_md_link(text, pos)
        if hit is None:
            break
        yield hit
        pos = hit[3]


@dataclass
class Section:
    directory: Path
    name: str
    parent: Section | None = None
    children: list[Section] = field(default_factory=list)
    existed_before: bool = True
    renamed_from: str | None = None

    @property
    def index_path(self) -> Path:
        contents_path = self.directory / "contents.md"
        if contents_path.is_file():
            return contents_path
        return self.directory / "index.md"

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


def parse_num_tuple(num_str: str) -> tuple[int, ...]:
    return tuple(int(part) for part in num_str.split("."))


def sort_key(name: str) -> tuple:
    match = NUMBER_PREFIX.match(name.strip())
    if not match:
        return (1, (), name.lower(), name)
    parts = parse_num_tuple(match.group(1))
    return (0, parts, name.lower(), name)


def discover(root: Path) -> Section:
    root_section = Section(
        directory=root,
        name=root.name,
        existed_before=(
            (root / "contents.md").is_file() or (root / "index.md").is_file()
        ),
    )

    def walk(section: Section) -> None:
        children: list[Section] = []
        for child in section.directory.iterdir():
            if not child.is_dir() or child.name.startswith("."):
                continue
            has_index = (
                (child / "contents.md").is_file() or (child / "index.md").is_file()
            )
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


def iter_sections(section: Section):
    yield section
    for child in section.children:
        yield from iter_sections(child)


def update_subtree_paths(section: Section, new_dir: Path) -> None:
    section.directory = new_dir
    for child in section.children:
        update_subtree_paths(child, new_dir / child.name)


def assign_missing_section_numbers(
    root: Section, dry_run: bool, details_by_dir: dict[Path, list[str]]
) -> None:
    """Assign non-colliding section numbers to unnumbered directories alphabetically."""
    used_tuples: set[tuple[int, ...]] = set()
    used_strings: set[str] = set()

    for sec in iter_sections(root):
        num = sec.section_number
        if num:
            used_strings.add(num)
            used_tuples.add(parse_num_tuple(num))

    def next_free_number(parent: Section | None) -> str:
        parent_num = parent.section_number if parent else None
        base_prefix = f"{parent_num}." if parent_num else ""
        counter = 1
        while True:
            candidate = f"{base_prefix}{counter}"
            cand_tuple = parse_num_tuple(candidate)
            if candidate not in used_strings and cand_tuple not in used_tuples:
                used_strings.add(candidate)
                used_tuples.add(cand_tuple)
                return candidate
            counter += 1

    queue: list[Section] = [root]
    while queue:
        current = queue.pop(0)
        unnumbered = [c for c in current.children if c.section_number is None]
        unnumbered.sort(key=lambda c: (c.name.lower(), c.name))

        for child in unnumbered:
            assigned_num = next_free_number(current)
            old_name = child.name
            new_name = f"{assigned_num} {old_name}".strip()
            new_dir = child.directory.parent / new_name
            msg = f"目录无节号，分配节号并重命名：{old_name} → {new_name}"
            details_by_dir.setdefault(child.directory, []).append(msg)
            child.renamed_from = old_name
            child.name = new_name
            if not dry_run:
                child.directory.rename(new_dir)
                update_subtree_paths(child, new_dir)

        current.children.sort(key=lambda c: sort_key(c.name))
        queue.extend(current.children)


def format_h1_for_section(section: Section, raw_h1_text: str | None) -> str:
    sec_num = section.section_number
    fallback_title = section.section_title_text or section.clean_name

    if raw_h1_text is not None:
        title_body = LEADING_SECTION_NUM.sub("", raw_h1_text.strip()).strip()
        if not title_body:
            title_body = fallback_title
    else:
        title_body = fallback_title

    if sec_num:
        return f"# {sec_num} {title_body}"
    return f"# {title_body}"


def format_intro_line(section: Section, existing_intro_text: str | None) -> str:
    content = (existing_intro_text or "").strip()
    if not content:
        content = section.section_title_text or section.clean_name
    return f"**介绍**: {content}"


def check_and_update_title_and_intro(
    section: Section,
    lines: list[str],
    details: list[str],
) -> tuple[list[str], bool]:
    changed = False
    work = list(lines)

    # 1. 收集所有 H1 行，保留第一处有效 H1，移除其余重复 H1
    h1_indices: list[int] = [
        idx for idx, line in enumerate(work) if H1.match(line) is not None
    ]
    first_h1_raw = H1.match(work[h1_indices[0]]).group(1) if h1_indices else None
    expected_h1 = format_h1_for_section(section, first_h1_raw)

    if len(h1_indices) > 1:
        extra_count = len(h1_indices) - 1
        details.append(f"移除重复标题 {extra_count} 处")
        for idx in reversed(h1_indices[1:]):
            work.pop(idx)
        changed = True

    h1_indices = [
        idx for idx, line in enumerate(work) if H1.match(line) is not None
    ]
    if not h1_indices:
        details.append(f"缺少题目，已添加：{expected_h1}")
        work = [expected_h1, "", *work]
        changed = True
    else:
        h1_idx = h1_indices[0]
        if work[h1_idx].rstrip() != expected_h1:
            details.append(f"更新题目：{work[h1_idx].strip()} → {expected_h1}")
            work[h1_idx] = expected_h1
            changed = True
        # 如果 H1 不在顶部且前面只有空白行，收拢多余前导空行
        if h1_idx > 0 and all(l.strip() == "" for l in work[:h1_idx]):
            work = work[h1_idx:]
            changed = True

    h1_idx = next(idx for idx, line in enumerate(work) if H1.match(line) is not None)

    # 2. 收集所有显式“介绍”行，保留第一条内容，移除其余重复“介绍”行
    intro_indices: list[int] = [
        idx for idx, line in enumerate(work) if INTRO_LINE.match(line) is not None
    ]
    existing_intro_val: str | None = None
    if intro_indices:
        m0 = INTRO_LINE.match(work[intro_indices[0]])
        if m0:
            existing_intro_val = m0.group("val")
        if len(intro_indices) > 1:
            extra_intro = len(intro_indices) - 1
            details.append(f"移除重复介绍 {extra_intro} 处")
            for idx in reversed(intro_indices[1:]):
                work.pop(idx)
            changed = True
        # 重新定位唯一显式介绍行
        intro_indices = [
            idx for idx, line in enumerate(work) if INTRO_LINE.match(line) is not None
        ]
        if intro_indices:
            idx0 = intro_indices[0]
            work.pop(idx0)
            if idx0 < len(work) and work[idx0].strip() == "":
                work.pop(idx0)
            h1_idx = next(
                idx for idx, line in enumerate(work) if H1.match(line) is not None
            )

    # 若没有显式介绍行，检查 H1 后第一个非空行是否为普通摘要段落
    if existing_intro_val is None:
        scan_idx = h1_idx + 1
        while scan_idx < len(work) and work[scan_idx].strip() == "":
            scan_idx += 1
        if scan_idx < len(work):
            candidate = work[scan_idx]
            is_structural = (
                H2_HEADING.match(candidate) is not None
                or H1.match(candidate) is not None
                or candidate.strip() == "---"
                or NAV_LINE.match(candidate) is not None
                or candidate.lstrip().startswith(("- ", "* ", "+ "))
            )
            if not is_structural:
                existing_intro_val = candidate.strip()
                work.pop(scan_idx)
                if scan_idx < len(work) and work[scan_idx].strip() == "":
                    work.pop(scan_idx)

    expected_intro = format_intro_line(section, existing_intro_val)
    if existing_intro_val is None:
        details.append(f"缺少介绍，已添加：{expected_intro}")
    elif f"**介绍**: {existing_intro_val.strip()}" != expected_intro:
        details.append(f"规范介绍格式 → {expected_intro}")

    after_h1 = work[h1_idx + 1 :]
    while after_h1 and after_h1[0].strip() == "":
        after_h1.pop(0)
    new_work = [*work[: h1_idx + 1], "", expected_intro]
    if after_h1:
        new_work.extend(["", *after_h1])
    if new_work != lines:
        changed = True
    return new_work, changed


def title_of(section: Section) -> str:
    if section.index_path.is_file():
        text = section.index_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            match = H1.match(line)
            if match:
                return (
                    format_h1_for_section(section, match.group(1))
                    .removeprefix("# ")
                    .strip()
                )
    return format_h1_for_section(section, None).removeprefix("# ").strip()


def render_new_index_base(section: Section) -> str:
    h1 = format_h1_for_section(section, None)
    intro = format_intro_line(section, None)
    return f"{h1}\n\n{intro}\n"


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
        link = extract_md_link(body)
        href = unquote(link[1]) if link else None
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
    link = extract_md_link(body)
    if link:
        _, _, start, end = link
        return body[:start] + target_md + body[end:]
    if "无" in body:
        return NONE_MARKER.sub(lambda _: target_md, body, count=1)
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
        for _, raw_href, _, _ in iter_md_links(line):
            href = unquote(raw_href).split("#", 1)[0].split("?", 1)[0]
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
    section: Section,
    root: Section,
    titles: dict[Path, str],
    pre_details: list[str],
) -> FileResult:
    created = not section.existed_before and not section.index_path.is_file()
    if created:
        original = render_new_index_base(section)
    else:
        original = section.index_path.read_text(encoding="utf-8")

    lines = original.splitlines()
    details: list[str] = list(pre_details)
    changed = created

    if created:
        details.append(f"新建 {section.index_path.name}（{section.clean_name}）")

    lines, meta_changed = check_and_update_title_and_intro(section, lines, details)
    if meta_changed:
        changed = True

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
    if original.endswith("\n") or changed:
        new_text += "\n"
    status = (
        "missing"
        if any(
            item.startswith(("缺少", "新建", "目录无节号")) for item in details
        )
        else "wrong"
    )
    return FileResult(
        section,
        status,
        details,
        new_text if changed else None,
        created=created,
    )


def display_path(section: Section, root: Path) -> str:
    return section.index_path.relative_to(root).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="核对并补齐教材目录节号、题目、介绍、子目录列表与三向导航链接"
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

    rename_details: dict[Path, list[str]] = {}
    assign_missing_section_numbers(root, dry_run=args.check, details_by_dir=rename_details)

    titles = {
        section.directory: title_of(section)
        for section in iter_sections(root)
    }

    results = [
        check_section(section, root, titles, rename_details.get(section.directory, []))
        for section in iter_sections(root)
    ]
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
            result.section.index_path.parent.mkdir(parents=True, exist_ok=True)
            result.section.index_path.write_text(result.new_text, encoding="utf-8")

    print(
        f"\n共 {len(results)} 个 contents.md / index.md（新建 {created_count} 个）："
        f"正确 {counts['ok']}，需要更新 {counts['wrong']}，缺少链接/文件 {counts['missing']}"
    )
    if args.check:
        print("未修改文件（--check）")
    else:
        print("已写回新建、错误或缺失的文件")
    return 1 if counts["wrong"] or counts["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
