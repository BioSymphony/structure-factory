#!/usr/bin/env python3
"""Inventory direct dependency pins and optionally verify that they resolve."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

GIT_PIN = re.compile(
    r"git\+(?P<url>https://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+?)"
    r"(?:@(?P<ref>\$?\{[A-Za-z_][A-Za-z0-9_]*\}|[A-Za-z0-9._/-]+))?"
    r"(?=[\s\"',;)\]}]|$)"
)
PYPI_PIN = re.compile(
    r"(?<![A-Za-z0-9._-])(?P<name>[A-Za-z][A-Za-z0-9._-]{1,62}[A-Za-z0-9])"
    r"==(?P<version>[0-9][A-Za-z0-9.*+!-]*)"
)
SCANNED_SUFFIXES = {"", ".cfg", ".json", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
FAILURES = {"dead_repo", "dead_ref", "dead_release"}
SKIP_TOP_LEVEL = {"tests"}


def tracked_files(root: Path) -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return [
        root / item
        for item in completed.stdout.splitlines()
        if Path(item).parts and Path(item).parts[0] not in SKIP_TOP_LEVEL
    ]


def scan(path: Path, root: Path) -> list[dict]:
    if path.suffix.lower() not in SCANNED_SUFFIXES or not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    relative = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name
    pins: list[dict] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for match in GIT_PIN.finditer(line):
            url = match.group("url").rstrip(".,:'\"")
            ref = match.group("ref")
            category = "templated" if ref and ("{" in ref or "$" in ref) else "unchecked"
            pins.append({"path": relative, "line": line_number, "kind": "git", "name": url, "ref": ref, "spec": match.group(0), "category": category, "detail": ""})
        for match in PYPI_PIN.finditer(line):
            version = match.group("version")
            if "*" in version or version.endswith(".x"):
                continue
            category = "alternate_index" if "+" in version else "unchecked"
            pins.append({"path": relative, "line": line_number, "kind": "pypi", "name": match.group("name"), "ref": version, "spec": match.group(0), "category": category, "detail": ""})
    return pins


def resolve(pin: dict, timeout: int) -> None:
    if pin["category"] != "unchecked":
        return
    if pin["kind"] == "git":
        command = ["git", "ls-remote", "--exit-code", pin["name"]]
        if pin["ref"] and not re.fullmatch(r"[0-9a-f]{7,40}", pin["ref"]):
            command.append(pin["ref"])
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as error:
            pin.update(category="dead_repo", detail=str(error))
            return
        if completed.returncode == 0:
            pin.update(category="ok", detail="remote resolved")
        else:
            category = "dead_ref" if pin["ref"] else "dead_repo"
            pin.update(category=category, detail=" ".join(completed.stderr.split())[:200])
        return
    url = f"https://pypi.org/pypi/{pin['name']}/{pin['ref']}/json"
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "bsf-pin-checker"}),
            timeout=timeout,
        ) as response:
            pin.update(category="ok", detail=f"HTTP {response.status}")
    except urllib.error.HTTPError as error:
        pin.update(category="dead_release" if error.code == 404 else "unchecked", detail=f"HTTP {error.code}")
    except (OSError, urllib.error.URLError) as error:
        pin.update(category="unchecked", detail=str(error))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    paths = [path.resolve() for path in args.paths] or tracked_files(root)
    pins = [pin for path in paths for pin in scan(path, root)]
    if args.online:
        for pin in pins:
            resolve(pin, args.timeout)
    categories = sorted({pin["category"] for pin in pins} | {"unchecked"})
    counts = {category: sum(pin["category"] == category for pin in pins) for category in categories}
    report = {"online": args.online, "counts": counts, "pins": pins}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"direct dependency pins: {len(pins)}")
        print(" ".join(f"{key}={value}" for key, value in sorted(counts.items())))
        if not args.online:
            print("Pass --online to resolve direct Git and PyPI pins.")
    return 1 if any(pin["category"] in FAILURES for pin in pins) else 0


if __name__ == "__main__":
    raise SystemExit(main())
