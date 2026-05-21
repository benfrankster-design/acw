---
class: raw
authority: instance
stability: in-progress
date: 2026-05-21
type: audit-report
subject: graphify
covers:
  - rules/codemap.md
  - skills/codemap/SKILL.md
  - skills/codemap/gotchas.md
  - skills/codemap/references/implementation-plan.md
  - migrations/0.9.9-to-0.10.0.yaml
  - migrations/pre-acw-to-0.10.0.yaml
  - rules/instance-types.md
  - rules/confidence-tagging.md
  - tools/scaffold-instance.py
  - tools/templates/acw-state.yaml.tmpl
---

# Graphify canonical audit — claims vs reality (2026-05-21)

Earlier ACW canonical work on the codemap module was authored from secondary-source articles (betterstack, pyshine, medium) without actually installing or running Graphify. This audit grades every Graphify-related claim in canonical against ground truth from `pip install graphifyy && graphify update` on real Python code.

## Ground truth (what I observed running graphifyy 0.8.14)

**Installation:** `pip install graphifyy` (two y's). CLI binary: `graphify`. Version probed: 0.8.14.

**Output structure (always at `<cwd>/graphify-out/`; no `--output-dir` flag):**

```
graphify-out/
├── graph.json              # NetworkX directed multigraph
├── graph.html              # interactive vis
├── GRAPH_REPORT.md         # markdown report
├── manifest.json           # per-file mtime + ast_hash + semantic_hash
├── cache/                  # incremental cache (ast/, stat-index.json)
├── .graphify_labels.json   # community labels (operator-editable)
└── .graphify_root          # workspace root marker
```

**Node schema (from probe):**

```json
{
  "label": "scaffold-instance.py",
  "file_type": "code",
  "source_file": "scaffold-instance.py",
  "source_location": "L1",
  "id": "scaffold_instance_py",
  "community": 2,
  "norm_label": "scaffold-instance.py"
}
```

`file_type` values observed: `document`, `code`, `rationale`. Others likely exist for SQL/scripts/images per the GitHub description but weren't in my probe.

**Edge schema (from probe):**

```json
{
  "relation": "calls",
  "context": "call",
  "confidence": "EXTRACTED",
  "confidence_score": 1.0,
  "weight": 1.0,
  "source": "...",
  "target": "...",
  "source_file": "lint-vocab.py",
  "source_location": "L128"
}
```

Edge `relation` values observed on Python code (AST-only run): `calls` (56), `contains` (32), `rationale_for` (17), `inherits` (1). LLM stage would add more.

**Confidence tagging confirmed:** `confidence: EXTRACTED|INFERRED|AMBIGUOUS` per edge. Also a numeric `confidence_score: 0.0–1.0` companion field I hadn't documented.

**Token cost on AST-only:** 0 input · 0 output. Confirmed in report.

**LLM provider:** Gemini. CLI prints: *"Tip: set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to use Gemini for semantic extraction."* Not Claude. Not local.

**Native CLI verbs:**

| Verb | Action |
|---|---|
| `update <path>` | AST extraction. No LLM. |
| `cluster-only <path>` | Rerun clustering on existing graph |
| `watch <path>` | File watcher |
| `query "<question>"` | BFS traversal with budget cap |
| `path "A" "B"` | Shortest path between nodes |
| `explain "X"` | Node + neighborhood explanation |
| `add <url>` | Fetch URL into corpus |
| `merge-graphs <g1> <g2>` | Cross-repo graph merge |
| `benchmark` | Token reduction measurement |
| `hook install` | **Post-commit** git hook (NOT pre-commit) |
| `claude install` | Writes graphify section to CLAUDE.md + PreToolUse hook |
| `gemini install`, `cursor install`, etc. | Other platform integrations |

## Grade per canonical file

### `rules/codemap.md` — needs substantial corrections

| Claim | Reality | Severity |
|---|---|---|
| "Wraps Graphify — does not reinvent" | Correct | ✓ |
| Two-stage extraction (AST + LLM) | Correct shape, but: AST stage emits `rationale_for` edges from rationale-tagged content, not just structural. LLM stage adds INFERRED edges. | minor |
| Output at `.acw/codemap/` | Graphify outputs to `graphify-out/` at cwd; wrapper must relocate or run inside `.acw/codemap/`. **No `--output-dir` flag.** | **breaking** |
| Node types: file / function / method / class / interface / struct / module / concept / decision | Graphify uses `file_type` field with values like `document`, `code`, `rationale`. There's no native "decision" node type — that's an ACW-specific bridge add-on. | moderate |
| Edge types: calls / imports / inherits / implements / references / rationale_for / implements_decision / semantically_similar_to | `calls`, `contains`, `rationale_for`, `inherits` confirmed. `imports`, `implements`, `references` plausible but unobserved in probe. `implements_decision` is ACW-specific, NOT Graphify-native. `semantically_similar_to` likely a semantic-stage edge but unconfirmed. | moderate |
| Confidence tagging: EXTRACTED / INFERRED / AMBIGUOUS | Correct. Also has numeric `confidence_score: 0.0–1.0` field per edge — not documented in my version. | minor |
| "LLM runs locally where possible (gsg-rag substrate already in place for GSG instances)" | **Wrong.** Graphify uses Gemini API. Not local. Not Claude. To run "locally" would require fork or alternative. | **breaking** |
| "Stage 2 reads `.acw/decisions/` entries to bridge code to decisions" | **Wrong.** Graphify reads docs (README, comments, docstrings) but knows nothing about ACW's `.acw/decisions/` convention. The bridge is ACW-side code we'd build on top, not built-in. | **breaking** |
| Stage triggers: pre-commit hook for AST | **Wrong direction.** Graphify ships `graphify hook install` for POST-commit hooks, not pre-commit. Pre-commit would block commits on failure; Graphify's post-commit fires after the commit lands. Different semantic. | moderate |
| `GRAPH_REPORT.md` is the auto-loaded surface | Correct. Confirmed structure: Corpus Check, Summary, Community Hubs, God Nodes, Surprising Connections, Communities, Knowledge Gaps, Suggested Questions. | ✓ |

### `skills/codemap/SKILL.md` — needs corrections aligned with rules

| Claim | Reality | Severity |
|---|---|---|
| Verbs: `rebuild`, `rebuild --ast-only`, `rebuild --semantic`, `status`, `audit` | Graphify uses `update`, `cluster-only`, `query`, `path`, `explain`. Wrapper would translate ACW verb names to Graphify CLI calls. Wrapper can shadow native names or rename. | moderate |
| Pre-flight: "Verify Graphify is installed and on PATH" | Correct approach. Confirmed `graphify --version` returns 0.8.14. | ✓ |
| Output structure: `.acw/codemap/GRAPH_REPORT.md` + `nodes.json` + `edges.json` + `communities.json` + `.cache/` | Graphify writes ONE `graph.json` (combined nodes/edges/hyperedges in NetworkX format), NOT separate `nodes.json` / `edges.json` / `communities.json`. Cache dir is `cache/` (no dot). | **breaking** |
| ACW-specific `implements_decision` edge bridge | Honestly framed as an ACW addition — still correct as a design but the description claimed Graphify's native Stage 2 does this. It doesn't. | minor (the bridge IS ACW-specific, but framing needed correction) |
| "Wrap Graphify rather than reinvent" | Correct. Wrapper can be much THINNER than I wrote since Graphify ships `query`, `path`, `explain` natively. | ✓ (under-spec) |

### `skills/codemap/gotchas.md`

| Claim | Reality |
|---|---|
| "Wrapper not yet implemented" | Still true. Now ready to author. |
| "Stage 2 LLM cost. Semantic extraction calls Claude API per chunk" | **Wrong — uses Gemini.** Patch. |
| "Cache staleness across branches" referencing `.acw/codemap/.cache/` | Path wrong — `cache/` (no dot). |

### `skills/codemap/references/implementation-plan.md`

Entire premise was "investigation deferred until next session." Investigation is now done. Replace with:
- Probe results section (what we found)
- Wrapper authoring steps (now concrete)
- `implements_decision` bridge implementation plan (the LLM bridge for code-to-decision linkage)

### `migrations/0.9.9-to-0.10.0.yaml`

```yaml
- kind: create_dir
  path: .acw/codemap/.cache
```

Should be `path: .acw/codemap/cache` (no dot). Or skip — Graphify creates `cache/` on first `update` run, so the migration's `create_dir` is belt-and-suspenders; the path correction is what matters when it does fire.

### `migrations/pre-acw-to-0.10.0.yaml`

Same correction: `.cache` → `cache`.

### `rules/instance-types.md`

```yaml
codemap_dir: .acw/codemap
codemap_report: .acw/codemap/GRAPH_REPORT.md
```

These are correct for the **post-relocation** state (after the wrapper moves `graphify-out/` contents into `.acw/codemap/`). Worth a clarifying note that Graphify itself writes to `graphify-out/` and the wrapper moves the contents.

### `rules/confidence-tagging.md`

Add the numeric `confidence_score` field (0.0–1.0) to the schema. Graphify emits this companion to the confidence tag. ACW convention should follow.

### `tools/scaffold-instance.py`

The scaffolder creates `.acw/codemap/` and `.acw/codemap/.cache/` for coding-project / library profiles. Same `.cache` → `cache` correction. Honestly: Graphify creates its own `cache/` on first run, so the scaffolder doesn't need to create the cache dir at all — it just needs to ensure `.acw/codemap/` exists as the relocation target.

### `tools/templates/acw-state.yaml.tmpl`

`paths.codemap_dir: .acw/codemap` — correct. `paths.codemap_report: .acw/codemap/GRAPH_REPORT.md` — correct.

## What Graphify has that I didn't know to include

These are real features that should inform the ACW codemap design:

1. **`graphify query "<question>" --budget N`** — BFS traversal returning context capped at N tokens. **The wrapper doesn't need to implement query logic; delegate to Graphify.**
2. **`graphify path "A" "B"`** — shortest path between nodes. Useful for debugging "what depends on X."
3. **`graphify explain "X"`** — plain-language node + neighborhood. Useful for onboarding.
4. **`graphify benchmark`** — measures token reduction vs naive full-corpus baseline. Should be in the codemap audit verb.
5. **`graphify merge-graphs`** — cross-repo graph merge. Relevant for the gsg-cs-* family of repos that share atlas and gsg-rag substrate.
6. **`graphify add <url>`** — pulls URL into corpus. Could integrate ACW's `raw/` content (research artifacts, external docs).
7. **`graphify claude install`** — Graphify ships its own Claude Code integration (CLAUDE.md section + PreToolUse hook). This OVERLAPS with ACW's `AGENTS.md` directive 7 / `auto_load_at_session_start` mechanism. **Need to decide:** use Graphify's native Claude install (which would write to CLAUDE.md, conflicting with ACW's "CLAUDE.md is a thin pointer" convention), OR have the ACW codemap auto-load list reference `.acw/codemap/GRAPH_REPORT.md` directly per the existing hook mechanism. Recommend the latter — keeps the auto-load surface single-purposed.

## What the wrapper actually needs to do (revised)

Much thinner than my prior writeup. Two ACW value-adds, nothing else:

**(a) Output relocation.** Run `graphify update <project-root>` from project root, then `mv graphify-out/* .acw/codemap/`. Or symlink. Or run inside `.acw/codemap/` and target the project root via absolute path. Pick one pattern and document.

**(b) `implements_decision` bridge.** Walk `.acw/decisions/entries/*.md`. For each decision, search `graph.json` nodes for symbol mentions in docstrings, comments, rationale-tagged content. Emit `implements_decision` edges with EXTRACTED confidence if a decision ID is literal in the source, INFERRED with confidence score if LLM-judged. Append to the graph (or sidecar `acw-edges.json` to avoid mutating Graphify's output).

Plus profile gating (coding-project / library only) and auto-load integration.

That's it. Everything else — query, path, explain, watch, benchmark — Graphify does natively. The wrapper invokes the right verb and passes through results.

## Recommended next moves

In order:

1. **Patch the canonical docs** — `rules/codemap.md`, `skills/codemap/SKILL.md`, `gotchas.md`, `implementation-plan.md`, both migration manifests, `rules/confidence-tagging.md`. About 1 hour of authoring.
2. **Author the wrapper** — `skills/codemap/references/rebuild.md`, `status.md`, `audit.md`. Now concrete. About 1-2 hours.
3. **Decide on Graphify's `claude install` vs ACW's auto-load** — design decision, single line in canonical once decided.
4. **Dogfood against cs-atlas** post-v0.10.0 upgrade. Verify the wrapper produces a usable `GRAPH_REPORT.md` and the bridge step finds real code-to-decision links.

## Honest framing

Earlier work was authored confidently in a domain I hadn't actually touched. The result was a mix of correct directional thinking ("two stages, confidence-tagged edges, Tree-sitter-based AST") and incorrect specifics ("uses Claude locally," "ACW-specific node types are native," "output goes to .acw/codemap/ directly"). The architecture survives the audit; the details need correction.

Net: this is fixable in one focused commit. The framework already in place is good; the corrections are narrow and concrete.
