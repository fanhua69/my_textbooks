#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from book_paths import find_book_root
from index_paths import index_filename


@dataclass
class SectionSpan:
    raw_title: str
    start_line: int
    end_line: int
    body: str


def find_chapter_dir(root: Path, chapter_id: str) -> Path:
    start = root.resolve()
    book_root = find_book_root(start)
    prefix = f"{chapter_id}_"
    matches: list[Path] = []

    if start.is_dir() and (start.name.strip() == chapter_id or start.name.strip().startswith(prefix)):
        matches.append(start)

    for p in book_root.rglob("*"):
        if not p.is_dir():
            continue
        clean_name = p.name.strip()
        if clean_name.startswith(prefix) or clean_name == chapter_id:
            matches.append(p)

    matches = list(dict.fromkeys(matches))

    matches.sort(key=lambda p: str(p))
    if not matches:
        raise FileNotFoundError(
            f"错误: 在书籍根目录 '{book_root}' 下未找到以 '{chapter_id}_' 开头的章节目录"
        )

    if len(matches) > 1:
        print(f"提示: 找到多个匹配目录，默认使用第一个: {matches[0]}", file=sys.stderr)

    return matches[0]


def find_chapter_entry(root: Path, chapter_id: str) -> tuple[Path, str]:
    """Return the matched directory or Markdown file and its kind."""
    start = root.resolve()
    book_root = find_book_root(start)
    prefix = f"{chapter_id}_"
    matches: list[tuple[Path, str]] = []

    candidates = [start] if start.exists() else []
    if start.is_dir():
        candidates.extend(p for p in book_root.rglob("*") if p.is_dir())
    candidates.extend(p for p in book_root.rglob("*") if p.is_file())

    for path in candidates:
        if path.is_dir():
            clean_name = path.name.strip()
            if clean_name == chapter_id or clean_name.startswith(prefix):
                matches.append((path, "directory"))
        elif path.is_file() and path.suffix.lower() == ".md":
            stem = path.stem.strip()
            if stem == chapter_id or stem.startswith(prefix):
                matches.append((path, "file"))

    matches = list(dict.fromkeys(matches))
    matches.sort(key=lambda item: (item[1], str(item[0])))
    if not matches:
        raise FileNotFoundError(
            f"错误: 在书籍根目录 '{book_root}' 下未找到以 '{chapter_id}' 对应的章节目录或 Markdown 文件"
        )
    if len(matches) > 1:
        print(f"提示: 找到多个匹配项，默认使用第一个: {matches[0][0]}", file=sys.stderr)
    return matches[0]


def clean_title(name: str) -> str:
    cleaned = name.strip()
    cleaned = re.sub(r"^\d+(?:[.．]\d+)+(?:[.．、])?\s*", "", cleaned)
    cleaned = re.sub(r"^\d+\\?[.．、]\s*", "", cleaned)
    cleaned = re.sub(r"^[零〇一二三四五六七八九十百千万两]+[.．、]\s*", "", cleaned)
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

    excluded = {"导航", "小节索引"}
    return [s for s in raw_spans if s.raw_title.strip() not in excluded]


def normalize_sec_body(sec_body: str) -> str:
    body_lines = sec_body.splitlines()
    if not body_lines:
        return ""
    if re.match(r"^\s*##\s+(?!#)", body_lines[0]):
        body_lines = body_lines[1:]
    return "\n".join(body_lines).strip()


def shift_sub_headings(text: str) -> str:
    """清理子小节标题的序号，并将 ### 及更深层级标题的 '#' 减一。"""
    out_lines: list[str] = []
    in_code = False

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue

        if not in_code:
            m = re.match(r"^(\s*)(#{2,6})(\s+)(.*)$", line)
            if m:
                indent, hashes, rest = m.group(1), m.group(2), m.group(3)
                title = m.group(4)
                new_hashes = "#" * (len(hashes) - 1) if len(hashes) >= 3 else hashes
                cleaned_title = clean_title(title)
                out_lines.append(f"{indent}{new_hashes} {cleaned_title}")
                continue

        out_lines.append(line)

    return "\n".join(out_lines).strip()


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
    out_lines = ["## 小节索引", ""]
    for sub_id, display_title, sub_dir_name in entries:
        encoded_dir = sub_dir_name.replace(" ", "%20")
        out_lines.append(
            f"- [{sub_id} {display_title}](./{encoded_dir}/{index_filename(sub_dir_name)})"
        )
    return "\n".join(out_lines)


