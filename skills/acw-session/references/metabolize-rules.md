# Metabolize Rules — Phase 3

What gets metabolized, what doesn't, and why. The principle: **prune stale narrative, never lose decision history**.

> **Path resolution.** This document uses `paths.X` shorthand (resolves from `acw-state.yaml::paths::X`) and `section_conventions.X` shorthand (resolves from the target file's frontmatter).

---

## Files that get metabolized

These hold current-state narrative. Stale entries get auto-updated or proposed for removal.

| File | What metabolizes | What does not |
|---|---|---|
| `paths.tasks_status` | `section_conventions.pending` items completed in code → move to the new Done block. Pending items superseded by decision → propose move to Parked. Parked items now in scope → propose move to Pending. | Done section's dated entries (history). Active Pending items still in flight. |
| `paths.decisions_log::section_conventions.open_questions` | Questions resolved this session → move to `section_conventions.decisions`. | Active open questions. |
| `paths.decisions_log::section_conventions.constraints` | Constraints whose underlying cause was fixed → propose removal with rationale. | Active constraints. |
| `paths.glossary` | Terms no longer referenced anywhere in the project → propose deprecation marker (do not delete). | Active terms. External vocabulary canons governed elsewhere. |
| Instance hard-rules file | Rules made obsolete by code changes → propose deprecation marker. | Active hard rules. |
| `paths.research_state` | Conception fields that drifted from current architecture → update with reference to the evolution entry that justifies. | Anything not justified by an evolution entry. |

---

## Files that NEVER get metabolized

Append-only history. Past entries are factual record, not stale.

- `paths.build_log` past entries — historical record of what was built when
- `paths.incidents` — append-only ledger
- `paths.evolution` past entries — each is a moment in time; supersede by appending a new entry
- Session captures already written under `paths.session_captures_dir`
- `paths.decisions_log::section_conventions.decisions` past entries — superseded entries get a `**Superseded by:**` line, never get deleted or rewritten
- `paths.decisions_log::section_conventions.resolved` — the answer-at-the-time is preserved even if facts later changed; new facts go in a new entry

---

## Files that are out of scope for this skill

These have their own governance and the skill never touches them. The list of out-of-scope directories varies by instance; common examples:

- Project source code (e.g., `pipeline/`, `src/`, `tests/`) — PR review path
- External wiki or documentation systems — own freshness SLA
- Eval rubrics, red-team sets — eval governance
- Vendor-specific catalogs — owning team's domain
- Prompt-engineering source — eval regression on every change

Each instance documents its own out-of-scope list in `rules/instance-hard-rules.md` or a sibling rules file.

---

## How to identify stale entries

### `paths.tasks_status` Pending — auto-update path

A pending task is "done" when:

- The named artifact exists in the project (file path resolves)
- The functionality described is callable
- The task description mentions a feature now visible in published documentation or source

Move to the new Done session block.

### `paths.decisions_log::section_conventions.open_questions` — auto-update path

An open question is "resolved" when:

- The session captured a clear answer (decision form: "we will / we won't")
- A new decision in `section_conventions.decisions` references the OQ via `**Resolves:**`

Move the OQ entry into the new Decision entry's `**Resolves:**` line; remove from Open Questions.

### `paths.glossary` terms — operator-confirm path

A term is "stale" when:

- No file in the project references it
- It hasn't appeared in any session capture for 90+ days

Propose deprecation, do not delete. Operator may have context the skill doesn't.

### Instance hard-rules — operator-confirm path

A rule is "obsolete" when:

- The behavior it forbids is impossible under current code (the rule no longer protects anything)
- A newer rule supersedes it

Propose deprecation marker, do not delete. Hard rules are stop-work; deletion requires explicit operator approval.

### Runbooks (if the instance maintains them) — operator-flag path

A runbook is "stale" when:

- File paths it references no longer exist
- Procedures it describes have been replaced by automation
- The skill or tool it documents has been removed

Flag for operator review with a list of broken references. Do not edit or delete.

---

## Rules of restraint

1. **When in doubt, propose, don't execute.** Operator-confirm is the safe default. Auto-update is reserved for unambiguous moves (Pending → Done when artifact exists; OQ → resolved when a decision references it).
2. **History is not stale.** Past dated entries in any file are not candidates for metabolization, period.
3. **Cross-file references must hold.** Before marking something stale, search the rest of the scaffolding for references. A glossary term referenced in a hard rule is not stale even if the codebase doesn't use it.
4. **Decision lineage must survive.** Every superseded decision keeps a pointer to its successor. Never break the chain.
5. **The metabolize report is the audit trail.** Every action — auto-update, propose, skip — gets a line in the report appended to `paths.build_log`.
