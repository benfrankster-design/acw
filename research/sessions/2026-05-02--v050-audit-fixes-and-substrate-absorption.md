---
date: 2026-05-02
participants: [operator, agent]
topic: v0.5.0 audit fixes and substrate absorption
decisions_made:
  - D-ACW-023
  - D-ACW-024
  - D-ACW-025
  - D-ACW-026
  - D-ACW-027
  - D-ACW-028
  - D-ACW-029
conceptual_shifts: yes
linked_files:
  - rules/skill-format.md
  - rules/multi-instance-topology.md
  - rules/instance-current-manifest.md
  - rules/manifest-discipline.md
  - acw-state.yaml
  - tools/templates/acw-state.yaml.tmpl
  - tools/templates/integrations-README.md.tmpl
  - tools/manifest.py
  - tests/test_manifest.py
  - skills/acw-instance/SKILL.md
  - skills/acw-instance/references/audit.md
  - skills/acw-instance/references/upgrade.md
  - skills/acw-instance/gotchas.md
  - skills/acw-session/SKILL.md
  - skills/acw-session/references/start.md
  - skills/acw-session/references/end.md
  - skills/acw-session/gotchas.md
  - integrations/README.md
  - runbooks/.gitkeep
  - briefings/.gitkeep
  - _buffer/2026-04-30-gsg-copilot-instance-extensions.md
  - _buffer/2026-05-01-cs-copilot-rename.md
  - CLAUDE.md
  - decisions/decision-log.md
  - tasks-status.md
  - build-log.md
duration_minutes: 180
---

# v0.5.0 — audit verb fixes and substrate absorption

## 1. Topic & Goal

The session opened with the operator pasting the first real `/acw-instance audit` output from `_Command` (run in a separate terminal session earlier in the day, immediately after v0.4.0 shipped). The audit ran cleanly at the surface — produced a routing table, identified canonical-shape and divergent files, surfaced 6 organic substrate findings — but exposed five bugs in v0.4.0 that prevented the verb from doing its actual job. Goal: fix the bugs, absorb the universal patterns the audit surfaced (briefings/, runbooks/, integrations/), and ship v0.5.0.

A secondary thread emerged mid-session about how to think about substrate categories generally — what counts as universal vs cockpit-specific, how the operator's task app and calendar relate to workspace substrate, what's the distinction between system inbox and operator inbox. That thread produced D-ACW-027 (the `_inbox/` → `_buffer/` rename) and informed the v0.6.0 scope queued for next session.

## 2. What was decided

- **D-ACW-023** — Hard-stop scan widened to count root-level organic substrate (briefings/, runbooks/, integrations/, custom-named directories) plus root-level non-canonical markdown files, in addition to the v0.4.0 logic that counted only `decisions/` and `rules/`. Threshold (default 5) applies to the total. The v0.4.0 scope missed exactly the case it was designed to catch — `_Command` had ~1 file each in `decisions/` and `rules/` (well under threshold) despite substantial organic substrate at root.
- **D-ACW-024** — Audit verb's Mode B walk made interactive: prompt per finding with the four-option route (`[a]/[b]/[s]/[n]`), write absorption candidates immediately on `[b]`, no static-report shortcut. Default routing changed from `[s] instance-specific` to "ask, don't guess" with explicit canonical comparison surfaced in the prompt.
- **D-ACW-025** — Reversed the `_Command` audit's verdict that `briefings/` is cockpit-specific. The pattern (agent-generated dated snapshot of aggregated state) is universal; only the aggregation content varies per workspace type.
- **D-ACW-026** — Retrospective on the `_Command` audit dogfood: v0.4.0 design was sound at the rule level but the verb had ambiguities and gaps that only surfaced under real-workspace use. Five bugs from one dogfood, all fixed in v0.5.0. Earn-by-incident loop closed.
- **D-ACW-027** — System cross-instance handoff directory renamed `_inbox/` → `_buffer/` per the operator's DIP vocabulary canon (which already declares "buffer" as the canonical term replacing inbox/queue/staging). Avoids collision with the operator-facing `inbox/` arriving in v0.6.0. Active substrate updated; append-only history retains historical references.
- **D-ACW-028** — Calendar, tasks, email stay external; don't duplicate in workspace substrate. The chief-of-staff affordance ("what's on my plate?") lives in agents that call appropriate MCPs at query time. Briefings is the aggregation/snapshot mechanism when the operator wants a moment-in-time view.
- **D-ACW-029** — Three new substrate directories shipped as universal canonical: `runbooks/` (operator how-to docs), `integrations/` (external-system docs with templated README), `briefings/` (agent-generated dated snapshots). All earned by `_Command` absorption.

## 3. What changed in the conception

Several conceptual shifts:

