# Incidents Format — Phase 1 (identify) + Phase 2 (write)

`incidents.jsonl` is the project's append-only log of documented incidents. JSONL — one entry per line. Three downstream consumers:

1. **Earn-by-incident decisions.** Several `synapse/Rules/` files and skill templates use incident counts as threshold evidence (e.g., "X is parked until N=3 incidents document the gap"). Tracking incidents is how parked items become buildable items.
2. **Cross-cutting pattern detection.** `/synthesize-themes` reads `incidents.jsonl` monthly to find recurring root causes across multiple incidents.
3. **Project memory.** When something bit us once, capturing the lesson prevents the same mistake in a different shape later.

Per-line schema (the standard in `synapse/Skills/exfil/references/project.md`):

```json
{"date":"YYYY-MM-DD","category":"<category>","summary":"<one-sentence summary>","detail":"<2–4 sentence factual description>","lesson":"<what we learned and how it changes future work>"}
```

All five fields are required. JSON encoding rules: ASCII-safe escapes, no embedded newlines (replace with `\n` if multi-line content is unavoidable).

## What counts as an incident

**Always log:**
- A bug that surfaced during build, smoke test, or eval and was fixed in the same session. (e.g., the cache_control 4-cap bug from 2026-04-30: detection event + root cause + fix + lesson.)
- A governance violation discovered (hard rule leak, scrub gap, lint failure that should have been caught earlier).
- A scrub that missed a file the operator later flagged.
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

Use one of these category strings. Add new categories to this list (in `references/incidents-format.md`) when a recurring pattern doesn't fit.

| Category | What it covers |
|---|---|
| `implementation-bug` | Code defect surfaced during smoke test or eval; root cause + fix in same session |
| `governance-leak` | Hard rule violation found in project files (HR-CP-NNN, scrub gap, etc.) |
| `environment-state` | Substrate or dependency state surprise (venv, .env, secrets, dev tunnel) |
| `wrong-assumption` | Earlier decision rested on a premise this session disproved |
| `scale-vulnerability` | Pattern that works at current scale but won't at 10x; documented before incident |
| `earn-by-incident-evidence` | Add-1 entry for a parked item's N-count (operator-correction loop, etc.) |
| `process-gap` | Skill/runbook/workflow missed a case the operator surfaced |
| `vendor-surprise` | Anthropic SDK / Phoenix / Zoho / etc. behaved differently than docs implied |
| `data-quality` | Wiki / golden set / eval data error caught downstream |

## Examples

```jsonl
{"date":"2026-04-30","category":"implementation-bug","summary":"cache_control 4-breakpoint cap hit on iter 5 of agent loop","detail":"First-pass prompt-cache implementation in pipeline/copilot.py accumulated cache_control breakpoints (system + every iteration's tool_result). Iteration 5 of the smoke-test run hit Anthropic's 4-cap and 400'd. Rolling-strip helper _strip_message_cache_breakpoints() resolves; second run completed cleanly.","lesson":"Cumulative-prefix matching means only the latest cache_control breakpoint is needed; rolling-strip pattern keeps requests under the cap regardless of iteration count. Codified in D-011."}
{"date":"2026-04-30","category":"governance-leak","summary":"HR-CP-009 name leak in research-state.yaml not caught in Session 8 scrub","detail":"Four team-member ids (robert-givens, ben-frank, summer, mike) survived in research/research-state.yaml::dependencies after the 2026-04-29 operator-name scrub. Surfaced during 2026-04-30 metabolize; scrubbed to role labels in same session.","lesson":"Scrub passes need explicit file enumeration of project scope (decisions/, rules/, research/, tasks-status, build-log, glossary, threat-model, incidents.jsonl, runbooks/, prompts/, eval/), not relying on grep-as-you-go. capture-and-metabolize Phase 3 should re-run an HR-CP-009 grep across project scope every time."}
```

## Writing rules

1. **One incident, one line.** Multi-issue sessions write multiple lines.
2. **Append-only.** Never edit past lines; if a prior entry was wrong, append a new one with `category: "wrong-assumption"` correcting it.
3. **Date is the date the incident happened.** If you're catching up on incidents from earlier, use the actual incident date, not today's date. Capture-and-metabolize fires at end-of-session so the dates line up by default; backfilling needs care.
4. **Detail is factual, not narrative.** Write what happened, not what was felt. The lesson field carries the interpretive work.
5. **Lesson is actionable.** "Don't do X again" is weak. "Codified in D-NNN" or "added HR-CP-NNN" or "now grep for Y in scrub passes" is strong. The lesson should change behavior.

## When in doubt

Log it. The cost of a redundant entry is one line. The cost of a missed entry is the same problem biting twice.
