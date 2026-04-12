#!/usr/bin/env python3
"""Tests for tools/lint-vocab.py. Stdlib unittest only."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINT = REPO_ROOT / "tools" / "lint-vocab.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def run_lint(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class TestLintVocab(unittest.TestCase):
    def test_clean_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            clean = Path(tmp) / "clean.md"
            clean.write_text("This content is fine.\n", encoding="utf-8")
            result = run_lint(str(FIXTURES / "glossary-good.md"), "--content-dir", tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_detects_forbidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.md"
            bad.write_text((FIXTURES / "glossary-bad.md").read_text(encoding="utf-8"), encoding="utf-8")
            result = run_lint(str(FIXTURES / "glossary-good.md"), "--content-dir", tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("forbidden synonym", result.stdout)

    def test_missing_glossary(self):
        result = run_lint("nonexistent-glossary.md")
        self.assertEqual(result.returncode, 2)

    def test_utf8_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "utf8.md"
            path.write_text("Café résumé — ünicode ok.\n", encoding="utf-8")
            result = run_lint(str(FIXTURES / "glossary-good.md"), "--content-dir", tmp)
            self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
