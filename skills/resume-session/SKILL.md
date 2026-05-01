---
name: resume-session
description: >
  Session-start bookend for an ACW instance. Loads variable context that doesn't
  belong in the auto-loaded substrate: the most recent session captures
  (sections §5–§7 only — §1–§4 are already distributed into auto-loaded files)
  and any queued research prompts in research/queries/. Each prompt file holds
  its own lifecycle — capture-and-metabolize bakes the substrate synthesis into
  the prompt; deep-research appends findings to the same file; consumed prompts
  move to research/queries/_consumed/. There is no synthesis subdirectory.

  Also reads `<repo>/_inbox/` for unread cross-project notifications dropped by
  other ACW instances. Surfaces them to the operator and lets them decide
  whether to act, archive (move to `_inbox/_read/`), or ignore.

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

The host-native auto-load (per `acw-state.yaml::auto_load_at_session_start`) already provides slow-changing substrate. This skill loads the rotating parts.

## Instructions

When invoked, execute five steps in order. Operator confirmation is not required for the loads; they are read-only.

### Step 1 — Load the three most recent session captures (§5–§7 only)

1. Glob `research/sessions/*.md`. Sort by filename date descending. Take the top 3.
2. For each: read sections §5 (Open questions left), §6 (Operator directives, verbatim), and §7 (Cleaned transcript excerpt). Skip §1–§4 — those are already distributed into the auto-loaded substrate.
3. If a capture is shorter than the standard format and §5–§7 don't exist as named sections, fall back to reading the whole file. Don't fail.

### Step 2 — Load queued research prompts

1. Glob `research/queries/*.md` (top level only; do NOT descend into `_consumed/`).
2. Read each fully. These are synthesis-shaped prompts produced by `/capture-and-metabolize` Phase 5 in a prior session.

### Step 3 — Detect whether each queued prompt has been answered

For each queued prompt:
1. Inspect content for a `## Findings` or `## Key Findings` heading (per the `append_findings_to_self: true` convention).
2. If findings exist: note as "synthesis loaded" — file already loaded carries both prompt and findings. Capture-and-metabolize will sweep it to `_consumed/` at next session close.
3. If no findings: note as "ready to fire" — operator will run `/deep-research` (or equivalent) against it this session.

### Step 4 — Read cross-project inbox

1. Check `<repo>/_inbox/` (top level only; do NOT descend into `_read/`).
2. For each unread file (`read: false` in frontmatter, or no `read` field), surface to the operator: source project, date, topic, one-line summary.
3. Do not auto-act. Operator decides per file: act on it, archive (move to `_inbox/_read/`), or ignore (leave for later).
4. If `_inbox/` does not exist, skip silently.

### Step 5 — Report

One-paragraph chat summary with:

- Last session: date, topic, one-sentence outcome (from §5 of most recent capture or its frontmatter `topic`).
- Queued prompts: count, plus for each: name + status (`ready to fire` or `findings already in file`).
- Inbox notifications: count of unread (if any).
- Recommended next action: either "fire deep-research against `<path>`" or "build per findings in `<path>`" or "act on inbox notification from `<project>`" or "no queued work; continue per tasks-status::Pending".
- Total tokens loaded (approximate, optional).

## When NOT to fire

- The session is a quick one-off task where the auto-loaded substrate alone is sufficient.
- The operator is working in a sub-system that doesn't depend on the recent session arc.
- A session capture has not yet been written by `/capture-and-metabolize` and the conversation is the canonical memory.

## Output

No files written. Chat reply only.
