# upgrade

Executes the migration plan produced by the spine. Single approval gate. After the operator approves, full migration runs without per-file prompts (unless `[?]` rows remain). Uses `git mv` on tracked workspaces. Recommends a pre-migration safety commit. Refreshes `rules/instance-current-manifest.md` from canonical, bumps `last_reconciled_version`, logs a decision-log entry.

## Mental model

Adopt-and-migrate. The workspace's pre-ACW persistent-memory content moves into ACW-canonical destinations, reshaped to canonical format. Source files delete after content lands at the destination. The end state: the workspace looks structurally identical to ACW canonical but holds its own operational history.

This verb is not interactive at the per-file level. It's interactive at the **plan level** — one approval gate before any write fires. After approval, execution is bulk and visible in chat as it runs.

## After the spine

The orchestrator's Step 5 produces the migration plan. Upgrade's job is to:

1. Run pre-flight safety checks.
2. Print the plan and request a single approval.
3. Resolve any `[?]` rows interactively (this is the only per-file prompt).
4. Execute the plan in bulk.
5. Refresh canonical cache, bump versions, log decision-log entry.

## Pre-flight safety checks

Before printing the plan for approval:

### Git initialization

If the workspace is not a git repository:

```
This workspace is not git-tracked. Migration includes destructive operations
(file moves, deletes, reshape-and-delete-source). Without git history, mistakes
are unrecoverable.

Initialize git and create an initial commit before proceeding?
  [y]  Recommended — run `git init`, stage current state, commit as "pre-acw-migration baseline"
  [n]  Proceed anyway (NOT recommended)
  [q]  Quit
```

On `[y]`: run `git init`, then `git add -A`, then `git commit -m "pre-acw-migration baseline"`. Use `git mv` for the upgrade run.

On `[n]`: warn loudly, use plain `mv` and `rm` for the upgrade run.

On `[q]`: exit cleanly.

### Pre-migration safety commit

If the workspace is git-tracked AND has uncommitted changes:

```
Workspace has uncommitted changes. A pre-migration safety commit is recommended
so the entire migration can be rolled back as a single revert if anything goes wrong.

Create pre-migration safety commit now?
  [y]  Recommended — stage current state and commit as "pre-acw-migration safety commit"
  [n]  Proceed without safety commit (rollback becomes manual)
  [q]  Quit
```

On `[y]`: `git add -A`, `git commit -m "pre-acw-migration safety commit"`.

On `[n]`: proceed.

On `[q]`: exit cleanly.

### Pre-commit hook awareness

If `.git/hooks/pre-commit` exists or `.pre-commit-config.yaml` is present, note in the safety prompt: *"pre-commit hooks detected. Migration commits will run them. Secret-scanning hooks (gitleaks, etc.) may catch sensitive content during the migration commit; address findings before the commit lands."*

## Plan approval gate

Print the migration plan from `references/audit.md` (verbatim format). After the plan, prompt:

```
──────────────────────────────────────────────────────────────────────
Migration plan summary:
  <N> moves
  <M> reshapes
  <P> merges
  <Q> write-canonical
  <R> deletes
  <S> instance-specific declarations
  <T> absorption candidates  (will write to ACW _buffer/)
  <U> ambiguous [?] routings  (will resolve interactively before bulk execution)

Total file operations: <total>

Approve and execute the full plan?
  [y]  Approve — resolve [?] rows then execute
  [n]  Cancel — no writes
  [m]  Modify the plan first (operator pastes annotations or asks for revisions)
```

On `[n]`: exit. Print one-line: *"upgrade cancelled. No writes performed."*

On `[m]`: enter a revision dialogue. Operator names rows to change action on; verb updates the plan; reprompt approval. Loop until `[y]` or `[n]`.

On `[y]`: proceed to `[?]` resolution (if any), then bulk execution.

## Resolve `[?]` rows

For each `[?]` row in the approved plan, prompt:

```
─────────────────────────────────────
Ambiguous routing: <path>
Candidate routings:
  a) <action> → <destination>  — <rationale>
  b) <action> → <destination>  — <rationale>
  ...
  s) skip (leave-untouched on this pass)

Choose:
─────────────────────────────────────
```

Update the plan in memory. After all `[?]` rows resolve, proceed to bulk execution.

## Bulk execution

Execute plan rows in this order (dependency-aware):

