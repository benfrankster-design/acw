---
scope: end
---

# Distribution Rules — Phase 2

How session content lands in scaffolding files. Strict rules per file. Each file has an "always-safe" pattern (Phase 2 may execute) and an "operator-confirm" pattern (Phase 2 must propose, not execute).

> **Path resolution.** `paths.X` resolves from `acw-state.yaml::paths::X`. `section_conventions.X` resolves from the target file's frontmatter. The skill never hardcodes a path.

> **Substrate-shape portability.** Operations on decisions and glossary branch on `acw-state.yaml::decision_tracking.mode` and `acw-state.yaml::glossary.mode`. Each mode dispatches to its own write pattern below. The skill is portable across both shapes — never assume one shape; read the mode field.

---

## Decisions

### Mode: `single-file` (canonical default)

Decisions, open questions, constraints, resolved questions live as sections inside one file at `paths.decisions_log`. Sections resolved via `section_conventions.<name>` per that file's frontmatter (defaults: `decisions`, `open_questions`, `constraints`, `resolved`).

**Always-safe writes:**
- **Append a new decision** to `section_conventions.decisions` with the next id (`D-{project.code}-NNN` if `project.code` is set, else `D-NNN`). Scan existing entries to determine the next number. Required body fields: `**Date:**`, `**Decision:**`, `**Rationale:**`, `**Source:**`. The session capture file must reference the new decision id in its frontmatter.
- **Move a resolved Open Question** from `section_conventions.open_questions` to `section_conventions.decisions`. Preserve OQ id as a `**Resolves:**` line on the new decision entry.
- **Append a new constraint** to `section_conventions.constraints` with `C-{project.code}-NNN` id (or `C-NNN`).
- **Append a new resolved question** to `section_conventions.resolved` when the session captured a fact-verification answer (not a decision).

**Operator-confirm writes:**
- **Mark a decision as superseded.** Add `**Superseded by:** <new id> (YYYY-MM-DD)` to the prior entry; create the new entry. Propose with rationale.
- **Remove a constraint** because the underlying issue was fixed. Propose with rationale; do not auto-delete.

**Never:** edit a prior decision's text in place. Auto-add an Open Question without operator phrasing.

### Mode: `wiki`

Decisions are atomic per-entry files under `paths.decisions_entries_dir`, `paths.decisions_open_questions_dir`, `paths.decisions_constraints_dir`. A thin index at `paths.decisions_index` carries id + date + status + headline per entry.

**Always-safe writes:**
- **Create a new decision file** at `<decisions_entries_dir>/<id>-<slug>.md` where `id = D-{project.code}-NNN` (next available — scan all entries dirs for highest id, increment) and `slug = slugify(title)[:60]`. Frontmatter per `decision_tracking.entry_frontmatter_required` (typically: `id`, `title`, `date`, `status: accepted`, `kind: decision`, `updated`). Body: `# <id> — <title>` then `**Date:**`, `**Decision:**`, `**Rationale:**`, `**Source:**`, optional `**Rejected alternatives:**`. The session capture file must reference the new decision id in its frontmatter.
- **Resolve an Open Question:** move file from `decisions_open_questions_dir/<oq-id>-<slug>.md` to `decisions_entries_dir/<oq-id>-<slug>.md` (preserve the OQ id as the filename id — the resolved entry continues to carry its OQ id, not a new D id). Update frontmatter: `kind: decision`, `status: resolved`, add `resolves: <oq-id>` and `resolved_by_decision: <new D id if applicable>`. Update `updated:` to today.
- **Create a new open question** at `<decisions_open_questions_dir>/<oq-id>-<slug>.md` with `kind: open-question`, `status: open`.
- **Create a new constraint** at `<decisions_constraints_dir>/<cg-id>-<slug>.md` with `kind: constraint`, `status: accepted`.
- **Regenerate INDEX** after any of the above by invoking `decision_tracking.regenerate_index_cmd` (typically `python tools/migrate_to_wiki.py`) if declared. If `regenerate_index_cmd` is absent, append one line to `paths.decisions_index` directly under the appropriate section (Open Questions / Recent Decisions / Constraints & Gotchas) following the format of existing lines.

**Operator-confirm writes:**
- **Mark a decision as superseded.** Edit the prior entry's frontmatter: `status: superseded`, `superseded_by: <new id>`, `updated: <today>`. Create the new entry. Regenerate INDEX. Never delete the prior file.
- **Mark a constraint as resolved** (underlying issue fixed). Edit frontmatter: `status: resolved`, `updated: <today>`. Propose, don't auto-execute.

**Never:** edit a prior entry's body text in place. Past entries are append-only in spirit; corrections add a new entry that supersedes.

---

## Glossary

### Mode: `single-file` (canonical default)

Terms live as `## <term>` sections inside `paths.glossary`.

**Always-safe writes:** append a new term at the bottom (or alphabetically — match existing file convention).

**Operator-confirm writes:**
- **Redefine a term:** preserve prior definition; add `**Redefined YYYY-MM-DD:**` inline.
- **Mark deprecated:** add `**Deprecated YYYY-MM-DD:**` inline. Do not delete.

**Never:** touch external vocabulary canons (e.g., customer-voice canon).

### Mode: `wiki`

Terms are atomic per-entry files at `glossary.entries_dir/<slug>.md` with frontmatter `term`, `status`. A thin index at `glossary.index` lists term + link per entry.

