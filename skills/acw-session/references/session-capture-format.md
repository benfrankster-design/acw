# Session Capture Format

Every session capture file lives at `paths.session_captures_dir / YYYY-MM-DD--<topic-slug>.md`. Multiple captures on the same day get suffixed `-2`, `-3` etc.

> **Path resolution.** `paths.X` resolves at runtime per the SKILL.md preamble.

## Frontmatter

```yaml
---
date: YYYY-MM-DD
participants: [operator, agent]
topic: 3–7 word noun phrase
decisions_made: [<id>, <id>]   # decision-log ids referenced or created
conceptual_shifts: [yes|no]
linked_files:
  - path/to/file/edited/in/this/session
duration_minutes: <approximate>
---
```

## Body sections (in order)

### 1. Topic & Goal

One paragraph. What was the session about? What were we trying to accomplish?

### 2. What was decided

Bulleted list. Each decision with its decision-log id (or "new <id>" if added by this skill in Phase 2). Quote operator-supplied directives verbatim where the wording matters. Decisions that did not resolve in this session go to "Open questions left," not here.

### 3. What changed in the conception

Free-form. If `paths.evolution` got an entry, summarize it here and link to that entry's date. If no shifts, write "No conceptual shifts; this was a build/work session."

### 4. What was built / changed

Bulleted list of files created, modified, or deleted with one-line each. Cross-reference `linked_files` in the frontmatter.

### 5. Open questions left — structured

Anything raised but not resolved. If they were promoted to the open-questions surface in Phase 2 (a section in single-file mode, a file in wiki mode), note OQ ids. **Phase 5 (research-prompt builder) reads this section as Track A input** — write it with that consumer in mind.

Each unresolved design question gets a structured block (not just a bullet). Format:

```markdown
#### OQ-<id> — <one-line question>

**Question:** <one-paragraph statement of the unresolved question, written so a researcher who hasn't seen the session can understand it cold>

**Candidates considered:** <bulleted list of approaches the session weighed, with a brief note on each — what's appealing, what's worrying>

**Why unresolved:** <one sentence on what would let us close it — usually "needs deep research," "needs operator decision," "needs platform engineering input," or "needs a real incident to disambiguate">

**Who needs to weigh in:** <operator, platform engineering, deep-research artifact, pilot data, etc.>
```

Examples of what counts as a Phase-5-actionable design question:
- The shape of a new agent affordance whose API isn't yet locked.
- A tradeoff between two architectural patterns where the session reasoned about both but didn't pick.
- A scale-vulnerable pattern that the session noticed but didn't fix.
- A "we don't know what we don't know" gap — explicitly write what's unknown.

What does NOT belong here:
- Tasks (those go to `paths.tasks_status` `section_conventions.pending`).
- Decisions already made (those go to the decisions surface per `decision_tracking.mode`: section in single-file mode, file under entries/ in wiki mode).
- Personal preferences pending operator call (those go to open-questions surface with an OQ id — section in single-file mode, file under open-questions/ in wiki mode — and a short prose paragraph, not the structured block).

A session may end with zero unresolved design questions. In that case write `*(None — session closed cleanly.)*` and Phase 5 will know not to build a Track A.

### 6. Operator directives (verbatim)

Direct quotes from the operator that constitute hard guidance. These are the entries the agent should honor in future sessions even if the surrounding context is gone. Format:

> "Operator said: '...verbatim quote...' (turn N)"

### 7. Cleaned transcript excerpt (optional)

Only include for sessions where exact wording matters and is hard to summarize. Use the transcript-cleaning rules. Otherwise skip.

## Naming

Topic slug: lowercase, hyphens, max 50 chars. Strip articles ("the", "a"). Examples:

- `2026-04-28--unified-tool-surface.md`
- `2026-04-28--operator-as-api-substitute-pattern.md`
- `2026-04-28--connector-scope-locked.md`

## What does not go in a session capture

- Boilerplate reassurance ("happy to help!")
- Unread tool-call output dumps
- System reminders
- Conversational pleasantries with no decision content
- Code blocks already saved to source files (reference the file path instead of duplicating)
