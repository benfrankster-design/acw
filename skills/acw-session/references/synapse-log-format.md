# Synapse Log Format — Phase 4

Phase 4 fires only when `acw-state.yaml::synapse_log_path` is set. It appends a session block to `<synapse_log_path>/YYYY-MM-DD.md`, mirroring whatever cross-project day-index format the operator uses. The block format below is the default; instances may override by declaring their own format reference in `acw-state.yaml::synapse_log_format` (future field, not currently supported).

> **Path resolution.** `paths.X` resolves at runtime per the SKILL.md preamble. `<synapse_log_path>` is read from the state file directly.

## Day file structure

If `<synapse_log_path>/YYYY-MM-DD.md` does not exist, create it with this header:

```markdown
# Session Log — YYYY-MM-DD
```

If it exists, append the new session block under a horizontal rule (`---`) only if the prior block doesn't already end with one. Most blocks end without one; just append directly after the last line of the prior block.

## Session block format

Append this block, replacing all `<...>` placeholders. The `<topic>` is the same 3–7 word phrase used in the session capture filename and in the tasks-status session block heading.

```markdown
## Session — <project.name> (<topic>)
- **Directory**: <repo absolute path>
- **Full capture**: `<paths.session_captures_dir>/YYYY-MM-DD--<topic-slug>.md`

### What we worked on
- <Bulleted list. One bullet per substantive thread. Cite decision IDs, hard rule IDs, constraint IDs, file paths inline.>
- <Each bullet is one sentence to one paragraph max. Scannable, not exhaustive — the session capture file is the exhaustive record; this is the next-day index.>

### What was decided
- <Bulleted list of decisions and conclusions. Quote operator directives verbatim where wording matters.>
- <Decisions that did NOT resolve go to "Where things were left," not here.>

### Where things were left
- <Handoff state. What the next session needs to know to pick up cleanly.>
- <Any cross-project to-dos surfaced.>
- <Any blocked-on-X items: platform engineering, deep research, operator decision.>
- <If Phase 5 fired, include: "Research-prompt artifact queued at `<paths.research_queries_dir>/<file>.md` to fire next session start.">
```

## Rules for content

1. **Mirror, don't duplicate.** The session capture file in `paths.session_captures_dir` is the canonical record. The synapse log block is the index. Anything load-bearing in the synapse block must also be in the capture file.

2. **Same data, different audience.** The capture file is for project-internal reference (decision IDs, file paths, structured open questions). The synapse log block is for the operator scanning the day's work across all projects. Strip project-internal jargon where it doesn't help cross-project recall.

3. **No raw transcript.** Even when the capture file includes a §7 cleaned transcript excerpt, the synapse log block summarizes — never quotes long passages.

4. **Cross-reference the capture.** The `**Full capture**` line is mandatory.

5. **Project name in the heading is `<project.name>` from `acw-state.yaml`.** If `project.name` is absent, fall back to the repo's directory name. Cross-project search relies on this convention.

## What does NOT go in the synapse log

- Multi-paragraph prose exposition.
- Code snippets longer than one line.
- Tool-call dumps or raw command output.
- Anything that would be redundant after reading the linked capture file.
- The metabolize report (that lives in `paths.build_log`).
- The research-prompt artifact contents (that lives in `paths.research_queries_dir`).

## Multiple sessions in one day

If the operator runs capture-and-metabolize twice on the same project on the same day, append a second `## Session` block under the first. Distinguish the topics in the heading so the operator can tell them apart at a glance.

## When the day file already has cross-project content

If `<synapse_log_path>/YYYY-MM-DD.md` already contains session blocks for other projects, the new session block goes at the bottom in the order it was captured. Do NOT reorder existing blocks. Do NOT collapse blocks from different projects.
