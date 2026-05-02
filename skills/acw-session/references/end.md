# end

Session-end verb. Five-phase pass: capture, distribute, metabolize, optional synapse log, optional research prompt. Edits substrate per discipline rules. Bulk of specialist-work logic lives in the sub-references in this directory.

## After the spine

The orchestrator's spine has resolved configuration, paths, inbox state, and recent capture paths. The end verb runs Phases 1–3 always; Phase 4 conditional on `synapse_log_path`; Phase 5 conditional on operator confirmation.

## Phase 1 — Capture

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

## Phase 2 — Distribute

**Distribution scope rule (load-bearing).** Distribute only project-specific findings into this project's substrate. A finding qualifies as project-specific when it shapes how *this* project will be built, decided, or used going forward. Findings about another project, a cross-cutting framework, or operator-personal infrastructure do NOT enter this project's substrate.

For each project-specific candidate from Phase 1, edit the appropriate scaffolding file. Strict rules in `references/distribution-rules.md`. Summary:

- New decisions → append to `paths.decisions_log` under `section_conventions.decisions` with next `D-{project.code}-NNN` id (or `D-NNN` if absent).
- Resolved open questions → move from `section_conventions.open_questions` to `section_conventions.decisions` with resolution note.
- New constraints → append to `section_conventions.constraints`.
- Conceptual shifts → prepend new entry to `paths.evolution`.
- Term additions / redefinitions → edit `paths.glossary`.
- New hard rules → append to instance hard-rules file with `HR-{project.code}-NNN` id (or `HR-NNN` if absent).
- **`paths.tasks_status` — full session block** under `section_conventions.done` per `rules/task-tracking.md`. Format in `references/distribution-rules.md`.
- New tasks → append to `section_conventions.pending`.
- Newly parked → move to `section_conventions.parked` with reason.
- New sources → append to `paths.sources`.
- **New incidents → append one JSONL line per incident to `paths.incidents`.** Append-only; never edit past lines. See `rules/incident-tracking.md` and `references/incidents-format.md`.
- Build progress narrative → append entry (newest first) to `paths.build_log`.

`paths.research_state` updates only when a Phase 1 finding actually changes the conception (architectural shift, scope change, abstraction-layer change, tool-surface change). Routine work does NOT update research-state.

**Auto-load list maintenance.** If Phase 2 creates a new top-level substrate file that meets the substrate-worthy test in `references/distribution-rules.md`, append its path to `acw-state.yaml::auto_load_at_session_start` via `manifest.append`. Additive only; removal requires a decision-log entry.

**Manifest classification (conditional).** If this instance uses the three-layer manifest (template_layer / instance_layer / meta_layer non-empty), surface a classification prompt for every new file Phase 2 creates at a tracked path: **"template_layer / instance_layer / meta_layer?"** Default to `instance_layer` (asymmetry rationale in `rules/manifest-discipline.md`). Operator answer appends via `manifest.append`. Additive only. If blocks absent or empty, skip silently.

