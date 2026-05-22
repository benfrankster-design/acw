---
id: D-ACW-054
title: "ACW-managed post-commit hook fills codemap update lifecycle gap left by D-ACW-052"
date: 2026-05-21
status: accepted
kind: decision
updated: 2026-05-21
supersedes: []
related_to:
  - id: D-ACW-052
    confidence: EXTRACTED
  - id: D-ACW-047
    confidence: EXTRACTED
  - id: C-005
    confidence: EXTRACTED
---

# D-ACW-054 — ACW-managed post-commit codemap auto-update

## Decision

ACW ships two new tools to own the codemap update lifecycle that D-ACW-052 deliberately left on-demand:

1. **`tools/codemap-update.py`** — stdlib-only Python wrapper that runs `graphify update <project_root>` from `.acw/codemap/` (Pattern A) and promotes canonical output files to `.acw/codemap/` only on success. Canonical surface is never mutated on failure. Designed for both hook invocation (`--ast-only`) and direct operator use.

2. **`tools/install-hooks.py`** — stdlib-only installer that writes an ACW-owned post-commit git hook entry into `.git/hooks/post-commit`. Appends to existing hooks rather than overwriting. Idempotent (marker-based). Opt-in: operators run it after cloning.

The post-commit hook fires `codemap-update.py --ast-only` in the background after every commit. The AST graph stays current without operator intervention. Bridge and semantic rebuilds remain operator-invoked.

## What D-ACW-052 left open

D-ACW-052 correctly rejected Graphify's `graphify hook install` (would use Graphify's update lifecycle unmediated by ACW) and `graphify claude install` (writes Graphify-owned content into CLAUDE.md, forbidden by C-005). The consequence was that the codemap could go stale between commits and stay stale until the operator remembered to run `/codemap rebuild`. For a post-commit hook that runs silently, there was no ACW-owned solution.

This decision fills that gap without violating any of D-ACW-052's constraints: the hook is ACW-managed Python, no Graphify-owned content enters CLAUDE.md or `.claude/settings.json`, and the hook is opt-in (not auto-installed).

## Design details

**Run-in-place, not temp-dir.** The `rebuild.md` spec described a temp-dir approach for failure isolation. We deviate here: running graphify from a temp dir destroys `graphify-out/cache/` on every run, defeating incremental rebuilds. Instead the wrapper runs graphify from `.acw/codemap/` directly. The incremental invariant is preserved at the canonical surface level: `GRAPH_REPORT.md`, `graph.json`, and peer files are only promoted (copied) after a successful run. Partial `graphify-out/` state on failure is acceptable — it's Graphify's internal cache, not the load-bearing surface.

**AST-only from the hook.** Bridge (`implements_decision`) and Stage 2 (Gemini) are skipped in hook mode. Both require LLM calls and both are non-deterministic — unsuitable for a silent background trigger. Hook = cheap and deterministic. Full rebuild = operator decision.

**Opt-in installation.** `.git/hooks/` is not tracked by git. The install script must be re-run after each fresh clone. This is documented behavior (the script prints a reminder). Automatic installation via `scaffold-instance.py` is deferred — it would require a separate decision when that tool evolves.

**Append, not overwrite.** The installer detects an existing post-commit hook and appends rather than overwriting, to avoid stomping other hooks (linters, test runners, etc.). The ACW entry is idempotent: a marker string prevents double-installation.

## Consequences

- Codemap stays current with code after every commit for instances that run `python tools/install-hooks.py`.
- Operators with pre-existing post-commit hooks are not disrupted.
- `graphify-out/` is now a first-class directory inside `.acw/codemap/` (not just a transient artifact). Its `cache/` subdirectory persists across runs.
- `tools/codemap-update.py` is also the unshipped Python wrapper the codemap skill contract already specified — this decision ships it. The bridge step (implements_decision) remains unshipped and is a follow-on task.
- `rules/codemap.md` and `skills/codemap/SKILL.md` updated to reflect the new ACW-owned hook trigger.

## Cross-references

- Authority: D-ACW-052 (integration model this decision extends).
- Constraint respected: C-005 (no Graphify content in CLAUDE.md).
- Companion: D-ACW-047 (CLAUDE.md thin pointer — unchanged).
- Files shipped: `tools/codemap-update.py`, `tools/install-hooks.py`.
