---
scope: end
---

# Distribution Rules — Phase 2

How session content lands in scaffolding files. Strict rules per file. Each file has an "always-safe" pattern (Phase 2 may execute) and an "operator-confirm" pattern (Phase 2 must propose, not execute).

> **Path resolution.** `paths.X` resolves from `acw-state.yaml::paths::X`. `section_conventions.X` resolves from the target file's frontmatter. The skill never hardcodes a path.

> **Substrate-shape portability.** Operations on decisions and glossary branch on `acw-state.yaml::decision_tracking.mode` and `acw-state.yaml::glossary.mode`. Each mode dispatches to its own write pattern below. The skill is portable across both shapes — never assume one shape; read the mode field.

---

## Decisions

Format authority: `rules/decision-tracking.md` owns body fields, supersession marker, and id prefix convention (`D-{project.code}-NNN` or `D-NNN`). Wiki frontmatter authority: `acw-state.yaml::decision_tracking.entry_frontmatter_required / status_values / kind_values`. The skill performs the operations; format details come from the authoritative source.

### Mode: `single-file` (canonical default)

Substrate at `paths.decisions_log`; sections resolved via `section_conventions.{decisions, open_questions, constraints, resolved}`.

**Always-safe writes:**
- Append a new decision to the decisions section (next id; auto-scan).
- Move a resolved Open Question into the decisions section with a `**Resolves:**` line preserving the OQ id.
- Append a new constraint (next `C-` id) or resolved question.

**Operator-confirm writes:** mark a decision superseded (add marker on prior, create new entry); remove a constraint (underlying issue fixed).

**Never:** edit a prior decision's text in place. Auto-add an OQ without operator phrasing.

### Mode: `wiki`

Substrate at `paths.{decisions_entries_dir, decisions_open_questions_dir, decisions_constraints_dir}`; thin INDEX at `paths.decisions_index`.

**Always-safe writes:**
- New decision: file at `<decisions_entries_dir>/<id>-<slug>.md` where `slug = slugify(title)[:60]`; id auto-scanned; frontmatter per `decision_tracking.entry_frontmatter_required`. INDEX placement: `## Decisions` section.
- Resolved OQ: move file from `decisions_open_questions_dir` → `decisions_entries_dir`, **preserving the OQ id as filename id** (the file stays `OQ-NNN-<slug>.md`, NOT renamed to `D-NNN`); update frontmatter `kind: decision`, `status: resolved`, add `resolves` + `resolved_by_decision`. INDEX placement: **stays in `## Open Questions`** with the entry annotated `_(status: resolved)_` and the link updated to the new `entries/` path. This preserves OQ traceability — the `## Decisions` section is reserved for `D-NNN` entries authored as decisions from the start, not OQ resolution records.
- New OQ → `decisions_open_questions_dir` (`kind: open-question`, `status: open`). INDEX placement: `## Open Questions` with `_(status: open)_`.
- New constraint → `decisions_constraints_dir` (`kind: constraint`, `status: accepted`). INDEX placement: `## Constraints`.
- Regenerate INDEX after any write via `decision_tracking.regenerate_index_cmd` (or append one line directly if unset). **Note:** in wiki mode, `tools/migrate_to_wiki.py` is migration-only (single-file → wiki shape); it does NOT regenerate INDEX from existing wiki entries. Until a regenerate-mode lands in that tool, INDEX maintenance in wiki mode is by direct edit (append the link line under the correct section per the placement rules above).

**Operator-confirm writes:** mark a decision superseded (edit prior frontmatter + create new entry + regenerate INDEX); mark a constraint resolved.

**Never:** edit a prior entry's body text in place. Past entries are append-only in spirit.

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

Format authority: `rules/instance-hard-rules.md` (template). Mode-invariant — hard rules are a single file regardless of decision/glossary mode. Id prefix follows the same convention as decisions (`HR-{project.code}-NNN` or `HR-NNN`).

**Always-safe writes:** append a new rule at the bottom of the appropriate section with text + rationale.

**Operator-confirm writes:** modify an existing rule (propose with diff; record in `paths.evolution`); mark a rule deprecated.

**Never:** auto-delete a hard rule.

---

## `paths.evolution`

Shape is mode-invariant.

**Always-safe writes:** prepend a new entry at the top (newest first), format: `### YYYY-MM-DD — <Title>` with `**Changed:**`, `**Replaced:**`, `**Justified by:**`, optionally `**Stale in template:**`.

**Never:** edit any prior entry. Skip the entry if the conception didn't shift but a build session happened — that goes to `paths.build_log`.

---

## `paths.tasks_status`

Format authority: `rules/task-tracking.md` (Pending-only canonical since v0.9.3; archive shape `<paths.archives_dir>/tasks-status/YYYY-MM.md` since v0.9.5; session-block format). Pre-v0.10.0 instances resolve `archives_dir` to `archives` at workspace root; v0.10.0+ resolves to `.acw/archives`.

**Always-safe writes (live file):** append new Pending task; remove completed task as part of writing the session block to archive.

**Always-safe writes (archive `<paths.archives_dir>/tasks-status/YYYY-MM.md`):** append a dated session block to the current month's archive file (create file + folder if absent with archive frontmatter; register in `acw-state.yaml::meta_layer` on first write via Phase 2 symmetric archive-registration).

**Never:** write to a Done or Parked section in the live file (sections don't exist in v0.9.3+); touch prior dated entries in archive; auto-delete from Pending without an explicit completion signal.

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
