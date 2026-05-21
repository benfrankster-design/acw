# rebuild

The `rebuild` verb produces a fresh `.acw/codemap/` from the current source tree. Three modes:

| Mode | What runs | When to use |
|---|---|---|
| `rebuild` (default) | AST + optional Stage 2 (if env_secrets satisfied) + `implements_decision` bridge | Routine full refresh. |
| `rebuild --ast-only` | AST only | Fast refresh; pre-commit-friendly; skip when no decisions changed. |
| `rebuild --semantic` | Stage 2 + bridge only (assumes AST is current) | Re-run after large decision-log changes without re-walking source. |

## Pre-flight (shared spine)

Before any rebuild fires, the wrapper runs the SKILL.md pre-flight gates in order:

1. Profile check (must be `coding-project` or `library`, or codemap explicitly in `modules:`).
2. Module check.
3. Graphify availability — `subprocess.run(["graphify", "--version"])` returns 0; binary name is `graphify` even though the package is `graphifyy`. If absent: print `pip install graphifyy` and exit non-zero.
4. CLAUDE.md integrity per C-005 — refuse if any non-pointer content (Graphify-managed block, `<!-- BEGIN GRAPHIFY -->`, PreToolUse hook fragments) is detected. Point operator at `/acw-instance audit` for cleanup.
5. env_secrets gate — applies only when `--semantic` is on the command line OR default-mode is about to invoke Stage 2. Walk `acw-state.yaml::env_secrets`; for each entry where `required_by` matches `/codemap rebuild --semantic` AND `when` is `on-opt-in` or `always`, verify `os.environ[name]` is set. Missing → refuse with a one-line pointer naming the missing variable and the `.env` / shell-env supply pattern. Operator can re-run with `--ast-only` to bypass.
6. Codemap dir check — `mkdir -p .acw/codemap` if missing.

Any pre-flight failure exits without invoking Graphify or mutating the workspace.

## Stage 1 — AST (always, except `--semantic`)

Invocation:

```
subprocess.run(["graphify", "update", str(project_root)], cwd=run_dir, check=True)
```

`project_root` is the workspace root (absolute path). `run_dir` is the directory `graphify-out/` will land in — pick one pattern per the implementation-plan tradeoffs:

- **Pattern A (recommended):** `run_dir = .acw/codemap/`. After the call, `graphify-out/` is at `.acw/codemap/graphify-out/`; the wrapper moves its contents up one level and removes the empty `graphify-out/`. Simplest mental model; relocation is one `shutil.move` loop.
- **Pattern B:** `run_dir = project_root`. `graphify-out/` lands at project root; `shutil.move("graphify-out", ".acw/codemap")` with overwrite handling. Requires `.acw/codemap/` to be empty or pre-cleaned.

Choose Pattern A by default; the wrapper documents the choice in the run output so operators can verify.

Cache lives in `.acw/codemap/cache/` (no leading dot) per Graphify's convention. Graphify manages it; the wrapper does not touch it.

## Stage 2 — Semantic (Gemini, opt-in)

Runs only when `--semantic` is explicit OR `rebuild` default-mode and Stage 2 secrets are present.

Graphify's semantic stage is invoked by re-running `graphify update` after the env vars are set — Graphify auto-detects the keys and routes through Gemini. No separate flag is required.

```
env = {**os.environ}   # GEMINI_API_KEY / GOOGLE_API_KEY already set by operator
subprocess.run(["graphify", "update", str(project_root)], cwd=run_dir, env=env, check=True)
```

Token cost: nonzero. Report the count from Graphify's stdout in the rebuild summary.

If both AST and Stage 2 are needed in one invocation, run AST first (no env vars), then Stage 2 (with env vars). Two passes; cache makes the second fast.

## ACW bridge — `implements_decision`

Runs after Graphify finishes, before the rebuild summary prints. Skipped on `--ast-only`.

Algorithm:

1. Load `.acw/codemap/graph.json` (NetworkX JSON). Build a quick index: `{node_id: node_attrs}` and `{file_path: [node_ids]}`.
2. Walk `.acw/decisions/entries/*.md`. For each entry, extract its `id:` from frontmatter (e.g., `D-ACW-052`).
3. For each decision id, scan node attributes (`source_file`, docstring excerpts captured by Graphify) AND the raw source files referenced for literal id matches.
4. **Literal match path:** if a source file contains the decision id as a literal substring (allowing for surrounding punctuation), emit one edge per occurrence:
   ```json
   {
     "source": "<symbol node id>",
     "target": "<decision id>",
     "relation": "implements_decision",
     "confidence": "EXTRACTED",
     "confidence_score": 1.0,
     "source_file": "...",
     "source_location": "L<n>"
   }
   ```
5. **LLM judgment path (optional, gated by env_secrets):** for each decision, optionally ask Claude via the Anthropic SDK whether each candidate symbol (filtered by file overlap or community membership) implements the decision's intent. Prompt:
   > "Decision: <decision title + body excerpt>. Candidate code symbol: <symbol name + docstring + signature>. Does this code implement the decision's intent? Reply with JSON: `{verdict: yes|no, confidence: 0.0-1.0, reason: '<one sentence>'}`."

   On `verdict: yes` with `confidence >= 0.6`, emit an INFERRED edge with the model's confidence and reason captured in a `rationale` field.
6. Write all bridge edges to `.acw/codemap/acw-edges.json` (overwrite each run; sidecar, not a merge into `graph.json`).
7. Append a "Code-to-decision bridges" section to `.acw/codemap/GRAPH_REPORT.md` listing edges grouped by decision, sorted by confidence descending.

The LLM judgment path is gated by an env_secret declaration for `ANTHROPIC_API_KEY` (already in the operator's stack, but declare it for portability). On absence, the bridge runs literal-match-only and notes the limitation in the report.

## Rebuild summary (stdout)

After all stages complete, print a one-block summary:

```
[codemap] rebuild complete
  Mode: <ast-only | full | semantic-only>
  Nodes: <N> (document <a>, code <b>, rationale <c>)
  Edges: <N> total
    EXTRACTED: <n>
    INFERRED:  <n> (avg confidence <x.xx>)
    AMBIGUOUS: <n>
  Bridge edges: <N> implements_decision (<a> EXTRACTED, <b> INFERRED)
  Token cost: <n> input · <n> output (Graphify Stage 2)
                <n> input · <n> output (Claude bridge)
  Output: .acw/codemap/GRAPH_REPORT.md
```

## Failure modes

- **Graphify exits non-zero.** Forward stderr to operator; do NOT mutate `.acw/codemap/` (leave previous good state intact). The wrapper writes to a temp directory and only swaps in on success.
- **Stage 2 fails mid-run** (Gemini quota, network). Fall back to AST-only and warn in the summary; do not abort the bridge step.
- **Bridge LLM fails.** Fall back to literal-match-only bridge; warn in the summary.
- **acw-edges.json write fails.** Roll back to the previous file; warn.

## Idempotency

`/codemap rebuild --ast-only` is safe to run repeatedly without side effects beyond cache updates and a fresh report. Full `rebuild` is idempotent at the graph level; the bridge step's INFERRED edges may vary across runs due to LLM nondeterminism — this is acceptable, as `confidence_score` captures the model's certainty per run.
