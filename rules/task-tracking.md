---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Task Tracking

Every ACW instance maintains a `tasks-status.md` at the repo root tracking active work. Distinct from `decisions/decision-log.md` (settled choices) and `incidents.jsonl` (forensic events). Tasks are *units of work*; decisions are *settled choices*; incidents are *evidence*.

## What `tasks-status.md` tracks (workspace-purpose, not operator-personal)

`tasks-status.md` tracks **the workspace's purpose-tracker** — work items that advance what this workspace is for. It adapts to its workspace type:

| Workspace type | What `tasks-status.md` holds |
|---|---|
| **Cockpit** | Workspace configuration + chief-of-staff operations. *"Configure the new Slack MCP, set up daily briefing skill, run weekly metrics review."* |
| **Project** | Project deliverables. *"Ship feature X, fix bug Y, complete migration Z."* |
| **Full / org-brain** | Org-level coordination work. *"Promote departmental pattern A to org-brain, retire deprecated taxonomy B."* |

What `tasks-status.md` does **NOT** hold:

- **Operator's personal life tasks** — *"pick up kids, doctor's appointment, call mom."* These live in the operator's external task app (Todoist, Reminders, etc.), not in workspace substrate. Mirroring tasks locally creates sync rot; the operator already has them on their phone.
- **Calendar events** — same logic. Calendar lives in Google/iCloud/Nextcloud; never mirrored to workspace substrate. When a snapshot is wanted, briefing skills aggregate calendar + workspace state into a `briefings/` artifact at generation time.
- **Email** — same logic. Email lives in Gmail/Outlook; never mirrored.

The general rule: **don't duplicate operator-accessible-on-phone surfaces in workspace substrate.** Lean on MCP integrations for live data; lean on briefings for moment-in-time aggregations.

The operator's `inbox/` (v0.6.0) is the workspace-side capture surface for items the operator wants to triage *into* `tasks-status::Pending` or `inbox/ideas/`. It's an inbound-funnel; tasks-status is the committed-work outcome.

## File location

`tasks-status.md` at the repo root. Auto-loaded at session start (see `acw-state.yaml::auto_load_at_session_start`).

## Pending-only (v0.9.3+ canonical shape)

**One section. No Done. No Parked.** Per the absorbed proposal from _Command 2026-05-12: tasks-status is the live work queue. Completed work archives on completion (no interval cadence). Deferred-but-keep ideas route to `inbox/ideas/` or earn a decision-log entry. Truly stale items die in conversation.

```markdown
## Pending

🔬 [FIRE AT NEXT SESSION START] Run `/deep-research` against `research/queries/2026-04-30-async-design.md` — answers Track A unresolved questions from prior session.

- **Build the X subsystem** — context + acceptance criteria
- **Investigate Y crash** — context
```

The pinned-marker convention cues the next session what to fire first. `/acw-session start` reads the top of Pending to surface fire-tasks.

## Done — archive on completion (no interval cadence)

When a task is completed:

1. **Move it out of `tasks-status.md` immediately** as part of the session that completed it. The completed task does not sit in `tasks-status.md` waiting for a weekly archive sweep.
2. **Land it in `archives/tasks-status/YYYY-MM.md`** (current month) under that session's dated block. Append-only; never edit past entries.
3. **`/acw-session end` Phase 2** writes the session block to the archive file, not to a Done section in the live file.

Archive file convention (v0.9.5+):
- Path: `archives/tasks-status/YYYY-MM.md` — dedicated folder; one file per calendar month.
- Frontmatter: `class: archive, authority: derived, stability: stable, loaded_by_agent: no`.
- Registered in `acw-state.yaml::meta_layer`.
- Monthly rotation: new calendar month → new file. No size threshold; each month rolls cleanly.
- Pre-v0.9.5 grandfathered shape: `tasks-status-YYYY-Q*.md` at workspace root (quarterly). Existing instances may carry both; new archives go into the monthly folder shape.

Session-block format inside the archive:

```markdown
### YYYY-MM-DD — [topic phrase] (Session N)

- Built X (decisions/decision-log.md::D-NP-007 in single-file mode, or decisions/entries/D-NP-007-... in wiki mode)
- Added HR-NP-002 forbidding writes to read-only/
- Captured session: sessions/YYYY-MM-DD--topic-slug.md
```

