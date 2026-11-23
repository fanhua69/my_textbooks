#!/usr/bin/env python3
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SectionSpan:
    raw_title: str
    start_line: int  # 0-based inclusive in lines
    end_line: int    # 0-based exclusive in lines
    body: str


def find_chapter_dir(root: Path, chapter_id: str) -> Path:
    prefix = f"{chapter_id}_"
    matches: list[Path] = []

    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        clean_name = p.name.strip()
        if clean_name.startswith(prefix) or clean_name == chapter_id:
            matches.append(p)

    matches.sort(key=lambda p: str(p))
    if not matches:
        raise FileNotFoundError(
            f"错误: 在 '{root.resolve()}' 下未找到以 '{chapter_id}_' 开头的目录"
        )

    if len(matches) > 1:
        print(f"提示: 找到多个匹配目录，默认使用第一个: {matches[0]}", file=sys.stderr)

    return matches[0]


def clean_title(name: str) -> str:
    cleaned = re.sub(r"^\d+\.\s+", "", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def sanitize_dirname(name: str) -> str:
    base = clean_title(name)
    cleaned = re.sub(r'[\\/:*?"<>|]', " ", base)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def trim_utf8_bytes(text: str, max_bytes: int = 180) -> str:
    raw = text.encode("utf-8")
    if len(raw) <= max_bytes:
        return text
    return raw[:max_bytes].decode("utf-8", errors="ignore").rstrip()


def split_sections_with_spans(content: str) -> list[SectionSpan]:
    lines = content.splitlines(keepends=True)
    raw_spans: list[SectionSpan] = []
    current_raw_title: str | None = None
    current_start: int | None = None
    in_code = False

    for idx, line in enumerate(lines):
        stripped_line = line.rstrip("\r\n")
        if stripped_line.lstrip().startswith("```"):
            in_code = not in_code
            continue

        if not in_code:
            m = re.match(r"^\s*##\s+(?!#)(.+)$", stripped_line)
            if m:
                if current_raw_title is not None and current_start is not None:
                    body_text = "".join(lines[current_start:idx]).strip()
                    raw_spans.append(
                        SectionSpan(
                            raw_title=current_raw_title,
                            start_line=current_start,
                            end_line=idx,
                            body=body_text,
                        )
                    )
                current_raw_title = m.group(1).strip()
                current_start = idx

    if current_raw_title is not None and current_start is not None:
        body_text = "".join(lines[current_start : len(lines)]).strip()
        raw_spans.append(
            SectionSpan(
                raw_title=current_raw_title,
                start_line=current_start,
                end_line=len(lines),
                body=body_text,
            )
        )

    return [s for s in raw_spans if s.raw_title.strip() != "导航"]


def normalize_sec_body(sec_body: str) -> str:
    body_lines = sec_body.splitlines()
    if not body_lines:
        return ""
    if re.match(r"^\s*##\s+(?!#)", body_lines[0]):
        body_lines = body_lines[1:]
    return "\n".join(body_lines).strip()


def extract_summary(sec_title: str, clean_body: str) -> str:
    body_lines = clean_body.splitlines()
    in_code = False
    para_buf: list[str] = []

    for raw in body_lines:
        s = raw.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not s:
            if para_buf:
                break
            continue
        if s.startswith(("#", "---", "***", ">", "- ", "* ", "+ ")):
            if para_buf:
                break
            continue
        clean_s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
        para_buf.append(clean_s)

    summary = " ".join(para_buf).strip()
    if not summary:
        summary = f"本节介绍“{sec_title}”的核心概念与实践要点。"
    if len(summary) > 160:
        summary = summary[:157].rstrip() + "..."
    return summary


def build_links_block(entries: list[tuple[str, str, str]]) -> str:
    lines = ["## 小节索引", ""]
    for sub_id, display_title, sub_dir_name in entries:
        encoded_dir = sub_dir_name.replace(" ", "%20")
        lines.append(f"- [{sub_id} {display_title}](./{encoded_dir}/index.md)")
    lines.append("")
    return "\n".join(lines)


def update_parent_index(
    content: str,
    spans: list[SectionSpan],
    link_entries: list[tuple[str, str, str]],
) -> str:
    lines = content.splitlines(keepends=True)
    first_start = spans[0].start_line
    last_end = spans[-1].end_line

    prefix_text = "".join(lines[:first_start]).rstrip()
    suffix_text = "".join(lines[last_end:]).strip()
    links_block = build_links_block(link_entries).strip()

    parts = [p for p in (prefix_text, links_block, suffix_text) if p]
    return "\n\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按 '##' 二级标题拆分指定章节下的 index.md 为子目录与子 index.md，并回写父 index.md 链接"
    )
    parser.add_argument("chapter_id", help="章节号，例如 1.1.1 或 2.1.4")
    parser.add_argument("--dry-run", action="store_true", help="仅预览将创建的目录与文件，不实际写入")
    parser.add_argument("--force", action="store_true", help="若目标 index.md 已存在则覆盖")
    parser.add_argument("--keep-source", action="store_true", help="保留父 index.md 中已被拆分的 '##' 片段")
    parser.add_argument("--root", default=".", help="递归查找章节目录的根路径（默认: 当前目录）")

    args = parser.parse_args()
    root_path = Path(args.root)

    try:
        target_dir = find_chapter_dir(root_path, args.chapter_id)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    index_file = target_dir / "index.md"
    if not index_file.is_file():
        print(f"错误: 未找到文件 '{index_file}'", file=sys.stderr)
        return 1

    content = index_file.read_text(encoding="utf-8")
    spans = split_sections_with_spans(content)

    if not spans:
        print(f"提示: '{index_file}' 中未找到任何可拆分的 '##' 二级标题片段。", file=sys.stderr)
        return 1

    print(f"源目录: {target_dir}")
    print(f"共检测到 {len(spans)} 个有效 '##' 片段:\n")

    link_entries: list[tuple[str, str, str]] = []

    for idx, span in enumerate(spans, start=1):
        sub_id = f"{args.chapter_id}.{idx}"
        display_title = clean_title(span.raw_title)
        safe_title = sanitize_dirname(span.raw_title)
        raw_dir_name = f"{sub_id}_{safe_title}"
        sub_dir_name = trim_utf8_bytes(raw_dir_name, max_bytes=180)
        sub_dir_path = target_dir / sub_dir_name
        sub_index_path = sub_dir_path / "index.md"
        clean_body = normalize_sec_body(span.body)
        summary = extract_summary(display_title, clean_body)

        sub_markdown = (
            f"# {sub_id} {display_title}\n\n"
            f"> **简介**：{summary}\n\n"
            f"---\n\n"
            f"{clean_body}\n"
        )

        link_entries.append((sub_id, display_title, sub_dir_name))
        print(f"  [{idx}] {sub_dir_name}/index.md")

        if args.dry_run:
            continue

        sub_dir_path.mkdir(parents=True, exist_ok=True)
        if sub_index_path.exists() and not args.force:
            print(f"      跳过已存在文件（使用 --force 覆盖）: {sub_index_path}")
            continue

        sub_index_path.write_text(sub_markdown, encoding="utf-8")

    updated_parent = update_parent_index(content, spans, link_entries)

    if args.dry_run:
        print("\n(--dry-run 模式：未写入任何文件，预览父 index.md 如下)")
        print("---")
        print(updated_parent)
    else:
        if not args.keep_source:
            index_file.write_text(updated_parent, encoding="utf-8")
            print(f"\n已更新父目录索引并移除被拆分片段: {index_file}")
        else:
            print("\n(--keep-source 模式：未修改父 index.md)")
        print("拆分完成。")

    return 0


if __name__ == "__main__":
    sys.exit(main())