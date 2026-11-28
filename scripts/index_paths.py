"""Helpers for numbered textbook index filenames."""

from __future__ import annotations

import re
from pathlib import Path


_SECTION_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)(?=[_\s-]|$)")
_INDEX_MARKER = re.compile(r"^(.+)\.0_index(\d*)\.md$", re.IGNORECASE)
_CHINESE_INDEX_MARKER = re.compile(
    r"^(\d+(?:\.\d+)*)(?:\.0)?_简介(\d*)\.md$", re.IGNORECASE
)
_SECTIONED_INDEX_MARKER = re.compile(
    r"^(\d+(?:\.\d+)*)_index(\d*)\.md$", re.IGNORECASE
)
_LEGACY_INDEX = re.compile(r"^(?:~|_)?index(\d*)\.md$", re.IGNORECASE)
_CONTENTS_FILENAMES = {"目录.md", "contents.md"}


def directory_identifier(directory: Path | str) -> str:
    name = directory.name if isinstance(directory, Path) else directory
    match = _SECTION_PREFIX.match(name)
    return match.group(1) if match else name


def uses_chinese_index(directory: Path | str) -> bool:
    """Choose the index language from direct child names in this directory."""
    if not isinstance(directory, Path):
        directory = Path(directory)
    if not directory.is_dir():
        return False

    chinese_count = 0
    english_count = 0
    for entry in directory.iterdir():
        name = entry.name
        if name in _CONTENTS_FILENAMES:
            continue
        if re.fullmatch(
            r"^(?:~|_)?index\d*\.md$|"
            r"^\d+(?:\.\d+)*(?:\.0)?_index\d*\.md$|"
            r"^\d+(?:\.\d+)*(?:\.0)?_简介\d*\.md$",
            name,
            re.IGNORECASE,
        ):
            continue
        chinese_count += sum("\u4e00" <= char <= "\u9fff" for char in name)
        english_count += sum(char.isascii() and char.isalpha() for char in name)

    return chinese_count > english_count


def contents_filename(directory: Path | str) -> str:
    return "目录.md" if uses_chinese_index(directory) else "contents.md"


def index_filename(directory: Path | str, duplicate: int = 1) -> str:
    identifier = directory_identifier(directory)
    suffix = "" if duplicate == 1 else str(duplicate)
    if uses_chinese_index(directory):
        return f"{identifier}.0_简介{suffix}.md"
    return f"{identifier}.0_index{suffix}.md"


def index_marker_parts(filename: str) -> tuple[str, int] | None:
    match = _INDEX_MARKER.fullmatch(filename)
    if match is not None:
        identifier = match.group(1)
        if identifier.endswith(".0"):
            identifier = identifier[:-2]
        return identifier, int(match.group(2) or 1)

    match = _CHINESE_INDEX_MARKER.fullmatch(filename)
    if match is not None:
        identifier = match.group(1)
        if identifier.endswith(".0"):
            identifier = identifier[:-2]
        return identifier, int(match.group(2) or 1)

    match = _SECTIONED_INDEX_MARKER.fullmatch(filename)
    if match is not None:
        name_match = re.fullmatch(
            r"^(\d+(?:\.\d+)*)_index(\d*)\.md$", filename, re.IGNORECASE
        )
        if name_match is not None:
            return name_match.group(1), int(name_match.group(2) or 1)

    return None


def is_index_marker_name(filename: str) -> bool:
    return (
        _INDEX_MARKER.fullmatch(filename) is not None
        or _CHINESE_INDEX_MARKER.fullmatch(filename) is not None
        or _SECTIONED_INDEX_MARKER.fullmatch(filename) is not None
        or _LEGACY_INDEX.fullmatch(filename) is not None
    )
