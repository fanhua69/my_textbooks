"""Helpers for locating textbook roots."""

from __future__ import annotations

import os
import re
from pathlib import Path

from index_paths import is_index_marker_name


SECTION_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)(?:_|$)")
META_DIRECTORY = ".meta"
REMOVED_DIRECTORY = ".removed"


def _is_metadata_or_removed_path(path: Path) -> bool:
    return any(
        part in {META_DIRECTORY, REMOVED_DIRECTORY}
        for part in path.parts
    )


def find_book_root(start: Path) -> Path:
    """Return the nearest ancestor containing a book marker file, stopping at home."""
    current = start.expanduser().resolve()
    home_dir = Path.home().resolve()
    if not current.is_dir():
        current = current.parent

    while True:
        inside_auxiliary = _is_metadata_or_removed_path(current)
        has_metadata_contents = not inside_auxiliary and (
            current / META_DIRECTORY / "contents.md"
        ).is_file()
        has_legacy_contents = (
            not inside_auxiliary
            and any(
                (current / name).is_file() for name in ("目录.md", "contents.md")
            )
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
    return _matching_section_entries(
        list_section_entries(book_root, recursive=True),
        section_num,
    )


def list_section_entries(
    start: Path,
    *,
    recursive: bool = False,
    include_start: bool = False,
) -> list[tuple[Path, str]]:
    """List numbered section directories and Markdown files under ``start``."""
    root = start.expanduser().resolve()
    if not root.is_dir() or _is_metadata_or_removed_path(root):
        return []

    candidates: list[Path] = []
    if include_start:
        candidates.append(root)

    if recursive:
        def raise_walk_error(error: OSError) -> None:
            raise error

        for directory, subdirectories, filenames in os.walk(
            root,
            topdown=True,
            onerror=raise_walk_error,
            followlinks=False,
        ):
            folder = Path(directory)
            subdirectories[:] = [
                name
                for name in subdirectories
                if name not in {META_DIRECTORY, REMOVED_DIRECTORY}
                and not (folder / name).is_symlink()
            ]
            candidates.extend(folder / name for name in subdirectories)
            candidates.extend(folder / name for name in filenames)
    else:
        candidates.extend(root.iterdir())

    entries: list[tuple[Path, str]] = []
    for path in candidates:
        if path.is_symlink():
            continue
        if path.is_dir():
            kind = "directory"
            name = path.name
        elif path.is_file() and path.suffix.lower() == ".md":
            kind = "file"
            name = path.stem
            if is_index_marker_name(path.name):
                continue
        else:
            continue

        if SECTION_NUMBER_RE.match(name) is not None:
            entries.append((path, kind))

    return sorted(entries, key=lambda item: (str(item[0]), item[1]))


def find_direct_section_entries(
    parent: Path,
    section_num: str,
    *,
    kind: str | None = None,
) -> list[tuple[Path, str]]:
    """Find numbered section entries directly inside ``parent``."""
    entries = _matching_section_entries(list_section_entries(parent), section_num)
    if kind is not None:
        entries = [
            (path, entry_kind)
            for path, entry_kind in entries
            if entry_kind == kind
        ]
    return entries


def _matching_section_entries(
    entries: list[tuple[Path, str]],
    section_num: str,
) -> list[tuple[Path, str]]:
    if re.fullmatch(r"\d+(?:\.\d+)*", section_num.strip()) is None:
        return []
    expected_number = tuple(int(part) for part in section_num.strip().split("."))

    matches = []
    for path, kind in entries:
        name = path.name if kind == "directory" else path.stem
        match = SECTION_NUMBER_RE.match(name.strip())
        if match is None:
            continue
        number = tuple(int(part) for part in match.group(1).split("."))
        if number == expected_number:
            matches.append((path, kind))

    return sorted(matches, key=lambda item: (item[1], str(item[0])))


def list_directories(
    start: Path,
    *,
    recursive: bool = False,
    include_start: bool = False,
) -> list[Path]:
    """List directories while excluding metadata and archived trees."""
    root = start.expanduser().resolve()
    if not root.is_dir() or _is_metadata_or_removed_path(root):
        return []

    directories: list[Path] = [root] if include_start else []
    if recursive:
        def raise_walk_error(error: OSError) -> None:
            raise error

        for directory, subdirectories, _ in os.walk(
            root,
            topdown=True,
            onerror=raise_walk_error,
            followlinks=False,
        ):
            folder = Path(directory)
            subdirectories[:] = [
                name
                for name in subdirectories
                if name not in {META_DIRECTORY, REMOVED_DIRECTORY}
                and not (folder / name).is_symlink()
            ]
            directories.extend(folder / name for name in subdirectories)
    else:
        directories.extend(
            path
            for path in root.iterdir()
            if path.name not in {META_DIRECTORY, REMOVED_DIRECTORY}
            and path.is_dir()
            and not path.is_symlink()
        )

    return sorted(set(directories), key=lambda path: str(path))


def discover_book_roots(start: Path) -> list[Path]:
    """Find the nearest ancestor book root, or all roots below ``start``."""
    current = start.expanduser().resolve()
    if not current.is_dir():
        current = current.parent

    try:
        return [find_book_root(current)]
    except FileNotFoundError:
        pass
    if _is_metadata_or_removed_path(current):
        return []

    def raise_walk_error(error: OSError) -> None:
        raise error

    roots: list[Path] = []
    for directory, subdirectories, files in os.walk(current, onerror=raise_walk_error):
        directory_path = Path(directory)
        if directory_path.name in {META_DIRECTORY, REMOVED_DIRECTORY}:
            subdirectories[:] = []
            continue
        subdirectories[:] = [
            name
            for name in subdirectories
            if name not in {META_DIRECTORY, REMOVED_DIRECTORY}
            and not (directory_path / name).is_symlink()
        ]
        has_root_marker = (
            directory_path / META_DIRECTORY / "contents.md"
        ).is_file() or any(
            name in files and (directory_path / name).is_file()
            for name in ("目录.md", "contents.md")
        )
        if has_root_marker:
            roots.append(directory_path)

    return sorted(roots)
