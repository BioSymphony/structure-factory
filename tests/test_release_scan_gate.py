from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("make"), "make is required")
class SecretScanGateTests(unittest.TestCase):
    def test_each_scan_failure_blocks_release(self) -> None:
        for history_status, directory_status in ((19, 0), (0, 23), (0, 0)):
            with self.subTest(history=history_status, directory=directory_status):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    scanner = root / "gitleaks"
                    scanner.write_text(
                        '#!/bin/sh\n'
                        'case "$1" in\n'
                        f'  detect) exit {history_status} ;;\n'
                        f'  dir) exit {directory_status} ;;\n'
                        '  *) exit 99 ;;\n'
                        'esac\n',
                        encoding="utf-8",
                    )
                    scanner.chmod(0o755)
                    result = subprocess.run(
                        ["make", "-f", str(ROOT / "Makefile"), "secret-scan"],
                        cwd=root,
                        env={**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]},
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(
                        result.returncode == 0,
                        history_status == 0 and directory_status == 0,
                        result.stdout + result.stderr,
                    )
