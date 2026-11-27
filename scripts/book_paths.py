"""Helpers for locating textbook roots."""

from __future__ import annotations

import os
from pathlib import Path


def find_book_root(start: Path) -> Path:
    """Return the nearest ancestor containing ``contents.md``."""
    current = start.expanduser().resolve()
    if not current.is_dir():
        current = current.parent

    while True:
        if (current / "contents.md").is_file():
            return current
        if current.parent == current:
            break
        current = current.parent

    raise FileNotFoundError(
        f"从当前目录向上未找到包含 contents.md 的教材根目录: {start}"
    )


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
        subdirectories[:] = [
            name
            for name in subdirectories
            if not (directory_path / name).is_symlink()
        ]
        if "contents.md" in files and (directory_path / "contents.md").is_file():
            roots.append(directory_path)

    return sorted(roots)
