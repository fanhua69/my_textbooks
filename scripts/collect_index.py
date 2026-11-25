
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recursively collect all files from a textbook directory.

index.md files are renamed with their directory section number:
    1.2.2/index.md -> 1.2.2_index.md

Other files are prefixed with the same section number when they are
inside a numbered directory:
    1.2.2/readme.pdf -> 1.2.2_readme.pdf

Usage:
    python collect_index.py SOURCE_DIR DEST_DIR
"""

import argparse
import shutil
import sys
from pathlib import Path
import re


SECTION_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)[_\s]+")


def get_section_number(directory: Path, source_dir: Path) -> str | None:
    current = directory
    while current != source_dir:
        match = SECTION_PREFIX.match(current.name)
        if match:
            return match.group(1)
        if source_dir not in current.parents:
            break
        current = current.parent
    return None


def collect_index_files(source_dir: Path, dest_dir: Path):
    source_dir = source_dir.resolve()
    dest_dir = dest_dir.resolve()

    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source directory not found: {source_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Recursively find every regular file.
    source_files = [
        p for p in source_dir.rglob("*")
        if p.is_file()
        and not p.is_symlink()
        and dest_dir not in p.parents
    ]

    # Check filename collisions before copying.
    targets = {}

    for src in sorted(source_files, key=lambda p: p.as_posix()):
        section_number = get_section_number(src.parent, source_dir)

        if src.parent == source_dir:
            target_name = src.name
        elif src.name.lower() == "index.md":
            if section_number:
                target_name = f"{section_number}_index.md"
            else:
                target_name = f"{src.parent.name}_index.md"
        elif section_number:
            target_name = f"{section_number}_{src.name}"
        else:
            target_name = f"{src.parent.name}_{src.name}"

        target = dest_dir / target_name

        if target in targets:
            raise RuntimeError(
                f"Filename collision: {target.name}\n"
                f"  First:  {targets[target]}\n"
                f"  Second: {src}\n"
                "Two directories have the same name."
            )

        targets[target] = src

    # Copy files.
    print(f"\nFound {len(source_files)} files.\n")

    for src, target in (
        (src, dest) for dest, src in targets.items()
    ):
        shutil.copy2(src, target)
        print(f"[COPY] {src.relative_to(source_dir)}")
        print(f"    -> {target}")

    print(f"\nCompleted: {len(source_files)} files copied.")
    print(f"Destination: {dest_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Collect all files recursively, prefixing names with section numbers."
    )

    parser.add_argument("source", help="Source directory")
    parser.add_argument("destination", help="Destination directory")

    args = parser.parse_args()

    try:
        collect_index_files(
            Path(args.source),
            Path(args.destination)
        )
    except (OSError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
