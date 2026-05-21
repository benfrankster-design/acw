---
id: D-ACW-042
title: "v0.9.1: bi-weekly rolling-window discipline for decision-log; doctrine completion + global synapse trim"
date: 2026-05-05
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-042 — v0.9.1: bi-weekly rolling-window discipline for decision-log; doctrine completion + global synapse trim

**Date:** 2026-05-05

**Decision:** Five changes ship together as v0.9.1, a doctrine-completion patch on v0.9.0:

1. **`rules/decision-tracking.md`** gains a "Rolling-window discipline" section parallel to the v0.9.0 addition in `rules/task-tracking.md`. Cadence: **bi-weekly** (every two weeks). Mechanism: entries dated > 14 days old archive to `decisions/decision-log-YYYY-Q*.md` (meta_layer, frontmatter `class: archive, authority: derived, stability: stable, loaded_by_agent: no`). Replace archived content in the live file with a one-line pointer. Threshold trigger from `rules/auto-load-discipline.md` (~15k tokens) is the secondary fire condition: archive aggressively whenever the live file crosses threshold even if entries are < 14 days old. Open Questions, Constraints and Gotchas, and Resolved Questions sections do not archive — they're active surfaces, not historical narrative.

2. **`rules/task-tracking.md`** rolling-window section updated: cadence aligns to **bi-weekly** (was "Sessions ≥ N-2"). The session-count heuristic was a v0.9.0 placeholder when the cadence question was unresolved; bi-weekly gives a clean date-based cutoff that works across both decision-log and tasks-status under one rule shape. Archive file pattern unchanged (`tasks-status-YYYY-Q*.md`).

3. **`rules/auto-load-discipline.md`** caveats updated: both `decisions/decision-log.md` and `tasks-status.md` canonical-recommendation caveats now reference the bi-weekly cadence and point at the appropriate tracking rule for the mechanism.

4. **`rules/instance-current-manifest.md`** gains a new earned-in-0.9.1 entry for `decision-log-YYYY-Q*.md` archive shape; existing tasks-status archive entry text updated to bi-weekly cadence (earned-in-0.9.0 unchanged).

5. **ACW substrate split applied:** entries D-ACW-034 down through D-004 (dated 2026-04-30 to 2026-05-02) moved to `decisions/decision-log-2026-Q2.md`. Live file retains D-ACW-035 onward (8 entries inline). Archive file added to `acw-state.yaml::meta_layer`. **Companion global-layer trim:** moved six ACW-canonical duplicates from `~/synapse/Rules/` (auto-loaded globally via the `~/.claude/rules` junction) to `~/synapse/Reference/acw-canonical/` (sibling, not auto-loaded). ~85k off global memory load on every workspace, every session. Files moved: `instance-current-manifest.md`, `auto-load-discipline.md`, `Procedures/{skill-format, pipeline-roles, capability-broker, decision-tracking}.md`. Global `~/.claude/CLAUDE.md` Rules Index updated to reflect the new location. Five citation references in `cs-copilot/` now point at the old path; doc-only, fix-on-touch.

**Rationale:** The cost-friction incident from v0.9.0 (operator hit halfway through Max-plan weekly budget after 2 days) attacked the bookend's per-invocation cost. v0.9.0 then attacked the structural per-session-load cost via auto-load discipline. v0.9.1 closes two follow-on gaps surfaced this session:

- **Decision-log doctrine gap.** v0.9.0's `rules/auto-load-discipline.md` named the threshold for `decisions/decision-log.md` (~15k tokens) but pointed at `rules/decision-tracking.md` for the mechanism. That mechanism wasn't there — `decision-tracking.md` only described splitting into four files when the log gets too big to navigate. The threshold was canon; the rolling-window mechanism analogous to `task-tracking.md` v0.9.0 was missing. v0.9.1 adds it.

- **Global-layer bloat.** Operator screenshot showed 79.2k of memory files at session start, with synapse/Rules/instance-current-manifest.md (35.8k!) loading globally via the `~/.claude/rules` junction even when in non-ACW workspaces. The synapse copies were stale duplicates of ACW canonical (Pending item from v0.8.0). Moving them out of the auto-load path closes the bloat without losing reference access.

The unified bi-weekly cadence across decision-log and tasks-status closes a smaller doctrinal inconsistency: v0.9.0 used "Sessions ≥ N-2" for tasks-status (placeholder when the cadence question was unresolved); the underlying need is the same — keep the file lean, archive what's stale. Bi-weekly works as a date-based cutoff for both files under one rule shape.

**Source:** Operator session 2026-05-05 immediately after v0.9.0 ship. Operator surfaced context-budget bloat via screenshot showing 79.2k memory files. Operator quote: *"for the decisions doctrine Im noticing this is already a problem. lets do this bi-weekly actually (every two weeks) rolling window with the decision logs. and we were supposed to split tasks status. lets just do it now. make it canon so every instance gets the update."*

**Open follow-ups:**

- **Downstream propagation.** Doctrine flows to instances via `/acw-instance upgrade`: the new `rules/decision-tracking.md` section + revised `rules/task-tracking.md` cadence + revised `rules/auto-load-discipline.md` caveats land in template_layer; the v0.9.1 manifest registry entry surfaces drift on instances at `last_reconciled_version` < 0.9.1. The audit verb walks each instance's decision-log and tasks-status against the bi-weekly cutoff and proposes archive splits when entries exceed the window.
- **`tasks-status.md` rolling window for ACW already-applied (v0.9.0).** Sessions 12–14 inline are within the bi-weekly window (dates 2026-05-03 through 2026-05-05; today 2026-05-05). Bi-weekly cadence change is forward-looking; ACW's tasks-status doesn't need a re-split.
- **Cs-copilot citation refresh.** Five files in `~/projects/cs-copilot/` cite `~/.claude/rules/Procedures/{skill-format, capability-broker, decision-tracking}.md` paths that no longer exist post-trim. Citation-only, not load-bearing. Fix when cs-copilot is touched next.
- **v1.0.0 promotion timing.** Per operator directive in v0.9.0, nothing new ships before 1.0.0 promotion. v0.9.1 is a doctrinal patch completing v0.9.0 — does not extend scope, just closes specification gaps. Soak window continues.

**Risks:**

- **Risk: bi-weekly cutoff removes decisions in active reference.** Mitigation: the live file's pointer line names the archive file; agents reading recent decisions see the redirect immediately. Archive file is in `meta_layer` so it stays in the workspace; only loses auto-load.
- **Risk: cs-copilot stale citations.** Already noted. Doc-only.
- **Risk: synapse trim breaks downstream skill.** Already verified — the only references in the codebase are the five cs-copilot citations. No skill or script reads the moved paths programmatically.
