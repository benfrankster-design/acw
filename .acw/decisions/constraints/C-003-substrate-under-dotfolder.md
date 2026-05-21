---
id: C-003
title: "ACW operator-metadata substrate must live under .acw/"
date: 2026-05-21
status: active
kind: constraint
updated: 2026-05-21
authority: D-ACW-050
applies_to: all-instances-v0.10.0+
---

# C-003 — ACW substrate must live under .acw/

## Constraint

From v0.10.0 forward, no ACW operator-metadata substrate file or directory may be created, moved, or copied to the workspace root. All such substrate lives under `.acw/`.

## What counts as ACW operator-metadata substrate

- `decisions/` (entries, open-questions, constraints, INDEX)
- `glossary/` (entries, INDEX)
- `sessions/` (captures, `.current-session` tracker)
- `raw/` (formerly `_buffer/`; transient routing area)
- `plans/`
- `briefings/`
- `inbox/`
- `archives/`
- `deferred/` (derived view from `DEFERRED.md`)
- `codemap/` (coding-project and library only)
- `acw-state.yaml`
- `build-log.md`
- `incidents.jsonl`
- `tasks-status.md`
- `DEFERRED.md`
- `CHANGELOG.md`

## What does NOT count (stays at workspace root)

- `rules/` — load-bearing convention for skill discovery; future migration question deferred to OQ-COPS-019.
- Entry-point docs: `AGENTS.md`, `CLAUDE.md`, `README.md`, `AUTHOR.md`, `LINEAGE.md`, `ORCHESTRATION.md`, `SKEPTIC.md`, `LICENSE-*`.
- Project artifacts: `research/`, `threat-model.md`, `runbooks/` (per instance call), `integrations/`, `context/`, `tests/`, `tools/`, `skills/`.
- Code directories: `src/`, `lib/`, `app/`, `pkg/`, etc.

## Enforcement

- Stop-work for any session that creates ACW substrate at the workspace root.
- `/acw-instance audit` flags any drift (root-level substrate files outside the allowed list).
- `/acw-instance upgrade` migrates pre-0.10.0 instances to the new shape on first upgrade.
- New instance scaffolding via `tools/scaffold-instance.py` produces the `.acw/` shape from v0.10.0 forward.

## Exceptions

None canonical. Instance-specific deviations require:

1. A decision-log entry naming the rationale.
2. The deviating file or directory declared in `acw-state.yaml::instance_specific_substrate`.
3. The deviation surfaces in `/acw-instance audit` as informational, not as drift.

## Authority

D-ACW-050 (v0.10.0). Constraint derives from the decision; cannot be relaxed without superseding the decision.
