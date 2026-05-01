# Metabolize Rules — Phase 3

What gets metabolized, what doesn't, and why. The principle: **prune stale narrative, never lose decision history**.

---

## Files that get metabolized

These hold current-state narrative. Stale entries get auto-updated or proposed for removal.

| File | What metabolizes | What does not |
|---|---|---|
| `tasks-status.md` | `Pending` items completed in code → move to `Done`. `Pending` items superseded by decision → propose move to `Parked`. `Parked` items now in scope → propose move to `Pending`. | `Done` section's dated entries (history). Active `Pending` items still in flight. |
| `decisions/decision-log.md::Open Questions` | Questions resolved this session → move to `## Decisions`. | Active open questions. |
| `decisions/decision-log.md::Constraints & Gotchas` | Constraints whose underlying cause was fixed → propose removal with rationale. | Active constraints. |
| `glossary.md` | Terms no longer referenced anywhere in the project → propose deprecation marker (do not delete). | Active terms. Customer-voice canon (`wiki/terms.yaml`). |
| `rules/instance-hard-rules.md` | Rules made obsolete by code changes → propose deprecation marker. | Active hard rules. |
| `runbooks/*.md` | Runbooks pointing at code paths that no longer exist → flag for operator review. | Runbooks describing extant procedures. |
| `research/research-state.yaml` | Conception fields that drifted from current architecture → update with reference to the evolution.md entry that justifies. | Anything not justified by an evolution.md entry. |

---

## Files that NEVER get metabolized

Append-only history. Past entries are factual record, not stale.

- `build-log.md` past entries — historical record of what was built when
- `incidents.jsonl` — append-only ledger
- `research/evolution.md` past entries — each is a moment in time; supersede by appending a new entry
- `research/sessions/*.md` — once written, frozen
- `decisions/decision-log.md::Decisions` past entries — superseded entries get a `**Superseded by:**` line, never get deleted or rewritten
- `decisions/decision-log.md::Resolved Questions` — the answer-at-the-time is preserved even if facts later changed; new facts go in a new entry

---

## Files that are out of scope for this skill

These have their own governance. Do not touch.

- `pipeline/` — source code; PR review path
- `tests/` — source code
- `wiki/pages/` and `wiki/terms.yaml` — wiki_lint + freshness SLA
- `wiki/decision-tables/` — same as wiki
- `eval/rubrics/` — eval governance
- `eval/red-team/injection-set.yaml` — eval governance
- `catalogs/14-api-catalog.yaml` — platform engineering's domain
- `pipeline/prompts/*.md` — prompt-engineering governance (eval regression on every change)

---

## How to identify stale entries

### `tasks-status.md::Pending` — auto-update path

A pending task is "done" when:

- The named artifact exists in the project (file path resolves)
- The functionality described is callable
- The task description mentions a feature now visible in `README.md` or `pipeline/`

Move to Done. Add today's date heading to Done if not already there.

### `decisions/decision-log.md::Open Questions` — auto-update path

An open question is "resolved" when:

- The session captured a clear answer (decision form: "we will / we won't")
- A new decision in `## Decisions` references the OQ via `**Resolves:**`

Move the OQ entry into the new Decision entry's `**Resolves:**` line; remove from `## Open Questions`.

### `glossary.md` terms — operator-confirm path

A term is "stale" when:

- No file in `pipeline/`, `runbooks/`, `decisions/`, `research/`, or `rules/` references it
- It hasn't appeared in any session capture for 90+ days

Propose deprecation, do not delete. Operator may have context Claude doesn't.

### `rules/instance-hard-rules.md` — operator-confirm path

A rule is "obsolete" when:

- The behavior it forbids is impossible under current code (the rule no longer protects anything)
- A newer rule supersedes it

Propose deprecation marker, do not delete. Hard rules are stop-work; deletion requires explicit operator approval.

### `runbooks/*.md` — operator-flag path

A runbook is "stale" when:

- File paths it references no longer exist
- Procedures it describes have been replaced by automation
- The skill or tool it documents has been removed

Flag for operator review with a list of broken references. Do not edit or delete.

---

## Rules of restraint

1. **When in doubt, propose, don't execute.** Operator-confirm is the safe default. Auto-update is reserved for unambiguous moves (Pending → Done when artifact exists; OQ → resolved when D-NNN references it).
2. **History is not stale.** Past dated entries in any file are not candidates for metabolization, period.
3. **Cross-file references must hold.** Before marking something stale, search the rest of the scaffolding for references. A glossary term referenced in a hard rule is not stale even if the codebase doesn't use it.
4. **Decision lineage must survive.** Every superseded decision keeps a pointer to its successor. Never break the chain.
5. **The metabolize report is the audit trail.** Every action — auto-update, propose, skip — gets a line in the report appended to `build-log.md`.