1. **`write-canonical`** for new directories and skeletal files (so destinations exist before moves/reshapes target them).
2. **`reshape`** in place (no source path change).
3. **`move`** — `git mv <source> <destination>` on tracked workspaces; plain `mv` otherwise.
4. **`reshape`** with source-to-destination path change — write reshaped content at canonical destination, then delete source (`git rm` or `rm`).
5. **`merge`** — read source, integrate into destination per the plan's one-line description, then delete source.
6. **`delete`** — `git rm` or `rm`.
7. **`instance-specific`** — append to `acw-state.yaml::instance_specific_substrate` with operator-supplied rationale and a generated decision-log id; create the corresponding decision-log entry.
8. **`absorption-candidate`** — verify cross-repo write authority, write candidate to ACW `_buffer/`, append to local `divergent_pending_review`. (Detail below.)
9. **Recommended-blocks gaps** — `tools/manifest.py append` (or upsert) on `acw-state.yaml`. Block-by-block.

For each row, print one line as it executes: `[move] decisions/old.md → decisions/decision-log.md ✓` or `[reshape] tasks-status.md (in place) ✓` or `[error] <row> — <message>`.

On error: stop, print summary of completed rows, do not bump `last_reconciled_version`. Operator decides whether to roll back via `git revert` of the safety commit, fix the issue, or re-run.

### Reshape execution

Reshape is the most content-sensitive action. The verb:

1. Reads the source file.
2. Applies canonical format (frontmatter, sections, ids, append-only structure).
3. Writes the reshaped content at the canonical destination.
4. **Verifies content presence at destination** — read it back, confirm size and content checks pass.
5. Deletes the source (only after verification succeeds).

For complex reshapes (multi-source merges, content composition from operator inputs), the verb may delegate to a research subagent for content drafting, then verify and write. Today's `_Command` dogfood used 8 parallel research subagents for content proposals; this is supported and recommended for substantial reshape rows.

### Absorption candidate execution

For each `absorption-candidate` row:

1. **Verify cross-repo write authority.** Check this workspace's `acw-state.yaml::cross_repo_writes` for the absolute path of ACW's `_buffer/` directory.
   - If declared → proceed.
   - If not declared → prompt: *"Cross-repo write to ACW's `_buffer/` requires declaration in `cross_repo_writes`. Add now? [y/N]"* On `y`: append the path to `cross_repo_writes`. On `n`: skip the absorption write; leave the source file in place; note in summary report.
2. **Write the absorption candidate** to `ACW/_buffer/YYYY-MM-DD-<workspace>-<topic-slug>-absorption-candidate.md` per the format in `rules/multi-instance-topology.md` § "Absorption candidate format."
3. **Record divergence locally:** append to `acw-state.yaml::divergent_pending_review` with `path`, `absorption_candidate` (path to the `_buffer/` note), `sent_date: <today>`, `status: pending`.
4. The source file stays in place pending ACW's absorption review. Do NOT delete or reshape it.

## Auto-load discipline application

Authoritative source: `rules/auto-load-discipline.md` (canonical claims, demotion list) + audit-emitted verdict table per `references/audit.md`.

For each auto-load plan row from the audit, execute under the same approval gate:

- `KEEP` / `KEEP (migrate-to-structured)` — write structured `path / claim / earned_by` triple. Canonical claims come from the rule; operator supplies claims for `KEEP (instance-specific)` rows that lack one.
- `DEMOTE` — remove the entry from `auto_load_at_session_start`. File stays in workspace; only the auto-load reference drops. Print: `[demote] auto_load_at_session_start: removed <path> — <reason>`.
- `REVIEW` — prompt operator: `k`eep (declare claim), `d`emote, or `s`kip (stays as legacy-pending-review).

When `CLAUDE.md` or other host entry files carry mirror `@`-imports of the auto-load list, propose a corresponding edit to keep them in sync (operator confirms).

Append one summary line to the migration's decision-log entry: *Auto-load discipline applied: kept K entries, migrated M to structured form, demoted D entries.*

No-op if `auto_load_at_session_start` already matches the rule's canonical recommendations in structured form.

## Single-file → wiki migration (mandatory, v0.9.8+ doctrine)

Wiki mode is canonical (D-ACW-048). When the workspace presents single-file legacy shape (`decisions/decision-log.md` or `glossary.md`), the upgrade verb performs a complete migration. Not optional, not gated by a workspace mode key — wiki is the only mode.

Steps under the standard plan-approval gate:

