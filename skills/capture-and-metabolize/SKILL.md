---
name: capture-and-metabolize
description: >
  End-of-session steward for an ACW instance. Runs a five-phase pass — capture
  the session, distribute findings into living scaffolding, metabolize stale
  entries, optionally append a synapse session log, and (conditionally) build a
  next-session research prompt — so the project's decisions, evolution,
  glossary, tasks-status, build-log, sources, hard rules, and incidents stay
  current in one bookend pass.

  Reads project-specific configuration from `acw-state.yaml`:
  `project.code` (HR id prefix), `project.name`, `synapse_log_path` (Phase 4
  destination; null disables), `cross_repo_writes` (allowed external write
  surfaces), `voice` (voice references applied to transcript cleanup), and
  `auto_load_at_session_start` (substrate already in context — do not re-read).

  Produces up to five artifacts:
  (1) session capture at research/sessions/YYYY-MM-DD--<topic>.md;
  (2) targeted edits to scaffolding files including a full session block
  appended to tasks-status.md;
  (3) a metabolize report appended to build-log.md;
  (4) a synapse session log block (only if synapse_log_path is set);
  (5) optionally — only on operator confirmation at the Phase 5 prompt — a
  deep-research prompt at research/queries/YYYY-MM-DD-<topic>.md, with a
  next-session-start marker pinned at the top of tasks-status.md::Pending.

  Triggered by the operator running /capture-and-metabolize at the end of a
  substantive working session, or manually when scaffolding has drifted from
  current reality. Never fires automatically.

  Pairs with /resume-session as the session-start bookend.
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Curation | High |

# capture-and-metabolize

Sequential orchestrator that runs five phases: **capture**, **distribute**, **metabolize**, **synapse-log** (conditional on `acw-state.yaml::synapse_log_path`), and **research-prompt** (conditional on operator confirmation). Sub-phases are internal until operational friction earns their separation into standalone skills (see `references/sub-step-discipline.md`).

## Configuration

Before Phase 1, read `acw-state.yaml` once and resolve:

- `project.code` → prefix for new hard-rule ids (`HR-{CODE}-NNN`) and decision ids (`D-{CODE}-NNN`). **Optional.** If the `project:` block is absent, new ids ship without prefix (`D-NNN`, `HR-NNN`) and continue any existing unprefixed numbering in the decision log. Do not fail; do not invent a prefix.
- `project.name` → used in narrative output where the project is named. **Optional**, defaults to the repo's directory name.
- `synapse_log_path` → Phase 4 destination. If null or absent, Phase 4 is skipped entirely; do not warn.
- `cross_repo_writes` → list of paths outside the repo this skill may write to. Empty list or absent = no external writes allowed (vault-boundary discipline).
- `voice` → list of voice-reference files applied during transcript cleanup. Empty list or absent = no voice opinion.
- `auto_load_at_session_start` → files already in context; never re-read in this skill.
- `template_layer` / `instance_layer` / `meta_layer` → if these blocks are present and non-empty, this instance uses the three-layer manifest discipline. Phase 2 will surface classification prompts for new tracked-path files. If any of these blocks is absent or empty, the manifest classification step in Phase 2 silently skips. See `rules/manifest-discipline.md` for the pattern.

## Instructions

When invoked, execute Phases 1–3 always. Phase 4 fires only if `synapse_log_path` is set. Phase 5 fires only on operator confirmation. Read `references/` for full rules before acting on edge cases.

### Phase 1 — Capture

