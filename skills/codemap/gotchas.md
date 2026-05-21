# Gotchas

- **Profile gating is enforced.** `/codemap` refuses on profiles other than `coding-project` and `library` unless codemap is explicitly in `modules:`. Operators sometimes try to run codemap on spec-project instances — it correctly refuses.

- **AMBIGUOUS edges accumulating.** If `/codemap audit` repeatedly reports the same AMBIGUOUS edges, that's signal the operator needs to triage them (promote to EXTRACTED with explicit annotation, demote to INFERRED with score, or delete). Don't filter them silently.

- **Stage 2 LLM cost.** Semantic extraction calls Claude API per chunk. On large codebases this is real money. Default to `--ast-only` for routine rebuilds; reserve full rebuild for "just landed a decision that should connect to code" moments.

- **Cache staleness across branches.** If the operator switches git branches with substantially different code, the file-level cache may carry stale entries. Force-rebuild via `/codemap rebuild --full --no-cache` if branch-switching is part of the workflow.

- **Graphify version drift.** `.acw/codemap/.graphify-version` records which Graphify version produced the current graph. If Graphify updates and changes its output schema, the wrapper detects and rebuilds from scratch rather than merging incompatible state.

- **Wrapper not yet implemented.** As of 2026-05-21, the wrapper is deferred (see `references/implementation-plan.md`). `/codemap rebuild` exits with a "not yet implemented" message pointing at the plan. Do not silently no-op.

- **Conflation with `/substrate-map`.** Operator may invoke `/codemap` expecting cross-reference navigation across substrate (decisions/glossary/incidents). That's `/substrate-map`. `/codemap` covers source code structure, not substrate. Both compose; neither replaces the other.
