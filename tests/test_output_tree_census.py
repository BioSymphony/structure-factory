from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "structure_factory" / "output_tree_census.py"


def run(left: Path, right: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(left), str(right), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


class OutputTreeCensusTests(unittest.TestCase):
    def test_census_partitions_the_complete_path_union(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left, right = root / "left", root / "right"
            left.mkdir()
            right.mkdir()
            for tree, values in (
                (left, {"same": "x", "changed": "a", "left": "l"}),
                (right, {"same": "x", "changed": "b", "right": "r"}),
            ):
                for name, value in values.items():
                    (tree / name).write_text(value, encoding="utf-8")
            completed = run(left, right)
        self.assertEqual(1, completed.returncode)
        result = json.loads(completed.stdout)
        self.assertEqual(4, result["total"])
        self.assertEqual(["same"], result["identical"])
        self.assertEqual(["changed"], result["differing"])
        self.assertEqual(["left"], result["only_in_left"])
        self.assertEqual(["right"], result["only_in_right"])

    def test_identical_trees_exit_zero_and_symlinks_are_not_followed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left, right = root / "left", root / "right"
            left.mkdir()
            right.mkdir()
            (left / "same").write_text("x", encoding="utf-8")
            (right / "same").write_text("x", encoding="utf-8")
            (right / "ignored-link").symlink_to(right / "same")
            completed = run(left, right)
        self.assertEqual(0, completed.returncode)
        self.assertTrue(json.loads(completed.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
