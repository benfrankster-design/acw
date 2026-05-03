# start

Session-start verb. Loads variable context that doesn't belong in auto-loaded substrate, surfaces drift, reports state to the operator. Read-only on substrate.

## After the spine

The orchestrator's spine has already loaded `paths`, the `_buffer/` state (Step 3), and the 3 most recent session captures (Step 4 paths only). The start verb consumes those plus reads queued research prompts and runs the drift check.

## Step 1 — Read recent session captures (§5–§7 only)

For each of the up-to-3 capture file paths handed off from spine Step 4:
1. Read sections §5 (Open questions left), §6 (Operator directives, verbatim), and §7 (Cleaned transcript excerpt). Skip §1–§4 — those are distributed into auto-loaded substrate already.
2. If the capture is shorter than standard and §5–§7 don't exist as named sections, fall back to reading the whole file. Don't fail.

## Step 2 — Load queued research prompts

1. Glob the top level of `paths.research_queries_dir` for `*.md` (top level only; do NOT descend into `paths.research_queries_consumed_dir`).
2. Read each fully. These are synthesis-shaped prompts produced by the `end` verb's Phase 5 in a prior session.

## Step 3 — Detect whether each queued prompt has been answered

For each queued prompt:
- Inspect for a `## Findings` or `## Key Findings` heading (per `append_findings_to_self: true`).
- Findings present → note as "synthesis loaded"; the `end` verb will sweep it to consumed at session close.
- Findings absent → note as "ready to fire"; operator will run `/deep-research` (or equivalent) against it this session.

## Step 4 — Surface buffer notifications from spine Step 3

For each unread file the spine collected (`read: false` in frontmatter, or no `read` field), surface to operator: source project, date, topic, one-line summary. Do not auto-act. Operator decides per file: act on it, archive (move to a `_read/` subdirectory of the buffer), or ignore.

## Step 5 — Drift check

Read `rules/instance-current-manifest.md` (the local cache; updated by `/acw-instance upgrade`). For each entry whose **earned in** version is newer than `acw-state.yaml::last_reconciled_version` (semantic-version comparison, NOT date), check the state file:

- Block absent → flag.
- Block present-but-empty (`block: []` or `block: {}`) → do NOT flag (deliberate opt-out).
- Block present and populated → do NOT flag.

If `last_reconciled_version` is absent, treat as `"0.0.0"` (flag everything with an earned-in version).

If gaps exist, surface a one-line alert at the start of the report:

```
[acw-drift] Your instance is reconciled to ACW <last_reconciled_version> as of <last_reconciled>. Current ACW (<version>) expects N additional blocks: <names>. Run /acw-instance upgrade to reconcile.
```

No gaps → no alert; quiet success.

## Step 6 — Report

One-paragraph chat summary with:

- Drift alert (if Step 5 detected gaps).
- Last session: date, topic, one-sentence outcome.
- Queued prompts: count, plus for each: name + status (synthesis loaded / ready to fire).
- Inbox notifications: count of unread (if any).
- Pending review entries from `divergent_pending_review` (if any): note status reminder.
- Recommended next action.

## When NOT to fire (verb-specific)

- Quick one-off task where auto-loaded substrate alone is sufficient.
- Sub-system work that doesn't depend on the recent session arc.
- A session capture has not yet been written and the conversation itself is the canonical memory.

## Output

No files written. Chat report only.
