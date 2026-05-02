# Gotchas — capture-and-metabolize

## Failure modes and what to do instead

> **Path resolution.** Throughout, `paths.X` resolves from `acw-state.yaml::paths::X` per the SKILL.md preamble. `section_conventions.X` resolves from the target file's frontmatter.

- **Pretending session content is decision content** → If the session contained discussion that did not resolve into a decision (e.g., the operator thinking out loud before deciding), do NOT promote it to `paths.decisions_log`. The session capture file holds the discussion; only resolved positions go to the decision log.

- **Auto-deleting glossary terms** → If a term in `paths.glossary` no longer appears in code, runbooks, or other scaffolding, do NOT auto-delete. Propose for operator review. Terms can be load-bearing in conversation context that the codebase doesn't reflect.

- **Touching external vocabulary canons thinking they're the project glossary** → They are not. External canons (e.g., a customer-voice canon governed elsewhere) are distinct from `paths.glossary`. Most session-derived term changes go to `paths.glossary`. External canon changes are rarer and require explicit operator approval per their own rules.

- **Rewriting past evolution entries** → `paths.evolution` is append-only newest-first. Each entry is a moment in time. If an old entry is "wrong," append a new entry that supersedes it; do not edit the old entry.

- **Stripping context from session capture** → When cleaning the transcript, err on keeping more than less. The session file is the historical record. Keep verbatim quotes for decisions and operator directives. Strip only pure tool noise (e.g., empty bash outputs, system reminders, redundant tool-result echoes that the agent already summarized).

- **Metabolizing the Done section of `paths.tasks_status`** → Done accumulates dated entries. Old entries are not stale; they are history. Do not collapse or delete them. If Done becomes long, the operator can manually archive to a dated `tasks-status-YYYY-Q.md` file (not within scope of this skill).

- **Treating Parked items as stale** → Parked items are intentionally deferred, not forgotten. Do not auto-remove them. If a Parked item appears to have been silently overtaken (e.g., the underlying need was solved differently), propose for operator review with the reasoning, do not execute.

- **Adding decisions without a date** → Every decision entry MUST include the date. Use today's actual date as established by the session context, not a placeholder.

- **Distributing into `paths.build_log` past entries** → `paths.build_log` is append-only newest-first. New entries go on top. Past entries are historical record; do not edit them.

- **Skipping the metabolize report when nothing changed** → Always append the report, even if all three subsections are empty. The empty report is itself a signal that the session was clean and nothing drifted.

- **Confusing the Open Questions section of decision-log with TODO** → Open Questions are decisions awaiting operator call. They are not "things to do." Do not auto-resolve them or move to Pending; only move when the session captured an actual resolution.

- **Posting to `paths.research_state` for routine work** → research-state only updates when the **conception** changed. Build sessions that fix a bug, add a feature within scope, or update narrative content do NOT change conception. Only architectural shifts, tool-surface changes, scope changes, and abstraction-layer changes update research-state.

- **Editing project source code or other governed surfaces** → Out of scope for this skill. Source code, tests, external wiki, eval rubrics, and so on each have their own governance (PR review, lint, eval regression). The skill is governance for narrative scaffolding, not for source.

- **Capturing a session with no substance** → If the session was conversational with no decisions, shifts, or task completions, do not write a session capture. Print a short note: "session was conversational; nothing to capture." The exception is when the operator explicitly invoked the skill — write a minimal capture noting the absence so the invocation is itself logged.

- **Forgetting to update Pending when a decision created new work** → A decision that says "we will build X" implies X is a new pending task. Capture both: the decision AND the corresponding task in `paths.tasks_status` `section_conventions.pending`.

- **Treating `paths.incidents` as never-touch instead of append-only** → Past lines are never edited (immutable). New lines ARE written by Phase 2 distribute when the session surfaced a bug, governance leak, environment-state surprise, wrong-assumption, scale-vulnerability, or earn-by-incident-evidence. Empty incidents file after a debug-heavy session is a missed write, not clean output. Detection rules in `references/incidents-format.md`.

- **Skipping Phase 4 when synapse_log_path is set** → Phase 4 writes to `<synapse_log_path>/YYYY-MM-DD.md` even though the session capture already records everything. The synapse log is the operator's cross-project day-index. If you skip Phase 4, the operator has to fire a separate session-logger to recover. (When `synapse_log_path` is null, skip Phase 4 silently — that's correct.)

- **Writing tasks-status as task-by-task moves instead of a session block** → The Phase 2 tasks-status rule writes a *full session block* under `section_conventions.done`, not individual line items. The session block matches the format used by prior Sessions in the file. Format in `references/distribution-rules.md` under "Session-block format."

- **Phase 5 builds a prompt with no Track A or Track B content** → If both tracks are empty, do NOT write the artifact and do NOT pin a fire-task. Track C alone never justifies firing. Print "No research-worthy material; Track C alone does not justify firing" and exit Phase 5 cleanly.

- **Phase 5 overwrites a prior fire-task that the operator hadn't fired yet** → If a `🔬 [FIRE AT NEXT SESSION START]` task is already pinned at the top of `paths.tasks_status` `section_conventions.pending`, the new fire-task is appended below it (or the operator is asked which to keep). Two queued research artifacts is acceptable; silent overwrite is not.

- **Re-reading substrate at the start of Phase 5** → Don't. Phases 1–4 already read the substrate; it's in context. The only conditional read in Phase 5 is "load the last 2–3 session captures if not already in context" — and that's only because those files might have been written by *prior* sessions and not loaded this session.

- **Writing incidents with vague lessons** → "Don't do X again" is weak. Strong lessons cite a codification: "Codified in D-NNN," "Added HR-NNN," "Added scrub-scope rule to capture-and-metabolize Phase 3." If the lesson can't cite a structural change, the incident might not be incident-worthy — or the lesson hasn't been fully extracted yet. In that case, capture the incident and flag the missing codification as an open question (Phase 1 §5).

- **Hardcoding a path** → Never. Use `paths.X` shorthand throughout this skill's content. Hardcoded paths break portability across instances. If you need a new substrate location, add it to `acw-state.yaml::paths::<key>` (and document the canonical default in `rules/manifest-discipline.md` if the key is intended to be standard across instances).
