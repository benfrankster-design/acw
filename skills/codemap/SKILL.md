---
name: codemap
description: >
  Builds and maintains the codebase knowledge graph for coding-project and
  library instance types. Wraps Graphify (https://graphify.net) — does not
  reinvent. Output lands at `.acw/codemap/` with `GRAPH_REPORT.md` as the
  agent-consumed surface. Two-stage extraction (AST + LLM) with edge
  confidence tagging per `rules/confidence-tagging.md`. Operator-invoked
  via `/codemap rebuild | status | audit`.
role: orchestrator
capabilities:
  - source.read
  - substrate.write
  - external-tool.graphify
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | Medium |

# codemap

> **Implementation status (2026-05-21):** SKILL contract authored; Graphify CLI wrapper deferred to a follow-up session. The wrapper needs the actual Graphify CLI surface probed (output format, exit codes, flags) before it can be authored safely. This file defines the contract; `references/implementation-plan.md` covers the wrapper TODO and the steps to land it.

Object-centered orchestrator. Object: the codebase knowledge graph for this instance. Verbs: operations on it.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `rebuild` | Full rebuild: AST extraction (Stage 1) + LLM semantic extraction (Stage 2). | `references/rebuild.md` |
| `rebuild --ast-only` | Stage 1 only. Cheap, deterministic. Pre-commit hook integration uses this. | `references/rebuild.md` |
| `rebuild --semantic` | Stage 2 only. Re-runs LLM extraction over already-AST'd source. Use after substantial decision-log changes. | `references/rebuild.md` |
| `status` | Report cache freshness, last rebuild timestamps, edge counts by tag. | `references/status.md` |
| `audit` | Walk graph for AMBIGUOUS edges and stale references; report. | `references/audit.md` |

Routing: argument required. No-arg invocation prints this table. Unknown command errors with the table.

## Pre-flight gates

Before any verb fires:

1. **Profile check.** Read `acw-state.yaml::profile`. Only `coding-project` and `library` profiles adopt codemap by default. For other profiles, refuse with: *"codemap not adopted by profile `<profile>`. Declare codemap in `modules:` explicitly to opt in."*
2. **Module check.** Read `acw-state.yaml::modules`. If codemap isn't in the effective module list, refuse as above.
3. **Graphify availability.** Verify Graphify is installed and on PATH. If not: print install instructions (link to https://graphify.net) and exit.
4. **Codemap dir check.** Verify `.acw/codemap/` exists. Create if missing.

## After pre-flight

Verb-specific work. Each verb reads `.acw/codemap/` state, dispatches to Graphify with appropriate flags, routes Graphify's output into the canonical `.acw/codemap/` shape, applies ACW-specific transformations (decision-bridge edges from `.acw/decisions/`), and emits the operator-facing report.

## Output

For `rebuild`:

```
.acw/codemap/
├── GRAPH_REPORT.md          # auto-loaded summary the agent consumes
├── nodes.json               # graph nodes (files, functions, classes, concepts)
├── edges.json               # edges with type + confidence tags
├── communities.json         # cluster analysis
├── .cache/                  # per-file incremental rebuild cache
└── .graphify-version        # which Graphify version produced the current graph
```

For `status` and `audit`: report-only, no file writes beyond an updated audit timestamp.

## Confidence tagging

Every edge carries one of three tags per `rules/confidence-tagging.md`:

- **EXTRACTED** — AST-derived. Confidence 1.0. `calls`, `imports`, `inherits`, `implements` typically EXTRACTED.
- **INFERRED** — LLM-derived from docs/comments/decisions. Confidence 0.0-1.0. `rationale_for`, `implements_decision`, `semantically_similar_to` typically INFERRED.
- **AMBIGUOUS** — conflicting signals. Flagged for review. `/codemap audit` surfaces these.

## ACW-specific bridge: `implements_decision` edges

Beyond Graphify's standard output, codemap adds edges connecting code symbols to ACW decisions. The LLM stage reads `.acw/decisions/entries/*.md` and walks code symbols looking for connections:

- A function whose docstring or rationale-comment references a decision ID (`D-CATL-003`) → `implements_decision` edge, EXTRACTED.
- A function whose behavior implements the intent of a decision (no explicit reference) → `implements_decision` edge, INFERRED with confidence score.

This is what makes codemap a substrate-aware code map rather than a generic codebase graph. The decision log governs what the code is FOR; codemap connects code to that governance.

## Composes with `/substrate-map` and `gsg-rag`

- `/codemap` → code structure traversal
- `/substrate-map` → substrate cross-reference rendering
- `gsg-rag` (where applicable per instance) → prose retrieval

Three different navigable surfaces. None replaces the others. An agent working in a coding-project instance can query all three depending on what it needs.

## What this skill is NOT

- **Not a code-search tool.** ripgrep is the right tool for text search. Codemap returns structured relationships.
- **Not a documentation generator.** `GRAPH_REPORT.md` is a navigation aid, not API documentation.
- **Not auto-rebuild on every commit.** Pre-commit hook (when configured) runs `rebuild --ast-only`, which is cheap. Stage 2 is operator-on-demand.
- **Not adopted by all profiles.** Only `coding-project` and `library`. Spec-project and org-brain don't have code to map.
