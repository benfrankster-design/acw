---
scope: end
---

# Metabolize Rules — Phase 3

What gets metabolized, what doesn't, and why. The principle: **prune stale narrative, never lose decision history**.

> **Path resolution.** `paths.X` resolves from `acw-state.yaml::paths::X`. `section_conventions.X` from target file frontmatter.

> **Substrate-shape portability.** Decision and glossary operations branch on `acw-state.yaml::decision_tracking.mode` and `glossary.mode`. The metabolize logic is the same per principle; the *write mechanics* differ per mode. Read the mode field; never assume one shape.

---

## Files that get metabolized

These hold current-state narrative. Stale entries get auto-updated or proposed for removal.

| File / surface | What metabolizes | What does not |
|---|---|---|
| `paths.tasks_status` | Pending items completed → write dated session block to `tasks-status-YYYY-Q*.md` archive AND remove the item from Pending. Pending items superseded by decision → propose either removal (truly stale) or move to `inbox/ideas/` (deferred-but-keep). | Archive file's dated entries (history). Active Pending. |
| Decisions: open questions | Questions resolved this session → move to decisions surface. | Active open questions. |
| Decisions: constraints | Constraints whose underlying cause was fixed → propose removal/resolution. | Active constraints. |
| Glossary | Terms no longer referenced → propose deprecation marker (do not delete). | Active terms. External vocabulary canons governed elsewhere. |
| Instance hard-rules file | Rules made obsolete by code changes → propose deprecation marker. | Active hard rules. |
| `paths.research_state` | Conception fields drifted from current architecture → update with reference to the justifying evolution entry. | Anything not justified by an evolution entry. |

---

## Files that NEVER get metabolized

Append-only history. Past entries are factual record, not stale.

- `paths.build_log` past entries
- `paths.incidents` — append-only ledger
- `paths.evolution` past entries — supersede by appending, not editing
- Session captures already written
- Decisions past entries (regardless of mode) — superseded entries get a supersession marker, never deleted or rewritten
- Resolved questions (single-file mode `section_conventions.resolved` / wiki mode `status: resolved` entries) — answer-at-the-time is preserved

---

## Files that are out of scope for this skill

Project source, external wiki, eval rubrics, vendor catalogs. Each instance declares its own out-of-scope list in `rules/instance-hard-rules.md`.

---

## How to identify stale entries

### `paths.tasks_status` Pending — auto-update path

A pending task is "done" when:
- The named artifact exists (file path resolves)
- The functionality described is callable
- The task description mentions a feature now in published docs or source

Move to the new Done session block.

### Decisions: open questions — auto-update path

An open question is resolved when the session captured a clear answer AND a new decision references the OQ via `**Resolves:**` (single-file mode) or `resolves:` frontmatter (wiki mode).

**Single-file mode:** move OQ entry from `section_conventions.open_questions` to `section_conventions.decisions` as part of the new Decision's `**Resolves:**` line; remove the standalone OQ entry.

**Wiki mode:** move the OQ file from `decisions_open_questions_dir` to `decisions_entries_dir`. Update its frontmatter (`kind: decision`, `status: resolved`, `resolved_by_decision: <new D id>`, `updated: <today>`). Preserve the OQ id as the filename id — resolved entries carry their OQ id. Regenerate INDEX.

### Glossary terms — operator-confirm path

A term is stale when:
- No file in the project references it
- It hasn't appeared in any session capture for 90+ days

**Single-file mode:** propose adding `**Deprecated YYYY-MM-DD:**` inline. Do not delete.

**Wiki mode:** propose editing the term entry's frontmatter `status: deprecated`. Do not delete the file. Regenerate INDEX.

Operator may have context the skill doesn't — always propose, never auto-execute.

### Instance hard-rules — operator-confirm path

A rule is obsolete when the behavior it forbids is impossible under current code, or a newer rule supersedes it.

Propose deprecation marker. Hard rules are stop-work; deletion requires explicit operator approval.

### Runbooks (if the instance maintains them) — operator-flag path

Flag stale runbooks (broken file references, replaced procedures, removed skills/tools) for operator review with a list of broken references. Do not edit or delete.

---

## Rules of restraint

1. **When in doubt, propose, don't execute.** Operator-confirm is the safe default. Auto-update is reserved for unambiguous moves.
2. **History is not stale.** Past dated entries in any file are not metabolization candidates, period.
3. **Cross-file references must hold.** Before marking something stale, search the rest of the scaffolding. A glossary term referenced in a hard rule is not stale even if the codebase doesn't use it.
4. **Decision lineage must survive.** Every superseded decision keeps a pointer to its successor. Never break the chain.
5. **The metabolize report is the audit trail.** Every action — auto-update, propose, skip — gets a line in the report appended to `paths.build_log`.
6. **Mode-portability is non-negotiable.** A metabolize step that works only on one substrate mode is a bug. Read the mode field; dispatch correctly.