1. Run `python tools/migrate_to_wiki.py` against the live `decisions/decision-log.md` to produce `decisions/entries/`, `decisions/open-questions/`, `decisions/constraints/`, and `decisions/INDEX.md`.
2. **Re-split every pre-existing rolling-window archive** matching `decisions/decision-log-YYYY-Q*.md` into per-entry wiki files via `python tools/migrate_to_wiki.py --archive=<path>`. All historical decisions land in `decisions/entries/`.
3. Delete the live `decision-log.md` source and every quarterly archive file after content verification. Remove the archive entries from `acw-state.yaml::meta_layer`.
4. Update `acw-state.yaml::decision_tracking` to wiki shape (`mode: wiki`, plus `index`, `entries_dir`, `open_questions_dir`, `constraints_dir`, `archive_pattern`, `regenerate_index_cmd`, `entry_frontmatter_required`, `status_values`, `kind_values`).
5. Update `acw-state.yaml::paths` from single-file keys to wiki keys (`decisions_index`, `decisions_entries_dir`, etc.).
6. Update `acw-state.yaml::auto_load_at_session_start` to point at `decisions/INDEX.md` (and `glossary/INDEX.md`) instead of the single-file paths.
7. The SessionStart hook (`.claude/hooks/load-context.py`) reads `auto_load_at_session_start` at runtime, so no host entry file edits are required beyond the state-file change.
8. The same migration applies symmetrically for glossary using the same tool against `glossary.md`.

Doctrine: in wiki mode, ALL decisions live in `decisions/entries/`. Single-file mode is retired.

## Optional patterns (earn-by-discipline) — context/contacts/

If the audit emitted an `opt-in (context/contacts/)` row and the operator accepted at plan-review time, execute:

1. Write `context/contacts/INDEX.md` from `tools/templates/context-contacts-INDEX.md.tmpl` (substitute `{{PROJECT_NAME}}` from `acw-state.yaml::project.name`).
2. Create `context/contacts/entries/` with a `.gitkeep`.
3. Append the path to `acw-state.yaml::instance_specific_substrate` with rationale `opt-in: context/contacts/ wiki pattern adopted via /acw-instance upgrade`.
4. Log a decision-log entry in wiki shape: title `Adopted context/contacts/ wiki pattern`, kind `decision`, rationale supplied by operator (or default: "operator opted in during /acw-instance upgrade plan review").

If declined → no write; the opt-in re-surfaces on the next audit until accepted or the operator explicitly declares it `instance-specific-declined` via decision-log entry.

## v0.5.0 migration: `_inbox/` → `_buffer/`

Before bulk execution, detect the legacy directory name (this is automatic, no operator prompt needed beyond the plan-approval gate which already includes it):

- If `<workspace>/_inbox/` exists AND `<workspace>/_buffer/` does not exist → execute as part of the plan: `git mv _inbox _buffer` (or filesystem move). Update `acw-state.yaml::paths::buffer_dir` and `acw-state.yaml::empty_dirs`.
- If both exist → halt with: ambiguous state, manual cleanup required. Bail before any other writes.

## Host entry file migration (Claude Code) — v0.9.7

Authoritative source: `rules/instance-current-manifest.md` § "Host entry file shape (Claude Code) — v0.9.7" + the v0.9.7 canonical templates fetched from `tools/templates/load-context.py.tmpl` and `tools/templates/settings.json.tmpl`.

Execute only when `CLAUDE.md` exists at workspace root (mirror of the audit pass trigger). Instances without a Claude Code entry file skip this pass. The audit verb emits up to four plan rows for this migration; execute under the standard plan-approval gate:

### CLAUDE.md trim

If plan row present: overwrite `CLAUDE.md` with the literal string `See AGENTS.md.\n` (one line, trailing newline). The pre-migration content is preserved in the safety commit; no separate backup is written. Print: `[reshape] CLAUDE.md (trimmed to thin pointer) ✓`.

### `.claude/settings.json` write

If `WRITE-CANONICAL`: write the fetched `tools/templates/settings.json.tmpl` content verbatim to `.claude/settings.json`. Create `.claude/` directory if absent.

If `RESHAPE`: read existing `.claude/settings.json`, parse as JSON. Replace `hooks.SessionStart` with the canonical block (preserve `hooks.<other-event>` entries the operator has added). Write back as indented JSON (2-space indent). Print: `[reshape] .claude/settings.json (SessionStart hook updated) ✓`.

### `.claude/hooks/load-context.py` write

