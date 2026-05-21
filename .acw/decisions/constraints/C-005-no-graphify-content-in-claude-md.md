---
id: C-005
title: "No Graphify content in any instance's CLAUDE.md"
date: 2026-05-21
status: active
kind: constraint
updated: 2026-05-21
authority: D-ACW-052
applies_to: all-instances-v0.10.1+
---

# C-005 — No Graphify content in CLAUDE.md

## Constraint

`graphify claude install` MUST NOT be run on any ACW instance. CLAUDE.md remains a one-line pointer per D-ACW-047. Codemap integration with Claude Code runs through ACW's auto-load mechanism (`acw-state.yaml::auto_load_at_session_start` consumed by `.claude/hooks/load-context.py`), never through Graphify's native CLAUDE.md writer.

## What this means concretely

- No `<!-- BEGIN GRAPHIFY -->` or equivalent Graphify-managed block appears in any instance's CLAUDE.md.
- No PreToolUse hook installed by Graphify is permitted in `.claude/settings.json`. (ACW's SessionStart hook is the canonical mechanism.)
- The `/codemap` skill MUST NOT call `graphify claude install`, `graphify gemini install`, `graphify cursor install`, or any other Graphify host-integration verb.
- If an operator inherits an instance where `graphify claude install` was previously run, `/acw-instance audit` detects the Graphify block and proposes removal as a plan row.

## What does NOT change

- `graphify update`, `graphify query`, `graphify path`, `graphify explain`, `graphify hook install` (post-commit), and other Graphify verbs that do NOT touch CLAUDE.md or `.claude/` are permitted internally by the `/codemap` wrapper.
- Graphify itself is a permitted dependency; only its host-integration writers are forbidden.
- The auto-loaded surface is `.acw/codemap/GRAPH_REPORT.md`, declared in `acw-state.yaml::auto_load_at_session_start` for coding-project / library profiles.

## Enforcement

- Stop-work for any session that runs `graphify claude install` or that writes Graphify-managed content into CLAUDE.md.
- `/acw-instance audit` walks CLAUDE.md and flags any non-pointer content as drift.
- `/codemap` skill's pre-flight verifies CLAUDE.md is the one-line pointer; refuses if drift detected and points operator at audit.

## Rationale

CLAUDE.md is the host-specific entry-point file. Per D-ACW-047, it stays minimal (one line pointing to AGENTS.md) precisely so the manifest (`acw-state.yaml::auto_load_at_session_start`) is the single source of truth for what gets auto-loaded. Allowing Graphify to write its own block into CLAUDE.md re-creates the drift surface D-ACW-047 was authored to eliminate.

## Authority

D-ACW-052. Constraint derives from the decision; cannot be relaxed without superseding D-ACW-052.
