# Distribution Rules — Phase 2

How session content lands in scaffolding files. Strict rules per file. Each file has an "always-safe" pattern (Phase 2 may execute) and an "operator-confirm" pattern (Phase 2 must propose, not execute).

---

## `decisions/decision-log.md`

### Always-safe writes

- **Append a new decision** to `## Decisions` with the next D-NNN id (look at existing entries, increment by 1). Required fields per existing entries: `**Date:**`, `**Status:**`, `**Decision:**`, `**Why/Rationale:**`, `**Rejected alternatives:**` (if any). The session capture file must reference the new D-NNN id in its frontmatter.
- **Move a resolved Open Question** from `## Open Questions` to `## Decisions`. The OQ-NNN id is preserved as a `**Resolves:**` line on the new decision entry.
- **Append a new constraint** to `## Constraints & Gotchas` with C-NNN id.
- **Append a new resolved question** to `## Resolved Questions` when the session captured a fact-verification answer (not a decision — facts about how the platform actually works).

### Operator-confirm writes

- **Mark a decision as superseded.** Don't delete; add `**Superseded by:** D-MMM (YYYY-MM-DD)` to the prior entry and create the new D-MMM. Propose this for operator review with the rationale.
- **Remove a constraint** because the underlying issue was fixed. Propose with rationale; do not auto-delete.

### Never

- Edit a prior decision's text in place. Decisions are append-only in spirit.
- Auto-add an Open Question without operator phrasing. Open Questions are operator-surfaced, not Claude-surfaced.

---

## `research/evolution.md`

### Always-safe writes

- **Prepend a new entry** at the top of the file (newest first), under the existing format: `## YYYY-MM-DD — <Title>` with `**What changed:**`, `**Why:**`, `**Source:**`, `**Effect on conception:**`, optionally `**Recorded in:**` (linking to the decision-log entry).

### Never

- Edit any prior entry. Each is a moment in time.
- Skip the entry if the conception didn't shift but a build session happened — that goes to `build-log.md`, not `evolution.md`.

---

## `glossary.md`

### Always-safe writes

- **Append a new term** under `## Terms` in alphabetical-ish order or at the bottom with related terms.

### Operator-confirm writes

- **Redefine a term**: do not delete prior definition. Add inline note `**Redefined YYYY-MM-DD:**` followed by the new wording. Propose for review.
- **Mark a term deprecated** when no longer in use anywhere. Add `**Deprecated YYYY-MM-DD:**` inline. Don't delete; propose for review.

### Never

- Touch `wiki/terms.yaml`. That is the customer-voice canon, governed differently.

---

## `rules/instance-hard-rules.md`

### Always-safe writes

- **Append a new HR-CP-NNN rule** at the bottom of `## Hard Rules (project-specific)` with rule text + rationale.

### Operator-confirm writes

- **Modify an existing HR-CP-NNN rule** when the session changed its scope or wording. Propose with the diff for operator review. After approval, update `research/evolution.md` to record the change.
- **Mark a rule deprecated** with `**Deprecated YYYY-MM-DD:**`. Don't delete.

### Never

- Auto-delete a hard rule. Hard rules are stop-work-if-violated; deletion requires explicit operator confirm.

---

## `tasks-status.md`

### Always-safe writes

- **Write a full session block at the top of `## Done`.** This is the load-bearing tasks-status update — it replaces what `/log-session` would write. Format below. Append the new block above prior session blocks (newest first within `## Done`).
- **Move a task from Pending to Done** as part of writing the session block. The session block IS the Done entry; individual line items move into it rather than being listed separately.
- **Append a new pending task** to `## Pending` when the session created new work.
- **Append a new parked item** to `## Parked` when the session deferred something with reason.
- **Move a Pending item to Parked** if the session explicitly deferred it.

### Session-block format

The session block written to `## Done` matches the existing pattern used by Sessions 1–9 in this project. Specifically:

```markdown
### YYYY-MM-DD — Session N — <topic phrase from session capture frontmatter>

- <Decision id appended to log>: <one-line summary> — <file paths or refs>
- `path/to/file.py` — <one-line description of change>
- <Hard rule HR-CP-NNN added>: <short summary>
- <Smoke test result | bug encountered + fix | blocker resolved | other narrative bullet>
- Capture-and-metabolize Phase 1+2 ran end-of-session: session capture written to `research/sessions/<file>.md`; <decisions appended>; <evolution updated>; <research-prompt artifact path if Phase 5 fired>.
```

Rules for the session block:
- The first line is `### YYYY-MM-DD — Session N — <topic>`. `N` is determined by counting prior session blocks in `## Done` (Session 1 was the project scaffold; the next block is Session N+1).
- Every bullet is one line, scannable. No multi-paragraph prose.
- Cite decision IDs (`D-NNN`), hard rule IDs (`HR-CP-NNN`), constraint IDs (`C-NNN`), open-question IDs (`OQ-NNN`) inline so the operator can cross-reference without leaving the file.
- File paths use forward slashes and are written as backticked code spans.
- Last bullet always notes that capture-and-metabolize ran, with paths to the session capture file and any research-prompt artifact.

### Operator-confirm writes

- **Remove a Parked item** as no longer relevant. Propose with rationale; do not auto-delete.
- **Move a Parked item to Pending** when the session brings it back into scope.

### Operator-confirm writes

- **Remove a Parked item** as no longer relevant. Propose with rationale; do not auto-delete.
- **Move a Parked item to Pending** when the session brings it back into scope.

### Never

- Touch the `Done` section's prior dated entries. They are history.
- Auto-delete from `Pending` without confirming the task is done or moved.

---

## `build-log.md`

### Always-safe writes

- **Prepend a new entry** at the top (newest first). Format: `## YYYY-MM-DD — <Title>` with a paragraph describing what was built, paths touched, and any new decisions/runbooks/etc.
- **Append the metabolize report** to the bottom of the new entry. Format defined in `metabolize-report-format.md`.

### Never

- Edit prior entries.

---

## `research/research-state.yaml`

### Always-safe writes

- **Update conception fields** (scope, audience, application, exclusions) only when the session explicitly changed them.
- **Update architecture.tool_surface** when tools are added, removed, or repurposed.
- **Bump architecture.current** version when a PRD revision is finalized.
- **Update dependencies** when blockers shift.

### Operator-confirm writes

- **Move legacy items to a new `legacy_v_X` block** when superseding architecture.

### Never

- Edit research-state for build sessions that didn't shift conception. Build narrative goes to `build-log.md`.

---

## `research/sources.md`

### Always-safe writes

- **Append a new source** under the appropriate section (Internal, External, Pending).

### Never

- Remove a prior source even if it became less relevant. Sources are history.

---

## Cross-file consistency rules

- If a new decision in `decisions/decision-log.md` introduces a new term, the term must also land in `glossary.md`.
- If a new decision creates new pending work, the work must also appear in `tasks-status.md::Pending`.
- If `evolution.md` gets a new entry, the corresponding decision-log entry should reference it via `**Recorded in:**`.
- If `research-state.yaml` updates its conception, `evolution.md` must have a new entry justifying the update.
