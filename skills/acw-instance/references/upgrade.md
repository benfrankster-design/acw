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
  <T> absorption candidates  (will write to ACW .acw/raw/ as kind=absorption)
  <U> ambiguous [?] routings  (will resolve interactively before bulk execution)
  Cross-repo signals: bugs and issues hit during execution will flush to ACW .acw/raw/ at end-of-run (one authority prompt on first emit if cross_repo_writes is undeclared).

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

## Migration-manifest execution (v0.10.0+)

> **Architectural note (D-ACW-050, D-ACW-051):** From v0.10.0 forward, version-to-version migrations live as declarative data in `migrations/<from>-to-<to>.yaml` per `rules/migration-manifest.md`. The audit reads the relevant manifest(s) and emits plan rows; the upgrade executor walks them under the standard plan-approval gate. The version-specific sections later in this file (v0.5.0 `_inbox/` → `_buffer/`, v0.9.7 CLAUDE.md trim, v0.9.8 single-file → wiki migration) remain for instances on those legacy versions; they will retire when no instance remains at the corresponding source version.

### How manifests map to existing plan-row actions

The manifest step-kind enum from `rules/migration-manifest.md` maps to actions the audit phase already emits and the bulk executor already handles:

| Manifest step kind | Plan-row action | Notes |
|---|---|---|
| `create_dir` | `write-canonical` (directory) | Idempotent; no-op on existing. |
| `git_mv` (single move) | `move` | Standard `git mv` for tracked workspaces. |
| `git_mv` (moves list with rename) | `move` x N | Batch — emitted as one plan row group; executor walks them as a unit so a single failure surfaces cleanly. |
| `update_acw_state` | `reshape` (acw-state.yaml in place) | New parameters: `path_prefix_substrate`, `rename_keys`, `add_fields`, `set_fields`. Calls `tools/manifest.py` for each block change. |
| `update_file` | `reshape` (in place) | Targeted text replace; refuses on conflict (replace target not found). |
| `rebuild_index` | `reshape` (in place) | Calls `python tools/migrate_to_wiki.py` or the instance's `regenerate_index_cmd` from `acw-state.yaml::decision_tracking`. |
| `add_file` | `write-canonical` | Renders from a `content_template` with `content_tokens` substitution. |
| `remove_gitignore_rule` | `reshape` (`.gitignore` in place) | New action: edits `.gitignore` to remove a specific rule line. |
| `run_hook` | `reshape` (custom) | Executes a script in `tools/migration-hooks/`. Use sparingly; declarative steps preferred. |
| `only_if` conditional | filter on row generation | Audit phase evaluates `only_if` against `operator_prompts` answers and skips the row if false. |
| `operator_prompts` | `[?]` row | Each prompt becomes an interactive resolution at plan-approval time, before bulk execution. |

### Audit-phase behavior for manifest-driven workspaces

When the audit detects a `from_version` match in `migrations/<from>-to-<to>.yaml`:

1. Read the manifest.
2. Evaluate `prerequisites` — abort plan generation with clear message if any prerequisite fails.
3. For each operator prompt in `operator_prompts`, emit a `[?]` resolution row at the top of the plan with the prompt text, enum, and default.
4. For each step in `steps`, generate plan rows per the mapping table above. Steps with `only_if` defer row generation until `[?]` resolution time.
5. The standard plan-approval gate fires once across the full row set.

If an instance is multiple versions behind (e.g., `0.9.7 → 0.10.0`), the audit chains manifests in version order, emitting one combined plan. Each manifest's prerequisites are evaluated against the state the previous manifest would have produced. Operator prompts surface in chain order (earlier-manifest prompts first).

### Pre-v0.10.0 instances without manifest

For instances at versions older than 0.9.9 where intermediate migration manifests do not yet exist in canonical, the audit falls back to the version-specific sections later in this file (v0.5.0, v0.9.7, v0.9.8). Equivalent manifests will be authored over time; until then, the embedded logic ships the upgrade safely.

### Executor verification status (2026-05-21, updated Session 24)

All step kinds required by `migrations/0.9.9-to-0.10.0.yaml` and `migrations/pre-acw-to-0.10.0.yaml` are now specified for execution. Concrete behavior for each appears in "Step kind execution detail" below.

