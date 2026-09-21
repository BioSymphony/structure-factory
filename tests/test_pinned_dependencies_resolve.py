from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "structure_factory" / "check_pinned_dependencies_resolve.py"


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


class PinnedDependencyResolutionTests(unittest.TestCase):
    def test_offline_inventory_finds_direct_git_and_pypi_pins(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "requirements.txt"
            target.write_text(
                "example @ git+https://github.com/example/project.git@v1.2.3\n"
                "example-package==4.5.6\n",
                encoding="utf-8",
            )
            completed = run(str(target), "--repo-root", str(root), "--json")
        self.assertEqual(0, completed.returncode, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(
            {("git", "v1.2.3"), ("pypi", "4.5.6")},
            {(row["kind"], row["ref"]) for row in report["pins"]},
        )
        self.assertEqual(2, report["counts"]["unchecked"])

    def test_ranges_are_not_misreported_as_exact_releases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "requirements.txt"
            target.write_text(
                "example-package==4.*\nother-package==3.1.x\n",
                encoding="utf-8",
            )
            completed = run(str(target), "--repo-root", str(root), "--json")
        self.assertEqual(0, completed.returncode)
        self.assertEqual([], json.loads(completed.stdout)["pins"])

    def test_repository_inventory_runs_without_network(self) -> None:
        completed = run("--repo-root", str(ROOT), "--json")
        self.assertEqual(0, completed.returncode, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertTrue(
            any(row["spec"] == "esm==3.4.1.post1" for row in report["pins"])
        )


if __name__ == "__main__":
    unittest.main()
