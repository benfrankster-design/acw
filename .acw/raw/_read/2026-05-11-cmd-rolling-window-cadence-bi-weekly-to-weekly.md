---
from_project: _Command
from_session_capture: ~/_Command/sessions/.current-session (2026-05-11)
date: 2026-05-11
topic: Rolling-window archive cadence tightened bi-weekly → weekly (tasks-status + decision-log)
read: true
absorbed_in: decisions/decision-log.md::D-ACW-043 (v0.9.3 bundle, 2026-05-12)
---

# Notification — Rolling-window archive cadence tightened from bi-weekly to weekly

**What happened.** Today's `_Command` session opened to a "Prompt is too long" error when invoking `/acw-session`. Diagnosis: auto-loaded substrate had grown to ~190 KB (tasks-status 112 KB + decision-log 54 KB + glossary 16 KB), which combined with global rules and the SessionStart summary blew past Claude Code's prompt limit before the skill could even fire. The previously-shipped v0.9.1 rolling-window discipline was working as designed (bi-weekly cadence; 14-day window) — but the cadence was mis-calibrated for `_Command`'s session density. The 5/05 archive run was 6 days ago and a second archive was already overdue. Threshold trigger (~15k tokens) had also tripped on decision-log without anyone noticing.

Operator directive: tighten the rule itself, not just run a one-off sweep.

**What changed in ACW canonical.** Doctrine edits applied to:

- `rules/task-tracking.md` — "bi-weekly" → "weekly"; "more than 14 days" → "more than 7 days"
- `rules/decision-tracking.md` — same swap; all bi-weekly references replaced
- `rules/auto-load-discipline.md` — caveat references updated for both `decisions/decision-log.md` and `tasks-status.md`
- `rules/instance-current-manifest.md` — both archive entries (`tasks-status-YYYY-Q*.md` and `decision-log-YYYY-Q*.md`) updated; "age past 14 days" → "age past 7 days"
- `acw-state.yaml` — `version: 0.9.1` → `0.9.2`, `last_reconciled: 2026-05-05` → `2026-05-11`, `last_reconciled_version: 0.9.1` → `0.9.2`

Threshold trigger (~15k tokens) preserved unchanged as the safety net.

**Why this matters for ACW canonical and other instances.** Two consumer-instance angles:

1. **Calibration was wrong for at least one instance.** `_Command` has high session density (multiple captures per day across operator + meeting + project work). The 14-day bi-weekly window protected too much historical narrative as load-bearing context. Other instances with lower session density (frank-context, cx-dashboard-saas) may not feel the friction yet, but the 7-day cadence is harmless for them — archive simply fires more often with fewer entries per run. No instance is worse off under the new cadence.

2. **First-ever decision-log archive run for `_Command` happened in the same session.** Per v0.9.1 doctrine, decision-log archive earns its first run when entries age past the window OR file exceeds ~15k tokens. Both conditions were tripped before the cadence change; the new 7-day cutoff just made the archive scope larger (15 entries: D-001..D-005 + D-CMD-001..D-CMD-010). Archive file `decisions/decision-log-2026-Q2.md` registered in `acw-state.yaml::meta_layer`.

**Numbers.**

- `_Command/tasks-status.md`: 112 KB → 46 KB (saved 66 KB)
- `_Command/decisions/decision-log.md`: 54 KB → 29 KB (saved 25 KB)
- Net auto-load relief: ~94 KB
- `/acw-session` fits now

**Absorption candidates for ACW canonical (beyond the doctrine edit already applied):**

1. **Add a cadence-friction telemetry signal.** When a session opens to "Prompt is too long" or when auto-loaded substrate exceeds some ceiling (say 150 KB), `/acw-session start` should surface this as a drift signal and propose an archive run before the operator hits the skill that broke. Today's incident was caught by the operator noticing the UI error, not by ACW.

2. **Re-evaluate the bi-weekly v. weekly default for new instances.** v0.9.2 ships weekly; the question is whether existing instances should migrate or whether bi-weekly is still right for low-density instances. Suggest: weekly is the default; instances with thin substrate (e.g., frank-context pre-engagement) can leave the cadence at bi-weekly in their local `rules/` override if it ever surfaces as friction.

3. **Symmetric archive registration check.** `_Command`'s `tasks-status-2026-Q2.md` was already in `acw-state.yaml::meta_layer`, but `decisions/decision-log-2026-Q2.md` had to be added by hand. `/acw-session end` Phase 2 (or `/acw-instance audit`) should propose meta_layer registration whenever an archive file appears at a known canonical path.

**Local decision-log entry:** `_Command/decisions/decision-log.md::D-CMD-024` — full rationale, rejected alternatives, execution details.

**Cross-references:**

- `Projects/acw/rules/task-tracking.md` (updated)
- `Projects/acw/rules/decision-tracking.md` (updated)
- `Projects/acw/rules/auto-load-discipline.md` (updated)
- `Projects/acw/rules/instance-current-manifest.md` (updated)
- `Projects/acw/acw-state.yaml` (version-bumped)
- `_Command/decisions/decision-log.md::D-CMD-024`
- `_Command/acw-state.yaml::meta_layer` (registered new decision-log archive)