1. Identify the topic of the session: 3–7 word noun phrase summarizing what was worked on.
2. Identify decisions made (→ `decisions/decision-log.md` candidates).
3. Identify conceptual shifts (→ `research/evolution.md` candidates).
4. Identify terms that entered or shifted meaning (→ `glossary.md` candidates).
5. Identify tasks completed, started, or parked (→ `tasks-status.md` candidates).
6. Identify hard-rule changes (→ `rules/instance-hard-rules.md` candidates, prefix `HR-{project.code}-NNN`).
7. Identify external sources cited (→ `research/sources.md` candidates).
8. **Identify incidents** — bugs that surfaced and were fixed, governance violations discovered, scale-vulnerability evidence, deferred-pattern N+1 evidence, wrong-assumptions that surfaced. Each becomes one JSONL line in `incidents.jsonl`. Schema and detection rules in `references/incidents-format.md`.
9. **Surface unresolved design questions** — section §5 of the capture file gets one structured block per unresolved question. Format: `question / candidates considered / why unresolved / who needs to weigh in`. See `references/session-capture-format.md` §5.
10. Write the session capture to `research/sessions/YYYY-MM-DD--<topic-slug>.md` per `references/session-capture-format.md`. Use today's actual date.
11. Clean transcript noise per `references/transcript-cleaning-rules.md`. If `acw-state.yaml::voice` is non-empty, apply voice references; otherwise skip voice cleanup.

### Phase 2 — Distribute

**Distribution scope rule (load-bearing).** Distribute only project-specific findings into this project's substrate. A finding qualifies as project-specific when it shapes how *this* project will be built, decided, or used going forward. Findings about another project, a cross-cutting framework, or operator-personal infrastructure do NOT enter this project's substrate. Cross-project session content stays in the session capture but does not pollute decisions, evolution, hard rules, glossary, tasks-status, or build-log here.

For each project-specific candidate identified in Phase 1, edit the appropriate scaffolding file. Strict rules in `references/distribution-rules.md`. Summary:

- New decisions → append to `decisions/decision-log.md` under `## Decisions and Rationale` with next `D-{project.code}-NNN` id
- Resolved open questions → move from `## Open Questions` to `## Decisions and Rationale` with resolution note
- New constraints → append to `## Constraints and Gotchas`
- Conceptual shifts → prepend new entry to `research/evolution.md`
- Term additions / redefinitions → edit `glossary.md`
- New hard rules → append to `rules/instance-hard-rules.md` with `HR-{project.code}-NNN` id
- **`tasks-status.md` — full session block** under `## Done` per `rules/task-tracking.md`. Format defined in `references/distribution-rules.md` under "tasks-status.md".
- New tasks → append to `## Pending`
- Newly parked → move to `## Parked` with reason
- New sources → append to `research/sources.md`
- **New incidents → append one JSONL line per incident to `incidents.jsonl`.** Append-only; never edit past lines. See `rules/incident-tracking.md` and `references/incidents-format.md`.
- Build progress narrative → append entry (newest first) to `build-log.md`

`research/research-state.yaml` updates only when a Phase 1 finding actually changes the conception (architectural shift, scope change, abstraction-layer change, tool-surface change). Routine work does NOT update research-state.

**Auto-load list maintenance.** If Phase 2 creates a new top-level substrate file (rules file, status file, glossary supplement) that meets the substrate-worthy test in `references/distribution-rules.md`, append its path to `acw-state.yaml::auto_load_at_session_start`. Additive only. Removal is forbidden by skill; it requires an explicit operator decision-log entry.

**Manifest classification (conditional).** If this instance uses the three-layer manifest (per Configuration above — `template_layer` / `instance_layer` / `meta_layer` blocks exist and are non-empty in `acw-state.yaml`), then for every new file Phase 2 creates at a tracked path (root, `rules/`, `tools/`, `skills/`), surface a classification prompt to the operator: **"template_layer / instance_layer / meta_layer?"** Default to `instance_layer` (the conservative choice — see `rules/manifest-discipline.md` for the asymmetry rationale). Operator answer appends to the appropriate list in `acw-state.yaml`. Additive only; demotion (template → instance, or template → meta) is forbidden by skill and requires an explicit decision-log entry. If this instance does not use the manifest (blocks absent or empty), this step silently skips.

**Cross-repo writes.** If a finding implies a write to a path outside the project repo, the path MUST be in `acw-state.yaml::cross_repo_writes`. If not, refuse the write and surface the path to the operator.

