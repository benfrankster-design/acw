# update

Mid-session checkpoint verb. Reads `<sessions_dir>/.current-session`; appends a timestamped note to the active capture file under `## Updates`. No metabolize, no distribute, no Phase 2-5 work. Cheap by design — Haiku-grade end-to-end, runs in seconds.

Closes the gap between session-start and session-end: lets the operator log progress mid-flow without paying full session-end cost. Models on the [Ian Nuttall claude-sessions](https://github.com/iannuttall/claude-sessions) `session-update` precedent.

## After the spine

The orchestrator's spine has loaded `paths`, the `_buffer/` state, and recent capture paths. Update only needs `paths.session_captures_dir`. The other spine outputs are unused for this verb (no drift check, no buffer surfacing, no recent-capture reads).

## Step 1 — Resolve the active capture file

1. Compute `<sessions_dir>/.current-session` from `paths.session_captures_dir` (canonical default `sessions`).
2. **Read tracker.** If the tracker file exists and is non-empty, treat its content as the relative filename of the active capture (e.g., `2026-05-04--bookend-efficiency.md`). Resolve to full path `<sessions_dir>/<filename>`.
3. **If the file referenced by the tracker exists,** use it. Skip Step 2.
4. **If the tracker is missing, empty, or points to a non-existent file,** self-bootstrap (Step 2).

## Step 2 — Self-bootstrap (only if no active capture)

The whole point of `update` is being frictionless mid-session. Refusing because of missing setup state defeats the purpose. Bootstrap quietly:

1. Today's date: `YYYY-MM-DD` (use today's actual date).
2. Topic slug: derive from the operator's note (first 3-5 meaningful words, kebab-case, ASCII only). If the note is short or generic, default to `untitled`.
3. Capture path: `<sessions_dir>/YYYY-MM-DD--<topic>.md`.
4. If a file already exists at that path, append numeric suffix.
5. Create the file with the same frontmatter shape `start` writes (see `references/start.md` Step 0 §6).
6. Write the relative filename to `<sessions_dir>/.current-session`.

The bootstrap-created file becomes the canonical capture for this session. When `/acw-session end` runs later, it reads the tracker, finds this file, runs Phase 1 (which may rename `untitled` to a topic-from-Phase-1), and proceeds normally.

## Step 3 — Append the note

1. Format the entry block:

```
### YYYY-MM-DD HH:MM

<note text exactly as the operator provided, no editorialization>
```

Use 24-hour local time. The operator's note may be multiple paragraphs; preserve them verbatim. Do not summarize, restructure, or apply voice cleanup — `update` is operator's voice straight in.

2. Locate the `## Updates` section in the active capture file. If absent (a hand-written capture file or older shape), append the section heading first, then the entry. Otherwise append the entry under the existing heading.

3. Write to disk.

## Step 4 — Confirm

One-line chat reply only:

```
Note appended to <relative path>
```

No metabolize report, no summary, no further analysis. The operator already knows what they wrote.

## When NOT to fire (verb-specific)

- Mid-conversation when the note is incidental and not worth persisting (the conversation transcript itself is sufficient).
- Verbatim transcript dumps — those belong in the operator's normal notes app, not the session capture.
- After `/acw-session end` clears the tracker but before a fresh `/acw-session start` — `update` will self-bootstrap, which may not be what the operator wanted. If the operator is genuinely between sessions, prefer to start fresh.

## Output

One file modified: the active capture, with a new entry appended under `## Updates`. The tracker file may be created if self-bootstrap fired.

No other artifacts. No substrate writes. No Phase 2-5 work.

## Cost shape

This verb exists specifically to be cheap. Haiku-default (per skill frontmatter) handles every step. Total token cost should be a small fraction of `/acw-session end quick` and a tiny fraction of `/acw-session end full`. If `update` ever feels expensive, that's a signal it's doing too much; cut scope.