- **Earn-by-incident isn't just for new primitives; it works for fixing existing ones too.** v0.4.0's audit verb had real architectural intent but the implementation didn't quite deliver. Five bugs from one dogfood. The right response was a fast v0.5.0, not a defensive rewrite of the spec to claim the bugs were "interpretation issues." Real fix: tighten the spec so the implementation can't drift, and document the bugs as the incident that earned the tightening.
- **Universal vs instance-specific isn't about role; it's about whether the pattern shape generalizes.** Initial `_Command` audit verdict marked briefings/runbooks/integrations as cockpit-specific. Operator pushed back: the *content* varies by workspace type, but the *pattern shape* is universal. Briefings work in cockpit (calendar+tasks+email), in project (PR+build+issues), in full/org-brain (cross-domain rollups). Same substrate, different aggregation. That distinction (shape vs content) is the right discriminator.
- **DIP vocabulary canon is operative, not just historical.** The operator's synapse global rules already declared "buffer" as the canonical term replacing inbox/queue/staging. ACW canonical wasn't honoring it. v0.5.0 brings ACW canonical inline. Vocabulary discipline beats path-stickiness.
- **Don't duplicate operator-accessible surfaces in workspace substrate.** Calendar lives in Google/Nextcloud/iCloud; tasks live in Todoist; email lives in Gmail/Outlook. All are accessible on phone and desktop via native apps. Mirroring locally creates sync rot. The right pattern: lean on MCP for live data; briefings aggregate for moment-in-time snapshots.
- **Cockpit isn't a role; it's a workspace type.** Operator clarified: leadership workspace IS cockpit. So is CS-agent's, developer's, designer's, anyone with both a job and personal life touching the same machine. Per `research/07-instance-types.md` the canonical types are Full/Cockpit/Project/Read-Only — leadership doesn't appear because it's not a separate type. Updated examples accordingly.

## 4. What was built / changed

**Three commits in v0.5.0, one push:**

**Commit 1 — `fix(skills): audit/upgrade verb fixes + _inbox/ -> _buffer/ rename`** (af1ba73)
- `skills/acw-instance/references/audit.md` rewritten with interactive Mode B walk, skills audit in spine, absorption flow for unregistered workspaces, default routing changed.
- `skills/acw-instance/references/upgrade.md` updated with widened hard-stop scope and v0.5.0 migration step (detects legacy `_inbox/`, proposes rename).
- `_inbox/` → `_buffer/` rename via `git mv` (preserves history of the two existing notification files).
- Active substrate updated: `acw-state.yaml`, `rules/multi-instance-topology.md`, `rules/instance-current-manifest.md`, `rules/manifest-discipline.md`, `rules/skill-format.md`, all `skills/acw-instance/` files, all `skills/acw-session/` files, `CLAUDE.md`, `tools/manifest.py` canonical defaults, `tests/test_manifest.py`.

**Commit 2 — `feat: runbooks/, integrations/, briefings/ as canonical substrate`** (cf68dba area)
- New canonical directories: `runbooks/`, `integrations/`, `briefings/`.
- `integrations/README.md` rendered from new template `tools/templates/integrations-README.md.tmpl`.
- `runbooks/.gitkeep` and `briefings/.gitkeep` for empty directory scaffolding.
- `acw-state.yaml::empty_dirs` extended with `runbooks` and `briefings`; `instance_layer` extended with `integrations/README.md`.
- `rules/instance-current-manifest.md` adds three new registry entries earned in v0.5.0.
- `rules/manifest-discipline.md` and `tools/manifest.py` add canonical default paths for `runbooks_dir`, `integrations_dir`, `briefings_dir`.
- `tools/templates/acw-state.yaml.tmpl` baseline `last_reconciled_version` bumped to `0.5.0`.
- Scaffolder dry-run verified produces correct shape.

**Commit 3 — `chore(v0.5.0): housekeeping`** (6320270)
- `acw-state.yaml::version` and `last_reconciled_version` → `0.5.0`.
- `decisions/decision-log.md` adds D-ACW-023 through D-ACW-029 (seven entries).
- `tasks-status.md` Pending updated for v0.6.0 + re-dogfood task; Done block for Session 8.
- `CLAUDE.md` "Where things live" extended with runbooks/integrations/briefings entries.
- Build-log entry narrating the session arc and the metabolize report.

Push to `origin/master` succeeded: `192d9d5..6320270`.

## 5. Open questions left — structured

#### OQ-ACW-008 — How does the operator-facing `inbox/` (v0.6.0) relate to `tasks-status.md` and `briefings/`?

