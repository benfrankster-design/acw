---
date: 2026-05-13
topic: v0.9.6 wiki migration + /acw-session model-pin fix
status: complete
---

# Session 2026-05-13 — v0.9.6 wiki migration + /acw-session model-pin fix

## 1. Topic

Bundled ship: v0.9.6 wiki migration doctrine flip (archives re-split into wiki), `/acw-session` redundancy refactor mirroring D-ACW-044's `/acw-instance` work, plus a follow-on fix for `/acw-session` failing "Prompt is too long" on Opus 1M sessions.

## 2. Decisions made

- **D-ACW-045** — v0.9.6 ship: wiki migration re-splits archives + `/acw-session` redundancy refactor. (Already written this session.)
- **D-ACW-046** — Skill `model:` frontmatter on orchestrators traps parent context inside the pinned model's window. `/acw-session` had `model: claude-sonnet-4-6`; at 300k Opus 1M context it overflowed Sonnet's 200k window. Fix: drop `model:` pin from orchestrator SKILL.md so it inherits the parent session model; keep Sonnet escalation scoped to the Phase 3/5 judgment subagent where context is isolated.

## 3. Conceptual shifts

- **Skill `model:` pin is a context-window trap, not just a cost knob.** Previously we thought of `model:` as choosing the cheapest model that could do the job. The Opus-1M-session failure showed it also caps the inherited conversation context to that model's window. Orchestrators that run inline (not as isolated subagents) should leave `model:` unset and inherit the parent. Pin model ONLY on subagent definitions where context is freshly bounded.

## 4. Terms entered/shifted

- No new glossary terms; existing vocabulary stands.

## 5. Tasks completed / started

Completed this session (and earlier today):
- v0.9.6 doctrine flip shipped (wiki migration re-splits archives).
- Q2 archive re-split into wiki entries; `decisions/decision-log-2026-Q2.md` deleted.
- `/acw-session` redundancy refactor: 7 sites collapsed to rule/state-file pointers.
- `tools/migrate_to_wiki.py --archive=<path>` flag added.
- `rules/substrate-boundary.md` shipped + registered (D-ACW-044).
- Skill model-pin fix: dropped `model:` from `skills/acw-session/SKILL.md`.

No new pending tasks.

## 6. Hard-rule changes

None.

## 7. External sources cited

None.

## 8. Incidents

- **Skill orchestrator pinned to subagent model.** `/acw-session` SKILL.md declared `model: claude-sonnet-4-6`. On Opus 1M session at ~300k context, the harness routed the skill invocation to Sonnet, which rejected the prompt as oversized (Sonnet 200k window). Workaround: `/compact` reduced context below 200k so Sonnet accepted. Root fix: removed the `model:` pin so the orchestrator inherits the parent session model. Severity: medium (skill unusable in long sessions). Prevention: orchestrators that run inline inherit parent; only subagent definitions pin model.

## 9. Unresolved questions

None blocking. Open follow-ups already cataloged in D-ACW-045.

## Updates
