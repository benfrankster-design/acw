#!/usr/bin/env python3
"""Tests for tools/manifest.py. Stdlib unittest only.

Spec under test: rules/manifest-discipline.md → "Manifest tooling spec".
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from manifest import (  # noqa: E402
    CANONICAL_DEFAULTS,
    KNOWN_DICTS,
    KNOWN_LISTS,
    UNSUPPORTED,
    ManifestError,
    append,
    contains,
    load,
    validate,
)


SAMPLE_YAML = """\
# Top-level comment
version: "0.2.0-rc4"
last_reconciled: "2026-05-02"

# Three-layer manifest
template_layer:
  - AGENTS.md
  - rules/foo.md

meta_layer:
  - LINEAGE.md

empty_dirs: []

auto_load_at_session_start:
  - tasks-status.md
  - glossary.md

cross_repo_writes: []

voice: []

# Substrate paths — partial; rest fall back to canonical defaults
paths:
  decisions_log: decisions/decision-log.md
  tasks_status: tasks-status.md
"""


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self._tmp.name)
        self.state_file = self.tmpdir / "acw-state.yaml"
        self.state_file.write_text(SAMPLE_YAML, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    # ---------- load ----------

    def test_load_returns_existing_list(self):
        self.assertEqual(
            load(self.state_file, "template_layer"),
            ["AGENTS.md", "rules/foo.md"],
        )

    def test_load_returns_empty_for_inline_empty_list(self):
        self.assertEqual(load(self.state_file, "empty_dirs"), [])

    def test_load_returns_empty_for_absent_list_block(self):
        # Strip auto_load_at_session_start from sample
        text = self.state_file.read_text(encoding="utf-8")
        text = text.replace(
            "auto_load_at_session_start:\n  - tasks-status.md\n  - glossary.md\n", ""
        )
        self.state_file.write_text(text, encoding="utf-8")
        self.assertEqual(load(self.state_file, "auto_load_at_session_start"), [])

    def test_load_paths_merges_canonical_defaults(self):
        result = load(self.state_file, "paths")
        # File-defined keys present
        self.assertEqual(result["decisions_log"], "decisions/decision-log.md")
        self.assertEqual(result["tasks_status"], "tasks-status.md")
        # Canonical defaults fill the rest
        self.assertEqual(result["inbox_dir"], "_inbox")
        self.assertEqual(result["build_log"], "build-log.md")
        # Should have all canonical keys
        for key in CANONICAL_DEFAULTS["paths"]:
            self.assertIn(key, result)

    def test_load_paths_with_no_block_returns_all_defaults(self):
        text = self.state_file.read_text(encoding="utf-8")
        text = text.replace(
            "# Substrate paths — partial; rest fall back to canonical defaults\n"
            "paths:\n"
            "  decisions_log: decisions/decision-log.md\n"
            "  tasks_status: tasks-status.md\n",
            "",
        )
        self.state_file.write_text(text, encoding="utf-8")
        result = load(self.state_file, "paths")
        self.assertEqual(result, CANONICAL_DEFAULTS["paths"])

    def test_load_paths_override_wins(self):
        # File overrides decisions_log; default would be the same value here.
        # Test with a real override:
        text = self.state_file.read_text(encoding="utf-8")
        text = text.replace(
            "decisions_log: decisions/decision-log.md",
            "decisions_log: state/decisions.md",
        )
        self.state_file.write_text(text, encoding="utf-8")
        result = load(self.state_file, "paths")
        self.assertEqual(result["decisions_log"], "state/decisions.md")

    def test_load_unknown_block_raises(self):
        with self.assertRaises(ManifestError):
            load(self.state_file, "nonexistent_block")

    def test_load_unsupported_block_raises(self):
        with self.assertRaises(ManifestError):
            load(self.state_file, "instance_layer")

    # ---------- append ----------

    def test_append_adds_value_to_list(self):
        self.assertTrue(append(self.state_file, "template_layer", "rules/baz.md"))
        self.assertIn("rules/baz.md", load(self.state_file, "template_layer"))

    def test_append_refuses_duplicate_returns_false(self):
        self.assertFalse(append(self.state_file, "template_layer", "AGENTS.md"))

    def test_append_unknown_block_raises(self):
        with self.assertRaises(ManifestError):
            append(self.state_file, "nonexistent", "foo")

    def test_append_unsupported_block_raises(self):
        with self.assertRaises(ManifestError):
            append(self.state_file, "instance_layer", "anything")

    def test_append_to_inline_empty_list_converts_to_multiline(self):
        self.assertTrue(append(self.state_file, "empty_dirs", "research/sessions"))
        loaded = load(self.state_file, "empty_dirs")
        self.assertEqual(loaded, ["research/sessions"])

    def test_append_to_absent_block_creates_block(self):
        # Strip a block, then append
        text = self.state_file.read_text(encoding="utf-8")
        text = text.replace("voice: []\n", "")
        self.state_file.write_text(text, encoding="utf-8")
        self.assertTrue(append(self.state_file, "voice", "rules/voice/example.md"))
        self.assertIn("rules/voice/example.md", load(self.state_file, "voice"))

    def test_append_paths_inserts_new_key(self):
        self.assertTrue(
            append(self.state_file, "paths", ("custom_key", "custom/path.md"))
        )
        loaded = load(self.state_file, "paths")
        self.assertEqual(loaded["custom_key"], "custom/path.md")

    def test_append_paths_updates_existing_key(self):
        self.assertTrue(
            append(self.state_file, "paths", ("decisions_log", "alt/decisions.md"))
        )
        loaded = load(self.state_file, "paths")
        self.assertEqual(loaded["decisions_log"], "alt/decisions.md")

    def test_append_paths_no_op_when_value_unchanged(self):
        self.assertFalse(
            append(
                self.state_file,
                "paths",
                ("decisions_log", "decisions/decision-log.md"),
            )
        )

    def test_append_paths_requires_tuple(self):
        with self.assertRaises(ManifestError):
            append(self.state_file, "paths", "not-a-tuple")

    # ---------- contains ----------

    def test_contains_true_when_present_in_list(self):
        self.assertTrue(contains(self.state_file, "template_layer", "AGENTS.md"))

    def test_contains_false_when_absent_from_list(self):
        self.assertFalse(contains(self.state_file, "template_layer", "missing.md"))

    def test_contains_paths_default_key_present(self):
        # Key that's only in canonical defaults, not in the file
        self.assertTrue(contains(self.state_file, "paths", "inbox_dir"))

    def test_contains_paths_explicit_key_present(self):
        self.assertTrue(contains(self.state_file, "paths", "decisions_log"))

    def test_contains_paths_unknown_key_absent(self):
        self.assertFalse(contains(self.state_file, "paths", "nonexistent_key"))

    # ---------- validate ----------

    def test_validate_passes_clean_list(self):
        validate(self.state_file, "template_layer")  # no exception

    def test_validate_passes_clean_paths(self):
        validate(self.state_file, "paths")  # no exception

    def test_validate_raises_on_duplicate_in_list(self):
        text = self.state_file.read_text(encoding="utf-8")
        text = text.replace(
            "template_layer:\n  - AGENTS.md\n  - rules/foo.md\n",
            "template_layer:\n  - AGENTS.md\n  - AGENTS.md\n",
        )
        self.state_file.write_text(text, encoding="utf-8")
        with self.assertRaises(ManifestError):
            validate(self.state_file, "template_layer")

    def test_validate_passes_on_absent_block(self):
        text = self.state_file.read_text(encoding="utf-8")
        text = text.replace("voice: []\n", "")
        self.state_file.write_text(text, encoding="utf-8")
        validate(self.state_file, "voice")  # no exception — absent is valid

    def test_validate_unknown_block_raises(self):
        with self.assertRaises(ManifestError):
            validate(self.state_file, "nonexistent_block")

    # ---------- yaml round-trip ----------

    def test_round_trip_preserves_unrelated_content(self):
        before_lines = self.state_file.read_text(encoding="utf-8").splitlines()
        append(self.state_file, "template_layer", "rules/baz.md")
        after = self.state_file.read_text(encoding="utf-8")
        # Other blocks intact
        self.assertIn('version: "0.2.0-rc4"', after)
        self.assertIn("meta_layer:", after)
        self.assertIn("LINEAGE.md", after)
        self.assertIn("paths:", after)
        # Top comment preserved
        self.assertTrue(any("# Top-level comment" in line for line in before_lines))
        self.assertIn("# Top-level comment", after)

    def test_round_trip_preserves_block_comments(self):
        text = """\