**Why archive on completion (no interval):** the prior rolling-window-cadence pattern (`tasks-status.md::Done` accumulates for 7 days, then archives) was the wrong abstraction. Done is not a work-queue state; it's a write-once historical entry. Live file should never carry completed work. Archiving on completion is the simpler primitive and removes a category of "is this stale enough to archive yet" judgment from `/acw-session end`. Empirically: _Command hit "Prompt is too long" twice in a week (2026-05-11 and 2026-05-12) partly because Done sat in the live file even with weekly cadence.

## Parked — retired (v0.9.3+)

The Parked section is no longer maintained. Two replacement surfaces for deferred-but-keep ideas:

1. **`inbox/ideas/`** — wiki-shaped (one file per idea, frontmatter `type: idea, status: parked, date: YYYY-MM-DD`). Already canonical per v0.6.0+. Items here load on demand, not at session start.
2. **`decisions/decision-log.md`** (or `decisions/entries/` in wiki mode) — if the deferral itself is architectural (we considered X and decided not to do it now), it's a decision, not a parked idea. Log it.

**Why retire Parked:** the prior Parked section accumulated long-tail ideas with no review cadence and no consumer. Most entries never came back into scope. The ones that mattered should have been ideas (`inbox/ideas/`) or decisions (decision-log) all along. The middle category was a holding pattern that bloated `tasks-status.md` without earning a load slot.

Existing Parked content at retirement time archives in place inside the archive file's final Parked block — frozen, not active.

## Discipline

- **Pending → archive is a session-end action.** When a session completes a Pending item, `/acw-session end` Phase 2 writes the dated session block to the archive file *and* removes the item from `tasks-status.md::Pending`. Not separate edits.
- **Never edit past archive entries.** Archive is append-only, dated. Old session blocks are historical record.
- **Pinned markers go at the top of Pending.** Visual convention: emoji or `[FIRE AT NEXT SESSION START]` tag.
- **New deferred ideas → `inbox/ideas/` or `decision-log`.** Not the live tasks-status.

## Why this is separate from decision-tracking

Decisions answer *what was chosen*. Tasks answer *what is being worked on*. A decision creates tasks; a task does not create a decision. The two files are MECE: a settled choice goes in decision-log, a unit of work goes in tasks-status.

## Relation to `/acw-session end`

Phase 2 writes the dated archive block to `archives/tasks-status/YYYY-MM.md` (current month). Phase 2 also removes completed items from `tasks-status.md::Pending`. The skill never edits past archive blocks. Pre-v0.9.5 grandfathered files (`tasks-status-YYYY-Q*.md` at workspace root) remain valid for read; new writes land in the monthly shape.

## Relation to `inbox/` (operator capture surface)

`inbox/` is the operator's untriaged-items surface. Items there get triaged into one of:

- `tasks-status.md::Pending` — committed workspace work.
- `inbox/ideas/` — deferred-but-keep ideas (the replacement for the old Parked section).
- The operator's external task app — personal life tasks (not workspace substrate).
- Deleted — not actually a task.

Triage is operator-driven (or triage-skill-driven where applicable). `tasks-status.md` is the committed-work outcome of that triage; `inbox/` is the inbound funnel. Items don't live in `inbox/` long-term; they get processed and removed.

## Migration from pre-v0.9.3 instances

Instances on the three-section shape (Pending / Done / Parked) migrate as follows:

1. Move existing Done content to `archives/tasks-status/YYYY-MM.md` archive files (split by month if the source spans multiple).
2. Move existing Parked content to the relevant month's archive as a final Parked-frozen block. Cherry-pick anything still active into `inbox/ideas/` (with `type: idea, status: parked, date:` frontmatter) or the decision-log (if architectural).
3. Rewrite `tasks-status.md` to Pending-only.
4. Update local rules mirror if the instance carries one.
5. Log the migration in the decision-log.

`_Command` migrated 2026-05-12 (D-CMD-030).

## v0.9.5+ archive-folder migration

Pre-v0.9.5 instances on the root-level quarterly shape (`tasks-status-YYYY-Q*.md` at workspace root) migrate as follows:

1. `mkdir -p archives/tasks-status/`.
2. Split each quarterly archive into per-month files (`archives/tasks-status/YYYY-MM.md`) by entry date. If the operator prefers, the existing quarterly file may be grandfathered as `archives/tasks-status/YYYY-Q*.md` (kept whole, moved into the folder); only new writes go into the monthly shape.
3. Remove the root-level archive files; update `acw-state.yaml::meta_layer` to point at the new paths.
4. Update any pointer line in the live `tasks-status.md` preamble.
