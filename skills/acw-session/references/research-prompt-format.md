# Research Prompt Format — Phase 5

Phase 5 fires only when the operator confirms at the prompt: **"Build research prompt now? [y/N]"**. When fired, it produces a deep-research prompt artifact at `paths.research_queries_dir / YYYY-MM-DD-<topic-slug>.md` and pins a fire-task at the top of `paths.tasks_status` `section_conventions.pending`.

> **Path resolution.** `paths.X` and `section_conventions.X` resolve at runtime per the SKILL.md preamble.

## When the prompt artifact is produced

Phase 5 produces an artifact only when there is research-worthy material. Three tracks; the artifact ships if Track A or Track B has content:

- **Track A** — Session-specific design questions. Sourced from Phase 1 §5 of the just-written session capture. Empty if §5 was `*(None — session closed cleanly.)*`.
- **Track B** — Project-wide improvement opportunities. Sourced from cross-substrate gaps surfaced during Phases 2–3.
- **Track C** — Standing — substrate and scaffolding evolution. Always present. Watching brief on what's evolving in scaffolding patterns the project could absorb.

**Empty Track A + empty Track B**: skip artifact, print "No research-worthy material; Track C alone does not justify firing," exit Phase 5.

**Track A or Track B has content**: write the artifact with all three tracks included, pin the fire-task.

## Artifact filename

`paths.research_queries_dir / YYYY-MM-DD-<topic-slug>.md`. Topic slug matches the session capture's topic slug (or close to it — research-prompts that span more than one session's topic get a clearer disambiguating slug).

## Artifact frontmatter

```yaml
---
queued_by: YYYY-MM-DD capture-and-metabolize session
fire_with: /deep-research
fire_at: next session start
append_findings_to_self: true
session_capture_link: <paths.session_captures_dir>/YYYY-MM-DD--<topic-slug>.md
expected_duration_minutes: <integer; default 25>
---
```

`append_findings_to_self: true` is the load-bearing convention: deep-research appends its findings to the same file rather than writing a sibling artifact. Resume-session detects findings and routes the file to `paths.research_queries_consumed_dir` at the next session-end metabolize.

## Artifact body structure

```markdown
# Deep-Research Prompt — <project-relevant title>

<One-paragraph framing: what this research is for, what produced it, what consumes it.>

Two research tracks plus one standing track. Run them in one synthesis pass — many findings will cross-reference.

---

## Project context (load-bearing for the research)

<3–5 short paragraphs. What the project is. What just shipped (with decision IDs). What's queued / blocked / unbuilt. Constraints to respect across all findings (key hard rules + scale posture). The researcher must be able to pick up cold from this section alone.>

---

## Track A — <one-line title from the session capture §5 question>

<For each unresolved design question from Phase 1 §5, one Track A subsection. If multiple questions, repeat the subsection structure.>

**The problem.** <1–2 paragraph statement of the unresolved question. Cite the OQ id.>

**Research questions for Track A:**

1. <Substantive numbered questions, each with sub-bullets where useful.>
2. ...

**Track A deliverable.** <One paragraph on the form the answer should take. Default: a ratified design ready to build.>

---

## Track B — Project-wide improvement opportunities

**Goal of Track B.** <One sentence on what kind of recommendations are wanted.>

**Research questions for Track B:**

1. **<Theme>?** <Numbered questions with sub-bullets covering: cost/latency/quality wins, scale-vulnerable patterns, eval-substrate gaps, missing skills/tools, plan errors of omission, what's appearing in current literature.>
2. ...

**Track B deliverable.** A prioritized list of recommendations, each tagged with (impact, effort, risk-of-skipping), categorized as: ship-now / earn-by-incident / discard. The list becomes input to the next tasks-status update.

---

## Track C — Standing — substrate and scaffolding evolution (watching brief)

**Goal.** Surface what's evolving in project-scaffolding, context-engineering, and agent-substrate patterns that this project could absorb.

**Research questions for Track C:**

1. What's appearing in project scaffolding for AI-collaborated projects (decision logs, evolution files, session capture patterns, incidents tracking, research-state files, append-only history vs. living docs)?
2. What's emerging in context-engineering practice — patterns for what gets loaded at session start, how substrate is partitioned, how skills consume substrate without re-reading?
3. Are there agent-substrate primitives (memory APIs, durable-execution patterns, agent inboxes, capability brokers) that are now production-ready and worth a watching-brief read?
4. Anti-patterns in scaffolding adoption — where do projects bog down adopting patterns that don't fit their scale?

**Track C deliverable.** 3–5 bullets max. One-line observations with a "promote / watch / discard" tag. Track C never drives the artifact; it rides on Track A or Track B.

---

## Source hierarchy and retrieval guidance

1. **Primary** — Anthropic docs, peer-reviewed papers (arxiv), engineering blogs from the orgs building the patterns.
2. **Secondary** — well-maintained OSS implementations, reference architectures from cloud providers.
3. **Tertiary** — community write-ups, conference talks, podcasts.

Cross-reference with prior project research. Don't duplicate; build on existing artifacts.

---

## Output expectations

Findings appended to this same file (per `append_findings_to_self: true`) under a `## Findings` heading. Three top-level subsections matching Track A, B, C. Each Track ends with a clearly-marked **Recommendations** subsection.

After findings are appended:
1. Append a one-line entry to `paths.sources` pointing at this file.
2. Update any related OQ entry in `paths.decisions_log::section_conventions.open_questions` with a `**Research artifact:**` line linking to this file.
3. Open a discussion in chat to walk the operator through the recommendations — Track A first, then Track B, then Track C as a quick "anything caught my eye" pass.
```

## Fire-task pinning

After the artifact is written, edit `paths.tasks_status` `section_conventions.pending` to pin the fire-task at the very top:

```markdown
- **🔬 [FIRE AT NEXT SESSION START] Run `/deep-research` against `<paths.research_queries_dir>/YYYY-MM-DD-<topic-slug>.md`** — covers (Track A) <one-line summary of A> and (Track B) <one-line summary of B>. Track A unblocks <forcing function>; Track B reshapes this Pending list. Track C watching brief on substrate evolution. Expected duration ~<N> min. After findings land: append source pointer, link from any related OQ, walk through recommendations in chat.
```

If a prior fire-task is still pinned at the top (operator hadn't run the previous one yet), do NOT overwrite it. Either:
- Append the new fire-task as a second pinned item below the prior one, with a note "(this session's prompt; prior session's prompt above is still queued)", OR
- Print a warning to the operator: "A prior research-prompt is still queued at <path>. Pin this new one too, or replace?"

Default to appending; let the operator decide whether to retire the older artifact.

## Build-log breadcrumb

Append a one-line entry to the just-written `paths.build_log` session entry, in the metabolize report's Auto-updated subsection:

```markdown
- **Phase 5 fired** — research-prompt artifact queued at `<paths.research_queries_dir>/YYYY-MM-DD-<topic-slug>.md`; fire-task pinned at top of `paths.tasks_status` Pending.
```

If Phase 5 fired but produced no artifact (Track A + Track B both empty), append:

```markdown
- **Phase 5 fired but produced no artifact** — Tracks A and B were both empty; Track C alone does not justify firing. Skipped.
```