| Step kind | Status | Notes |
|---|---|---|
| `create_dir` | ready | Idempotent. Plan-row action: `write-canonical` (dir). |
| `git_mv` (single + batch) | ready | Standard. Use `git mv` if tracked; plain `mv` otherwise. |
| `git_mv` with `optional: true` | **ready (Session 24)** | Skip-if-source-missing tolerance for pre-acw bootstrap. Detail below. |
| `update_acw_state` | ready | Full `path_prefix_substrate` / `rename_keys` / `add_fields` / `set_fields` coverage. Detail below. |
| `update_file` | ready | Targeted text replace; refuse-on-conflict. Detail below. |
| `rebuild_index` | ready | Calls `python tools/migrate_to_wiki.py` or `acw-state.yaml::decision_tracking.regenerate_index_cmd`. |
| `add_file` | ready | Renders from `content_template` with `content_tokens` substitution. |
| `remove_gitignore_rule` | **ready (Session 24)** | Read .gitignore, drop matching line, write back. Detail below. |
| `only_if` conditional | **ready (Session 24)** | Evaluated in audit phase against `operator_prompts` answers; rows filter before plan emission. Detail below. |
| `run_hook` | ready (limited) | Executes a script in `tools/migration-hooks/`. Used by pre-acw bootstrap (`migrate_to_wiki.py`, `bootstrap-empty-dirs.py`). |

Recommended: dry-run `migrations/0.9.9-to-0.10.0.yaml` against a copy of a v0.9.9 instance before running for real. The dry-run path emits the plan without executing; gaps surface as warnings.

### Step kind execution detail (v0.10.0+ manifest support)

The mapping table earlier in this file shows how each step kind translates into the existing plan-row action enum. This section nails down execution behavior for the step kinds that had open questions before Session 24.

**`remove_gitignore_rule`.**

Manifest schema:

```yaml
- kind: remove_gitignore_rule
  rule: ".acw/"           # exact line text to remove
  reason: "..."           # surfaced in plan-row and log
```

Plan-row action: `reshape` on `<workspace>/.gitignore`. Plan-row description: `[reshape] .gitignore: remove rule "<rule>" — <reason>`.

Execution:

1. Read `<workspace>/.gitignore`. If file is absent, treat as no-op (idempotent — the rule is already not present) and print `[skip] .gitignore: rule already absent (no .gitignore file)`.
2. Walk lines. For each line where `line.strip() == rule.strip()` (whitespace-tolerant exact match), drop the line. Preserve comments, blank lines, and all other rules verbatim.
3. If no line matched, treat as no-op and print `[skip] .gitignore: rule "<rule>" not found (already removed)`.
4. If one or more lines matched, write the modified content back. Use `git add .gitignore` on tracked workspaces so the change lands in the migration commit.
5. Print `[reshape] .gitignore: removed "<rule>" (<N> line(s)) ✓`.

Refuse-on-ambiguity policy: this step does NOT do partial-line matching or regex matching. If an operator's `.gitignore` has the rule as part of a longer line (`.acw/  # legacy`), the line is preserved untouched and a `[?]` plan row is emitted asking the operator to confirm whether to remove the longer form.

**`only_if` conditional.**

Manifest schema (on any step):

```yaml
- kind: create_dir
  path: .acw/codemap
  only_if: { field: profile, in: [coding-project, library] }
```

Supported predicates:

| Form | Meaning |
|---|---|
| `{ field: <name>, equals: <value> }` | True when the named field's resolved value equals `<value>` exactly. |
| `{ field: <name>, in: [<v1>, <v2>, ...] }` | True when the value is one of the listed options. |
| `{ field: <name>, not_equals: <value> }` | Inverse of `equals`. |
| `{ field: <name>, present: true }` | True when the field resolved to a non-null, non-empty value. |
| `{ all: [<predicate>, <predicate>, ...] }` | Conjunction. |
| `{ any: [<predicate>, <predicate>, ...] }` | Disjunction. |

Field resolution order (first hit wins):

