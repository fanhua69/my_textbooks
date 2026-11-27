"""Helpers for numbered textbook index filenames."""

from __future__ import annotations

import re
from pathlib import Path


_SECTION_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)(?=[_\s-]|$)")
_INDEX_MARKER = re.compile(r"^(.+)\.0_index(\d*)\.md$", re.IGNORECASE)
_SECTIONED_INDEX_MARKER = re.compile(
    r"^\d+(?:\.\d+)*_index\d*\.md$", re.IGNORECASE
)
_LEGACY_INDEX = re.compile(r"^(?:~|_)?index(\d*)\.md$", re.IGNORECASE)


def directory_identifier(directory: Path | str) -> str:
    name = directory.name if isinstance(directory, Path) else directory
    match = _SECTION_PREFIX.match(name)
    return match.group(1) if match else name


def index_filename(directory: Path | str, duplicate: int = 1) -> str:
    identifier = directory_identifier(directory)
    suffix = "" if duplicate == 1 else str(duplicate)
    return f"{identifier}.0_index{suffix}.md"


def index_marker_parts(filename: str) -> tuple[str, int] | None:
    match = _INDEX_MARKER.fullmatch(filename)
    if match is None:
        return None
    return match.group(1), int(match.group(2) or 1)


def is_index_marker_name(filename: str) -> bool:
    return (
        _INDEX_MARKER.fullmatch(filename) is not None
        or _SECTIONED_INDEX_MARKER.fullmatch(filename) is not None
        or _LEGACY_INDEX.fullmatch(filename) is not None
    )