def build_file_links_block(entries: list[tuple[str, str, str]]) -> str:
    out_lines = ["## 小节索引", ""]
    for sub_id, display_title, file_name in entries:
        encoded_file = file_name.replace(" ", "%20")
        out_lines.append(f"- [{sub_id} {display_title}](./{encoded_file})")
    return "\n".join(out_lines)


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
    links_block = build_links_block(link_entries)

    parts = [p for p in (prefix_text, links_block, suffix_text) if p]
    return "\n\n".join(parts) + "\n"


def split_directory_chapter(
    target_dir: Path,
    chapter_id: str,
    dry_run: bool,
    force: bool,
    keep_source: bool,
) -> tuple[bool, Path]:
    """Split a directory chapter's numbered index file into sibling Markdown files."""
    index_file = target_dir / index_filename(target_dir)
    if not index_file.is_file():
        raise FileNotFoundError(f"错误: 未找到文件 '{index_file}'")

    content = index_file.read_text(encoding="utf-8")
    spans = split_sections_with_spans(content)
    if not spans:
        return False, index_file

    if not dry_run:
        book_root = find_book_root(index_file)
        removed_dir = book_root / "removed"
        removed_dir.mkdir(parents=True, exist_ok=True)

        archived_name = index_filename(target_dir)
        archived_file = removed_dir / archived_name
        if archived_file.exists() and not force:
            print(f"      removed目录中已存在归档文件（使用 --force 覆盖）: {archived_file}")
        else:
            shutil.copy2(index_file, archived_file)
            print(f"\n已归档原索引文件: {archived_file}")

    print(f"源目录: {target_dir}")
    print(f"共检测到 {len(spans)} 个有效 '##' 片段:\n")

    link_entries: list[tuple[str, str, str]] = []
    for idx, span in enumerate(spans, start=1):
        sub_id = f"{chapter_id}.{idx}"
        display_title = clean_title(span.raw_title)
        safe_title = sanitize_dirname(span.raw_title)
        raw_body = normalize_sec_body(span.body)
        clean_body = shift_sub_headings(raw_body)
        summary = extract_summary(display_title, clean_body)

        raw_file_name = f"{sub_id}_{safe_title}.md"
        sub_file_name = trim_utf8_bytes(raw_file_name, max_bytes=180)
        sub_file_path = target_dir / sub_file_name
        link_entries.append((sub_id, display_title, sub_file_name))
        print(f"  [{idx}] {sub_file_name}")

        if dry_run:
            continue
        if sub_file_path.exists() and not force:
            print(f"      跳过已存在文件（使用 --force 覆盖）: {sub_file_path}")
            continue

        sub_markdown = (
            f"# {sub_id} {display_title}\n\n"
            f"> **简介**：{summary}\n\n"
            f"---\n\n"
            f"{clean_body}\n"
        )
        sub_file_path.write_text(sub_markdown, encoding="utf-8")

    updated_index = update_parent_index_with_files(content, spans, link_entries)
    if dry_run:
        print(
            f"\n(--dry-run 模式：未写入任何文件，预览 {index_file.name} 如下)"
        )
        print("---")
        print(updated_index)
        return True, index_file

    if not keep_source:
        index_file.write_text(updated_index, encoding="utf-8")
        print(f"\n已更新目录索引并移除被拆分片段: {index_file}")
    else:
        print("\n(--keep-source 模式：未修改索引文件)")
    return True, index_file


