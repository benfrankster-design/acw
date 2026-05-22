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

`.acw/codemap/` (per `rules/instance-types.md` path mapping). The wrapper's job is to relocate Graphify's native output into this canonical location.

**Graphify native output (what `graphify update` writes):**

```
graphify-out/                     # at cwd; NO --output-dir flag
├── graph.json                    # NetworkX directed multigraph (nodes + edges combined)
├── graph.html                    # interactive vis
├── GRAPH_REPORT.md               # markdown report
├── manifest.json                 # per-file mtime + ast_hash + semantic_hash
├── cache/                        # per-file incremental cache (NOT .cache)
├── .graphify_labels.json         # community labels (operator-editable)
└── .graphify_root                # workspace root marker
```

**ACW relocated form (what the wrapper produces):**

```
.acw/codemap/
├── GRAPH_REPORT.md               # auto-loaded summary — the agent's primary consumption surface
├── graph.json                    # NetworkX directed multigraph
├── graph.html                    # interactive vis
├── manifest.json                 # per-file mtime + ast_hash + semantic_hash
├── cache/                        # per-file incremental rebuild cache
├── acw-edges.json                # ACW-specific implements_decision edges (when bridge runs)
├── .graphify_labels.json         # community labels
└── .graphify_root                # workspace root marker
```

`GRAPH_REPORT.md` is the only file auto-loaded at session start (declared in `acw-state.yaml::auto_load_at_session_start` per D-ACW-052). Everything else is backing storage queryable on demand via `graphify query`, `graphify path`, `graphify explain`.

There is no `nodes.json` / `edges.json` / `communities.json` split — Graphify writes one combined `graph.json` (NetworkX format) and the wrapper does not break it apart.

## Node types

Graphify emits nodes with a `file_type` field. Observed values from probe (graphifyy 0.8.14):

- **document** — markdown, prose, design docs
- **code** — source files (Python, TS, Go, etc.)
- **rationale** — extracted rationale-tagged content from docstrings, comments, or rationale-tagged sections

Other `file_type` values may appear for SQL, scripts, images per Graphify's roadmap. Update this list when a new value surfaces in production graphs.

There is no native "decision" node type. The bridge to ACW decisions is built on top via the `implements_decision` edge (see below), not by introducing a Graphify-native node type.

## Edge types

Graphify emits edges with a `relation` field. Observed on AST-only Python probe:

| relation | Source | Stage |
|---|---|---|
| `calls` | AST call site | EXTRACTED (Stage 1) |
| `contains` | AST containment (module → class → function) | EXTRACTED (Stage 1) |
| `rationale_for` | docstring/comment → symbol | EXTRACTED (Stage 1, from rationale-tagged content) |
| `inherits` | class → class | EXTRACTED (Stage 1) |

Stage 2 (Gemini, opt-in) adds INFERRED edges. Common candidates per Graphify documentation: `references`, `semantically_similar_to`, `implements`. Verify in your instance's graph after first semantic run.

ACW adds one bridge edge type via the `implements_decision` bridge (not Graphify-native):

- `implements_decision` — code symbol → ACW decision entry. EXTRACTED when the decision id is a literal in the source. INFERRED with confidence score when LLM-judged. Authored by the ACW-side bridge step, not Graphify.

## Confidence tagging

Every edge carries a confidence tag per `rules/confidence-tagging.md`, plus a numeric `confidence_score` companion field:

- **EXTRACTED** — from deterministic source (AST, frontmatter, literal id). `confidence_score: 1.0`.
- **INFERRED** — from LLM analysis (semantic stage, decision-bridge judgment). `confidence_score: 0.0–1.0` (explicit number required).
- **AMBIGUOUS** — conflicting signals. `confidence_score` not assigned. Flagged for review.

Graphify emits both the tag and the numeric score natively. Surface both in any audit or report view.

## Build stages

**Stage 1 — Deterministic (AST), free.**

`graphify update <project-root>` runs Tree-sitter against source files and extracts file list, function and class definitions, call graph, containment, inheritance, and `rationale_for` edges from rationale-tagged content. Reproducible, language-aware, zero LLM cost. All edges tagged EXTRACTED with `confidence_score: 1.0`.

**Stage 2 — Semantic (Gemini), opt-in.**

Graphify's native semantic stage uses Gemini (`GEMINI_API_KEY` or `GOOGLE_API_KEY` env var; CLI prints a tip when keys are absent). NOT Claude. NOT local.

Opt-in pattern: declare the required secret in `acw-state.yaml::env_secrets`; the operator supplies the value via per-instance `.env` (gitignored) or shell env. The wrapper reads from `os.environ` and refuses cleanly if the declared secret is missing.

For most ACW instances the semantic value-add comes from the `implements_decision` bridge (via Claude — see below), not from Graphify's Stage 2. Stage 2 stays available but is not the default.

**ACW-specific bridge — `implements_decision` (via Claude).**

After Graphify produces `graph.json`, the bridge step:

1. Walks `.acw/decisions/entries/*.md`.
2. For each decision, scans graph nodes for symbol mentions in docstrings, comments, and rationale-tagged content.
3. Emits `implements_decision` edges:
   - EXTRACTED with `confidence_score: 1.0` when the decision id is a literal in the source.
   - INFERRED with `confidence_score: 0.0–1.0` when the LLM judges semantic implementation.