**Always-safe writes:**
- **Create a new term file** at `<entries_dir>/<slug>.md` where `slug = slugify(term)`. Frontmatter: `term: "<term>"`, `status: active`. Body: `# <term>` then definition prose.
- **Regenerate INDEX** after the write by invoking `glossary.regenerate_index_cmd` if declared, else append one line to `glossary.index` directly.

**Operator-confirm writes:**
- **Redefine a term:** edit the entry's body (this is the one place body-edit is allowed for glossary; terms are living definitions, not append-only history). Add a one-line `**Redefined YYYY-MM-DD:**` note at the top of the body. Propose.
- **Mark deprecated:** edit frontmatter `status: deprecated`. Do not delete the file.

**Never:** touch external vocabulary canons.

---

## Instance hard-rules file (declared as instance_layer)

Shape is mode-invariant — hard rules live as a single file regardless of decision/glossary mode.

**Always-safe writes:** append a new rule at the bottom of the appropriate hard-rules section with rule text + rationale. Use `HR-{project.code}-NNN` if `project.code` is set, else `HR-NNN`.

**Operator-confirm writes:**
- **Modify an existing rule** when the session changed its scope or wording. Propose with diff. After approval, update `paths.evolution` to record the change.
- **Mark a rule deprecated** with `**Deprecated YYYY-MM-DD:**`. Don't delete.

**Never:** auto-delete a hard rule.

---

## `paths.evolution`

Shape is mode-invariant.

**Always-safe writes:** prepend a new entry at the top (newest first), format: `### YYYY-MM-DD — <Title>` with `**Changed:**`, `**Replaced:**`, `**Justified by:**`, optionally `**Stale in template:**`.

**Never:** edit any prior entry. Skip the entry if the conception didn't shift but a build session happened — that goes to `paths.build_log`.

---

## `paths.tasks_status`

Tasks-status is a work-queue primitive, not knowledge-graph. **Pending-only** (v0.9.3+ canonical per `rules/task-tracking.md`). No Done section. No Parked section. Completed work archives on completion to `tasks-status-YYYY-Q*.md`. Deferred ideas route to `inbox/ideas/` or `decision-log`.

**Always-safe writes (live file):**
- **Append a new pending task** to the Pending section when the session created new work.
- **Remove a completed task from the Pending section** as part of writing the session block to the archive (next bullet). The completed task does not move to a Done section — Done lives in the archive file only.

**Always-safe writes (archive file `tasks-status-YYYY-Q*.md`):**
- **Append a dated session block** at the bottom of the current quarter's archive file (or under a relevant date heading; newest content at file end is fine since archive is read on demand). Format below. Create the archive file if it doesn't exist (frontmatter per `rules/task-tracking.md`). Register the new archive in `acw-state.yaml::meta_layer` (Phase 2 symmetric archive-registration check).

### Session-block format (written to archive)

```markdown
### YYYY-MM-DD — Session N — <topic phrase>

- <Decision id>: <one-line summary> — <file paths or refs>
- `path/to/file.py` — <one-line description of change>
- <Hard rule id added>: <short summary>
- <Smoke test result | bug encountered + fix | blocker resolved>
- Capture-and-metabolize ran: session capture at `<paths.session_captures_dir>/<file>.md`; <decisions appended>; <research-prompt artifact path if Phase 5 fired>.
```

Rules: bullets are one line each. Cite IDs inline. Forward-slash paths in backticks. Last bullet notes capture-and-metabolize ran.

**Never:**
- Write to a Done section in `tasks-status.md` (the section doesn't exist in v0.9.3+ shape).
- Write to a Parked section in `tasks-status.md` (the section doesn't exist in v0.9.3+ shape; deferred ideas → `inbox/ideas/` instead).
- Touch prior dated entries in the archive file. Archive is append-only.
- Auto-delete from Pending without an explicit completion signal (artifact exists, functionality callable, etc.).

---

## `paths.build_log`

Append-only narrative. Shape is mode-invariant.

**Always-safe writes:** prepend a new entry at the top. Format: `## YYYY-MM-DD — <Title>` paragraph describing what was built, paths touched, decisions/runbooks. Append the metabolize report to the bottom of the new entry per `metabolize-report-format.md`.

**Never:** edit prior entries.

---

## `paths.research_state`

Always-safe: update conception fields only when the session explicitly changed them. Bump architecture version on major revision.

Operator-confirm: move legacy items to a new `legacy_v_X` block when superseding architecture.

Never: edit for build sessions that didn't shift conception.

---

## `paths.sources`

Always-safe: append under the appropriate section.

Never: remove a prior source.

---

## `paths.incidents`

Append-only JSONL. One line per incident. Schema in `incidents-format.md`.

**Never:** edit past lines.

---

## Cross-file consistency rules

These hold across both modes — read in terms of the operations above:

- If a new decision introduces a new term, the term must also land in glossary (per the active glossary mode).
- If a new decision creates new pending work, the work must also appear in `paths.tasks_status` `section_conventions.pending`.
- If `paths.evolution` gets a new entry, the corresponding decision should reference it via `**Recorded in:**` (single-file mode body field, or wiki-mode frontmatter `recorded_in:`).
- If `paths.research_state` updates its conception, `paths.evolution` must have a new entry justifying the update.
