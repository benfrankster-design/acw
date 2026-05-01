# Sub-step Discipline — Internal Phases

Per `~/.claude/rules/Procedures/skill-format.md`:

> An orchestrator skill may declare sub-steps in its instructions that correspond to pipeline-worker roles. The sub-steps are internal to the orchestration until operational friction earns their separation into standalone skills.

This skill has three sub-steps. Until friction earns the split, all three live inside this single orchestrator.

## The three sub-steps

| Sub-step | Pipeline role (16-role appendix) | Description |
|---|---|---|
| Phase 1 — Capture | extractor + composer | Extract decisions/shifts/tasks/terms from transcript; compose session capture file |
| Phase 2 — Distribute | router + committer | Route extracted content to appropriate scaffolding files; commit edits |
| Phase 3 — Metabolize | auditor + sanitizer | Audit scaffolding for stale entries; sanitize via auto-update or operator-confirm |

## When to split

Each sub-step earns its own skill when:

- **Capture earns its own skill** when sessions need to be captured independently of distribution. For example, when an external system (a meeting recorder, a Slack huddle, a teammate's session) provides a transcript that needs cleaning + storing without immediately distributing into scaffolding.
- **Distribute earns its own skill** when a session capture (or any other source) needs to be fanned out into scaffolding without re-running capture. For example, when a previous session was captured but distribution was skipped or done partially, and the operator wants to redo just the distribution.
- **Metabolize earns its own skill** when the operator wants to run a stale-check pass without a recent session — e.g., scheduled monthly hygiene. This is the most likely first split because it's an obvious independent operation.

## Promotion procedure

When friction earns a split:

1. Log the friction in `incidents.jsonl` (one line: when, what, what was incurred)
2. Create a new skill folder under `gsg-copilot/skills/<sub-step-name>/`
3. Move the relevant sub-step's logic into the new skill
4. Update this skill's SKILL.md to delegate to the new skill (becomes a true orchestrator)
5. Add a decision log entry recording the split

## Don't split prematurely

Single-operator scale: three skills doing one thing each is more friction than one skill doing three things. The orchestrator's value is that the operator types one slash command and gets the full sequence. Splitting before friction is real means the operator has to remember to run three commands in order.

The 16-role taxonomy is a teaching aid for thinking about the sub-steps. It is not a mandate to ship 16 skills.
