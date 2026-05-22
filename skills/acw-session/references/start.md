# start

Session-start verb. Initializes the active capture file and tracker, loads variable context that doesn't belong in auto-loaded substrate, surfaces drift, reports state to the operator.

## After the spine

The orchestrator's spine has already loaded `paths`, the `_buffer/` state (Step 3), and the 3 most recent session captures (Step 4 paths only). The start verb consumes those, initializes today's capture file + tracker, reads queued research prompts, and runs the drift check.

## Step 0 — Initialize active capture file and tracker

Run before reading anything else. Creates the file `update` and `end` will operate on.

### Step 0a — Unclosed-prior-session check (BEFORE any writes)

Read `<sessions_dir>/.current-session` if present. If the tracker names a session file:

1. Open that file. Inspect its frontmatter / closing section for evidence the prior session was bookended via `/acw-session end`:
   - `stability: complete` (set by `end`'s Phase 1 cleanup) → session was closed; proceed.
   - `last_completed_phase: 0` (or any phase < 7) → session was started but never closed.
   - No `stability` field and no closing markers (no `## Phase N` blocks, no Phase 7 summary) → ambiguous; treat as unclosed.
2. If unclosed, surface a warning to the operator BEFORE overwriting the tracker:

```
[acw-session warn] Unclosed prior session detected:
  Tracker: <sessions_dir>/.current-session
  Names:   <prior-filename>
  Status:  last_completed_phase = <N> (or "no phase markers found")

Options:
  [e] Run /acw-session end against the prior session FIRST (recommended).
      You'll re-invoke /acw-session start afterwards.
  [o] Orphan the prior session and proceed.
      The prior capture file stays on disk but the tracker is overwritten;
      /acw-session end will require an explicit filename to close it later.
  [q] Quit; do nothing.
```

3. Wait for operator choice. On `[e]`: exit cleanly with a single-line reminder to run `/acw-session end <prior-filename>`, then re-invoke start. On `[o]`: proceed to Step 0b; record an entry in the new session's capture file under `## Orphaned prior session` naming the file so it remains discoverable. On `[q]`: exit.

If the tracker is absent or empty, skip the warning and proceed directly to Step 0b.

### Step 0b — Create new capture file and tracker

1. Resolve `<sessions_dir>` from `paths.session_captures_dir` (canonical default `sessions`).
2. Today's date: `YYYY-MM-DD` (use today's actual date, not the agent's training-data assumption).
3. Session name: argument to `/acw-session start` if provided (e.g., `/acw-session start auth-refactor`), else `untitled`. Slug: lowercase, hyphens, ASCII only.
4. Compute capture path: `<sessions_dir>/YYYY-MM-DD--<name>.md`.
5. If the file already exists at that path (multiple `/acw-session start` calls same day with same name), append numeric suffix: `--<name>-2.md`, `--<name>-3.md`, etc.
6. Create the file with frontmatter and `## Updates` section:

```markdown
---
class: capture
authority: skill
stability: in-progress
date: YYYY-MM-DD
topic: <name or "untitled">
---

# Session capture YYYY-MM-DD — <name>

## Updates

<!-- /acw-session update appends timestamped notes here -->
```

7. Write the relative filename (e.g., `2026-05-04--bookend-efficiency.md`) to `<sessions_dir>/.current-session`. Single line, no trailing newline.

If the instance does not use `/acw-session start` (skips straight to `update` or `end`), Steps in this verb don't run; `update` self-bootstraps and `end` writes its own capture at end-time. See those references.

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

**Acted-on tracking.** When the operator chooses "act on it" and the resulting work lands in this session (decision, incident, hard-rule edit, canonical patch, etc.), the buffer note source is recorded so `/acw-session end` Phase 2 buffer sweep can move it to `_buffer/_read/` automatically. Active session's acted-on buffer notes are tracked in the capture file under `## Buffer notes acted on` (one bullet per source filename). The `end` verb reads this section and performs the moves.

## Step 5 — Drift check

**Short-circuit (cheap path).** `/acw-instance upgrade` writes the local manifest cache and `last_reconciled_version` in the same atomic step and stamps `synced_to: <version>` in the manifest's frontmatter. Read ONLY the manifest's frontmatter (cheap — first ~10 lines). If `synced_to` is present AND equal to `acw-state.yaml::last_reconciled_version`, skip the walk and emit "no drift" silently — every entry's earned-in version is at-or-before `last_reconciled_version` by construction, so gaps are structurally impossible.

Fall through to the full walk if any of the following:
- `synced_to` is absent (instance pre-dates this field; never upgraded since v0.9.9; manually-written manifest).
- `synced_to` mismatches `last_reconciled_version` (broken upgrade, manual edit, or the operator copied a newer canonical without bumping state).
- `last_reconciled_version` is absent in `acw-state.yaml` (never-upgraded instance).

**Full walk (fallback).** Read `rules/instance-current-manifest.md` (the local cache; updated by `/acw-instance upgrade`). For each entry whose **earned in** version is newer than `acw-state.yaml::last_reconciled_version` (semantic-version comparison, NOT date), check the state file:

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
