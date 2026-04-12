#!/usr/bin/env python3
"""Tests for tools/log-incident.py. Stdlib unittest only."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_INCIDENT = REPO_ROOT / "tools" / "log-incident.py"


def run_cmd(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LOG_INCIDENT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(cwd),
    )


class TestLogIncident(unittest.TestCase):
    def test_log_appends_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            result = run_cmd(cwd, "log", "test-primitive", "med", "smoke test")
            self.assertEqual(result.returncode, 0, result.stderr)
            ledger = cwd / "incidents.jsonl"
            self.assertTrue(ledger.exists())
            obj = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(obj["primitive"], "test-primitive")
            self.assertEqual(obj["severity"], "med")
            self.assertEqual(obj["symptom"], "smoke test")

    def test_count_filters_by_severity(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            run_cmd(cwd, "log", "p1", "low", "ignore me")
            run_cmd(cwd, "log", "p1", "med", "count me")
            run_cmd(cwd, "log", "p1", "high", "count me too")
            result = run_cmd(cwd, "count", "--primitive", "p1")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "2")

    def test_count_filters_by_primitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            run_cmd(cwd, "log", "p1", "high", "a")
            run_cmd(cwd, "log", "p2", "high", "b")
            result = run_cmd(cwd, "count", "--primitive", "p1")
            self.assertEqual(result.stdout.strip(), "1")

    def test_check_drift_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "DEFERRED.md").write_text(
                "| # | Name | Class | One-line | Activation trigger | Pointer |\n"
                "|---|---|---|---|---|---|\n"
                "| 1 | alpha | schema | summary text | three collisions detected | `deferred/alpha/` |\n",
                encoding="utf-8",
            )
            (cwd / "deferred" / "alpha").mkdir(parents=True)
            (cwd / "deferred" / "alpha" / "README.md").write_text(
                "# Alpha\n\nActivation trigger:\nthree collisions detected in routing\n\n",
                encoding="utf-8",
            )
            result = run_cmd(cwd, "check-drift")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_drift_detects_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "DEFERRED.md").write_text(
                "| # | Name | Class | One-line | Activation trigger | Pointer |\n"
                "|---|---|---|---|---|---|\n"
                "| 1 | alpha | schema | summary text | three collisions detected | `deferred/alpha/` |\n",
                encoding="utf-8",
            )
            (cwd / "deferred").mkdir()
            result = run_cmd(cwd, "check-drift")
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