If `WRITE-CANONICAL` or `RESHAPE`: write the fetched `tools/templates/load-context.py.tmpl` content verbatim to `.claude/hooks/load-context.py`. Create `.claude/hooks/` directory if absent. The script is canonical; instance-specific customization happens via `acw-state.yaml::auto_load_at_session_start`, not by editing the hook. Print: `[reshape] .claude/hooks/load-context.py (canonical template applied) ✓`.

### AGENTS.md edits

If plan row present:

1. Replace the entirety of directive 7's bullet with the canonical v0.9.7 wording (SessionStart hook implementation pointer). Fetch the canonical AGENTS.md from GitHub, extract directive 7 verbatim, apply.
2. After the directives list, insert the `## Auto-load (Resource / When / Why)` section if absent. Content from canonical AGENTS.md.
3. After Auto-load section, insert `## What NOT to Load` section if absent. Content from canonical AGENTS.md.
4. All other AGENTS.md content (other directives, "Operational commands", "Why AGENTS.md and not CLAUDE.md", "Not a content file", operator additions) preserved.

Print: `[reshape] AGENTS.md (directive 7 + Auto-load + What NOT to Load sections updated) ✓`.

### Post-migration smoke test

After the four writes complete, smoke-test the hook:

```bash
python .claude/hooks/load-context.py
```

