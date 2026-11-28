"""Helpers for numbered textbook index filenames."""

from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit


_SECTION_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)(?=[_\s-]|$)")
_INDEX_MARKER = re.compile(r"^(.+)\.0_index(\d*)\.md$", re.IGNORECASE)
_CHINESE_INDEX_MARKER = re.compile(
    r"^(\d+(?:\.\d+)*)(?:\.0)?_简介(\d*)\.md$", re.IGNORECASE
)
_SECTIONED_INDEX_MARKER = re.compile(
    r"^(\d+(?:\.\d+)*)_index(\d*)\.md$", re.IGNORECASE
)
_LEGACY_INDEX = re.compile(r"^(?:~|_)?index(\d*)\.md$", re.IGNORECASE)
_ARCHIVED_INDEX = re.compile(r"^.+_(?:index|简介)\d*\.md$", re.IGNORECASE)
META_DIRECTORY = ".meta"


def directory_identifier(directory: Path | str) -> str:
    name = directory.name if isinstance(directory, Path) else directory
    match = _SECTION_PREFIX.match(name)
    return match.group(1) if match else name


def index_filename(directory: Path | str, duplicate: int = 1) -> str:
    identifier = directory_identifier(directory)
    suffix = "" if duplicate == 1 else str(duplicate)
    return f"{identifier}_index{suffix}.md"


def metadata_directory(book_root: Path) -> Path:
    return book_root / META_DIRECTORY


def metadata_contents_path(book_root: Path) -> Path:
    return metadata_directory(book_root) / "contents.md"


def metadata_index_path(
    book_root: Path,
    section_directory: Path,
    duplicate: int = 1,
) -> Path:
    if section_directory.resolve() == book_root.resolve():
        return metadata_contents_path(book_root)
    return metadata_directory(book_root) / index_filename(
        section_directory, duplicate
    )


def migrate_indexes_to_metadata(book_root: Path) -> int:
    """Move legacy per-directory indexes into the book's central .meta directory."""
    book_root = book_root.resolve()
    meta = metadata_directory(book_root)
    meta.mkdir(parents=True, exist_ok=True)
    moved = 0

    def raise_walk_error(error: OSError) -> None:
        raise error

    for directory, subdirectories, filenames in os.walk(
        book_root,
        topdown=True,
        onerror=raise_walk_error,
        followlinks=False,
    ):
        folder = Path(directory)
        subdirectories[:] = [
            name for name in subdirectories
            if name != META_DIRECTORY and not (folder / name).is_symlink()
        ]
        if folder == meta or meta in folder.parents:
            continue

        marker_files = [
            folder / name
            for name in filenames
            if (folder / name).is_file()
            and not (folder / name).is_symlink()
            and is_index_marker_name(name)
        ]
        content_files = [
            folder / name
            for name in filenames
            if name in {"目录.md", "contents.md"}
            and (folder / name).is_file()
            and not (folder / name).is_symlink()
        ]
        if folder == book_root:
            if content_files:
                _move_metadata_files(content_files, metadata_contents_path(book_root))
                moved += len(content_files)
            for marker_file in marker_files:
                _move_metadata_files(
                    [marker_file],
                    metadata_directory(book_root) / marker_file.name,
                )
                moved += 1
            continue

        relative_parts = folder.relative_to(book_root).parts
        if "removed" in relative_parts:
            archive_parts = relative_parts[relative_parts.index("removed") + 1 :]
            archive_dir = metadata_directory(book_root) / "removed" / Path(
                *archive_parts
            )
            for name in filenames:
                if not _ARCHIVED_INDEX.fullmatch(name):
                    continue
                source = folder / name
                if source.is_file() and not source.is_symlink():
                    _move_metadata_files([source], [archive_dir / name])
                    moved += 1
            continue

        identifier = directory_identifier(folder)
        if not re.fullmatch(r"\d+(?:\.\d+)*", identifier):
            continue

        marker_files.extend(content_files)
        if marker_files:
            _move_metadata_files(
                marker_files, metadata_index_path(book_root, folder)
            )
            moved += len(marker_files)

    rebase_metadata_links(book_root)
    return moved


def rebase_metadata_links(book_root: Path) -> None:
    """Keep local links in moved index files pointed at their original targets."""
    book_root = book_root.resolve()
    meta = metadata_directory(book_root)
    section_directories: dict[str, Path] = {}
    for directory, subdirectories, _ in os.walk(book_root):
        folder = Path(directory)
        subdirectories[:] = [
            name for name in subdirectories
            if name != META_DIRECTORY and not (folder / name).is_symlink()
        ]
        if folder == book_root:
            continue
        identifier = directory_identifier(folder)
        if re.fullmatch(r"\d+(?:\.\d+)*", identifier):
            section_directories[identifier] = folder

    link_pattern = re.compile(
        r"(?P<prefix>!?\[[^\]]*\]\()"
        r"(?P<url><[^>]+>|[^)\s]+)"
        r"(?P<suffix>\))"
    )

    for source in meta.glob("*.md"):
        if source.name == "contents.md":
            origin = book_root
        else:
            marker = index_marker_parts(source.name)
            origin = section_directories.get(marker[0]) if marker else None
            if origin is None:
                continue

        original = source.read_text(encoding="utf-8")

        def rebase(match: re.Match[str]) -> str:
            raw_url = match.group("url")
            bracketed = raw_url.startswith("<") and raw_url.endswith(">")
            url = raw_url[1:-1] if bracketed else raw_url
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                return match.group(0)
            decoded_path = unquote(parts.path)
            if decoded_path.startswith("/"):
                return match.group(0)

            target = (meta / decoded_path).resolve()
            if target.exists():
                return match.group(0)

            original_target = (origin / decoded_path).resolve()
            if original_target.exists():
                target = original_target
            else:
                marker = index_marker_parts(Path(decoded_path).name)
                if marker is None:
                    return match.group(0)
                target = meta / index_filename(marker[0], marker[1])
                if not target.is_file():
                    return match.group(0)

            relative = Path(os.path.relpath(target, meta)).as_posix()
            rebased_url = urlunsplit(
                (
                    "",
                    "",
                    quote(relative, safe="/-._~"),
                    parts.query,
                    parts.fragment,
                )
            )
            if bracketed:
                rebased_url = f"<{rebased_url}>"
            return f"{match.group('prefix')}{rebased_url}{match.group('suffix')}"

        updated = link_pattern.sub(rebase, original)
        if updated != original:
            source.write_text(updated, encoding="utf-8")


def _move_metadata_files(sources: list[Path], destination: Path) -> None:
    if not sources:
        return
    sources = sorted(
        sources,
        key=lambda path: (path.stat().st_size, path.name.casefold(), path.name),
        reverse=True,
    )
    primary = destination
    primary.parent.mkdir(parents=True, exist_ok=True)
    next_duplicate = 1
    for source in sources:
        target = primary if next_duplicate == 1 else primary.with_name(
            f"{primary.stem}{next_duplicate}{primary.suffix}"
        )
        while target.exists():
            if target.read_bytes() == source.read_bytes():
                source.unlink()
                next_duplicate += 1
                break
            next_duplicate += 1
            target = primary.with_name(
                f"{primary.stem}{next_duplicate}{primary.suffix}"
            )
        else:
            source.rename(target)
            next_duplicate += 1


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
