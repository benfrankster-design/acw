---
status: superseded
superseded_by: skills/acw-session/ (verb: end)
superseded_in: 0.4.0
name: capture-and-metabolize
description: >
  End-of-session steward for an ACW instance. Runs a five-phase pass — capture
  the session, distribute findings into living scaffolding, metabolize stale
  entries, optionally append a synapse session log, and (conditionally) build a
  next-session research prompt — so the project's substrate stays current in
  one bookend pass.

  Reads project-specific configuration from `acw-state.yaml`, including the
  `paths:` block that resolves substrate file locations. The skill ships in the
  template and runs in any instance regardless of directory layout, as long as
  the instance declares its paths or accepts canonical defaults.

  Produces up to five artifacts in the instance's substrate per its declared
  paths: a session capture, targeted edits to scaffolding files, a metabolize
  report appended to the build log, an optional synapse session log block, and
  optionally — only on operator confirmation — a deep-research prompt with a
  fire-task pinned to the tasks-status pending section.

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

Sequential orchestrator that runs five phases: **capture**, **distribute**, **metabolize**, **synapse-log** (conditional), and **research-prompt** (conditional). Sub-phases are internal until operational friction earns their separation into standalone skills (see `references/sub-step-discipline.md`).

## Path resolution

Throughout this document and its references, file locations are referred to by their manifest key, e.g. `paths.decisions_log`, not by hardcoded path. Every key resolves at runtime by reading `acw-state.yaml::paths::<key>` and falling back to the canonical default in `rules/manifest-discipline.md` if the key is absent. The skill never hardcodes a path; the instance's manifest is authoritative.

Section headings inside substrate files are resolved similarly: `section_conventions.<name>` reads from the target file's frontmatter (declared per `rules/task-tracking.md`, `rules/decision-tracking.md`, etc.), with documented defaults if the frontmatter is absent.

## Configuration

Before Phase 1, read `acw-state.yaml` once and resolve:

