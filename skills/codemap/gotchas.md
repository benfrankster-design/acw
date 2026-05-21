# Gotchas

- **Package name has two y's.** `pip install graphifyy` (NOT `graphify`). CLI binary IS `graphify`. Easy to typo the install command.

- **Output directory is not configurable.** Graphify writes to `<cwd>/graphify-out/` and has no `--output-dir` flag. The wrapper must either (a) run `graphify update` from a controlled directory and `mv graphify-out/* .acw/codemap/`, (b) symlink `graphify-out` to `.acw/codemap/`, or (c) run inside `.acw/codemap/` with the project root as an absolute path argument. Pick one and document per-instance.

- **Cache dir is `cache/`, not `.cache/`.** Earlier ACW canonical (pre-audit) wrote `.cache/` in several places — that was wrong. Graphify creates `cache/` (no leading dot) on first `update` run.

- **Stage 2 LLM is Gemini, not Claude.** Graphify's native semantic extraction calls Gemini (`GEMINI_API_KEY` or `GOOGLE_API_KEY`). The CLI prints a tip about this when keys are absent. The ACW operator's stack does not have Gemini by default; this is why `--semantic` is opt-in via `env_secrets` and AST-only is the default. The `implements_decision` bridge (ACW-specific) runs via Claude — that's a separate code path from Graphify's Stage 2.

- **`implements_decision` is ACW-specific, NOT Graphify-native.** Graphify reads docs (README, docstrings, comments) but knows nothing about ACW's `.acw/decisions/` convention. The bridge step is ACW-side code we build on top, writing to `acw-edges.json` sidecar. Per D-ACW-052.

- **`graphify claude install` is forbidden per C-005.** It writes a section into CLAUDE.md plus a PreToolUse hook, conflicting with ACW's "CLAUDE.md is a thin pointer" convention (D-ACW-047). The `/codemap` skill's pre-flight verifies CLAUDE.md integrity and refuses if a Graphify-managed block is present.

- **Profile gating is enforced.** `/codemap` refuses on profiles other than `coding-project` and `library` unless codemap is explicitly in `modules:`. Operators sometimes try to run codemap on spec-project instances — it correctly refuses.

- **AMBIGUOUS edges accumulating.** If `/codemap audit` repeatedly reports the same AMBIGUOUS edges, that's signal the operator needs to triage them (promote to EXTRACTED with explicit annotation, demote to INFERRED with score, or delete). Don't filter them silently.

- **Cache staleness across branches.** If the operator switches git branches with substantially different code, the file-level cache in `cache/` may carry stale entries. Force-rebuild by deleting `cache/` and re-running `graphify update`.

- **Single combined `graph.json`, not separate node/edge files.** Graphify writes one NetworkX directed-multigraph JSON. Earlier ACW canonical described a `nodes.json` / `edges.json` / `communities.json` split — that was a guess from secondary-source articles, not reality.

- **Wrapper authoring ready (2026-05-21).** Probe complete; CLI surface documented. Authoring `references/rebuild.md`, `status.md`, `audit.md` is the next discrete piece. Until shipped, `/codemap rebuild` exits with a "not yet implemented" message pointing at `references/implementation-plan.md`. Do not silently no-op.

- **Conflation with `/substrate-map`.** Operator may invoke `/codemap` expecting cross-reference navigation across substrate (decisions/glossary/incidents). That's `/substrate-map`. `/codemap` covers source code structure, not substrate. Both compose; neither replaces the other.
