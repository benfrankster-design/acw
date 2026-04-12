---
name: capture-session
description: >
  Cleans a session transcript, tags conceptual shifts, drafts evolution
  entries, and proposes research-state.yaml updates. Fires at the end of
  any session where the operator's understanding shifted. Not for routine
  session logging (use the instance's session logger). Not for research
  execution (use deep-research).
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | Highest |

# Capture Session

Preserve the conceptual provenance of a session. Turn a raw operator-AI conversation into a cleaned transcript with tagged shifts, an evolution log entry, and a proposed research-state.yaml update.

This skill is an orchestrator with four internal sub-steps. Each sub-step corresponds to a pipeline-worker role. At single-operator scale, the orchestrator handles all four. When a sub-step needs to be invoked independently, that's the incident that earns its separation into a standalone skill per `rules/skill-format.md`.

## When to fire

- End of a session where the operator's understanding genuinely shifted
- Operator says "capture this session," "save the transcript," "record what changed"
- After a research session that produced new findings worth preserving
- After a conversation with an external reviewer (ChatGPT, Claude.ai, a human) that changed the conception

## When NOT to fire

- Routine work session with no conceptual shifts — use the instance's session logger
- Session that only produced operational output (code, config, file edits) with no new thinking
- Quick lookup or single-question session

## Sub-steps

### Step 1 — Clean transcript (transformer)

Take the raw session conversation and produce a cleaned markdown transcript.

**What to clean:**
- Voice-to-text artifacts (garbled dictation, false starts, filler words)
- Tool-result dumps (remove entirely — preserve only the human-readable summary)
- System-reminder blocks (remove)
- Em dashes → commas (per brand voice)
- Transcription errors where meaning is unambiguous

**What to preserve:**
- Every substantive exchange between operator and agent
- The operator's exact reasoning, arguments, and pushbacks (clean the grammar, keep the thought)
- The agent's recommendations, analysis, and pivots
- Chronological order

**Output format:**
```markdown
---
date: YYYY-MM-DD
type: session-transcript
topic: [one-line topic]
scope: [what portion of the session this covers]
form: cleaned
---

# Session Transcript — YYYY-MM-DD

[Context paragraph: what preceded this session]

## Turn 1 — [description]

**Operator:** [cleaned prompt]

**Agent:** [cleaned response]

## Turn 2 — [description]
...
```

**Goal:** A future agent reading this transcript gets clean prose, understands the reasoning, and doesn't burn tokens parsing garbled speech-to-text. The cleaned transcript should be ~40-60% shorter than the raw conversation while preserving 100% of the substantive content.

### Step 2 — Tag conceptual shifts (extractor)

Read the cleaned transcript and identify moments where the operator's understanding changed. A conceptual shift is:

- A prior belief being replaced by a new one ("we used to think X, now we think Y")
- A new problem, pattern, or principle being named for the first time
- A scope change (broader or narrower than before)
- A structural insight (two things that were separate are actually one, or one thing that was unified is actually two)
- An earned finding from dogfooding, testing, or real-world use

**Not** a conceptual shift:
- A task being completed
- A file being created
- A decision about implementation detail (that's for the decision log)
- An opinion that wasn't tested against evidence

Tag each shift inline in the transcript with:
```
> **[SHIFT]** [one-line description of what changed]
```

### Step 3 — Draft evolution entry (composer)

For each tagged shift, draft an entry for `research/evolution.md`:

```markdown
### YYYY-MM-DD — [one-line description]

**Changed:** [the new belief]
**Replaced:** [the old belief]
**Justified by:** [source — the session transcript path + turn number]
**Stale in template:** [which files are now inconsistent, if any]
```

Present all draft entries to the operator for review. Operator approves, edits, or skips each one.

### Step 4 — Propose research-state.yaml update (committer)

Read the current `research/research-state.yaml`. For each approved evolution entry, check whether the state file needs updating:

- **New problem identified?** → Propose adding it to `problems:` with `origin: instance`
- **Foundation count changed?** → Propose updating `foundations.count`
- **New open question?** → Propose adding to `open_questions:` with `origin: instance`
- **Open question resolved?** → Propose moving to resolved with the answer
- **Scope changed?** → Propose updating `conception.scope` or `conception.application`
- **New prior art discovered?** → Propose adding to `prior_art.key_references`
- **Nothing changed in state?** → Report "no state update needed" — the shift was captured in evolution.md but doesn't affect the current conception snapshot

Present each proposed YAML edit to the operator. Show the current value and the proposed new value. Operator approves each edit individually.

Write approved edits to research-state.yaml. Update `last_updated` and `updated_by` fields.

### Step 5 — Save transcript

Save the cleaned transcript to `research/sessions/YYYY-MM-DD--{topic-slug}.md`.

If the session covered multiple topics, use the primary topic as the slug.

## Output

After all steps complete, confirm:

```
Capture complete:
- Transcript: research/sessions/YYYY-MM-DD--{slug}.md ([N] turns, [N] words)
- Shifts tagged: [N]
- Evolution entries: [N] approved, [N] skipped
- State updates: [N] proposed, [N] approved
- Stale flags: [list of files flagged, if any]
```

## Integration with session logging

Capture-session is NOT a replacement for the instance's session logger (e.g., `/log-session`). The session logger records what was *done* (files changed, tasks completed, deliverables shipped). Capture-session records what was *learned* (conceptual shifts, evolution entries, state updates). Both can run at the end of the same session. Run the session logger first (it captures the operational record), then capture-session (it captures the intellectual record).