# Header
version: "1.0"

# Block A
template_layer:
  - AGENTS.md
"""
        self.state_file.write_text(text, encoding="utf-8")
        append(self.state_file, "template_layer", "rules/new.md")
        result = self.state_file.read_text(encoding="utf-8")
        self.assertIn("# Header", result)
        self.assertIn("# Block A", result)

    # ---------- known-name registries ----------

    def test_paths_in_known_dicts(self):
        self.assertIn("paths", KNOWN_DICTS)

    def test_project_in_known_dicts(self):
        self.assertIn("project", KNOWN_DICTS)

    def test_load_project_returns_existing_block(self):
        # Append a project block to the sample
        text = self.state_file.read_text(encoding="utf-8")
        text = "project:\n  name: \"Sample\"\n  code: \"SMP\"\n  domain: \"testing\"\n\n" + text
        self.state_file.write_text(text, encoding="utf-8")
        result = load(self.state_file, "project")
        self.assertEqual(result, {"name": "Sample", "code": "SMP", "domain": "testing"})

    def test_load_project_returns_empty_dict_when_absent(self):
        # No project block in default sample — and project has no canonical defaults
        result = load(self.state_file, "project")
        self.assertEqual(result, {})

    def test_append_project_inserts_key(self):
        # Append a project block first, then update one of its keys
        text = self.state_file.read_text(encoding="utf-8")
        text = "project:\n  name: \"Sample\"\n  code: \"SMP\"\n  domain: \"testing\"\n\n" + text
        self.state_file.write_text(text, encoding="utf-8")
        self.assertTrue(append(self.state_file, "project", ("name", "Renamed")))
        result = load(self.state_file, "project")
        self.assertEqual(result["name"], "Renamed")

    def test_template_layer_in_known_lists(self):
        self.assertIn("template_layer", KNOWN_LISTS)

    def test_instance_layer_unsupported(self):
        self.assertIn("instance_layer", UNSUPPORTED)


if __name__ == "__main__":
    unittest.main()
