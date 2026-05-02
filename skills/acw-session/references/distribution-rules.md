# Distribution Rules — Phase 2

How session content lands in scaffolding files. Strict rules per file. Each file has an "always-safe" pattern (Phase 2 may execute) and an "operator-confirm" pattern (Phase 2 must propose, not execute).

> **Path resolution.** Throughout this document, file references use the `paths.X` shorthand (resolves from `acw-state.yaml::paths::X` per `rules/manifest-discipline.md`) and `section_conventions.X` shorthand (resolves from the target file's frontmatter). The skill never hardcodes a path.

---

## `paths.decisions_log`

### Always-safe writes

- **Append a new decision** to `section_conventions.decisions` with the next id (`D-{project.code}-NNN` if `project.code` is set, else `D-NNN`). Look at existing entries to determine the next number. Required fields per existing entries: `**Date:**`, `**Decision:**`, `**Rationale:**`, `**Source:**`. The session capture file must reference the new decision id in its frontmatter.
- **Move a resolved Open Question** from `section_conventions.open_questions` to `section_conventions.decisions`. The OQ id is preserved as a `**Resolves:**` line on the new decision entry.
- **Append a new constraint** to `section_conventions.constraints` with C-NNN id.
- **Append a new resolved question** to `section_conventions.resolved` when the session captured a fact-verification answer (not a decision — facts about how the project actually works).

### Operator-confirm writes

- **Mark a decision as superseded.** Don't delete; add `**Superseded by:** <new id> (YYYY-MM-DD)` to the prior entry and create the new entry. Propose this for operator review with the rationale.
- **Remove a constraint** because the underlying issue was fixed. Propose with rationale; do not auto-delete.

### Never

- Edit a prior decision's text in place. Decisions are append-only in spirit.
- Auto-add an Open Question without operator phrasing. Open Questions are operator-surfaced, not skill-surfaced.

---

## `paths.evolution`

### Always-safe writes

- **Prepend a new entry** at the top of the file (newest first), using the format documented in the file's own header: `### YYYY-MM-DD — <Title>` with `**Changed:**`, `**Replaced:**`, `**Justified by:**`, optionally `**Stale in template:**`.

### Never

- Edit any prior entry. Each is a moment in time.
- Skip the entry if the conception didn't shift but a build session happened — that goes to `paths.build_log`, not evolution.

---

## `paths.glossary`

### Always-safe writes

- **Append a new term** under the file's terms section in alphabetical-ish order or at the bottom with related terms.

### Operator-confirm writes

- **Redefine a term**: do not delete prior definition. Add inline note `**Redefined YYYY-MM-DD:**` followed by the new wording. Propose for review.
- **Mark a term deprecated** when no longer in use anywhere. Add `**Deprecated YYYY-MM-DD:**` inline. Don't delete; propose for review.

### Never

- Touch any external vocabulary canon (e.g., a customer-voice canon governed by separate rules). The project glossary at `paths.glossary` is project-internal.

---

## Instance hard-rules file (declared as instance_layer)

### Always-safe writes

- **Append a new rule** at the bottom of the appropriate hard-rules section with rule text + rationale. Use `HR-{project.code}-NNN` if `project.code` is set, else `HR-NNN`.

### Operator-confirm writes

- **Modify an existing rule** when the session changed its scope or wording. Propose with the diff for operator review. After approval, update `paths.evolution` to record the change.
- **Mark a rule deprecated** with `**Deprecated YYYY-MM-DD:**`. Don't delete.

### Never

- Auto-delete a hard rule. Hard rules are stop-work-if-violated; deletion requires explicit operator confirm.

---

## `paths.tasks_status`

### Always-safe writes

- **Write a full session block at the top of `section_conventions.done`.** This is the load-bearing tasks-status update. Format below. Append the new block above prior session blocks (newest first within the Done section).
- **Move a task from `section_conventions.pending` to the new Done block** as part of writing the session block. Individual line items move into the session block rather than being listed separately.
- **Append a new pending task** to `section_conventions.pending` when the session created new work.
- **Append a new parked item** to `section_conventions.parked` when the session deferred something with reason.
- **Move a Pending item to Parked** if the session explicitly deferred it.

### Session-block format

The session block written to the Done section matches the existing pattern used by prior session blocks in the project. Specifically:

```markdown
### YYYY-MM-DD — Session N — <topic phrase from session capture frontmatter>

- <Decision id appended to log>: <one-line summary> — <file paths or refs>
- `path/to/file.py` — <one-line description of change>
- <Hard rule id added>: <short summary>
- <Smoke test result | bug encountered + fix | blocker resolved | other narrative bullet>
- Capture-and-metabolize ran end-of-session: session capture written to `<paths.session_captures_dir>/<file>.md`; <decisions appended>; <evolution updated>; <research-prompt artifact path if Phase 5 fired>.
```

Rules for the session block:
- The first line is `### YYYY-MM-DD — Session N — <topic>`. `N` is determined by counting prior session blocks in Done (the next block is N+1).
- Every bullet is one line, scannable. No multi-paragraph prose.
- Cite decision IDs, hard rule IDs, constraint IDs, open-question IDs inline so the operator can cross-reference without leaving the file.
- File paths use forward slashes and are written as backticked code spans.
- Last bullet always notes that capture-and-metabolize ran, with paths to the session capture file and any research-prompt artifact.

### Operator-confirm writes

- **Remove a Parked item** as no longer relevant. Propose with rationale; do not auto-delete.
- **Move a Parked item to Pending** when the session brings it back into scope.

### Never

- Touch the Done section's prior dated entries. They are history.
- Auto-delete from Pending without confirming the task is done or moved.

---

## `paths.build_log`

### Always-safe writes

- **Prepend a new entry** at the top (newest first). Format: `## YYYY-MM-DD — <Title>` with a paragraph describing what was built, paths touched, and any new decisions/runbooks/etc.
- **Append the metabolize report** to the bottom of the new entry. Format defined in `metabolize-report-format.md`.

### Never

- Edit prior entries.

---

## `paths.research_state`

### Always-safe writes

- **Update conception fields** (scope, application, exclusions) only when the session explicitly changed them.
- **Update architecture or tool-surface fields** when tools are added, removed, or repurposed.
- **Bump architecture version** when a major revision is finalized.
- **Update dependencies** when blockers shift.

### Operator-confirm writes

- **Move legacy items to a new `legacy_v_X` block** when superseding architecture.

### Never

- Edit research-state for build sessions that didn't shift conception. Build narrative goes to `paths.build_log`.

---

## `paths.sources`

### Always-safe writes

- **Append a new source** under the appropriate section.

### Never

- Remove a prior source even if it became less relevant. Sources are history.

---

## Cross-file consistency rules

- If a new decision in `paths.decisions_log` introduces a new term, the term must also land in `paths.glossary`.
- If a new decision creates new pending work, the work must also appear in `paths.tasks_status` `section_conventions.pending`.
- If `paths.evolution` gets a new entry, the corresponding decision-log entry should reference it via `**Recorded in:**` (or equivalent).
- If `paths.research_state` updates its conception, `paths.evolution` must have a new entry justifying the update.
