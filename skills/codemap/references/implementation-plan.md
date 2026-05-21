# codemap implementation plan

The SKILL contract is authored (SKILL.md). The Graphify CLI surface has been probed and documented (graphifyy 0.8.14, audit at `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md`). The wrapper itself — `references/rebuild.md`, `status.md`, `audit.md`, plus the pass-through references — is the next discrete piece.

## Probe findings (ground truth from running `graphify update`)

**Install:** `pip install graphifyy` (two y's). CLI binary: `graphify`. Version probed: 0.8.14.

**Output structure (at `<cwd>/graphify-out/`; no `--output-dir` flag):**

```
graphify-out/
├── graph.json              # NetworkX directed multigraph (nodes + edges combined)
├── graph.html              # interactive vis
├── GRAPH_REPORT.md         # markdown report (the auto-loaded surface after relocation)
├── manifest.json           # per-file mtime + ast_hash + semantic_hash
├── cache/                  # incremental cache (NOT .cache)
├── .graphify_labels.json   # community labels
└── .graphify_root          # workspace root marker
```

**Native CLI verbs:**

| Verb | Action |
|---|---|
| `update <path>` | AST extraction. Free. |
| `cluster-only <path>` | Rerun clustering on existing graph |
| `watch <path>` | File watcher |
| `query "<question>"` | BFS traversal with budget cap |
| `path "A" "B"` | Shortest path between nodes |
| `explain "X"` | Node + neighborhood explanation |
| `add <url>` | Fetch URL into corpus |
| `merge-graphs <g1> <g2>` | Cross-repo graph merge |
| `benchmark` | Token reduction measurement |
| `hook install` | **Post-commit** git hook (NOT pre-commit) — NOT used by default |
| `claude install` | **FORBIDDEN per C-005.** Writes to CLAUDE.md; conflicts with D-ACW-047. |

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

Edge `relation` values observed on Python AST-only run: `calls`, `contains`, `rationale_for`, `inherits`. Stage 2 adds more (Gemini).

**Token cost on AST-only:** 0 input · 0 output. Confirmed.

**LLM provider for Stage 2:** Gemini. CLI prints: *"Tip: set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to use Gemini for semantic extraction."*

## What the wrapper needs to do

Much thinner than originally scoped. Two ACW value-adds, plus pass-through:

### (a) Output relocation

Run `graphify update <project-root>` from a controlled location, then relocate `graphify-out/*` to `.acw/codemap/`. Three viable patterns:

1. **Run from `.acw/codemap/`, target absolute path.** Cleanest if `.acw/codemap/.graphify_root` is set ahead of time. Graphify writes `graphify-out/` inside `.acw/codemap/`, then `mv .acw/codemap/graphify-out/* .acw/codemap/ && rmdir .acw/codemap/graphify-out`.
2. **Run from project root, mv after.** Simple `subprocess.run(["graphify", "update", "."])` then `shutil.move("graphify-out", ".acw/codemap/")` with overwrite handling.
3. **Symlink `graphify-out` → `.acw/codemap/`.** Works on POSIX; Windows needs admin or developer-mode symlinks. Skip unless cross-platform symlinks become trivial.

Recommend pattern 1 or 2; document the choice in `references/rebuild.md`.

### (b) `implements_decision` bridge via Claude

After `graph.json` is in `.acw/codemap/`:

1. Walk `.acw/decisions/entries/*.md`.
2. Load `graph.json` (NetworkX format).
3. For each decision, scan node `source_file` / docstring content / rationale-tagged nodes for:
   - **Literal id match** (`D-CATL-003` appears in source) → emit `implements_decision` edge, EXTRACTED, `confidence_score: 1.0`.
   - **LLM semantic judgment** via Anthropic SDK → emit edge, INFERRED, `confidence_score: <model output>`.
4. Write edges to `.acw/codemap/acw-edges.json` (sidecar; do NOT mutate Graphify's `graph.json`).
5. Append a "Code-to-decision bridges" section to `GRAPH_REPORT.md` listing the bridge edges with confidence scores.

LLM prompt should constrain to: "Does this code symbol implement the intent of this decision? Yes/no with confidence 0.0–1.0 and one-sentence justification."

### (c) Pass-through verbs

`query`, `path`, `explain` are pure pass-throughs: build `subprocess.run(["graphify", verb, *args])`, stream stdout to operator. The wrapper sets cwd to `.acw/codemap/` so Graphify reads the relocated graph.

`benchmark` runs inside audit verb: parse Graphify's token-reduction number, surface in audit report.

## Wrapper files to author

In order:

1. **`references/rebuild.md`** — verb behavior: pre-flight gates, profile/module check, env_secrets check (for `--semantic`), `graphify update` invocation, relocation, optional Stage 2, `implements_decision` bridge invocation.
2. **`references/status.md`** — verb behavior: read `.acw/codemap/manifest.json` + `graph.json`, report cache freshness (mtime vs source files), edge counts by tag, last bridge run timestamp.
3. **`references/audit.md`** — verb behavior: walk `graph.json` for AMBIGUOUS edges, walk `acw-edges.json` for stale decision refs (decisions that no longer exist), call `graphify benchmark` and surface token-reduction score, report.
4. **`references/query.md`, `path.md`, `explain.md`** — short reference files documenting the pass-through behavior.

## Dogfood target

cs-atlas, after its v0.10.0 upgrade lands. Profile = coding-project; has Python code and `.acw/decisions/` substrate. Expected outcome: `.acw/codemap/GRAPH_REPORT.md` lands; `implements_decision` bridge finds at least 2-3 literal-id matches across decision entries.

## Estimated effort

1-2 hours focused work. Probe is done; the unknowns are gone; the remaining work is mechanical wrapper code + reference-file authoring.

## What's already shipped

1. **SKILL.md contract.** Authored. Includes command table, pre-flight gates, output structure, ACW-bridge contract, MUST-NOT list.
2. **Substrate location.** `.acw/codemap/` directory created during instance upgrade for coding-project / library profiles via migration manifests.
3. **Auto-load entry.** Once `.acw/codemap/GRAPH_REPORT.md` exists, it gets added to `acw-state.yaml::auto_load_at_session_start` per D-ACW-052 and the coding-project profile's defaults.
4. **Decisions.** D-ACW-052 (integration via auto-load, not graphify claude install) and C-005 (stop-work on Graphify content in CLAUDE.md) authored.

## What's gated until the wrapper ships

Until the wrapper is authored, `/codemap rebuild` exits with: *"codemap wrapper not yet implemented; see skills/codemap/references/implementation-plan.md."* This is intentional — better to fail loudly than ship a broken wrapper.
