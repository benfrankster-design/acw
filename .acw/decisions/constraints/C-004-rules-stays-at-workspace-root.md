---
id: C-004
title: "rules/ stays at workspace root; do not migrate under .acw/"
date: 2026-05-21
status: active
kind: constraint
updated: 2026-05-21
authority: D-ACW-051
applies_to: all-instances-v0.10.0+
---

# C-004 — rules/ stays at workspace root

## Constraint

The `rules/` directory in every ACW instance lives at the workspace root, NOT under `.acw/`. The metadata-vs-contract distinction from D-ACW-051 holds: substrate (operator journal) goes under `.acw/`; contracts (instance rules) stay at root alongside AGENTS.md, CLAUDE.md, and project artifacts.

## What this means concretely

- Every `rules/*.md` file path in `acw-state.yaml::auto_load_at_session_start` and `canonical_runtime_files` uses the root-level path: `rules/instance-hard-rules.md`, NOT `.acw/rules/instance-hard-rules.md`.
- `/acw-instance audit` does NOT flag root-level `rules/` as substrate drift.
- The scaffolder (`tools/scaffold-instance.py`) generates `rules/` at the workspace root, not under `.acw/`.
- No `rules_dir` key exists in `acw-state.yaml::paths` (rules are not path-configurable).

## What does NOT change

- ACW operator-metadata substrate still lives under `.acw/` per C-003. This constraint is about `rules/` specifically, not a softening of the dotfolder convention.
- Project artifacts (research/, threat-model.md, etc.) still stay at workspace root per D-ACW-050.
- Per-instance hard rules in `rules/instance-hard-rules.md` are still operator-authored and reviewed at audit time.

## Enforcement

- Stop-work for any session that moves rules/ under `.acw/` or that creates a parallel `.acw/rules/` directory.
- `/acw-instance audit` treats root-level `rules/` as expected, not drift.
- Future canonical changes that touch rules/ shape (file renames, new rules) propagate via migration manifests in `migrations/`, never via `rules_dir` path indirection.

## Future revisitation

If a future version (v0.11+) makes skills fully path-agnostic — every path read through `acw-state.yaml::paths` with no hardcoded references — this constraint may be worth revisiting. At that point the load-bearing-convention argument weakens. Not relevant in v0.10.0; not a deferred item; only a flag for the future.

## Authority

D-ACW-051 (resolves OQ-COPS-019). Constraint derives from the decision; cannot be relaxed without superseding the decision.
