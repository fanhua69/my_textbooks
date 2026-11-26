#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Restore collected Markdown files into their corresponding directories.

Rules:
1. Match filename with directory name first (exact match).
2. If no exact match, remove leading section numbers (e.g. 1.2.3_)
   from both names and compare again.
3. Copy the source file into the matched directory as _index.md.
4. If _index.md (or _index2.md, _index3.md, ...) already exists:
   - If any of them has identical content to the source file: skip copying.
   - Otherwise: save the source file as the next available _indexN.md
     (_index2.md, _index3.md, ...). Existing files are never overwritten.
5. Skip files whose matching directory cannot be found.

Usage:
    python restore_index.py SOURCE_DIR TARGET_DIR
"""

import argparse
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path


# Match section numbers such as:
# 1_
# 1.2_
# 1.2.3_
SECTION_PREFIX = re.compile(r"^\d+(?:\.\d+)*_")

# Match _index.md, _index2.md, _index3.md, ...
INDEX_FILE = re.compile(r"^_index(\d*)\.md$")


def normalize_name(name: str) -> str:
    """Remove the leading section number."""
    return SECTION_PREFIX.sub("", name, count=1)


def build_directory_index(target_dir: Path):
    """Build exact-name and normalized-name directory indexes."""

    exact_index = defaultdict(list)
    normalized_index = defaultdict(list)

    # Include target root itself, as well as all subdirectories.
    directories = [target_dir] + [
        p for p in target_dir.rglob("*") if p.is_dir()
    ]

    for directory in directories:
        exact_index[directory.name].append(directory)
        normalized_index[normalize_name(directory.name)].append(directory)

    return exact_index, normalized_index


def find_target_directory(
    filename: str,
    exact_index,
    normalized_index
):
    """Find matching directory. Exact match has priority."""

    # 1. Try exact match.
    matches = exact_index.get(filename, [])

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        print(f"[AMBIGUOUS] Exact match: {filename}")
        return None

    # 2. Try matching after removing section numbers.
    normalized = normalize_name(filename)
    matches = normalized_index.get(normalized, [])

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        print(f"[AMBIGUOUS] Normalized match: {filename}")
        return None

    return None


def get_destination_file(target_dir: Path, source_file: Path):
    """
    Determine the destination file.

    Returns a tuple (destination, duplicate_of):
    - (_index.md, None)      : no _index.md yet, copy as _index.md
    - (_indexN.md, None)     : content differs, copy as next free _indexN.md
    - (None, existing_file)  : identical content already exists, skip copying
    """

    index_file = target_dir / "_index.md"
    # No existing _index.md.
    if not index_file.exists():
        return index_file, None

    # Collect all existing _index.md / _indexN.md files.
    existing = {}
    for p in target_dir.iterdir():
        m = INDEX_FILE.match(p.name)
        if m and p.is_file():
            existing[int(m.group(1) or 1)] = p

    # If any existing index file has identical content, skip.
    source_bytes = source_file.read_bytes()
    for number in sorted(existing):
        if existing[number].read_bytes() == source_bytes:
            return None, existing[number]

    # Otherwise use the next available number (_index2.md, _index3.md, ...).
    number = 2
    while number in existing:
        number += 1

    return target_dir / f"_index{number}.md", None


def restore_index_files(source_dir: Path, target_dir: Path):

    source_dir = source_dir.resolve()
    target_dir = target_dir.resolve()

    if not source_dir.is_dir():
        raise NotADirectoryError(
            f"Source directory not found: {source_dir}"
        )

    if not target_dir.is_dir():
        raise NotADirectoryError(
            f"Target directory not found: {target_dir}"
        )

    # Build directory lookup indexes.
    exact_index, normalized_index = build_directory_index(target_dir)

    # Only process .md files directly inside source_dir.
    source_files = sorted(
        p for p in source_dir.glob("*.md") if p.is_file()
    )

    copied = 0
    skipped = 0
    identical = 0
    renamed = 0

    print(f"\nSource: {source_dir}")
    print(f"Target: {target_dir}")
    print(f"Found {len(source_files)} Markdown files.\n")

    for source_file in source_files:

        # Remove .md extension to get directory name.
        directory_name = source_file.stem

        # Find corresponding target directory.
        matched_dir = find_target_directory(
            directory_name,
            exact_index,
            normalized_index
        )

        if matched_dir is None:
            print(f"[SKIP] No matching directory: {source_file.name}")
            skipped += 1
            continue

        # Determine destination (or detect identical content).
        destination, duplicate_of = get_destination_file(
            matched_dir, source_file
        )

        if destination is None:
            print(
                f"[IDENTICAL] {source_file.name} == {duplicate_of}, "
                f"not copied"
            )
            identical += 1
            continue

        # Copy file.
        shutil.copy2(source_file, destination)

        if destination.name == "_index.md":
            print(f"[COPY] {source_file.name} -> {destination}")
            copied += 1
        else:
            print(f"[RENAME] {source_file.name} -> {destination}")
            renamed += 1

    print("\n========== Summary ==========")
    print(f"New _index.md:         {copied}")
    print(f"Saved as _indexN.md:   {renamed}")
    print(f"Identical (not copied): {identical}")
    print(f"Skipped (no match):    {skipped}")
    print("=============================")


def main():

    parser = argparse.ArgumentParser(
        description="Restore collected Markdown files."
    )

    parser.add_argument("source", help="Source directory")
    parser.add_argument("target", help="Target directory")

    args = parser.parse_args()

    try:
        restore_index_files(
            Path(args.source),
            Path(args.target)
        )
    except (OSError, UnicodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
