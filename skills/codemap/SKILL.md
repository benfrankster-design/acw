---
name: codemap
description: >
  Builds and maintains the codebase knowledge graph for coding-project and
  library instance types. Wraps Graphify (https://graphify.net) — does not
  reinvent. Output relocated from Graphify's native `graphify-out/` to
  canonical `.acw/codemap/` with `GRAPH_REPORT.md` as the agent-consumed
  surface. Default is AST-only (free, deterministic); Stage 2 semantic
  extraction (Gemini) is opt-in via `acw-state.yaml::env_secrets`. ACW-specific
  `implements_decision` bridge runs via Claude. Operator-invoked via
  `/codemap rebuild | status | audit | query | path | explain`.
role: orchestrator
capabilities:
  - source.read
  - substrate.write
  - external-tool.graphify
  - external-tool.claude-api    # for implements_decision bridge only
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | Medium |

# codemap

> **Implementation status (2026-05-21):** SKILL contract authored; Graphify CLI surface probed and documented (graphifyy 0.8.14). Wrapper authoring is the next discrete piece — `references/rebuild.md`, `status.md`, `audit.md` not yet written. This file defines the contract; `references/implementation-plan.md` covers the concrete wrapper steps now that the probe is done. Per D-ACW-052: ACW auto-load wins over `graphify claude install`. Per C-005: stop-work on writing Graphify content into CLAUDE.md.

Object-centered orchestrator. Object: the codebase knowledge graph for this instance. Verbs: operations on it.

## Command table

| Command | What it does | Reference | Underlying Graphify |
|---|---|---|---|
| `rebuild` | Full: AST + (optional Stage 2) + `implements_decision` bridge | `references/rebuild.md` | `graphify update`, [+ Stage 2,] + bridge |
| `rebuild --ast-only` | Stage 1 only. Cheap, deterministic. Pre-commit-friendly. | `references/rebuild.md` | `graphify update` |
| `rebuild --semantic` | Stage 2 (Gemini) + bridge re-run; assumes AST is current | `references/rebuild.md` | `graphify cluster-only` (or update --semantic), + bridge |
| `status` | Report cache freshness, last rebuild timestamps, edge counts by tag | `references/status.md` | reads `graph.json`, `manifest.json` |
| `audit` | Walk for AMBIGUOUS edges and stale references; `graphify benchmark` for token-reduction signal | `references/audit.md` | reads `graph.json`; calls `graphify benchmark` |
| `query "<question>"` | BFS traversal with budget cap (pass-through) | `references/query.md` | `graphify query` |
| `path "A" "B"` | Shortest path between nodes (pass-through) | `references/path.md` | `graphify path` |
| `explain "X"` | Plain-language node + neighborhood (pass-through) | `references/explain.md` | `graphify explain` |

Routing: argument required. No-arg invocation prints this table. Unknown command errors with the table.

## Pre-flight gates

Before any verb fires:

1. **Profile check.** Read `acw-state.yaml::profile`. Only `coding-project` and `library` profiles adopt codemap by default. For other profiles, refuse with: *"codemap not adopted by profile `<profile>`. Declare codemap in `modules:` explicitly to opt in."*
2. **Module check.** Read `acw-state.yaml::modules`. If codemap isn't in the effective module list, refuse as above.
3. **Graphify availability.** Verify Graphify is installed and on PATH (`graphify --version`). If not: print install instructions (`pip install graphifyy` — note two y's; CLI binary is `graphify`) and exit.
4. **CLAUDE.md integrity check.** Verify CLAUDE.md is a one-line pointer per D-ACW-047. If a Graphify-managed block is present (artifact of someone running `graphify claude install` against an ACW instance), refuse with C-005 reference and point at `/acw-instance audit`.
5. **env_secrets check (for `--semantic` runs only).** Read `acw-state.yaml::env_secrets`. For each secret with `required_by` matching the current invocation and `when` matching the current mode, verify the variable is set in `os.environ`. Refuse cleanly if missing: *"`/codemap rebuild --semantic` requires `GEMINI_API_KEY` per env_secrets. Set in `.env` or shell env."*
6. **Codemap dir check.** Verify `.acw/codemap/` exists. Create if missing.

## After pre-flight

Verb-specific work. The rebuild family invokes Graphify, relocates its native `graphify-out/` to `.acw/codemap/`, optionally runs Stage 2, and optionally runs the `implements_decision` bridge. The query/path/explain family is a thin pass-through. The status/audit family reads the relocated graph.

## Output

For `rebuild` (relocated from Graphify's native `graphify-out/`):

```
.acw/codemap/
├── GRAPH_REPORT.md          # auto-loaded summary the agent consumes
├── graph.json               # NetworkX directed multigraph (nodes + edges combined)
├── graph.html               # interactive vis
├── manifest.json            # per-file mtime + ast_hash + semantic_hash
├── cache/                   # per-file incremental rebuild cache (Graphify-managed)
├── acw-edges.json           # implements_decision bridge edges (when bridge runs)
├── .graphify_labels.json    # community labels (operator-editable)
└── .graphify_root           # workspace root marker
```

There is no `nodes.json` / `edges.json` / `communities.json` split — Graphify writes one combined `graph.json` and the wrapper does not break it apart.

For `status` and `audit`: report-only, no file writes beyond an updated audit timestamp.

For `query`, `path`, `explain`: pass-through to Graphify; output to stdout.

## Confidence tagging

Every edge carries one of three tags per `rules/confidence-tagging.md`, plus a numeric `confidence_score` companion field:

- **EXTRACTED** — AST-derived or literal id match. `confidence_score: 1.0`. `calls`, `imports`, `inherits`, `contains` typically EXTRACTED. Decision-bridge edges where the decision id appears literally in source are also EXTRACTED.
- **INFERRED** — LLM-derived from docs/comments/decisions. `confidence_score: 0.0-1.0`. `rationale_for`, `semantically_similar_to`, `implements_decision` (LLM-judged) typically INFERRED.
- **AMBIGUOUS** — conflicting signals. Flagged for review. `/codemap audit` surfaces these.

Graphify emits both tag and numeric score natively per edge.

## ACW-specific bridge: `implements_decision` edges

Beyond Graphify's standard output, codemap adds edges connecting code symbols to ACW decisions. Per D-ACW-052, this bridge runs via Claude (Anthropic SDK), NOT Graphify's native Stage 2:

1. Walk `.acw/decisions/entries/*.md`.
2. For each decision, scan `graph.json` nodes for symbol mentions in docstrings, comments, and rationale-tagged content.
3. Emit `implements_decision` edges:
   - EXTRACTED with `confidence_score: 1.0` when the decision id (`D-CATL-003`) is a literal in the source.
   - INFERRED with `confidence_score: 0.0–1.0` when the LLM judges semantic implementation.
4. Write to `.acw/codemap/acw-edges.json` (sidecar to avoid mutating Graphify's `graph.json`).

This is what makes codemap a substrate-aware code map rather than a generic codebase graph. The decision log governs what the code is FOR; codemap connects code to that governance.

## What this skill MUST NOT do

- **MUST NOT run `graphify claude install`.** Per C-005. ACW's auto-load mechanism owns the Claude Code integration.
- **MUST NOT run `graphify hook install` by default.** Operator may opt in per-instance, but the default surface is on-demand `/codemap rebuild`.
- **MUST NOT mutate Graphify's `graph.json`.** ACW-specific edges go in the sidecar `acw-edges.json`.
- **MUST NOT default to Stage 2.** Default is AST-only. Stage 2 requires explicit `--semantic` flag AND env_secrets satisfaction.

## Composes with `/substrate-map` and `gsg-rag`

- `/codemap` → code structure traversal
- `/substrate-map` → substrate cross-reference rendering
- `gsg-rag` (where applicable per instance) → prose retrieval

Three different navigable surfaces. None replaces the others. An agent working in a coding-project instance can query all three depending on what it needs.

## What this skill is NOT

- **Not a code-search tool.** ripgrep is the right tool for text search. Codemap returns structured relationships.
- **Not a documentation generator.** `GRAPH_REPORT.md` is a navigation aid, not API documentation.
- **Not auto-rebuild on every commit.** Operator-driven via `/codemap rebuild`. Auto-load surfaces the latest `GRAPH_REPORT.md` at session start, which is fresh enough for codebase change cadence.
- **Not adopted by all profiles.** Only `coding-project` and `library`. Spec-project and org-brain don't have code to map.
