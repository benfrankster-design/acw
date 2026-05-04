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

## v0.9.0 migration: auto-load discipline

If the workspace's `acw-state.yaml::auto_load_at_session_start` block uses legacy bare-path form, OR contains entries declared as demotion candidates in `rules/auto-load-discipline.md`, the upgrade applies the audit's verdicts as part of the bulk execution:

1. **Convert bare-path entries to structured form** — for each `KEEP` or `KEEP (migrate-to-structured)` entry, write the structured `path / claim / earned_by` triple. Use the canonical claim from `rules/auto-load-discipline.md` for canonical-recommendation paths; prompt the operator for `claim` text on `KEEP (instance-specific)` entries that lack one.
2. **Remove demotion entries** — for each `DEMOTE` entry, remove from `auto_load_at_session_start`. The file itself stays in the workspace; only the auto-load reference is dropped. Print: `[demote] auto_load_at_session_start: removed <path> — <reason>` per row.
3. **Resolve REVIEW entries interactively** — for each `[?]` REVIEW plan row, prompt with options:
   ```
   Auto-load entry: <path>
   Form: bare-path (legacy)
   Not on canonical recommendations; no declared claim.

   Choose:
     k) KEEP — declare a claim for this instance-specific override
     d) DEMOTE — remove from auto_load_at_session_start (file stays in workspace)
     s) skip — leave as-is (entry stays as legacy-pending-review; surfaces again on next audit)
   ```
4. **Update host entry files** — when `CLAUDE.md` (or other host-specific entry files) carry mirror `@`-imports of the auto-load list, propose a corresponding edit to keep them in sync. Operator confirms.
5. **Decision-log entry** — append a row to the migration's decision-log entry naming the auto-load changes:
   ```
   - Auto-load discipline applied: kept <K> entries, migrated <M> to structured form, demoted <D> entries.
   ```

This step is performed only when the audit's plan includes auto-load rows. If `auto_load_at_session_start` is already fully canonical (4 structured entries matching the recommendations) the step is a no-op.

## v0.5.0 migration: `_inbox/` → `_buffer/`

Before bulk execution, detect the legacy directory name (this is automatic, no operator prompt needed beyond the plan-approval gate which already includes it):

- If `<workspace>/_inbox/` exists AND `<workspace>/_buffer/` does not exist → execute as part of the plan: `git mv _inbox _buffer` (or filesystem move). Update `acw-state.yaml::paths::buffer_dir` and `acw-state.yaml::empty_dirs`.
- If both exist → halt with: ambiguous state, manual cleanup required. Bail before any other writes.

## Resolve existing `divergent_pending_review` entries

After bulk execution, for each existing `divergent_pending_review` entry with `status: pending`:

- Compare the entry's file shape against the freshly-fetched canonical. If canonical now matches the workspace's shape → mark `absorbed`, surface to operator, clear the entry.
- If a rejection notification exists in this workspace's `_buffer/` from ACW (filename pattern `acw-rejection-<topic>.md`) → mark `rejected`, surface to operator. The rejected file then routes via the next `/acw-instance audit` as `move` or `reshape` to canonical.
- Else → keep `pending`, surface a one-line status reminder.

## Refresh canonical cache

Overwrite `<workspace>/rules/instance-current-manifest.md` with the fetched canonical content. The local file is now an up-to-date snapshot of "what canonical looks like at last reconciliation."

If `rules/instance-current-manifest.md` was missing entirely (common in unregistered adoption), this write also lands as part of bulk execution, before this step.

## Bump versions

1. Set `last_reconciled` to today's date (UTC, `YYYY-MM-DD`).
2. Set `last_reconciled_version` to the canonical's current `<version>`.

Use `tools/manifest.py append` (key/value upsert) or direct edit. Preserve all other content, comments, and ordering.

## Log decision-log entry

Append to `paths.decisions_log` `section_conventions.decisions`:

```markdown
### D-<CODE>-NNN — Instance migrated to ACW <version>

**Date:** YYYY-MM-DD
**Decision:** Migrated this instance to ACW canonical shape as of version <version>.
  Moved <N> files into canonical destinations.
  Reshaped <M> files to canonical format.
  Merged <P> files into existing canonical destinations.
  Wrote <Q> new canonical files.
  Deleted <R> source files post-migration.
  Declared <S> instance-specific substrate entries (see decision-log entries for rationale).
  Sent <T> absorption candidates to ACW _buffer/.
  Reconciled <V> recommended-blocks gaps in acw-state.yaml.
  Canonical manifest fetched from GitHub and cached locally.
**Rationale:** Adopt-and-migrate per /acw-instance upgrade. Workspace now structurally identical to ACW canonical; operational history preserved in canonical files.
**Source:** /acw-instance upgrade run on <date>.
**Pre-migration safety commit:** <commit hash, if created>.
**Migration commit:** <to be created after this entry lands>.
```

For each `instance-specific` row, additionally append a per-file rationale entry to `decisions/decision-log.md`:

```markdown
### D-<CODE>-NNN — <path> declared instance-specific substrate

**Date:** YYYY-MM-DD
**Decision:** Substrate at `<path>` declared instance-specific; will not be promoted to ACW canonical.
**Rationale:** <operator-supplied rationale during upgrade>.
**Source:** /acw-instance upgrade run on <date>.
```

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

When Step 2 of the spine flagged the workspace as unregistered (canonical signals at-or-above 3 OR substrate-shaped patterns present), the same plan-approval flow applies. The plan will include:

- `write-canonical` rows for the missing canonical files (`acw-state.yaml`, `rules/instance-current-manifest.md`, `decisions/decision-log.md` if absent, `tasks-status.md` if absent, `glossary.md` if absent, etc.).
- `move` and `reshape` rows for the substrate-shaped patterns the workspace already has.
- `instance-specific` declarations for substrate the operator wants kept as-is.
- `absorption-candidate` rows for net-new patterns that should flow upstream to ACW.

The hard-stop threshold from D-ACW-022 (`adopt_mode_organic_threshold`, default 5) is no longer a blocking gate at adopt time. Instead, the plan-approval gate IS the safety net: the operator sees every proposed routing in one coherent view before any write fires. This supersedes the v0.4.0 hard-stop — that gate existed to prevent steamrolling unregistered workspaces, and the plan-approval gate accomplishes the same thing more transparently.

The threshold remains in `acw-state.yaml` for backward compatibility but is no longer enforced as a bail condition. (Decision-log entry recommended on first upgrade post-v0.7.0 to formally retire the gate.)

For an unregistered workspace, the initial `acw-state.yaml` written as part of the plan execution carries:

```yaml
version: "<canonical-current-version>"
last_reconciled: "<today>"
last_reconciled_version: "0.0.0"   # drives a noisy first re-audit; quiets after next upgrade pass
is_canonical_source: false
project:
  name: "<operator-supplied>"
  code: "<operator-supplied>"
  domain: "<operator-supplied>"
paths:
  # canonical defaults; operator can override post-migration
```

After the migration commit, the next `/acw-instance audit` run will produce a clean plan (most rows `leave-untouched`) and a future `/acw-instance upgrade` will bump `last_reconciled_version` to the current canonical.

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
