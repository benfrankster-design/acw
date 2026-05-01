# Synapse Log Format — Phase 4

Phase 4 appends a session block to `synapse/Logs/YYYY-MM-DD.md` so the operator does not need to fire `/log-session` separately on this project. Format mirrors `/log-session`'s output exactly so the day file stays uniform across all projects the operator works on in a given day.

## Day file structure

If `synapse/Logs/YYYY-MM-DD.md` does not exist, create it with this header:

```markdown
# Claude Code Log - YYYY-MM-DD
```

If it exists, append the new session block under a horizontal rule (`---`) only if the prior block doesn't already end with one. Most blocks end without one; just append directly after the last line of the prior block.

## Session block format

Append this block, replacing all `<...>` placeholders. The `<topic>` is the same 3–7 word phrase used in the session capture filename and in the tasks-status session block heading.

```markdown
## Session — gsg-copilot (<topic>)
- **Directory**: C:\Users\benja\projects\gsg-copilot
- **Full capture**: `gsg-copilot/research/sessions/YYYY-MM-DD--<topic-slug>.md`

### What we worked on
- <Bulleted list. One bullet per substantive thread. Cite decision IDs (`D-NNN`), hard rule IDs (`HR-CP-NNN`), constraint IDs (`C-NNN`), file paths inline.>
- <Each bullet is one sentence to one paragraph max. Scannable, not exhaustive — the session capture file is the exhaustive record; this is the next-day index.>

### What was decided
- <Bulleted list of decisions and conclusions. Quote operator directives verbatim where wording matters.>
- <Decisions that did NOT resolve go to "Where things were left," not here.>

### Where things were left
- <Handoff state. What the next session needs to know to pick up cleanly.>
- <Any cross-project to-dos surfaced (e.g., "cs-atlas mirror needed").>
- <Any blocked-on-X items: platform engineering, deep research, operator decision.>
- <If Phase 5 fired, include: "Research-prompt artifact queued at `research/queries/<file>.md` to fire next session start.">
```

## Rules for content

1. **Mirror, don't duplicate.** The session capture file in `research/sessions/` is the canonical record. The synapse log block is the index. Anything load-bearing in the synapse block must also be in the capture file.

2. **Same data, different audience.** The capture file is for project-internal reference (decision IDs, file paths, structured open questions). The synapse log block is for the operator scanning the day's work across all projects. Strip project-internal jargon where it doesn't help cross-project recall.

3. **No raw transcript.** Even when the capture file includes a §7 cleaned transcript excerpt, the synapse log block summarizes — never quotes long passages.

4. **Cross-reference the capture.** The `**Full capture**` line is mandatory. It's the operator's path back to the detailed record.

5. **Project name in the heading is `gsg-copilot`.** Don't dress it up. Other projects use the same convention so cross-project search works.

## What does NOT go in the synapse log

- Multi-paragraph prose exposition.
- Code snippets longer than one line.
- Tool-call dumps or raw command output.
- Anything that would be redundant after reading the linked capture file.
- The metabolize report (that lives in `build-log.md`).
- The research-prompt artifact contents (that lives in `research/queries/`).

## Multiple sessions in one day

If the operator runs capture-and-metabolize twice on the same project on the same day, append a second `## Session` block under the first. Distinguish the topics in the heading so the operator can tell them apart at a glance:

```markdown
## Session — gsg-copilot (Phase 3 cache + streaming)
...

## Session — gsg-copilot (Phase 3 close-out and async design queued)
...
```

## When the day file already has cross-project content

If `synapse/Logs/YYYY-MM-DD.md` already contains session blocks for other projects (`_Command`, `frank-context`, etc.), the gsg-copilot session block goes at the bottom in the order it was captured. Do NOT reorder existing blocks. Do NOT collapse blocks from different projects.
