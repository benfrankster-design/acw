---
id: D-ACW-052
title: "Codemap integration: ACW auto-load wins; Graphify treated as internal AST engine"
date: 2026-05-21
status: accepted
kind: decision
updated: 2026-05-21
supersedes: []
related_to:
  - id: D-ACW-047
    confidence: EXTRACTED
  - id: D-ACW-050
    confidence: EXTRACTED
---

# D-ACW-052 — Codemap integration uses ACW auto-load, not graphify claude install

## Decision

The `/codemap` skill wraps Graphify but does NOT use Graphify's native `graphify claude install` integration. Instead:

1. **Auto-load via ACW's mechanism.** `.acw/codemap/GRAPH_REPORT.md` is registered in `acw-state.yaml::auto_load_at_session_start` per the coding-project / library profile defaults. The SessionStart hook (`.claude/hooks/load-context.py`) reads it like every other substrate module. One mechanism for everything: decisions INDEX, glossary INDEX, tasks-status, rules, codemap report — all load the same way.
2. **CLAUDE.md stays thin.** Per D-ACW-047, `CLAUDE.md` is a one-line pointer to `AGENTS.md`. `graphify claude install` (which writes a section into CLAUDE.md plus a PreToolUse hook) is NOT run on any ACW instance. C-005 codifies this as stop-work.
3. **AST-only is the default.** Graphify's Stage 1 (Tree-sitter AST extraction) is free, deterministic, and sufficient for most navigation needs. The `/codemap rebuild` default invocation runs AST-only via `graphify update <project-root>`.
4. **Graphify's Stage 2 (Gemini) is opt-in via env_secrets.** Instances that want native semantic extraction declare `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in `acw-state.yaml::env_secrets`. The operator supplies the value via per-instance `.env` (gitignored) or operator shell env. Skill reads from `os.environ`, refuses cleanly if the declared secret is missing.
5. **ACW-specific `implements_decision` bridge runs via Claude.** The semantic linkage that matters most to ACW — connecting code symbols to decision entries — runs through the Anthropic SDK (already in the operator's stack), not Graphify's native Stage 2. Walks `.acw/decisions/entries/*.md`, scans graph nodes for symbol mentions in docstrings/comments/rationale, emits `implements_decision` edges as a sidecar (`.acw/codemap/acw-edges.json`) or merged into `graph.json`.
6. **Treat Graphify as an internal AST engine, not a co-equal integration partner.** User-facing surface is `/codemap` (ACW skill). `graphify` (CLI) is delegated to internally. Operators do not invoke `graphify` directly in normal workflows.

## Rationale

**One mechanism for everything.** ACW already has a single, declarative auto-load contract (`acw-state.yaml::auto_load_at_session_start` consumed by the SessionStart hook). Adding a parallel mechanism via `graphify claude install` would split the load-bearing convention. Two paths to do the same thing creates drift, confusion, and a second place to debug when auto-load misbehaves.

**Thin pointer convention is load-bearing.** D-ACW-047 made CLAUDE.md a one-line pointer specifically to eliminate the drift surface between hardcoded `@`-imports and the manifest. `graphify claude install` would reintroduce drift by writing a Graphify-managed block into CLAUDE.md. That block would compete with ACW's manifest for ownership of the file's content.

**Codebase shape changes slowly.** Session-start loading is fresh enough. The PreToolUse hook approach (re-evaluating the graph mid-session) is overkill for the actual change cadence and adds runtime cost we don't need.

**ACW's value-add is the decision bridge, not the AST.** The differentiator between ACW codemap and raw Graphify is that ACW's substrate (`decisions/`) is semantically linked to code. Using Graphify's Gemini Stage 2 for this would route ACW substrate through Gemini and then mix it with Graphify's general semantic edges. Running the bridge via Claude (already in the ACW operator's stack) keeps the bridge step under ACW control, uses the API the operator pays for anyway, and produces edges that follow ACW's confidence-tagging discipline directly.

**Operator framing:** "This is ACW, not Graphify. We're using Graphify concepts and making it our own." Adopting Graphify's CLAUDE.md integration would reverse that — it would bend ACW shape to Graphify's idea of how to surface a codemap to Claude Code. The correct direction is: Graphify is a library we call; ACW owns the surface.

## What this means concretely

- `skills/codemap/SKILL.md` documents the wrapper's job as: profile-gate, run `graphify update <project-root>`, relocate `graphify-out/*` to `.acw/codemap/`, optionally run the `implements_decision` bridge via Claude.
- `rules/codemap.md` is rewritten to reflect AST-only default + opt-in Stage 2 + ACW-bridge-via-Claude.
- `rules/instance-current-manifest.md` gains an `env_secrets` block in the recommended-blocks registry (earned in v0.10.1). Schema: `name`, `required_by`, `when`, `notes`.
- The `tools/templates/acw-state.yaml.tmpl` scaffolds an `env_secrets:` block (commented out by default).
- `graphify hook install` (post-commit hook) is NOT used. Rebuilds happen on-demand via `/codemap rebuild`.
- `graphify claude install` is NEVER run. C-005 enforces stop-work.

## Counterarguments (considered and rejected)

**"Use Graphify's claude install for less work."** Rejected. The work saved is trivial (~10 lines of hook code). The drift surface added is significant (a parallel auto-load mechanism that owns part of CLAUDE.md).

**"Run Graphify's Gemini Stage 2 as the default semantic layer."** Rejected. (a) Operator does not have a Gemini API account; running by default would silently fail or require additional setup. (b) The semantic edges that matter most to ACW (code-to-decision) are not Graphify's strength; they're ACW's purpose. (c) Running ACW substrate through Gemini routes ACW data to a vendor not already in the operator's stack.

**"Run the implements_decision bridge as a Graphify plugin."** Rejected. Graphify's plugin model is not designed for ACW-shaped substrate (decisions, constraints, open-questions). Building a Graphify-side plugin would couple ACW to Graphify's release cadence and plugin API. A Python script in `skills/codemap/` that reads `.acw/decisions/entries/` and the produced `graph.json` is portable, debuggable, and under ACW's own control.

## Consequences

- `/codemap` skill ships with a clear, narrow contract. The wrapper is much thinner than originally planned.
- C-005 enforces stop-work on any Graphify content in any instance's CLAUDE.md.
- `env_secrets:` becomes a recommended block in v0.10.1; documented in `rules/instance-current-manifest.md`.
- Stage 2 native (Gemini) is available to instances that explicitly opt in via env_secrets. Default behavior never touches Gemini.
- `implements_decision` bridge is the semantic value-add. Authored in v0.10.1 alongside wrapper.

## Cross-references

- Companion to D-ACW-047 (CLAUDE.md thin pointer).
- Companion to D-ACW-050 (.acw/ dotfolder + instance types + codemap module).
- Authority for C-005 (no Graphify content in CLAUDE.md).
- Audit source: `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md`.
- Session source: `.acw/sessions/2026-05-21--graphify-probe-and-codemap-audit.md`.