**Question:** v0.6.0 will introduce `inbox/` as the operator's untriaged-items surface. Items there get routed into either `tasks-status.md::Pending` (workspace tasks), parked, or deleted. But the chief-of-staff briefings will also surface things — calendar items, email summaries — that look like "stuff to act on." Is the right model: briefings READ-ONLY surface state aggregations that the operator scans; inbox is the WRITE surface for operator-captured triage items? Or do briefings sometimes trigger inbox items (e.g., briefing surfaces "Heather's email needs response," which becomes an inbox item to triage)?

**Candidates considered:**
- **Strict separation** — briefings are read-only summaries; never write to inbox. Operator manually creates inbox entries when they see something in a briefing they want to track.
- **Briefing → inbox routing** — briefing skills can write items into inbox when they detect actionable surfaces (unanswered emails, urgent calendar, etc.). Operator triages from inbox.
- **Inbox-as-overflow** — briefings hold the canonical aggregation; inbox is for things that don't fit a briefing template (random captures, mid-session "remember this," etc.).

**Why unresolved:** Needs lived experience. The right answer depends on how the operator actually uses briefings — as a passive snapshot or as an active queue. v0.6.0 ships inbox/ without yet committing to a briefing-routing pattern.

**Who needs to weigh in:** Operator after running a few daily-briefing cycles in a cockpit instance.

#### OQ-ACW-009 — Should briefings be configured per workspace type, or per workspace?

**Question:** Briefings is universal in *shape*, but the *content* varies by workspace type — cockpit aggregates calendar+tasks+email; project aggregates PR+build+issues; full/org-brain aggregates cross-domain rollups. Where does the per-type configuration live? Three options: (a) hardcoded in briefing skills (each skill knows its workspace type and aggregates accordingly), (b) declared in `acw-state.yaml::briefing_aggregations` (operator-configurable per instance), (c) inferred from `acw-state.yaml::project::domain` (skill detects domain and picks aggregation pattern).

**Candidates considered:**
- (a) Simplest. Each briefing skill (e.g., `daily-briefing-cockpit`, `daily-briefing-project`) knows its template. Operator picks the skill that fits. Friction: two operators with similar setups but different domain emphases need to fork the skill.
- (b) Most flexible. `acw-state.yaml` declares which sources to aggregate. Skill is generic. Friction: more operator config burden upfront.
- (c) Cleanest if `project::domain` is reliable as a signal. Friction: domain is operator-supplied free text; agents can't reliably classify "what aggregation does 'consulting-services' want?"

**Why unresolved:** No briefing skills shipped yet in ACW canonical; this only matters when the first ones do. Defer to v0.7.0 or beyond.

**Who needs to weigh in:** Operator after at least one briefing skill is shipped and dogfooded.

## 6. Operator directives (verbatim)

> "It sent nothing to your inbox." (turn ~5)
> — The single-sentence observation that exposed the static-report-vs-interactive-walk bug. Pointing at exactly what was wrong without diagnosing it; the diagnosis fell out from there.

> "Don't you suggest what different kinds of notes a user like me would want to have, not just in a cockpit but in a project, in a coding project, in a leadership project and job role project?" (turn ~12)
> — Forced the per-workspace-type substrate-defaults framing that became D-ACW-029's discriminator.

> "Why didn't it include briefings, runbooks, and integrations in the absorption signal. Do you think those would be ideal upgrades to ACW? Why or why not?" (turn ~12)
> — Pushed back on the audit's conservative verdict. Right call. Two of three (runbooks, integrations) are universal; the third (briefings) is also universal once correctly framed.

> "Should the system inbox be called Inbox or Buffer? Just because I don't want to confuse the two." (turn ~16)
> — Surfaced the rename. Right reasoning; matches the operator's existing DIP vocabulary canon.

> "Don't worry about the notes one for now. Definitely let's add runbooks. Let's also absorb integrations, but we don't need to worry about what the subfolders are for now. You just put placeholders. Honestly, you don't even need to put placeholders there. Maybe just a README that explains this is the place for integrations, which could be APIs, could be MCPs, adapters, whatever." (turn ~18)
> — Locked the integrations/ shape as README-with-no-subfolder-structure. Cleaner than my initial template-everything proposal.

> "I think I'm going to go with that same advice for my tasks as well. I think it's probably just best that the operator use a task app." (turn ~20)
> — Extended the calendar-stays-external logic to tasks. Same reasoning. Both stay external; briefings is the aggregation surface.

> "Let's go cockpit versus project workspace, because leadership workspace really is a cockpit. Let's not just limit it to leadership." (turn ~22)
> — Reframing correction: cockpit is workspace type, not role. Per `research/07-instance-types.md`, leadership doesn't appear; it's just one operator's cockpit.

## 7. Cleaned transcript excerpt

Skipped — substantive content captured in §2-§6. The session was design-conversation-heavy; the operator's directives in §6 carry the wording that mattered.