**Cross-project notifications.** If the session touched another project, drop a notification at `<other-project-root>/_inbox/YYYY-MM-DD-<source-project>-<topic-slug>.md`. Frontmatter: `from_project`, `from_session_capture`, `date`, `topic`, `read: false`. Body: 5–15 lines summarizing what the receiving project should know. Notifications are append-only; never edit once written. Receiving project's next session reads `_inbox/` at session start.

### Phase 3 — Metabolize

Read the live state of the project. Compare against the scaffolding. Find stale items per `references/metabolize-rules.md`. Categories:

- **Auto-update** (always safe): move completed tasks from Pending → the session's Done block; mark resolved Open Questions as resolved when their decision is now in `## Decisions and Rationale`.
- **Operator-confirm** (propose, do not execute): items that look stale but might be load-bearing — Parked items, glossary terms no longer referenced, hard rules whose context has shifted.
- **Never edit past entries**: append-only history — `build-log.md` past entries, `incidents.jsonl` past lines, `research/evolution.md` past entries, `research/sessions/*` once written, Done blocks in `tasks-status.md`.

**Consumed-prompt sweep.** For each file in `research/queries/` (top level only), check whether deep-research has appended findings (heuristic: `## Findings` or `## Key Findings` heading present). If yes, move to `research/queries/_consumed/`. The single-file lifecycle convention: prompt and findings live together; `_consumed/` archives the full lifecycle. Create `_consumed/` if it does not exist.

Output the metabolize report appended to `build-log.md` under the new session's entry. Format in `references/metabolize-report-format.md`.

### Phase 4 — Synapse session log (conditional)

If `acw-state.yaml::synapse_log_path` is set, append a session block to `<synapse_log_path>/YYYY-MM-DD.md`. Format in `references/synapse-log-format.md`. If null, skip Phase 4 entirely; do not warn.

### Phase 5 — Research-prompt builder (conditional)

After Phases 1–4 complete, prompt: **"Build research prompt now? [y/N]"**

- **`n` (or no answer):** exit cleanly with summary of artifacts written.
- **`y`:** continue.

When fired:

1. **Verify recent-session context.** If the last 2–3 capture files in `research/sessions/` are not in context, read them now. Do not re-read substrate already auto-loaded.
2. **Build the artifact** at `research/queries/YYYY-MM-DD-<topic-slug>.md` per `references/research-prompt-format.md`. Frontmatter MUST include `append_findings_to_self: true` so deep-research appends rather than writing a sibling file. Three tracks:
   - **Track A — Session-specific design questions.** Sourced from Phase 1 §5 unresolved questions.
   - **Track B — Project-wide improvement opportunities.** Sourced from cross-substrate gaps surfaced in Phases 2–3.
   - **Track C — Standing — substrate and scaffolding evolution.** Always present, never primary driver. Asks the research to surface what's evolving in the project's own scaffolding patterns this project could absorb.
3. **Pin the fire-task** at the top of `tasks-status.md::Pending` with the `🔬 [FIRE AT NEXT SESSION START]` marker.
4. **Append a one-line entry to `build-log.md`** under the current session's metabolize report.

If both Track A and Track B are empty, skip writing the artifact and pinning the fire-task. Track C alone never justifies firing.

## Output

Up to five artifacts per invocation:

1. **Session capture** — `research/sessions/YYYY-MM-DD--<topic-slug>.md`
2. **Scaffolding edits** — targeted updates to `decisions/`, `research/`, `glossary.md`, `rules/`, `tasks-status.md`, `build-log.md`
3. **Metabolize report** — section appended to `build-log.md`
4. **Synapse session log** *(conditional on `synapse_log_path`)*
5. **Research-prompt artifact** *(conditional on Phase 5 confirmation)* — `research/queries/YYYY-MM-DD-<topic-slug>.md` with fire-task pinned

Chat reply summarizes all artifacts in <300 words.

## When NOT to fire

- Mid-session before substantive work has accumulated
- Conversation only (no decisions, no shifts, no completions)
- Operator explicitly says "don't capture this session"
