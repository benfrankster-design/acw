---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Task Tracking

Every ACW instance maintains a `tasks-status.md` at the repo root tracking active, completed, and parked work. Distinct from `decisions/decision-log.md` (settled choices) and `incidents.jsonl` (forensic events). Tasks are *units of work*; decisions are *settled choices*; incidents are *evidence*.

## File location

`tasks-status.md` at the repo root. Auto-loaded at session start (see `acw-state.yaml::auto_load_at_session_start`).

## Three sections

```markdown
## Pending

## Done

## Parked
```

### Pending

Active task queue. Newest pinned items at top with markers when they should fire at session start.

```markdown
## Pending

🔬 [FIRE AT NEXT SESSION START] Run `/deep-research` against `research/queries/2026-04-30-async-design.md` — answers Track A unresolved questions from prior session.

- [ ] Build the X subsystem
- [ ] Investigate Y crash
```

The pinned-marker convention cues the next session what to fire first. `/acw-session start` (or equivalent) reads the top of Pending to surface fire-tasks.

### Done

Append-only dated session blocks, newest first. Format:

```markdown
### YYYY-MM-DD — [topic phrase] (Session N)

- Built X (decisions/decision-log.md::D-NP-007)
- Added HR-NP-002 forbidding writes to read-only/
- Captured session: research/sessions/YYYY-MM-DD--topic-slug.md
```

Old entries are history. Do not collapse, edit, or remove them. If Done becomes long, archive to `tasks-status-YYYY-Q.md` via an explicit operator decision.

### Parked

Ideas surfaced during sessions but not earning a build. Each entry names what was parked and why. Parked items are intentionally deferred, not forgotten — never auto-remove.

```markdown
## Parked

- Idea: rebuild the runbook with a Mermaid diagram. Parked 2026-04-29 — current text version is sufficient until a reader complains.
```

## Discipline

- **Pending → Done is a session-end action.** When a session completes a Pending item, move it under that session's Done block, not as a separate line edit.
- **Never edit past Done entries.** Done is append-only, dated. Old session blocks are historical record.
- **Parked items are not stale.** Do not auto-archive Parked. Operator review only.
- **Pinned markers go at the top of Pending.** Visual convention: emoji or `[FIRE AT NEXT SESSION START]` tag.

## Why this is separate from decision-tracking

Decisions answer *what was chosen*. Tasks answer *what is being worked on*. A decision creates tasks; a task does not create a decision. The two files are MECE: a settled choice goes in `decision-log.md`, a unit of work goes in `tasks-status.md`.

## Relation to capture-and-metabolize

The session-end skill (`capture-and-metabolize` or equivalent) writes the dated Done block as part of Phase 2 distribution. The skill never edits past Done blocks. The skill never auto-removes Parked items.
