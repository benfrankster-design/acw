# Transcript Cleaning Rules

Used in Phase 1 (Capture) when writing the optional cleaned-transcript section. The default for session captures is summary, not transcript — only include cleaned transcript when exact wording matters.

## Strip these (always)

- System reminders (e.g., todo-list reminders, session-start hooks)
- Empty bash output
- Tool result echoes that the LLM has already summarized in its next response
- Boilerplate reassurance ("happy to help!", "great question!", "absolutely!")
- Pure status narration ("Let me read the file" → followed by Read tool call)
- Identical repeated content (LLM mistakenly reprinting the same thing twice)
- Verbose listings that are reproduced from a file already in the project (link to the file path instead)

## Keep these (always)

- Operator-supplied directives, verbatim
- Decisions made, verbatim where wording is load-bearing
- Disagreements (operator pushed back on a Claude proposal — keep both sides verbatim)
- Constraints surfaced (operator named a hard rule, a gotcha, a non-obvious consideration)
- Resolved fact-verification (operator confirmed how something actually works)

## Trim these (with judgment)

- Long bash command output → keep the relevant lines, replace bulk with `[output truncated; full in build-log]`
- Long file dumps → reference the file path, omit the inline content
- Tool-call argument lists with sensitive data → redact per HR-CP-002 (PII discipline)

## Format

When transcript excerpts are kept, mark each speaker:

```
> **Ben:** "<verbatim quote>"

> **Claude:** "<verbatim quote>"
```

Use `> [paraphrase]` for non-verbatim content if needed for context.

## When to skip the transcript section entirely

Default. Only include if:
- A decision wording is contested or might be reinterpreted later
- The session resolved a long-standing debate where the rationale needs preservation
- The operator explicitly asked for verbatim capture
