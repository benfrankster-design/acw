# Incidents Format — Phase 1 (identify) + Phase 2 (write)

`paths.incidents` is the project's append-only log of documented incidents. JSONL — one entry per line. Three downstream consumers:

1. **Earn-by-incident decisions.** Several rule files and skill templates use incident counts as threshold evidence (e.g., "X is parked until N=3 incidents document the gap"). Tracking incidents is how parked items become buildable items. See `rules/promotion-ritual.md`.
2. **Cross-cutting pattern detection.** Periodic synthesis reads incidents to find recurring root causes across multiple incidents.
3. **Project memory.** When something bit us once, capturing the lesson prevents the same mistake in a different shape later.

> **Path resolution.** `paths.incidents` resolves at runtime per the SKILL.md preamble. Schema authority lives in `rules/incident-tracking.md`; this document is the per-skill detection guide.

Per-line schema (defined in `rules/incident-tracking.md`):

```json
{"id":"<uuid>","timestamp":"<ISO8601 UTC>","primitive":"<name>","severity":"low|med|high","symptom":"<one-sentence summary>","operator":"<name>","category":"<category>"}
```

Required fields: `id`, `timestamp`, `primitive`, `severity`, `symptom`, `operator`. `category` is optional but strongly recommended. JSON encoding rules: ASCII-safe escapes, no embedded newlines (replace with `\n` if multi-line content is unavoidable).

## What counts as an incident

**Always log:**
- A bug that surfaced during build, smoke test, or eval and was fixed in the same session.
- A governance violation discovered (hard rule leak, scrub gap, lint failure that should have been caught earlier).
- An environment-state surprise that broke an assumed-stable substrate (e.g., venv lost packages between sessions).
- A wrong assumption that the session disproved (especially when the assumption was load-bearing for an earlier decision).
- A scale-vulnerability that surfaced before it bit production but should be tracked.
- An "earn-by-incident" pattern accumulating evidence — each occurrence is one incident even if no immediate fix lands.

**Sometimes log:**
- A near-miss where a guardrail caught something. (Log when the near-miss reveals a class of problem we should track. Skip when the guardrail is doing its job uneventfully.)
- A deferred-pattern observation. Log when it adds to the N-count for a parked item.

**Don't log:**
- Routine successes.
- Bugs in third-party code that were unrelated to project usage.
- Operator reasoning errors caught and corrected without consequence.
- Anything that's already a hard rule violation — those are stop-work events, not incidents to track.

## Category vocabulary

The seven canonical categories (defined in `rules/incident-tracking.md`):

| Category | What it covers |
|---|---|
| `implementation-bug` | Code defect surfaced during smoke test or eval; root cause + fix in same session |
| `governance-leak` | Hard rule violation found in project files |
| `environment-state` | Substrate or dependency state surprise (venv, .env, secrets, dev tunnel) |
| `wrong-assumption` | Earlier decision rested on a premise this session disproved |
| `scale-vulnerability` | Pattern that works at current scale but won't at 10x; documented before incident |
| `earn-by-incident` | Add-1 entry for a parked primitive's N-count |
| `process-gap` | Skill, runbook, or workflow missed a case the operator surfaced |

If a recurring pattern doesn't fit one of the seven, propose a new category via `rules/incident-tracking.md` (decision-log entry required).

## Writing rules

1. **One incident, one line.** Multi-issue sessions write multiple lines.
2. **Append-only.** Never edit past lines; if a prior entry was wrong, append a new one with `category: "wrong-assumption"` correcting it.
3. **Date is the date the incident happened.** If you're catching up on incidents from earlier, use the actual incident date, not today's date. Capture-and-metabolize fires at end-of-session so the dates line up by default; backfilling needs care.
4. **Symptom is factual, not narrative.** Write what happened, not what was felt.
5. **Lesson lives in a separate decision-log entry, not in the JSONL.** "Don't do X again" doesn't belong in the incident; "Codified in D-NNN" or "added HR-NNN" belongs in the decision log entry that references the incident id. The incident is the *evidence*; the decision is the *response*.

## Logging via tool

Use `tools/log-incident.py`:

```bash
python tools/log-incident.py log <primitive> <severity> "<symptom>" --category <category>
```

Tool returns the new uuid. Use that uuid when referencing the incident in decision-log entries.

## When in doubt

Log it. The cost of a redundant entry is one line. The cost of a missed entry is the same problem biting twice.