**Host entry file maintenance.** If host-specific entry files exist (declared via `host:` in `acw-state.yaml::instance_layer`, or conventionally named per a host's mechanism), surface a proposed edit when substrate shifts that the entry file should reflect: a file entered or left `auto_load_at_session_start`, a hard-rule principle was added or retired, a manifest layer for a class of files changed, the bookend skill names changed, or the project's "where things live" map shifted. Operator approves before the edit lands. Skip silently if no host entry files.

**Canonical-edit detection.** Compute the intersection of `auto_load_at_session_start` and `template_layer`. Files in this intersection are **canonical** — they propagate downstream from a publishing instance, or came from upstream and are read-only locally.

For each canonical file edited this session (detect via `git diff --name-only HEAD` against the file's path, scoped to this session's commit window), branch on `is_canonical_source`:

- **`is_canonical_source: true`** (publishing instance, e.g., ACW itself): surface *"Canonical file `<path>` was edited this session. Confirm: should `acw-state.yaml::version` bump? After version bump, push to GitHub before session end so downstream instances pick up the change on their next /acw-instance upgrade run."* On confirmation, append the version bump to the Phase 2 change set; otherwise leave version unchanged. Note in metabolize report whether a push is pending.
- **`is_canonical_source: false` or absent** (downstream consumer): warn *"You edited canonical file `<path>` locally. This file is template_layer content from upstream ACW; local edits won't propagate and may be overwritten on next /acw-instance upgrade. If you intended a substrate-level change, raise it upstream in ACW. If you intended an instance-specific override, place it in a sibling file (e.g., `rules/instance-extra-<name>.md`) instead."*

The skill does not block the edit. The warning surfaces the consequence.

If no canonical files were edited, skip silently.

**Cross-repo writes.** If a finding implies a write to a path outside the project repo, the path MUST be in `acw-state.yaml::cross_repo_writes`. If not, refuse and surface the path.

**Cross-project notifications.** If the session touched another project, drop a notification at the other project's `paths.inbox_dir / YYYY-MM-DD-<source-project>-<topic-slug>.md`. Frontmatter: `from_project`, `from_session_capture`, `date`, `topic`, `read: false`. Body: 5–15 lines summarizing what the receiving project should know. Append-only; never edit once written.

## Phase 3 — Metabolize

Read live state of the project. Compare against scaffolding. Find stale items per `references/metabolize-rules.md`. Categories:

- **Auto-update** (always safe): move completed tasks from `section_conventions.pending` → the session's `section_conventions.done` block; mark resolved Open Questions as resolved when their decision is now in `section_conventions.decisions`.
- **Operator-confirm** (propose, do not execute): items that look stale but might be load-bearing — Parked items, glossary terms no longer referenced, hard rules whose context has shifted.
- **Never edit past entries**: append-only history — `paths.build_log` past entries, `paths.incidents` past lines, `paths.evolution` past entries, captures already written, Done blocks.

**Consumed-prompt sweep.** For each file at the top level of `paths.research_queries_dir`, check whether deep-research has appended findings (`## Findings` or `## Key Findings` heading present). If yes, move to `paths.research_queries_consumed_dir`. Create the consumed directory if it doesn't exist.

Output the metabolize report appended to `paths.build_log` under the new session's entry. Format in `references/metabolize-report-format.md`.

## Phase 4 — Synapse session log (conditional)

If `synapse_log_path` is set, append a session block to `<synapse_log_path>/YYYY-MM-DD.md`. Format in `references/synapse-log-format.md`. If null/absent, skip Phase 4 entirely; do not warn.

## Phase 5 — Research-prompt builder (conditional)

After Phases 1–4 complete, prompt: **"Build research prompt now? [y/N]"**

- **`n` (or no answer):** exit cleanly with summary of artifacts written.
- **`y`:** continue.

When fired:

1. **Verify recent-session context.** If the last 2–3 capture files in `paths.session_captures_dir` are not in context, read them. Don't re-read substrate already auto-loaded.
2. **Build the artifact** at `paths.research_queries_dir / YYYY-MM-DD-<topic-slug>.md` per `references/research-prompt-format.md`. Frontmatter MUST include `append_findings_to_self: true`. Three tracks:
   - **Track A** — session-specific design questions (from Phase 1 §5 unresolved questions)
   - **Track B** — project-wide improvement opportunities (from cross-substrate gaps in Phases 2–3)
   - **Track C** — standing substrate and scaffolding evolution (always present, never primary driver)
3. **Pin the fire-task** at the top of `paths.tasks_status` `section_conventions.pending` with `🔬 [FIRE AT NEXT SESSION START]`.
4. **Append a one-line entry to `paths.build_log`** under the current session's metabolize report.

If both Track A and Track B are empty, skip writing the artifact and pinning the fire-task. Track C alone never justifies firing.

## Output

Up to five artifacts per invocation:

1. **Session capture** — file at `paths.session_captures_dir / YYYY-MM-DD--<topic-slug>.md`
2. **Scaffolding edits** — targeted updates to substrate files per Phase 2 rules
3. **Metabolize report** — section appended to `paths.build_log`
4. **Synapse session log** *(conditional on `synapse_log_path`)*
5. **Research-prompt artifact** *(conditional on Phase 5 confirmation)*

Chat reply summarizes all artifacts in <300 words.

## When NOT to fire (verb-specific)

- Mid-session before substantive work has accumulated.
- Conversation only (no decisions, no shifts, no completions).
- Operator explicitly says "don't capture this session."
