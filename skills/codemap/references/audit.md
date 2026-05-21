# audit

Read-only verb (with one optional Graphify invocation: `graphify benchmark`). Walks `.acw/codemap/` for quality signals: AMBIGUOUS edges, stale references, broken bridge edges, low-confidence INFERRED edges, and Graphify's token-reduction benchmark.

## Pre-flight

Profile + module checks. Graphify availability check ONLY if `--benchmark` is set (default: skip benchmark, audit is purely a reader).

## Reads

1. `.acw/codemap/graph.json` — full edge walk for AMBIGUOUS and low-confidence INFERRED.
2. `.acw/codemap/acw-edges.json` — bridge edges; check each `target` (decision id) still exists as a file in `.acw/decisions/entries/`.
3. `.acw/decisions/entries/*.md` — to detect decision deletions that orphan bridge edges.
4. Source files referenced by graph nodes — to detect deleted source files that leave orphaned nodes.

## Walks

### Walk 1 — AMBIGUOUS edges

Every edge with `confidence: "AMBIGUOUS"` is a triage item. Group by file pair, report:

```
AMBIGUOUS edges (review required): <N>
  <source> ↔ <target>  (relation: <r>, source_file: <f>:L<n>)
    Reason: <if present in edge metadata>
  ...
```

If `N == 0`, print one line: `AMBIGUOUS edges: 0 (clean)`.

### Walk 2 — Low-confidence INFERRED

Configurable threshold (default 0.5). Every edge with `confidence: "INFERRED"` AND `confidence_score < threshold`:

```
Low-confidence INFERRED edges (score < 0.5): <N>
  <source> → <target>  (relation: <r>, score: <x.xx>)
  ...
```

These are not blocking, but signal candidates for promotion (more evidence → EXTRACTED) or demotion (deletion).

### Walk 3 — Stale bridge edges

For each edge in `acw-edges.json`:

- **Target check.** Decision id (`target`) must correspond to a file in `.acw/decisions/entries/`. If missing → stale; the decision was deleted or renamed.
- **Source check.** Symbol node (`source`) must exist in `graph.json`. If missing → stale; the code was deleted or refactored.

Report:

```
Stale bridge edges: <N>
  Deleted decision targets: <M>
    <edge> → target <decision id> (no longer in .acw/decisions/entries/)
  Deleted source symbols: <K>
    <edge> source <symbol> (no longer in graph.json)
```

Stale edges block clean-audit status. Resolution: re-run `/codemap rebuild` to refresh the bridge.

### Walk 4 — Orphan nodes

Nodes in `graph.json` whose `source_file` no longer exists in the workspace:

```
Orphan nodes (source file deleted): <N>
  <node id> (was at <source_file>)
```

Resolution: `/codemap rebuild --ast-only` clears the cache and re-walks.

### Walk 5 — Benchmark (optional, `--benchmark`)

Invokes `graphify benchmark` and parses the token-reduction percentage. Reports:

```
Token reduction vs naive baseline: <X>%  (Graphify benchmark)
  Baseline cost:  <N> tokens (full-corpus re-read)
  Codemap cost:   <N> tokens (graph lookup)
```

Skipped by default. Use when you want a quantitative signal that the codemap is paying for itself.

## Report summary

After all walks, print a one-line summary and an exit code:

```
[codemap] audit complete
  AMBIGUOUS edges:        <N>
  Low-confidence INFERRED: <N>  (score < 0.5)
  Stale bridge edges:     <N>
  Orphan nodes:           <N>
  Status: <clean | needs-attention>
```

- `clean` — all four counts are 0.
- `needs-attention` — at least one count is non-zero.

## Exit codes

- `0` — audit clean.
- `1` — needs-attention (one or more findings).
- `2` — `.acw/codemap/` empty or `graph.json` absent.

`/acw-instance audit` may invoke `/codemap audit` as part of its broader workspace audit when the instance profile is coding-project or library. The exit code propagates.

## What audit does NOT do

- Does not auto-fix findings. Operator reviews and runs `/codemap rebuild` or hand-edits as appropriate.
- Does not mutate any file (except updating an audit-timestamp marker in `.acw/codemap/.last-audit`, if it exists).
- Does not run Stage 2 (Gemini). Pure read.
