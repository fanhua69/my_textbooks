
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recursively collect index.md files from subdirectories.

Output filename = immediate parent directory name + ".md"

Usage:
    python collect_index.py SOURCE_DIR DEST_DIR
"""

import argparse
import shutil
import sys
from pathlib import Path


def collect_index_files(source_dir: Path, dest_dir: Path):
    source_dir = source_dir.resolve()
    dest_dir = dest_dir.resolve()

    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source directory not found: {source_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Recursively find all index.md files.
    # Exclude index.md in the source root itself.
    index_files = [
        p for p in source_dir.rglob("index.md")
        if dest_dir not in p.parents
    ]

    # Check filename collisions before copying.
    targets = {}

    for src in index_files:
        target = dest_dir / f"{src.parent.name}.md"

        if target in targets:
            raise RuntimeError(
                f"Filename collision: {target.name}\n"
                f"  First:  {targets[target]}\n"
                f"  Second: {src}\n"
                "Two directories have the same name."
            )

        targets[target] = src

    # Copy files.
    print(f"\nFound {len(index_files)} index.md files.\n")

    for src, target in (
        (src, dest) for dest, src in targets.items()
    ):
        shutil.copy2(src, target)
        print(f"[COPY] {src.parent.name}/index.md")
        print(f"    -> {target}")

    print(f"\nCompleted: {len(index_files)} files copied.")
    print(f"Destination: {dest_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Collect all subdirectory index.md files."
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
