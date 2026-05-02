---
status: superseded
superseded_by: skills/acw-session/ (verb: start)
superseded_in: 0.4.0
name: resume-session
description: >
  Session-start bookend for an ACW instance. Loads variable context that doesn't
  belong in the auto-loaded substrate: the most recent session captures
  (sections §5–§7 only — §1–§4 are already distributed into auto-loaded files)
  and any queued research prompts. Each prompt file holds its own lifecycle —
  capture-and-metabolize bakes the substrate synthesis into the prompt;
  deep-research appends findings to the same file; consumed prompts move to a
  consumed directory. There is no synthesis subdirectory.

  Also reads the instance's inbox directory for unread cross-project
  notifications dropped by other ACW instances. Surfaces them to the operator.

  Produces no files. Outputs a one-paragraph chat summary naming what was
  loaded, what's still pending, and the recommended next action.

  Triggered by the operator running /resume-session at the start of a working
  session, after host-native auto-load completes (see AGENTS.md directive 7).
  Pairs with /capture-and-metabolize.
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | Medium |

# resume-session

Session-start bookend that loads variable context: recent session captures, queued research prompts, and cross-project notifications. Mirrors `/capture-and-metabolize` (end-of-session) so each session opens cleanly and closes cleanly.

## Path resolution

File locations referenced in this skill (`paths.session_captures_dir`, `paths.research_queries_dir`, `paths.research_queries_consumed_dir`, `paths.inbox_dir`, `paths.tasks_status`) resolve at runtime by reading `acw-state.yaml::paths::<key>` and falling back to the canonical default in `rules/manifest-discipline.md` if the key is absent. The skill never hardcodes a path.

## Instructions

When invoked, execute the steps below in order. Operator confirmation is not required for the loads; they are read-only.

### Step 1 — Load the three most recent session captures (§5–§7 only)

1. Glob the top level of `paths.session_captures_dir` for `*.md`. Sort by filename date descending. Take the top 3.
2. For each: read sections §5 (Open questions left), §6 (Operator directives, verbatim), and §7 (Cleaned transcript excerpt). Skip §1–§4 — those are already distributed into the auto-loaded substrate.
3. If a capture is shorter than the standard format and §5–§7 don't exist as named sections, fall back to reading the whole file. Don't fail.

### Step 2 — Load queued research prompts

1. Glob the top level of `paths.research_queries_dir` for `*.md` (top level only; do NOT descend into `paths.research_queries_consumed_dir`).
2. Read each fully. These are synthesis-shaped prompts produced by `/capture-and-metabolize` Phase 5 in a prior session.

### Step 3 — Detect whether each queued prompt has been answered

For each queued prompt:
1. Inspect content for a `## Findings` or `## Key Findings` heading (per the `append_findings_to_self: true` convention).
2. If findings exist: note as "synthesis loaded" — file already loaded carries both prompt and findings. Capture-and-metabolize will sweep it to the consumed directory at next session close.
3. If no findings: note as "ready to fire" — operator will run `/deep-research` (or equivalent) against it this session.

### Step 4 — Read cross-project inbox

1. Check `paths.inbox_dir` (top level only; do NOT descend into a `_read/` subdirectory).
2. For each unread file (`read: false` in frontmatter, or no `read` field), surface to the operator: source project, date, topic, one-line summary.
3. Do not auto-act. Operator decides per file: act on it, archive (move to a `_read/` subdirectory of the inbox), or ignore (leave for later).
4. If `paths.inbox_dir` does not exist, skip silently.

### Step 5 — Drift check

Read `rules/instance-current-manifest.md` (the recommended-blocks registry) and compare against this instance's `acw-state.yaml`. For each recommended entry whose **earned in** version is newer than `acw-state.yaml::last_reconciled_version` (semantic-version comparison, NOT date comparison), check the instance state file:

- Block absent → flag.
- Block present-but-empty (`block: []` or `block: {}`) → do NOT flag (deliberate opt-out).
- Block present and populated → do NOT flag.

If `last_reconciled_version` is absent, treat as `"0.0.0"` (flag everything that has an earned-in version).

If gaps exist, surface a one-line alert at the start of the report:

```
[acw-drift] Your instance is reconciled to ACW <last_reconciled_version> as of <last_reconciled>. Current ACW (<version>) expects N additional blocks: <names>. Run /upgrade-instance to reconcile.
```

If no gaps, no alert. Quiet success.

### Step 6 — Report

One-paragraph chat summary with:

- Drift alert (if Step 5 detected gaps).
- Last session: date, topic, one-sentence outcome.
- Queued prompts: count, plus for each: name + status.
- Inbox notifications: count of unread (if any).
- Recommended next action.

## When NOT to fire

- The session is a quick one-off task where the auto-loaded substrate alone is sufficient.
- The operator is working in a sub-system that doesn't depend on the recent session arc.
- A session capture has not yet been written by `/capture-and-metabolize` and the conversation is the canonical memory.

## Output

No files written. Chat reply only.
