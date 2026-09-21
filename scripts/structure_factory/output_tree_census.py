#!/usr/bin/env python3
"""Account for identical, changed, and one-sided files in two output trees."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def census(left: dict[str, str], right: dict[str, str]) -> dict:
    shared = sorted(set(left) & set(right))
    identical = [path for path in shared if left[path] == right[path]]
    differing = [path for path in shared if left[path] != right[path]]
    only_left = sorted(set(left) - set(right))
    only_right = sorted(set(right) - set(left))
    total = len(set(left) | set(right))
    assert len(identical) + len(differing) + len(only_left) + len(only_right) == total
    return {
        "ok": not (differing or only_left or only_right),
        "total": total,
        "identical": identical,
        "differing": differing,
        "only_in_left": only_left,
        "only_in_right": only_right,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.left.is_dir() or not args.right.is_dir():
        parser.error("both paths must be directories")
    result = census(digest_tree(args.left), digest_tree(args.right))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"{len(result['identical'])} identical; "
            f"{len(result['differing'])} differing; "
            f"{len(result['only_in_left'])} only in left; "
            f"{len(result['only_in_right'])} only in right"
        )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