4. Writes edges to `.acw/codemap/acw-edges.json` (sidecar to avoid mutating Graphify's `graph.json`).

The bridge runs via the Anthropic SDK (already in the operator's stack). This keeps ACW substrate under ACW control, uses the LLM the operator pays for anyway, and follows ACW's confidence-tagging discipline directly. Per D-ACW-052.

## Freshness

Graphify maintains its own per-file cache in `cache/` (manifest.json + ast hashes). On rebuild, Graphify detects changed files and re-runs AST only on what changed. The wrapper does not manage the cache; Graphify does.

The `implements_decision` bridge is rerun when:
- A new decision entry lands in `.acw/decisions/entries/`.
- A graph rebuild lands new code symbols.
- Operator explicitly requests via `/codemap rebuild --semantic`.

## Build triggers

| Trigger | AST | Stage 2 (Gemini) | implements_decision bridge |
|---|---|---|---|
| Operator: `/codemap rebuild` | YES | only if env_secrets present | YES |
| Operator: `/codemap rebuild --ast-only` | YES | NO | NO |
| Operator: `/codemap rebuild --semantic` | NO | YES (requires env_secrets) | YES |
| New decision landed | optional | NO | YES (operator-triggered) |
| ACW post-commit hook (`tools/install-hooks.py`) | YES (AST only, background) | NO | NO |

Graphify ships `graphify hook install` but ACW does NOT use it — that hook is Graphify-managed and would run outside ACW's update lifecycle (D-ACW-052, C-005). Instead, ACW ships its own post-commit hook via `tools/install-hooks.py`. The hook calls `tools/codemap-update.py --ast-only` in the background after every commit: fast, deterministic, no LLM cost. The AST graph stays current without operator intervention. Bridge and semantic rebuilds remain operator-invoked because they cost tokens and are non-deterministic.

The hook is opt-in — operators run `python tools/install-hooks.py` after cloning. `.git/hooks/` is not tracked by git; re-run after each fresh clone. Per D-ACW-054.

`graphify claude install` is NEVER used. Per D-ACW-052 and C-005, ACW's auto-load mechanism owns the Claude Code integration; CLAUDE.md stays a thin pointer.

## What GRAPH_REPORT.md contains

Auto-loaded summary. Graphify emits these sections natively (confirmed by probe):

- **Corpus Check** — file counts, languages detected
- **Summary** — node and edge counts by type
- **Community Hubs** — top communities by size
- **God Nodes** — highest-connectivity nodes
- **Surprising Connections** — high-degree cross-community edges
- **Communities** — per-community node lists
- **Knowledge Gaps** — areas thin on documentation or rationale
- **Suggested Questions** — LLM-suggested probes (when Stage 2 ran)

The wrapper does not regenerate this report; Graphify does. ACW adds an appended section when the `implements_decision` bridge runs:

- **Code-to-decision bridges** — `implements_decision` edges with confidence tags.

## Skill contract: `/codemap`

| Verb | Effect | Underlying Graphify call |
|---|---|---|
| `/codemap rebuild` | Full: AST + (optional Stage 2) + implements_decision bridge | `graphify update`, optionally Stage 2, then bridge |
| `/codemap rebuild --ast-only` | Stage 1 only (cheap). | `graphify update` |
| `/codemap rebuild --semantic` | Stage 2 + bridge re-run; assumes AST is current | `graphify cluster-only` (or update with semantic), then bridge |
| `/codemap status` | Report cache freshness, last rebuild, edge counts | reads `graph.json`, `manifest.json` |
| `/codemap audit` | Walk for AMBIGUOUS edges and stale references; also `graphify benchmark` for token-reduction signal | reads `graph.json`; calls `graphify benchmark` |
| `/codemap query "<question>"` | Pass-through to Graphify BFS | `graphify query` |
| `/codemap path "A" "B"` | Pass-through shortest path | `graphify path` |
| `/codemap explain "X"` | Pass-through node + neighborhood explanation | `graphify explain` |

## What codemap is NOT

- **Not a replacement for gsg-rag or equivalent prose retrieval.** gsg-rag handles HC articles, SOPs, design docs. Codemap handles code structure. They compose; the agent uses both.
- **Not a code-search tool.** Codemap returns structured relationships, not text matches. Use ripgrep for text search.
- **Not a documentation generator.** GRAPH_REPORT.md is a navigation aid, not API documentation.
- **Not auto-curated.** AMBIGUOUS edges and low-confidence INFERRED edges require human review. The graph is a draft until audited.

## Adoption is gated

Only `coding-project` and `library` instance types adopt codemap by default. Other profiles can opt in via explicit `modules:` declaration if their content includes substantial code (e.g., a spec-project that ships tooling alongside the spec).

`org-brain` and `spec-project` instances without code do not have codemap. Their navigable substrate is the wiki-shaped decisions, glossary, and research artifacts.

## Implementation: wrap Graphify

The `/codemap` skill wraps the Graphify CLI rather than reimplementing the extraction pipeline. Graphify is MIT-licensed, Python-based, and the load-bearing pieces (Tree-sitter integration, confidence tagging, NetworkX graph, Leiden community detection) are mature.

The wrapper's two value-adds:

**(a) Output relocation.** Graphify writes to `<cwd>/graphify-out/` and has no `--output-dir` flag. The wrapper runs `graphify update <project-root>` from a controlled directory and relocates the output to `.acw/codemap/` (mv, symlink, or run-in-place — pick one pattern per instance).

**(b) `implements_decision` bridge.** Walk `.acw/decisions/entries/*.md`, scan `graph.json` nodes for symbol mentions in source-tagged content, emit `implements_decision` edges to `.acw/codemap/acw-edges.json` with EXTRACTED (literal id match) or INFERRED (LLM-judged) tags plus a confidence score.

Plus profile gating (coding-project / library only), env_secrets pre-flight, and auto-load integration. Everything else — query, path, explain, watch, benchmark, merge-graphs — Graphify does natively; the wrapper just passes through.

When Graphify ships features that supersede the wrapper (e.g., native ACW substrate integration), revisit.
