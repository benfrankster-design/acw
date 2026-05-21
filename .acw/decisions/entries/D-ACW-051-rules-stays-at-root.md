---
id: D-ACW-051
title: "rules/ stays at workspace root, does not migrate under .acw/"
date: 2026-05-21
status: accepted
kind: decision
updated: 2026-05-21
supersedes: []
resolves:
  - id: OQ-COPS-019
    confidence: EXTRACTED
---

# D-ACW-051 — rules/ stays at workspace root

## Decision

The `rules/` directory in every ACW instance remains at the workspace root. It does NOT migrate under `.acw/` with the rest of the substrate.

This decision resolves OQ-COPS-019 (filed in cs-ops-spec 2026-05-21, deferred to canonical via the absorption proposal). Closes the pending question raised by D-ACW-050.

## Rationale

Rules are closer in shape to project configuration than to operator working memory:

- **Load-bearing convention.** Many ACW skills hard-code `rules/...` paths at the workspace root. `rules/instance-hard-rules.md`, `rules/pipeline-roles.md`, `rules/skill-format.md`, and others are referenced from skill prose and from `auto_load_at_session_start:`. Moving requires either adding a `rules_dir` path key with skill-side support or rewriting every skill that reads rules. Cost is high; benefit is consistency-of-naming.

- **Different mental model.** ACW substrate under `.acw/` is the *operator's journal* — decisions made, sessions captured, vocabulary defined, incidents recorded. Rules are the *instance contracts* the operator and skills both honor. The journal accumulates; the contracts constrain. Same logic that keeps `pyproject.toml` at the workspace root in Python projects (project config the tooling reads) rather than under `.python/`.

- **Discoverability for new agents.** An agent dropping into a workspace cold needs `rules/` immediately. AGENTS.md directs them to read `rules/pipeline-roles.md`, `rules/canon-governance.md`, `rules/instance-hard-rules.md` before any other action. Hiding rules behind a dotfolder adds a level of indirection that pays no benefit and costs cold-start clarity.

- **Naming consistency at root.** AGENTS.md, CLAUDE.md, README.md, LICENSE-*, threat-model.md, and project artifact dirs (research/, src/, tests/, tools/) all live at the workspace root. `rules/` belongs with them — contract layer, not operator journal.

## Counterargument (rejected)

The case for moving was: full consistency with the `.acw/` convention. "All ACW metadata under one dotfolder" reads cleanly as a single rule.

Rejected because: rules aren't ACW *metadata*, they're ACW *contracts*. The metadata-vs-contract distinction matters more than the naming uniformity. If a future version makes skills entirely path-agnostic via `paths:` keys, the question may be worth revisiting — but that's a v0.11+ concern, not blocking v0.10.0.

## Consequences

- `rules/` stays at the workspace root in every ACW instance, including all five downstream instances pending v0.10.0 upgrade (cs-ops-spec, cs-atlas, _command, cs-copilot, frank-context).
- No `rules_dir` key is added to `acw-state.yaml::paths`.
- `/acw-instance audit | upgrade` does not flag root-level `rules/` as substrate drift.
- C-004 codifies this as a constraint going forward.

## Cross-references

- Resolves OQ-COPS-019 (cs-ops-spec).
- Companion to D-ACW-050 (v0.10.0 .acw/ dotfolder convention).
- Authority for C-004 (rules/ stays at workspace root).
