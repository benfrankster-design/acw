---
id: D-ACW-037
title: "v0.8.0: bookend efficiency cluster (Haiku, subagent isolation, quick/full modes, /acw-session update verb, .current-session tracker, sessions/ at root, retire 4 superseded skills)"
date: 2026-05-04
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-037 — v0.8.0: bookend efficiency cluster (Haiku, subagent isolation, quick/full modes, /acw-session update verb, .current-session tracker, sessions/ at root, retire 4 superseded skills)

**Date:** 2026-05-04

**Decision:** Six changes ship together as v0.8.0:

1. `skills/acw-session/SKILL.md` declares `model: claude-haiku-4-5` in frontmatter. Phase steps that need real reasoning (Phase 3 operator-confirm proposals, Phase 5 research-prompt construction, meta-layer trigger proposed-edit text) escalate to Sonnet inline.
2. Bookend invokes a fresh subagent context to avoid inheriting the parent session's Opus 4.7 1M pricing.
3. `/acw-session end` defaults to **quick mode** (Phase 1 capture + minimal Phase 2 append-only writes + Phase 3 auto-update sweep). `full` argument runs all phases as previously documented. Phase 4 conditional on `--synapse` flag (quick) or `synapse_log_path` set (full); Phase 5 conditional on `--research` flag (quick) or operator confirmation (full).
4. New `/acw-session update` verb for mid-session checkpoints. Reads `.current-session`, appends timestamped note. Self-bootstraps if no tracker exists.
5. `paths.session_captures_dir` migrates from `research/sessions` to `sessions/` at root. Sessions are operational logs, not research artifacts. Existing capture files moved via `git mv`. `empty_dirs` swap.
6. The four superseded skills marked in `meta_layer` since v0.4.0 (`capture-session/`, `capture-and-metabolize/`, `resume-session/`, `upgrade-instance/`) are deleted from disk; their entries removed from `meta_layer`.
7. New `plans/` directory at workspace root for plan artifacts. Operational outputs from planning agents (or operator hand-written plans) save here as dated markdown (`plans/YYYY-MM-DD--<slug>.md`). Empty `.gitkeep` at scaffold time. New canonical default path `plans_dir: plans` in `acw-state.yaml::paths`. Convention only in v0.8.0 — no automatic writer skill; operator drops plans here manually. Earn-by-content reasoning: cheap to pre-create the directory; the writer skill earns its build only when convention demands automation.

**Rationale:** Operator session 2026-05-04 surfaced acute cost pressure — `/acw-session end` running 7-10 minutes per invocation on Opus 4.7 1M context, burning ~5-8M tokens per session, halfway through Max-plan weekly budget after 2 days. Cost-friction incident logged in `incidents.jsonl` this session. The bookend's work is overwhelmingly mechanical (read transcript, append to file, classify against manifest) — Haiku-grade in 80%+ of phases. Running mechanical bookend work at the most expensive Claude variant is structurally wrong. Quick mode collapses session-end to its append-only essentials, deferring expensive operator-interactive work to explicit `full` invocations at logical boundaries. The `update` verb closes a long-standing gap (binary bookend vs Ian Nuttall's session-update precedent) without paying full session-end cost. Sessions move to root because they are operational logs — `research/` is for design notes and queries. Superseded skill deletion closes a Pending item from v0.4.0 that the careful guardrail blocked from automated removal.

**Source:** Operator session 2026-05-04; deep-research note `research/11-session-continuity-prior-art.md` (Ian Nuttall claude-sessions precedent for `update` verb and `.current-session` tracker pattern; Anthropic Memory Stores filesystem-as-memory validation; ETH Zurich finding on hand-curated substrate); cost-friction incident logged this session.

**Open follow-ups:**

- **v0.9.0 — substrate earn-by-content refactor.** Scaffolder ships discipline floor only; bookend scaffolds substrate files on-demand when content earns them. Threshold table per content type to be argued through in `research/12-substrate-earn-by-content.md` (not yet written).
- **Future — `CLAUDE.md` becomes a thin pointer** ("see `AGENTS.md`"); `AGENTS.md` carries the substantive content currently in `CLAUDE.md` as the instance version of the file. Separate ship; not in v0.8.0 or v0.9.0.
- **Risk: `model:` frontmatter honored?** Field may not be honored by all Claude Code versions. If not honored, the skill still works at whatever model the harness picks; cost-cut is just smaller. No breakage.
- **Risk: quick mode defers operator-interactive work.** Manifest classification, host-entry-file maintenance, canonical-edit detection, meta-layer triggers, cross-repo writes, cross-project notifications accumulate until the next `/acw-session end full` runs them. Long stretches of quick-only mode could let substrate drift. Mitigation: audit verb catches structural gaps; operator instinct picks the heavy session.
- **Risk: self-bootstrap from `update` creates "untitled" capture files.** Mitigation: `end` always renames to topic-from-Phase-1; if operator never runs end, the file stays as-is, harmless.