def split_file_chapter(
    source_file: Path,
    chapter_id: str,
    dry_run: bool,
    force: bool,
    keep_source: bool,
) -> tuple[bool, Path]:
    """Convert a Markdown file into a same-name directory, then split it."""
    target_dir = source_file.with_name(source_file.stem)
    print(f"源文件: {source_file}")
    print(f"新建目录: {target_dir}")

    if dry_run:
        new_index = target_dir / index_filename(target_dir)
        print(f"  [{new_index}]")
        content = source_file.read_text(encoding="utf-8")
        spans = split_sections_with_spans(content)
        if not spans:
            return False, target_dir
        print(f"共检测到 {len(spans)} 个有效 '##' 片段:\n")
        return split_directory_dry_run(target_dir, chapter_id, spans)

    target_dir.mkdir(parents=True, exist_ok=True)
    index_file = target_dir / index_filename(target_dir)
    if index_file.exists() and not force:
        raise FileExistsError(
            f"目标 {index_file.name} 已存在（使用 --force 覆盖）: {index_file}"
        )

    shutil.move(str(source_file), str(index_file))
    print(f"已移动原文件并重命名为: {index_file}")
    return split_directory_chapter(
        target_dir,
        chapter_id,
        dry_run=False,
        force=force,
        keep_source=keep_source,
    )


def split_directory_dry_run(
    target_dir: Path,
    chapter_id: str,
    spans: list[SectionSpan],
) -> tuple[bool, Path]:
    """Preview file-mode split without creating or moving files."""
    for idx, span in enumerate(spans, start=1):
        display_title = clean_title(span.raw_title)
        safe_title = sanitize_dirname(span.raw_title)
        sub_id = f"{chapter_id}.{idx}"
        sub_file_name = trim_utf8_bytes(
            f"{sub_id}_{safe_title}.md",
            max_bytes=180,
        )
        print(f"  [{idx}] {target_dir.name}/{sub_file_name}")
    return True, target_dir


def update_parent_index_with_files(
    content: str,
    spans: list[SectionSpan],
    link_entries: list[tuple[str, str, str]],
) -> str:
    lines = content.splitlines(keepends=True)
    first_start = spans[0].start_line
    last_end = spans[-1].end_line
    prefix_text = "".join(lines[:first_start]).rstrip()
    suffix_text = "".join(lines[last_end:]).strip()
    links_block = build_file_links_block(link_entries)
    parts = [p for p in (prefix_text, links_block, suffix_text) if p]
    return "\n\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按 '##' 二级标题拆分章节目录的编号索引文件，或拆分章节 Markdown 文件到同名目录"
    )
    parser.add_argument("chapter_id", help="章节号，例如 1.1.1 或 2.1.4")
    parser.add_argument("--dry-run", action="store_true", help="仅预览将创建的目录与文件，不实际写入")
    parser.add_argument("--force", action="store_true", help="若目标编号索引文件已存在则覆盖")
    parser.add_argument("--keep-source", action="store_true", help="保留父索引文件中已被拆分的 '##' 片段")
    parser.add_argument("--root", default=".", help="递归查找章节目录的根路径（默认: 当前目录）")

    args = parser.parse_args()
    root_path = Path(args.root)

    try:
        target_entry, entry_kind = find_chapter_entry(root_path, args.chapter_id)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if entry_kind == "directory":
        split_directory_chapter(
            target_dir=target_entry,
            chapter_id=args.chapter_id,
            dry_run=args.dry_run,
            force=args.force,
            keep_source=args.keep_source,
        )
    else:
        split_file_chapter(
            source_file=target_entry,
            chapter_id=args.chapter_id,
            dry_run=args.dry_run,
            force=args.force,
            keep_source=args.keep_source,
        )

    if args.dry_run:
        return 0

    print("拆分完成。")

    scripts_dir = Path(__file__).resolve().parent
    book_root = find_book_root(root_path)
    subprocess.run(
        [
            sys.executable,
            str(scripts_dir / "check_folder_names.py"),
            "--root",
            str(book_root),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(scripts_dir / "check_chapter_links.py"),
            str(book_root),
        ],
        check=True,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())