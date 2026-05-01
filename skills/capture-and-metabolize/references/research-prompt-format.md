# Research Prompt Format — Phase 5

Phase 5 fires only when the operator confirms at the prompt: **"Build research prompt now? [y/N]"**. When fired, it produces a deep-research prompt artifact at `research/queries/YYYY-MM-DD-<topic-slug>.md` and pins a fire-task at the top of `tasks-status.md::Pending`.

## When the prompt artifact is produced

Phase 5 produces an artifact only when there is research-worthy material. Three tracks; the artifact ships if Track A or Track B has content:

- **Track A** — Session-specific design questions. Sourced from Phase 1 §5 of the just-written session capture. Empty if §5 was `*(None — session closed cleanly.)*`.
- **Track B** — Project-wide improvement opportunities. Sourced from cross-substrate gaps surfaced during Phases 2–3 (decisions left without a clear next step, scaffolding patterns that look fragile, eval-substrate gaps the operator flagged). Empty if Phases 2–3 didn't surface gaps.
- **Track C** — Standing — ACW-scaffolding best practices. Always present. Watching brief on what's evolving in project scaffolding, context engineering, and agent-substrate patterns.

**Empty Track A + empty Track B**: skip artifact, print "No research-worthy material; Track C alone does not justify firing," exit Phase 5.

**Track A or Track B has content**: write the artifact with all three tracks included, pin the fire-task.

## Artifact filename

`research/queries/YYYY-MM-DD-<topic-slug>.md`. Topic slug matches the session capture's topic slug (or close to it — research-prompts that span more than one session's topic get a clearer disambiguating slug).

## Artifact frontmatter

```yaml
---
queued_by: YYYY-MM-DD capture-and-metabolize session
fire_with: /deep-research
fire_at: next session start
target_artifact: Cortex/Resources/research/YYYY-MM-DD--<descriptive-slug>.md
expected_duration_minutes: <integer; default 25>
session_capture_link: research/sessions/YYYY-MM-DD--<topic-slug>.md
---
```

## Artifact body structure

```markdown
# Deep-Research Prompt — <project-relevant title>

<One-paragraph framing: what this research is for, what produced it, what consumes it.>

Two research tracks plus one standing track. Run them in one synthesis pass — many findings will cross-reference.

---

## Project context (load-bearing for the research)

<3–5 short paragraphs. What gsg-copilot is. What just shipped (with decision IDs). What's queued / blocked / unbuilt. Constraints to respect across all findings (key hard rules + scale posture). The researcher must be able to pick up cold from this section alone.>

---

## Track A — <one-line title from the session capture §5 question>

<For each unresolved design question from Phase 1 §5, one Track A subsection. If multiple questions, repeat the subsection structure.>

**The problem.** <1–2 paragraph statement of the unresolved question. Cite the OQ-NNN id.>

**Research questions for Track A:**

1. <Substantive numbered questions, each with sub-bullets where useful.>
2. ...

**Track A deliverable.** <One paragraph on the form the answer should take. Default: a ratified design ready to build.>

---

## Track B — Project-wide improvement opportunities

**Goal of Track B.** <One sentence on what kind of recommendations are wanted.>

**Research questions for Track B:**

1. **<Theme>?** <Numbered questions with sub-bullets covering: cost/latency/quality wins, scale-vulnerable patterns, eval-substrate gaps, missing skills/tools, plan errors of omission, what's appearing in current LLM-engineering literature.>
2. ...

**Track B deliverable.** A prioritized list of recommendations, each tagged with (impact, effort, risk-of-skipping), categorized as: ship-now / earn-by-incident / discard. The list becomes input to the next tasks-status update.

---

## Track C — Standing — ACW-scaffolding best practices (watching brief)

**Goal.** Surface what's evolving in project-scaffolding, context-engineering, and agent-substrate patterns that this project could absorb. The operator likes the current ACW-derived scaffolding and is open to refinement, not replacement.

**Research questions for Track C:**

1. What's appearing in 2026-Q1/Q2 in project scaffolding for AI-collaborated projects (decision logs, evolution files, session capture patterns, incidents tracking, research-state files, append-only history vs. living docs)?
2. What's emerging in context-engineering practice — patterns for what gets loaded at session start, how substrate is partitioned, how skills consume substrate without re-reading?
3. Are there agent-substrate primitives (memory APIs, durable-execution patterns, agent inboxes, capability brokers) that are now production-ready and worth a watching-brief read?
4. Anti-patterns in scaffolding adoption — where do projects bog down adopting patterns that don't fit their scale?

**Track C deliverable.** 3–5 bullets max. One-line observations with a "promote / watch / discard" tag. Track C never drives the artifact; it rides on Track A or Track B and provides peripheral vision.

---

## Source hierarchy and retrieval guidance

Per the synapse `deep-research` skill convention:

1. **Primary** — Anthropic docs, peer-reviewed papers (arxiv), engineering blogs from the orgs building the patterns.
2. **Secondary** — well-maintained OSS implementations, reference architectures from cloud providers.
3. **Tertiary** — community write-ups, conference talks, podcasts.

Cross-reference with prior project research already at `Cortex/Resources/research/`. Don't duplicate; build on existing artifacts.

---

## Output expectations

Single research artifact at the path in `target_artifact` (frontmatter). Three top-level sections matching Track A, B, C. Each Track ends with a clearly-marked **Recommendations** subsection.

After the artifact is written:
1. Append a one-line entry to `research/sources.md` under "Internal" pointing at the artifact.
2. Update any related `OQ-NNN` entry in `decisions/decision-log.md::Open Questions` with a `**Research artifact:**` line linking to the file.
3. Open a discussion in chat to walk Ben through the recommendations — Track A first (it has a forcing function), then Track B (which the operator triages into ship-now / park / discard), then Track C as a quick "anything caught my eye" pass.
```

## Fire-task pinning

After the artifact is written, edit `tasks-status.md::Pending` to pin the fire-task at the very top:

```markdown
## Pending (immediate next — Phase N)

- **🔬 [FIRE AT NEXT SESSION START] Run `/deep-research` against `research/queries/YYYY-MM-DD-<topic-slug>.md`** — produces a research artifact at `Cortex/Resources/research/YYYY-MM-DD--<descriptive-slug>.md` covering (Track A) <one-line summary of A> and (Track B) <one-line summary of B>. Track A unblocks <forcing function>; Track B reshapes this Pending list. Track C watching brief on ACW-scaffolding evolution. Expected duration ~<N> min. After the artifact lands: append source pointer to `research/sources.md`, link from any related OQ in `decision-log.md`, walk through recommendations in chat.
- <existing pending items follow>
```

If a prior fire-task is still pinned at the top (operator hadn't run the previous one yet), do NOT overwrite it. Either:
- Append the new fire-task as a second pinned item below the prior one, with a note "(this session's prompt; prior session's prompt above is still queued)", OR
- Print a warning to the operator: "A prior research-prompt is still queued at <path>. Pin this new one too, or replace?"

Default to appending; let the operator decide whether to retire the older artifact.

## Build-log breadcrumb

Append a one-line entry to the just-written `build-log.md` session entry, in the metabolize report's "Auto-updated" subsection:

```markdown
- **Phase 5 fired** — research-prompt artifact queued at `research/queries/YYYY-MM-DD-<topic-slug>.md`; fire-task pinned at top of `tasks-status.md::Pending`.
```

If Phase 5 fired but produced no artifact (Track A + Track B both empty), append:

```markdown
- **Phase 5 fired but produced no artifact** — Tracks A and B were both empty; Track C alone does not justify firing. Skipped.
```
