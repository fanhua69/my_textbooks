"""Helpers for locating textbook roots."""

from __future__ import annotations

import os
import re
from pathlib import Path


SECTION_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)(?:_|$)")


def find_book_root(start: Path) -> Path:
    """Return the nearest ancestor containing a book marker file, stopping at home."""
    current = start.expanduser().resolve()
    home_dir = Path.home().resolve()
    if not current.is_dir():
        current = current.parent

    while True:
        has_metadata_contents = (current / ".meta" / "contents.md").is_file()
        has_legacy_contents = current.name != ".meta" and any(
            (current / name).is_file() for name in ("目录.md", "contents.md")
        )
        if has_metadata_contents or has_legacy_contents:
            return current
        if current == home_dir or current.parent == current:
            break
        current = current.parent

    raise FileNotFoundError(
        f"从当前目录向上至 home 目录未找到教材目录标记文件: {start}"
    )


def find_section_entries(start: Path, section_num: str) -> list[tuple[Path, str]]:
    """Find matching section directories and Markdown files under the containing book."""
    book_root = find_book_root(start)
    number_match = re.fullmatch(r"\d+(?:\.\d+)*", section_num.strip())
    if number_match is None:
        return []
    expected_number = tuple(int(part) for part in section_num.strip().split("."))
    matches: list[tuple[Path, str]] = []

    for path in book_root.rglob("*"):
        if ".meta" in path.relative_to(book_root).parts:
            continue
        if path.is_dir():
            kind = "directory"
            name = path.name.strip()
        elif path.is_file() and path.suffix.lower() == ".md":
            kind = "file"
            name = path.stem.strip()
        else:
            continue

        match = SECTION_NUMBER_RE.match(name)
        if match is None:
            continue
        number = tuple(int(part) for part in match.group(1).split("."))
        if number == expected_number:
            matches.append((path, kind))

    return sorted(matches, key=lambda item: (item[1], str(item[0])))


def discover_book_roots(start: Path) -> list[Path]:
    """Find the nearest ancestor book root, or all roots below ``start``."""
    current = start.expanduser().resolve()
    if not current.is_dir():
        current = current.parent

    try:
        return [find_book_root(current)]
    except FileNotFoundError:
        pass

    def raise_walk_error(error: OSError) -> None:
        raise error

    roots: list[Path] = []
    for directory, subdirectories, files in os.walk(current, onerror=raise_walk_error):
        directory_path = Path(directory)
        if directory_path.name == ".meta":
            subdirectories[:] = []
            continue
        subdirectories[:] = [
            name
            for name in subdirectories
            if not (directory_path / name).is_symlink()
        ]
        has_root_marker = (directory_path / ".meta" / "contents.md").is_file() or any(
            name in files and (directory_path / name).is_file()
            for name in ("目录.md", "contents.md")
        )
        if has_root_marker:
            roots.append(directory_path)

    return sorted(roots)