1. Operator-prompt answers from this manifest's `operator_prompts` block (collected at `[?]` resolution time, before bulk execution).
2. Existing keys in the workspace's `acw-state.yaml` (read at audit time).
3. Default value declared on the operator-prompt entry, if the operator was not prompted (e.g., chain-mode where this manifest's prompt defaults applied because an earlier manifest already answered).

Execution:

- The audit phase resolves `only_if` predicates after all `operator_prompts` have answers (including defaults). Steps whose predicate evaluates `false` produce no plan rows.
- During the upgrade phase, predicate evaluation does NOT happen again. The plan already contains only the rows that matched. This avoids re-prompting and keeps execution deterministic.
- If a predicate references a `field:` that does not exist in operator prompts, the workspace state, or as a default, the audit phase logs a warning and treats the predicate as `false` (the conservative choice — skip rather than execute on an unknown).

Print at plan time: rows whose `only_if` matched appear normally; rows whose `only_if` did not match are listed in a single line below the plan: `Skipped by only_if: <N> rows (<one-line summary of which steps>)`.

**`git_mv` with `optional: true`.**

Manifest schema:

```yaml
- kind: git_mv
  moves:
    - { from: decisions, to: .acw/decisions, optional: true }
    - { from: _buffer, to: .acw/raw, optional: true }
```

Per-move flag, not per-step. Used in the pre-acw bootstrap manifest where the source workspace may have only a subset of substrate paths.

Execution:

For each move with `optional: true`:

1. Check whether `<from>` exists in the workspace.
2. If absent → skip this move silently. Print `[skip] git_mv <from> → <to>: source absent (optional)`.
3. If present → execute as a normal `git mv` (or plain `mv` on untracked workspaces).
4. The plan-row generation in audit phase still emits one row per declared move; rows for absent sources are tagged `[would-skip]` so the operator sees what was planned and what will no-op.

Moves without `optional: true` retain hard-fail behavior: missing source aborts the bulk execution with an error.

**`update_acw_state` subops (full coverage).**

Manifest schema:

```yaml
- kind: update_acw_state
  path_prefix_substrate:
    prefix: .acw/
    keys: [decisions_index, tasks_status, ...]
  rename_keys:
    buffer_dir: raw_dir
  add_fields:
    profile: spec-project          # default; operator prompt may overwrite
    modules: null
  set_fields:
    version: "0.10.0"
    last_reconciled_version: "0.10.0"
    last_reconciled: "<DATE>"
```

Plan-row action: `reshape` on `acw-state.yaml`. One row per logical sub-operation declared, grouped under one plan-row group.

Execution order within the step:

1. `path_prefix_substrate`: for each key in `keys`, read its current value from `acw-state.yaml::paths`; if the value does not already start with `prefix`, prepend `prefix` to the value; write back. Idempotent (already-prefixed keys are no-ops).
2. `rename_keys`: for each `<old>: <new>` pair, if `<old>` exists in `acw-state.yaml::paths`, move its value to `<new>` and remove `<old>`. Idempotent (missing `<old>` is no-op).
3. `add_fields`: for each `<key>: <value>` pair at the top level of `acw-state.yaml`, if the key is absent OR null, set to `<value>`. Operator-prompt answers (per `operator_prompts.<field>.affects`) override the manifest's default before this step fires.
4. `set_fields`: for each `<key>: <value>` pair at the top level, set unconditionally. Used for version bumps. `<DATE>` token resolves to today (UTC, `YYYY-MM-DD`).

Use `tools/manifest.py` (key/value upsert) for the writes; do not hand-edit. Preserve comments and key ordering for all blocks the step does not touch.

**`update_file` (text replace with refuse-on-conflict).**

Manifest schema:

```yaml
- kind: update_file
  path: AGENTS.md
  replace:
    - { find: "decisions/INDEX.md", with: ".acw/decisions/INDEX.md" }
    - { find: "tasks-status.md", with: ".acw/tasks-status.md" }
```

Plan-row action: `reshape` on `<path>`. Plan-row description lists how many replace pairs landed.

Execution:

1. Read `<path>`. Refuse if absent (the file is expected; abort step).
2. For each replace pair, count occurrences of `find` in the current text. Apply the replacement.
3. If a `find` value does not appear in the file: log a single warning line per missing pair (`[update_file] AGENTS.md: pattern "<find>" not found — operator-customized prose may need manual fixup`). Continue with remaining pairs.
4. If any `find` value appears alongside `with` already (i.e., the replacement is partially applied), the step still runs — the find/replace is idempotent for exact-string matches.
5. Write the modified content back.

The "refuse on conflict" intent here is narrow: refuse only if the file itself is missing. Missing patterns inside the file produce warnings, not failures, because operator-customized prose is a normal and expected occurrence.

## Bulk execution

Execute plan rows in this order (dependency-aware):

1. **`write-canonical`** for new directories and skeletal files (so destinations exist before moves/reshapes target them).
2. **`reshape`** in place (no source path change).
3. **`move`** — `git mv <source> <destination>` on tracked workspaces; plain `mv` otherwise.
4. **`reshape`** with source-to-destination path change — write reshaped content at canonical destination, then delete source (`git rm` or `rm`).
5. **`merge`** — read source, integrate into destination per the plan's one-line description, then delete source.
6. **`delete`** — `git rm` or `rm`.
7. **`instance-specific`** — append to `acw-state.yaml::instance_specific_substrate` with operator-supplied rationale and a generated decision-log id; create the corresponding decision-log entry.
8. **`absorption-candidate`** — emit as kind=`absorption` per "Cross-repo signal emission" below; also append to local `divergent_pending_review`.
9. **Recommended-blocks gaps** — `tools/manifest.py append` (or upsert) on `acw-state.yaml`. Block-by-block.
10. **Flush cross-repo signal buffer** — any `bug` or `issue` signals captured during execution emit now per "Cross-repo signal emission" below.

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

### Cross-repo signal emission

`/acw-instance` runs surface three kinds of signal that belong upstream in ACW, not in the downstream workspace. All three write to the same canonical destination — `ACW/.acw/raw/` — with a kind-prefixed filename and share one authority check.

**The three kinds:**

| Kind | Trigger | Filename suffix | Notes |
|---|---|---|---|
| `absorption` | Substrate-shape pattern in the workspace that is net-new to canonical or judged better than canonical. Emitted from `absorption-candidate` plan rows. | `-absorption-candidate.md` | Format per `rules/multi-instance-topology.md` § "Absorption candidate format." Source file stays in workspace pending ACW review. |
| `bug` | Defect in canonical hit during execution: template file out-of-sync with doctrine, tool errors on canonical input, canonical spec contradicts another canonical spec, recommended-blocks-registry entry references a missing path, etc. | `-canonical-bug.md` | Captured during bulk execution; flushed at end. Does NOT halt execution unless the defect blocks the row outright — the verb records and moves on. |
| `issue` | Operator-facing concern, ambiguity, or follow-up worth ACW's attention but not a defect. Operator may add at plan-approval time; verb may auto-detect (e.g., "canonical synced_to lags behind canonical version field"). | `-canonical-issue.md` | Lower bar than `bug`; no defect required. |

**Authority check (shared across all three kinds).** Before the first cross-repo write of a run:

1. Check this workspace's `acw-state.yaml::cross_repo_writes` for the absolute path of ACW's `.acw/raw/` directory.
2. If declared → proceed for all signals this run.
3. If not declared → prompt once: *"Cross-repo write to ACW's `.acw/raw/` requires declaration in `cross_repo_writes`. Add now? [y/N]"* On `y`: append the absolute path. On `n`: skip ALL cross-repo writes this run; capture-buffer entries are listed in the summary report so the operator can decide whether to copy them by hand.

**Filename pattern (all kinds):**

```
ACW/.acw/raw/YYYY-MM-DD-<workspace-slug>-<topic-slug><kind-suffix>
```

`<workspace-slug>` resolves from `acw-state.yaml::project.code` lowercased (e.g., `fc`, `cmd`, `csops`). `<topic-slug>` is generated from the signal's title (kebab-case, ≤40 chars).

**Note body (all kinds) — minimum frontmatter and structure:**

```markdown
---
kind: absorption | bug | issue
source_workspace: <project.name>
source_workspace_code: <project.code>
source_run: /acw-instance upgrade
source_date: YYYY-MM-DD
source_acw_version: <last_reconciled_version after this run>
status: pending
---

# <one-line title>

## Summary

<2–4 sentences. What was observed. Why it warrants ACW's attention.>

## Detail

<For absorption: the pattern, its current location in workspace, the proposed canonical shape.>
<For bug: the canonical file/path involved, the observed-vs-expected delta, a minimal repro if applicable.>
<For issue: the concern, the operator's framing if relevant, any candidate resolutions.>

## Source pointer

<Workspace-local pointer (decision-log entry id, file path, run summary line) so the ACW operator can ask back if needed.>
```

**Per-kind execution detail:**

*`absorption`* (one row per `absorption-candidate` plan row):

1. Render the note per the format above plus `rules/multi-instance-topology.md` § "Absorption candidate format" (which extends the body with diff/rationale fields).
2. Write to the path above.
3. Record divergence locally: append to `acw-state.yaml::divergent_pending_review` with `path`, `absorption_candidate` (path to the `.acw/raw/` note), `sent_date: <today>`, `status: pending`.
4. The source file stays in place pending ACW's review. Do NOT delete or reshape it.

*`bug`* (captured mid-execution; flushed at end-of-run):

1. When the verb encounters a canonical defect during bulk execution, it appends an in-memory signal record (kind=bug, title, detail) to a run-scoped capture buffer. Execution continues unless the defect hard-blocks the current row.
2. At end-of-run flush (after step 9 of bulk execution), each buffered bug renders to a note and writes to the path above.
3. No local divergence record is created — bugs are about canonical, not about this workspace.
4. Each bug emitted is also referenced in this run's decision-log entry under a "Canonical defects surfaced upstream" sub-section.

*`issue`* (added at plan-approval time, or auto-captured mid-run):

1. At plan-approval time, the verb invites a free-text issue note: *"Anything else you noticed about canonical during plan review worth surfacing upstream? Leave blank to skip; otherwise one-line title plus optional detail."* Multiple issues may be added.
2. The verb may also auto-capture issues during execution for soft-cases (e.g., warning lines from `tools/manifest.py`, `synced_to` field lag, recommended-block entries the operator chose to defer).
3. At end-of-run flush, each issue renders to a note and writes to the path above.
4. Issues are referenced in this run's decision-log entry under a "Canonical follow-ups surfaced upstream" sub-section.

**End-of-run summary line.** After bulk execution, print:

```
Cross-repo signals emitted to ACW/.acw/raw/: <Tabs> absorption, <Tbugs> bug, <Tissues> issue
```

If authority was declined, print instead:

```
Cross-repo signals captured but NOT emitted (cross_repo_writes not declared):
  absorption: <list of titles>
  bug:        <list of titles>
  issue:      <list of titles>
Copy by hand to ACW/.acw/raw/ if you want them landed.
```

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
- If a rejection notification exists in this workspace's `.acw/raw/` from ACW (filename pattern `acw-rejection-<topic>.md`) → mark `rejected`, surface to operator. The rejected file then routes via the next `/acw-instance audit` as `move` or `reshape` to canonical.
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
- **Decision:** one-line summary + per-action counts (moves, reshapes, merges, write-canonical, deletes, instance-specific declarations, absorption candidates, canonical bugs surfaced, canonical issues surfaced, recommended-blocks gaps reconciled, canonical manifest fetched).
- **Canonical defects surfaced upstream:** one-line per `bug` signal emitted, each pointing to the `.acw/raw/` filename written. Empty section if none.
- **Canonical follow-ups surfaced upstream:** one-line per `issue` signal emitted, each pointing to the `.acw/raw/` filename written. Empty section if none.
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
  Canonical bugs surfaced: <Tbugs>
  Canonical issues surfaced: <Tissues>
  Recommended blocks added to acw-state.yaml: <V>

Cross-repo signals emitted to ACW/.acw/raw/: <list of filenames, grouped by kind>
[Cross-repo signals captured but NOT emitted (cross_repo_writes undeclared): <list>]  <-- only if authority declined

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
- Cross-repo writes (absorption candidates, canonical bugs, canonical issues — all three signal kinds emitted to `ACW/.acw/raw/`) require explicit `cross_repo_writes` declaration. One prompt per run, not per signal.
- The verb never demotes layers, never removes blocks from `acw-state.yaml` without operator confirmation via `[?]` row, and never auto-commits the migration.

## Output

- Edits across the substrate boundary identified in Step 4 of the spine.
- Refresh of `rules/instance-current-manifest.md` from canonical.
- One or more decision-log entries (one for the migration, one per `instance-specific` declaration).
- Zero or more cross-repo signals in `ACW/.acw/raw/` (kinds: `absorption`, `bug`, `issue`).
- Chat summary report.
- Operator commits the migration manually after review.
