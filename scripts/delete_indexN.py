#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recursively delete all _index<digits>.md files
under the target directory and all its subdirectories.

_index.md is never touched.

Usage:
    python delete_indexN.py TARGET_DIR            # delete files
    python delete_indexN.py TARGET_DIR --dry-run  # only list files that would be deleted
"""

import argparse
import re
import sys
from pathlib import Path

# Match index<digits>.md, e.g. index1.md, index2.md, index01.md.
PATTERN = re.compile(r"^_index\d+\.md$")


def main():
    parser = argparse.ArgumentParser(
        description="Delete all index<digits>.md files recursively."
    )
    parser.add_argument("target", help="Target directory")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List matching files without deleting them",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    if not root.is_dir():
        print(f"ERROR: Target directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"Target: {root}\n")

    targets = sorted(
        p for p in root.rglob("*index*.md")
        if p.is_file() and PATTERN.match(p.name)
    )

    deleted = 0
    failed = 0

    for path in targets:
        if args.dry_run:
            print(f"[DRY-RUN] {path}")
            continue

        try:
            path.unlink()
            print(f"[DELETE] {path}")
            deleted += 1
        except OSError as e:
            print(f"[FAILED] {path}: {e}", file=sys.stderr)
            failed += 1

    print("\n========== Summary ==========")
    print(f"Matched: {len(targets)}")
    if not args.dry_run:
        print(f"Deleted: {deleted}")
        print(f"Failed:  {failed}")
    print("=============================")


if __name__ == "__main__":
    main()
