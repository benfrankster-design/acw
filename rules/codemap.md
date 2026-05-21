---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Codemap

Substrate module for coding-project and library instance types. A pre-computed, AI-consumable map of a codebase that an agent reads instead of re-scanning the source on every query. Modeled on Graphify (https://graphify.net) — wrap, don't reinvent.

## Why it exists

The bottleneck in AI-assisted work on existing codebases is context retrieval, not generation. Re-reading raw source every session burns tokens and degrades output. A pre-computed codemap collapses repeated expensive re-reads into cheap lookups against a structured artifact.

Empirical baseline (per Graphify): equivalent queries drop from ~14,000 tokens (raw source re-read) to a few hundred tokens (codemap lookup).

## Substrate location

`.acw/codemap/` (per `rules/instance-types.md` path mapping):

```
.acw/codemap/
├── GRAPH_REPORT.md           # auto-loaded summary — the agent's primary consumption surface
├── nodes.json                # raw graph nodes (files, functions, classes, concepts)
├── edges.json                # raw graph edges with type + confidence tags
├── communities.json          # cluster analysis (god nodes, hubs, surprising connections)
└── .cache/                   # per-file incremental rebuild cache
```

`GRAPH_REPORT.md` is the only file auto-loaded at session start. Everything else is backing storage queryable on demand.

## Node types

- **File** — a source file (`.py`, `.ts`, `.go`, etc.)
- **Function** / **method**
- **Class** / **interface** / **struct**
- **Module** — a logical grouping (Python package, Go package, TypeScript module)
- **Concept** — extracted from documentation; not a code symbol. Examples: "the auth boundary," "the customer-facing layer."
- **Decision** — cross-reference to an ACW decision entry. Codemap edges can link code symbols to decisions that govern them.

## Edge types

- **calls** (function → function)
- **imports** (file → file, module → module)
- **inherits** (class → class)
- **implements** (class → interface)
- **references** (any → any)
- **rationale_for** (concept → function/class) — semantic edge from docs
- **implements_decision** (function/class → decision) — codemap-to-substrate bridge
- **semantically_similar_to** (any → any) — LLM-inferred similarity

Every edge carries a confidence tag per `rules/confidence-tagging.md`:

- `EXTRACTED` (1.0) — from AST analysis. `calls`, `imports`, `inherits`, `implements` typically EXTRACTED.
- `INFERRED` (0.0–1.0) — from LLM analysis of prose. `rationale_for`, `implements_decision`, `semantically_similar_to` typically INFERRED.
- `AMBIGUOUS` — conflicting signals. Flagged for review.

## Build stages

**Stage 1 — Deterministic (AST).**

Tree-sitter or equivalent reads source files and extracts:
- File list
- Function and class definitions
- Import graph
- Call graph
- Inheritance and implementation relationships

Reproducible, language-aware, no LLM cost. All edges tagged EXTRACTED with confidence 1.0.

**Stage 2 — Semantic (LLM).**

LLM reads:
- README, AGENTS.md, design docs
- `.acw/decisions/` entries (to bridge code to decisions)
- Docstrings and rationale comments
- Architecture diagrams (if SVG/markdown)

Produces INFERRED edges connecting concepts to code, and code to decisions. Each edge has an explicit confidence score.

Stage 2 runs locally where possible to keep source on the operator's machine. For GSG instances, gsg-rag substrate is the locality vehicle (Claude API call with retrieved-chunks context, not raw-source-to-Claude).

## Freshness

File-level cache. On rebuild:

1. Detect changed files since last cache state.
2. Re-run Stage 1 (AST) on changed files only.
3. Re-run Stage 2 (LLM) only if:
   - Changed files touch documented rationale (docstrings, comments).
   - A new decision entry landed in `.acw/decisions/`.
   - Operator explicitly requests via `/codemap rebuild --semantic`.
4. Merge new extractions into existing graph. Drop stale edges where source files were deleted.
5. Regenerate `GRAPH_REPORT.md`, `communities.json`.

## Build triggers

| Trigger | Stage 1 | Stage 2 |
|---|---|---|
| Pre-commit hook | YES (cheap, fast, must pass) | NO |
| Post-commit | optional | NO |
| Scheduled / cron | optional | YES (e.g., nightly) |
| Operator: `/codemap rebuild` | YES | YES |
| Operator: `/codemap rebuild --ast-only` | YES | NO |
| Operator: `/codemap rebuild --semantic` | NO | YES |
| New decision landed | optional | YES (operator-triggered) |

Default: pre-commit runs Stage 1; Stage 2 is operator-on-demand.

## What GRAPH_REPORT.md contains

Auto-loaded summary. Structure:

```markdown
# Codemap Report — <project>

## Statistics
- Files: N
- Functions: N
- Classes: N
- Edges (EXTRACTED): N
- Edges (INFERRED): N (avg confidence 0.78)
- Edges (AMBIGUOUS): N

## Communities (top N by size)
- Auth community: 14 nodes, god node `AuthUser`
- Payment community: 22 nodes, god node `StripeClient`
- ...

## God nodes (highest connectivity)
- `AuthUser` (degree 47) — auth community
- `StripeClient` (degree 38) — payment community
- ...

## Code-to-decision bridges
- `auth.verify_token` implements_decision D-COPS-027 (OTP authentication is hard requirement)
  confidence: INFERRED 0.92
- ...

## Surprising connections
- `payment.refund` references `notification.email_template_3` — unexpected coupling
- ...

## AMBIGUOUS edges (review required)
- `user.create_account` ↔ `org.invite_member` — conflicting docstring claims
- ...
```

## Skill contract: `/codemap`

When the skill ships, the verb table is:

| Verb | Effect |
|---|---|
| `/codemap rebuild` | Full rebuild: Stage 1 + Stage 2. |
| `/codemap rebuild --ast-only` | Stage 1 only (cheap). |
| `/codemap rebuild --semantic` | Stage 2 only. |
| `/codemap status` | Report cache freshness, last rebuild timestamps, edge counts. |
| `/codemap audit` | Walk graph for AMBIGUOUS edges and stale references; report. |

## What codemap is NOT

- **Not a replacement for gsg-rag or equivalent prose retrieval.** gsg-rag handles HC articles, SOPs, design docs. Codemap handles code structure. They compose; the agent uses both.
- **Not a code-search tool.** Codemap returns structured relationships, not text matches. Use ripgrep for text search.
- **Not a documentation generator.** GRAPH_REPORT.md is a navigation aid, not API documentation.
- **Not auto-curated.** AMBIGUOUS edges and low-confidence INFERRED edges require human review. The graph is a draft until audited.

## Adoption is gated

Only `coding-project` and `library` instance types adopt codemap by default. Other profiles can opt in via explicit `modules:` declaration if their content includes substantial code (e.g., a spec-project that ships tooling alongside the spec).

`org-brain` and `spec-project` instances without code do not have codemap. Their navigable substrate is the wiki-shaped decisions, glossary, and research artifacts.

## Implementation: wrap Graphify

Recommended: the `/codemap` skill wraps the Graphify CLI rather than reimplementing the extraction pipeline. Graphify is MIT-licensed, Python-based, and the load-bearing pieces (Tree-sitter integration, confidence tagging, NetworkX graph, Leiden community detection) are mature.

The wrapper:
1. Invokes Graphify with the instance's source paths.
2. Receives Graphify's output (its `graphify-out/` directory).
3. Routes the output into the canonical `.acw/codemap/` shape.
4. Adds ACW-specific bridges: `implements_decision` edges by reading `.acw/decisions/` and matching code-to-decision via LLM.

When Graphify ships features that supersede the wrapper (e.g., native ACW integration), revisit.