Expected: exits 0, stdout is JSON with `hookSpecificOutput.additionalContext` field containing the four canonical auto-load files (or whatever the workspace's `acw-state.yaml::auto_load_at_session_start` declares).

On smoke-test failure: print `[error] Host entry file migration smoke test failed: <stderr>`. Surface as a halted-execution error; do not bump `last_reconciled_version`. Operator triages.

On smoke-test success: print `Host entry file (Claude Code) v0.9.7 shape applied. Hook smoke test passed.`

### Skip conditions

Skip the entire pass if the audit pass produced no plan rows for this migration (instance already at v0.9.7 shape).

## Resolve existing `divergent_pending_review` entries

After bulk execution, for each existing `divergent_pending_review` entry with `status: pending`:

- Compare the entry's file shape against the freshly-fetched canonical. If canonical now matches the workspace's shape → mark `absorbed`, surface to operator, clear the entry.
- If a rejection notification exists in this workspace's `_buffer/` from ACW (filename pattern `acw-rejection-<topic>.md`) → mark `rejected`, surface to operator. The rejected file then routes via the next `/acw-instance audit` as `move` or `reshape` to canonical.
- Else → keep `pending`, surface a one-line status reminder.

## Refresh canonical cache

Overwrite `<workspace>/rules/instance-current-manifest.md` with the fetched canonical content. The local file is now an up-to-date snapshot of "what canonical looks like at last reconciliation."

After overwrite, set the `synced_to:` frontmatter field on the local file to the canonical's current `<version>` (string, quoted). This field is the cheap-path signal `/acw-session start` Step 5 reads to skip the drift walk when nothing can have changed.

If `rules/instance-current-manifest.md` was missing entirely (common in unregistered adoption), this write also lands as part of bulk execution, before this step.

## Bump versions

1. Set `last_reconciled` to today's date (UTC, `YYYY-MM-DD`).
2. Set `last_reconciled_version` to the canonical's current `<version>`.

Use `tools/manifest.py append` (key/value upsert) or direct edit. Preserve all other content, comments, and ordering.

## Log decision-log entry

Format authority: `rules/decision-tracking.md` owns the single-file section format; `acw-state.yaml::decision_tracking.entry_frontmatter_required + status_values + kind_values` owns wiki-mode frontmatter. The skill writes the body content; format comes from those sources.

Mode-portable dispatch (read `acw-state.yaml::decision_tracking.mode`, default `single-file`):

- **single-file** → append a new entry under the configured decisions section in the file referenced by `paths.decisions_log` (or canonical default `decisions/decision-log.md`).
- **wiki** → write a new file at `<decisions_entries_dir>/D-<CODE>-NNN-<slug>.md` using the canonical frontmatter shape; then invoke `decision_tracking.regenerate_index_cmd` if declared, else append a one-line link to `<decisions_index>::## Recent Decisions`.

Body content the skill supplies (both modes):

- **Title:** `Instance migrated to ACW <version>`.
- **Date:** today (UTC).
- **Decision:** one-line summary + per-action counts (moves, reshapes, merges, write-canonical, deletes, instance-specific declarations, absorption candidates, recommended-blocks gaps reconciled, canonical manifest fetched).
- **Rationale:** adopt-and-migrate per `/acw-instance upgrade`; workspace now structurally identical to ACW canonical.
- **Source:** `/acw-instance upgrade` run on `<date>`.
- **Pre-migration safety commit:** `<hash>` (if created).
- **Migration commit:** placeholder ("to be created after this entry lands").

For each `instance-specific` row, write an additional rationale entry (same mode dispatch) with body: title `<path> declared instance-specific substrate`, decision naming the path, rationale supplied by operator during upgrade.

If this run was an unregistered-workspace adoption, prepend an additional entry recording the adoption itself (workspace registered, canonical manifest cached, initial `acw-state.yaml` written).

## Final summary report

Print to chat:

```
Instance migration complete.

[Adopted from unregistered substrate-shaped workspace.]   <-- only on adoption
[Pre-migration safety commit: <hash>]                      <-- only if created

Reconciled to ACW <version> as of <date>.
Canonical manifest cache: refreshed from GitHub.

Operations executed:
  Moved: <N>
  Reshaped: <M>
  Merged: <P>
  Wrote canonical: <Q>
  Deleted: <R>
  Declared instance-specific: <S>
  Absorption candidates sent: <T>
  Recommended blocks added to acw-state.yaml: <V>

Skipped: <list of skipped rows with reasons>
Pending review (respected, not modified): <list>
Instance-specific declared (respected, not modified): <list>

Logged: <decision-log entry id(s)>

Recommended next step: review the workspace, verify substrate shape, then commit:
  git add -A
  git commit -m "feat: migrate to ACW v<version> canonical shape"

The /acw-session start drift alert will quiet for blocks at-or-before v<version>.
```

The verb does NOT auto-commit the migration. Operator commits manually after review (consistent with ACW's general "no auto-commit" discipline). The pre-migration safety commit and the final migration commit bracket the entire operation; the operator can `git revert <migration-commit>` to roll back if needed.

## Adopt-mode (unregistered workspace)

When Step 2 of the spine flagged the workspace as unregistered, the same plan-approval flow applies. The plan's `write-canonical` rows are derived from canonical `acw-state.yaml::template_layer + instance_layer + empty_dirs + recommended_blocks` — every declared path that doesn't exist in the workspace becomes a write-canonical row. Decisions and glossary always scaffold in wiki shape (v0.9.8+, D-ACW-048): `decisions/INDEX.md`, `decisions/entries/`, `decisions/open-questions/`, `decisions/constraints/`, `glossary/INDEX.md`, `glossary/entries/`.

The hard-stop threshold from D-ACW-022 (`adopt_mode_organic_threshold`, default 5) is no longer enforced. The plan-approval gate is the safety net: operator sees every proposed routing in one coherent view before any write fires. The field stays in `acw-state.yaml` for backward compatibility; decision-log entry recommended on first upgrade post-v0.7.0 to formally retire.

The initial `acw-state.yaml` written for an adopted workspace is rendered from `tools/templates/acw-state.yaml.tmpl` (canonical scaffold source). Computed fields the verb fills in:

- `version` = canonical's current `<version>`
- `last_reconciled` = today (UTC)
- `last_reconciled_version` = `0.0.0` (drives one noisy re-audit; quiets after next upgrade pass)
- `is_canonical_source` = `false`
- `project.{name, code, domain}` = operator-supplied

After the migration commit, the next `/acw-instance audit` run produces a clean plan and a future `/acw-instance upgrade` bumps `last_reconciled_version` to current canonical.

## Safety

- Single approval gate. No writes fire before operator approves the full plan.
- Pre-migration safety commit recommended; offered automatically.
- `git init` offered for untracked workspaces before destructive operations.
- `git mv` preserves history on tracked workspaces.
- Source files delete only after content is verified at the canonical destination.
- Errors halt execution; partial state is preserved; `last_reconciled_version` only bumps after full pass completes.
- Cross-repo writes (absorption candidates) require explicit `cross_repo_writes` declaration.
- The verb never demotes layers, never removes blocks from `acw-state.yaml` without operator confirmation via `[?]` row, and never auto-commits the migration.

## Output

- Edits across the substrate boundary identified in Step 4 of the spine.
- Refresh of `rules/instance-current-manifest.md` from canonical.
- One or more decision-log entries (one for the migration, one per `instance-specific` declaration).
- Zero or more absorption candidates in ACW's `_buffer/`.
- Chat summary report.
- Operator commits the migration manually after review.
