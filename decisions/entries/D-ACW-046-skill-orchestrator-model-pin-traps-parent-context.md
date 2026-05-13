---
id: D-ACW-046
title: "Skill orchestrator model pin traps parent context — drop from /acw-session"
date: 2026-05-13
status: accepted
kind: decision
tags: [skill-format, model-routing, context-window, acw-session]
updated: 2026-05-13
---

# D-ACW-046 — Skill orchestrator model pin traps parent context — drop from /acw-session

**Date:** 2026-05-13

**Decision:** Remove `model:` frontmatter from `skills/acw-session/SKILL.md`. Orchestrator skills that run inline (i.e., not as isolated subagents) MUST inherit the parent session model. Pin `model:` ONLY on subagent definitions (e.g., `.claude/agents/session-end-judgment.md`) where context is freshly bounded by the harness.

**Rationale:** `/acw-session` declared `model: claude-sonnet-4-6` in SKILL.md frontmatter. When invoked from an Opus 1M session at ~300k tokens, the harness routed the skill to Sonnet, which rejected the prompt with "Prompt is too long" — Sonnet's window is 200k. The pin caused a context-window trap: the parent conversation's context is inherited by the inline orchestrator, but capped by the pinned model's window.

This reframes the `model:` field for orchestrators. It was previously treated as a cost knob ("run the cheap model where judgment isn't needed"). The Opus-1M-session incident showed it is also a window cap. For orchestrators that run inline, the cap is load-bearing in a bad way; for subagents that get a fresh bounded prompt, the cap is fine.

**Earned-by-incident:** single-incident emergency promotion. The failure was structural (skill unusable in any session that exceeds the pinned model's window) and the prevention is trivial (drop the field). Sonnet escalation for Phase 3/5 judgment work is preserved — those run as subagent dispatches per `references/end.md`, where the prompt is bounded.

**Generalization:** This applies to every orchestrator skill, not just `/acw-session`. `/acw-instance` already had no `model:` pin and is unaffected. Any future orchestrator authored in ACW canonical or derived instances should follow the same rule.

Future doctrine for `rules/skill-format.md` (not yet written here; earn when a second orchestrator hits the same trap):

> Orchestrator skills (skills with `role: orchestrator` that run inline rather than as isolated subagent dispatches) MUST NOT declare a `model:` field in frontmatter. They inherit the parent session model. Pin `model:` ONLY on subagent definitions where the prompt is fresh and bounded.

**Edit discipline:** pattern A. Single-line frontmatter edit; operator-confirmed; this entry is the durable receipt.

**Source:** Operator session 2026-05-13. After the v0.9.6 ship, `/acw-session` invocations failed repeatedly with "Prompt is too long". `/compact` restored functionality, confirming the issue was context size, not skill bundle. Operator's question: *"but we were at 300k token and using 1m opus. do you think its because the skill uses sonnet?"* — pinpointed the model-pin as the trap.

**Risks:**

- **Risk: inheriting Opus on a routine skill invocation is more expensive than Sonnet.** Mitigation: the orchestrator does little reasoning of its own (it dispatches to references and subagents). Token cost of the orchestrator itself is small. Heavy reasoning is already routed through the Phase 3/5 subagent which still uses Sonnet. Net cost difference is negligible.
- **Risk: future orchestrators forget the rule and re-introduce a `model:` pin.** Mitigation: a lint rule for `skills/*/SKILL.md` checking `role: orchestrator` rows for absent `model:` would be earn-by-incident; not shipped here.

**Open follow-ups:**

- **Codify in `rules/skill-format.md`.** Add the orchestrator-no-model-pin rule when a second orchestrator hits the same trap. Currently single-incident; rule prose deferred.
- **Audit other orchestrator skills across downstream instances.** Doctrine flows via `/acw-instance upgrade` once codified. Until then, manual check at next upgrade pass.
