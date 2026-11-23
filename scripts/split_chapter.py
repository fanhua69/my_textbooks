#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path


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
    # 去掉开头的 "1. "、"2. " 这类序号前缀，并规范化空白
    cleaned = re.sub(r"^\d+\.\s+", "", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def sanitize_dirname(name: str) -> str:
    base = clean_title(name)
    # 清理文件系统非法字符（/ \ : * ? " < > |）
    cleaned = re.sub(r'[\\/:*?"<>|]', " ", base)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def split_sections(content: str) -> list[tuple[str, str]]:
    lines = content.splitlines(keepends=True)
    sections: list[tuple[str, str]] = []
    current_raw_title: str | None = None
    current_lines: list[str] = []

    for line in lines:
        # 匹配行首可能有缩进的 "## "，排除 "###"
        m = re.match(r"^\s*##\s+(?!#)(.+?)\s*\r?\n?\$", line)
        if m:
            if current_raw_title is not None:
                sections.append((current_raw_title, "".join(current_lines).strip()))
            current_raw_title = m.group(1).strip()
            current_lines = [line]
        else:
            if current_raw_title is not None:
                current_lines.append(line)

    if current_raw_title is not None:
        sections.append((current_raw_title, "".join(current_lines).strip()))

    # 过滤掉“导航”片段
    return [(t, b) for (t, b) in sections if t.strip() != "导航"]


def normalize_sec_body(sec_body: str, cleaned_title: str) -> str:
    body_lines = sec_body.splitlines()
    if not body_lines:
        return sec_body
    if re.match(r"^\s*##\s+(?!#)", body_lines[0]):
        body_lines[0] = f"## {cleaned_title}"
    return "\n".join(body_lines).strip()


def extract_summary(sec_title: str, sec_body: str) -> str:
    body_lines = sec_body.splitlines()[1:]
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按 '##' 二级标题拆分指定章节下的 index.md 为子目录与子 index.md"
    )
    parser.add_argument("chapter_id", help="章节号，例如 1.1.1 或 2.1.4")
    parser.add_argument("--dry-run", action="store_true", help="仅预览将创建的目录与文件，不实际写入")
    parser.add_argument("--force", action="store_true", help="若目标 index.md 已存在则覆盖")
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
    sections = split_sections(content)

    if not sections:
        print(f"提示: '{index_file}' 中未找到任何可拆分的 '##' 二级标题片段。", file=sys.stderr)
        return 1

    print(f"源目录: {target_dir}")
    print(f"共检测到 {len(sections)} 个有效 '##' 片段:\n")

    for idx, (raw_title, raw_body) in enumerate(sections, start=1):
        sub_id = f"{args.chapter_id}.{idx}"
        display_title = clean_title(raw_title)
        safe_title = sanitize_dirname(raw_title)
        sub_dir_name = f"{sub_id}_{safe_title}"
        sub_dir_path = target_dir / sub_dir_name
        sub_index_path = sub_dir_path / "index.md"
        clean_body = normalize_sec_body(raw_body, display_title)
        summary = extract_summary(display_title, clean_body)

        sub_markdown = (
            f"# {sub_id} {display_title}\n\n"
            f"> **简介**：{summary}\n\n"
            f"---\n\n"
            f"{clean_body}\n"
        )

        print(f"  [{idx}] {sub_dir_name}/index.md")
        if args.dry_run:
            continue

        sub_dir_path.mkdir(parents=True, exist_ok=True)
        if sub_index_path.exists() and not args.force:
            print(f"      跳过已存在文件（使用 --force 覆盖）: {sub_index_path}")
            continue

        sub_index_path.write_text(sub_markdown, encoding="utf-8")

    if args.dry_run:
        print("\n(--dry-run 模式：未写入任何文件)")
    else:
        print("\n拆分完成。")

    return 0


if __name__ == "__main__":
    sys.exit(main())