- `project.code` → prefix for new hard-rule ids (`HR-{CODE}-NNN`) and decision ids (`D-{CODE}-NNN`). **Optional.** If the `project:` block is absent, new ids ship without prefix (`D-NNN`, `HR-NNN`) and continue any existing unprefixed numbering. Do not fail; do not invent a prefix.
- `project.name` → used in narrative output where the project is named. **Optional**, defaults to the repo's directory name.
- `paths` → substrate file locations. Read keys via `tools/manifest.py::load(state_file, "paths")` (or the equivalent in the host's runtime), which merges the file's overrides with the canonical defaults. **Optional**; absent block means all defaults apply.
- `synapse_log_path` → Phase 4 destination. If null or absent, Phase 4 is skipped entirely; do not warn.
- `cross_repo_writes` → list of paths outside the repo this skill may write to. Empty list or absent = no external writes allowed.
- `voice` → list of voice-reference files applied during transcript cleanup. Empty list or absent = no voice opinion.
- `auto_load_at_session_start` → files already in context; never re-read in this skill.
- `template_layer` / `instance_layer` / `meta_layer` → if present and non-empty, this instance uses the three-layer manifest discipline. Phase 2's manifest classification step fires for new tracked-path files. If absent or empty, the step silently skips.
- `is_canonical_source` → boolean flag declaring whether this instance publishes canonical content downstream. **Default `false`** (treat as a downstream consumer). Gates Phase 2's canonical-edit propagation behavior — see "Canonical-edit detection" below.

## Instructions

When invoked, execute Phases 1–3 always. Phase 4 fires only if `synapse_log_path` is set. Phase 5 fires only on operator confirmation. Read `references/` for full rules before acting on edge cases.

### Phase 1 — Capture

1. Identify the topic of the session: 3–7 word noun phrase.
2. Identify decisions made (→ `paths.decisions_log` candidates).
3. Identify conceptual shifts (→ `paths.evolution` candidates).
4. Identify terms that entered or shifted meaning (→ `paths.glossary` candidates).
5. Identify tasks completed, started, or parked (→ `paths.tasks_status` candidates).
6. Identify hard-rule changes (→ instance hard-rules file candidates, prefix `HR-{project.code}-NNN` if `project.code` is set).
7. Identify external sources cited (→ `paths.sources` candidates).
8. **Identify incidents.** Each becomes one JSONL line in `paths.incidents`. Schema and detection rules in `references/incidents-format.md`.
9. **Surface unresolved design questions.** Section §5 of the capture file gets one structured block per unresolved question. See `references/session-capture-format.md` §5.
10. Write the session capture to `paths.session_captures_dir / YYYY-MM-DD--<topic-slug>.md` per `references/session-capture-format.md`. Use today's actual date.
11. Clean transcript noise per `references/transcript-cleaning-rules.md`. If `voice` is non-empty, apply voice references; otherwise skip voice cleanup.

### Phase 2 — Distribute

**Distribution scope rule (load-bearing).** Distribute only project-specific findings into this project's substrate. A finding qualifies as project-specific when it shapes how *this* project will be built, decided, or used going forward. Findings about another project, a cross-cutting framework, or operator-personal infrastructure do NOT enter this project's substrate. Cross-project session content stays in the session capture but does not pollute the substrate here.

For each project-specific candidate identified in Phase 1, edit the appropriate scaffolding file. Strict rules in `references/distribution-rules.md`. Summary:

- New decisions → append to `paths.decisions_log` under `section_conventions.decisions` with next `D-{project.code}-NNN` id (or `D-NNN` if `project.code` is absent).
- Resolved open questions → move from `section_conventions.open_questions` to `section_conventions.decisions` with resolution note.
- New constraints → append to `section_conventions.constraints`.
- Conceptual shifts → prepend new entry to `paths.evolution`.
- Term additions / redefinitions → edit `paths.glossary`.
- New hard rules → append to the instance hard-rules file with `HR-{project.code}-NNN` id (or `HR-NNN` if `project.code` is absent).
- **`paths.tasks_status` — full session block** under `section_conventions.done` per `rules/task-tracking.md`. Format defined in `references/distribution-rules.md`.
- New tasks → append to `section_conventions.pending`.
- Newly parked → move to `section_conventions.parked` with reason.
- New sources → append to `paths.sources`.
- **New incidents → append one JSONL line per incident to `paths.incidents`.** Append-only; never edit past lines. See `rules/incident-tracking.md` and `references/incidents-format.md`.
- Build progress narrative → append entry (newest first) to `paths.build_log`.

`paths.research_state` updates only when a Phase 1 finding actually changes the conception (architectural shift, scope change, abstraction-layer change, tool-surface change). Routine work does NOT update research-state.

**Auto-load list maintenance.** If Phase 2 creates a new top-level substrate file that meets the substrate-worthy test in `references/distribution-rules.md`, append its path to `acw-state.yaml::auto_load_at_session_start` via `manifest.append`. Additive only. Removal is forbidden by skill; it requires an explicit operator decision-log entry.

**Manifest classification (conditional).** If this instance uses the three-layer manifest, then for every new file Phase 2 creates at a tracked path (root, `rules/`, `tools/`, `skills/`), surface a classification prompt to the operator: **"template_layer / instance_layer / meta_layer?"** Default to `instance_layer` (the conservative choice — see `rules/manifest-discipline.md` for the asymmetry rationale). Operator answer appends to the appropriate list via `manifest.append`. Additive only; demotion goes through the decision log. If the manifest blocks are absent or empty, this step silently skips.

**Host entry file maintenance.** If this instance has any host-specific entry files implementing `AGENTS.md` directive 7 (files declared with a `host:` key in `acw-state.yaml::instance_layer`, or files conventionally named per a host's mechanism), Phase 2 surfaces a proposed edit when substrate shifts in a way the entry file should reflect. Triggers include: a file entered or left `auto_load_at_session_start`, a hard-rule principle was added or retired, a manifest layer for a class of files changed, the bookend skill names changed, or the project's "where things live" map shifted. The proposal cites which sentence or list to update and why; the operator approves before the edit lands. If no host entry files are present, this step silently skips.

**Canonical-edit detection.** Compute the intersection of `auto_load_at_session_start` and `template_layer`. Files in this intersection are **canonical** — they exist in this instance and propagate to downstream instances (or, in a non-publishing instance, came from upstream and are read-only locally).

For each canonical file edited this session (detect via `git diff --name-only HEAD` against the file's path, scoped to the session's commit window; or by inspecting the session transcript for known edits), branch on `is_canonical_source`:

- **`is_canonical_source: true`** (publishing instance, e.g., ACW itself):
  - Surface the prompt: *"Canonical file `<path>` was edited this session. Confirm: should `acw-state.yaml::version` bump? If yes, propose `<current-version> → <next-version>` (semver bump per the size of the change). After version bump, push to GitHub before session end so downstream instances pick up the change on their next /upgrade-instance run."*
  - On operator confirmation, append the version bump to the Phase 2 change set; otherwise leave version unchanged.
  - Note in the metabolize report (Phase 3) that a canonical edit landed and whether a version bump and push are pending.
- **`is_canonical_source: false` or absent** (downstream consumer, every child instance):
  - Surface the warning: *"You edited canonical file `<path>` locally. This file is template_layer content from upstream ACW; local edits won't propagate and may be overwritten on next /upgrade-instance. If you intended a substrate-level change, raise it upstream in ACW. If you intended an instance-specific override, place it in a sibling file (e.g., `rules/instance-extra-<name>.md`) instead."*
  - The skill does not block the edit — the operator made it. The warning surfaces the consequence.

If no canonical files were edited, this step silently passes.

**Cross-repo writes.** If a finding implies a write to a path outside the project repo, the path MUST be in `acw-state.yaml::cross_repo_writes`. If not, refuse the write and surface the path to the operator.

**Cross-project notifications.** If the session touched another project, drop a notification at the other project's `paths.inbox_dir / YYYY-MM-DD-<source-project>-<topic-slug>.md`. Frontmatter: `from_project`, `from_session_capture`, `date`, `topic`, `read: false`. Body: 5–15 lines summarizing what the receiving project should know. Notifications are append-only; never edit once written. Receiving project's next session reads its own `paths.inbox_dir` at session start.

### Phase 3 — Metabolize

Read the live state of the project. Compare against the scaffolding. Find stale items per `references/metabolize-rules.md`. Categories:

- **Auto-update** (always safe): move completed tasks from `section_conventions.pending` → the session's `section_conventions.done` block; mark resolved Open Questions as resolved when their decision is now in `section_conventions.decisions`.
- **Operator-confirm** (propose, do not execute): items that look stale but might be load-bearing — Parked items, glossary terms no longer referenced, hard rules whose context has shifted.
- **Never edit past entries**: append-only history — `paths.build_log` past entries, `paths.incidents` past lines, `paths.evolution` past entries, captures already written under `paths.session_captures_dir`, Done blocks in `paths.tasks_status`.

**Consumed-prompt sweep.** For each file at the top level of `paths.research_queries_dir`, check whether deep-research has appended findings (heuristic: `## Findings` or `## Key Findings` heading present). If yes, move to `paths.research_queries_consumed_dir`. The single-file lifecycle convention: prompt and findings live together; the consumed directory archives the full lifecycle. Create the consumed directory if it does not exist.

Output the metabolize report appended to `paths.build_log` under the new session's entry. Format in `references/metabolize-report-format.md`.

### Phase 4 — Synapse session log (conditional)

If `synapse_log_path` is set, append a session block to `<synapse_log_path>/YYYY-MM-DD.md`. Format in `references/synapse-log-format.md`. If null or absent, skip Phase 4 entirely; do not warn.

### Phase 5 — Research-prompt builder (conditional)

After Phases 1–4 complete, prompt: **"Build research prompt now? [y/N]"**

- **`n` (or no answer):** exit cleanly with summary of artifacts written.
- **`y`:** continue.

When fired:

1. **Verify recent-session context.** If the last 2–3 capture files in `paths.session_captures_dir` are not in context, read them now. Do not re-read substrate already auto-loaded.
2. **Build the artifact** at `paths.research_queries_dir / YYYY-MM-DD-<topic-slug>.md` per `references/research-prompt-format.md`. Frontmatter MUST include `append_findings_to_self: true` so deep-research appends rather than writing a sibling file. Three tracks:
   - **Track A — Session-specific design questions.** Sourced from Phase 1 §5 unresolved questions.
   - **Track B — Project-wide improvement opportunities.** Sourced from cross-substrate gaps surfaced in Phases 2–3.
   - **Track C — Standing — substrate and scaffolding evolution.** Always present, never primary driver. Asks the research to surface what's evolving in the project's own scaffolding patterns this project could absorb.
3. **Pin the fire-task** at the top of `paths.tasks_status` `section_conventions.pending` with the `🔬 [FIRE AT NEXT SESSION START]` marker.
4. **Append a one-line entry to `paths.build_log`** under the current session's metabolize report.

If both Track A and Track B are empty, skip writing the artifact and pinning the fire-task. Track C alone never justifies firing.

## Output

Up to five artifacts per invocation:

1. **Session capture** — file at `paths.session_captures_dir / YYYY-MM-DD--<topic-slug>.md`
2. **Scaffolding edits** — targeted updates to substrate files per Phase 2 rules
3. **Metabolize report** — section appended to `paths.build_log`
4. **Synapse session log** *(conditional on `synapse_log_path`)*
5. **Research-prompt artifact** *(conditional on Phase 5 confirmation)* — file at `paths.research_queries_dir / YYYY-MM-DD-<topic-slug>.md` with fire-task pinned

Chat reply summarizes all artifacts in <300 words.

## When NOT to fire

- Mid-session before substantive work has accumulated
- Conversation only (no decisions, no shifts, no completions)
- Operator explicitly says "don't capture this session"
