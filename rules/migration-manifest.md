---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Migration manifest

Schema and conventions for `migrations/<from>-to-<to>.yaml` files in the ACW canonical repo. Each manifest declares the steps to upgrade an instance from one canonical version to the next. The `/acw-instance upgrade` skill reads a manifest and executes its steps generically; it does not know about specific versions.

## Why this exists

Skills are thin portable executors. The canonical repo is the source of truth. Migration knowledge belongs in declarative data files inside canonical, not embedded in skill prose. New canonical version → new manifest file in `migrations/` → instances pick up the upgrade path on next `/acw-instance upgrade`. Skill code does not change per version bump.

## Layout

```
acw/
├── migrations/
│   ├── 0.9.7-to-0.9.8.yaml
│   ├── 0.9.8-to-0.9.9.yaml
│   ├── 0.9.9-to-0.10.0.yaml
│   └── README.md            # operator-facing index
├── rules/
│   └── migration-manifest.md  # this file
└── ...
```

Naming: `<from_version>-to-<to_version>.yaml`. Exactly one manifest per consecutive-version pair. Skipping versions is not supported in v0.10.0; an instance two versions behind runs two manifests in order.

## Top-level schema

```yaml
from_version: "0.9.9"           # required — exact match against instance acw-state.yaml::version
to_version: "0.10.0"            # required — version the instance will be at after success
breaking: true                  # required boolean — does this break paths, schema, or skill API
description: "..."              # required — one-line human summary, surfaced in audit/upgrade plan
authority: "D-ACW-050"          # required — the canonical decision that authored this migration

prerequisites:                  # optional — gates that must pass before executing
  - kind: clean_working_tree
  - kind: minimum_version
    minimum: "0.9.7"            # refuse if instance is older than this

steps:                          # required — ordered list, executed serially
  - kind: <step-kind>
    ...
```

## Step kinds (v0.10.0 enum)

Each step has a `kind` field and parameters specific to that kind. The executor walks the steps in order. A step failure aborts the migration; the executor leaves the partial state visible and emits a recovery instruction.

### `create_dir`

Create a directory. Idempotent (no-op if exists).

```yaml
- kind: create_dir
  path: .acw
```

### `git_mv`

Move tracked files via `git mv` (preserves history). Accepts a list of (from, to) pairs. All moves run as one atomic batch; if any one fails, none persist.

```yaml
- kind: git_mv
  moves:
    - { from: decisions, to: .acw/decisions }
    - { from: glossary, to: .acw/glossary }
    - { from: sessions, to: .acw/sessions }
    - { from: _buffer, to: .acw/raw }       # rename + relocate in one move
```

### `update_acw_state`

Patch `acw-state.yaml` (after migration, the file is already at its new path if relocated by an earlier `git_mv` step; this step reads/writes from the new location).

```yaml
- kind: update_acw_state
  path_prefix_substrate:                    # add prefix to every substrate path
    prefix: .acw/
    keys:                                   # which paths-block keys to prefix
      - decisions_index
      - decisions_entries_dir
      - glossary_index
      - tasks_status
      - build_log
      - incidents
      - session_captures_dir
      - plans_dir
      - briefings_dir
      - inbox_dir
  rename_keys:                              # rename keys in the paths block
    buffer_dir: raw_dir
  add_fields:                               # add new top-level fields
    profile: spec-project                   # default; operator confirms during upgrade
    modules: null                           # null = use profile defaults
  set_fields:                               # overwrite existing top-level fields
    version: "0.10.0"
    last_reconciled_version: "0.10.0"
    last_reconciled: "<DATE>"               # special token: substituted with today's date
```

### `update_file`

Targeted text replacement in a tracked file. For simple known-content patches. Refuses on conflict (no auto-merge).

```yaml
- kind: update_file
  path: AGENTS.md
  replace:
    - find: "decisions/INDEX.md"
      with: ".acw/decisions/INDEX.md"
    - find: "tasks-status.md"
      with: ".acw/tasks-status.md"
```

### `rebuild_index`

Regenerate an INDEX.md file from its entries directory. Calls `tools/build-index.py` (or equivalent) with the configured path.

```yaml
- kind: rebuild_index
  paths:
    - .acw/decisions/INDEX.md
    - .acw/glossary/INDEX.md
```

### `add_file`

Create a new tracked file with declared content. Idempotent on identical content; refuses on conflict (content differs from declared).

```yaml
- kind: add_file
  path: .acw/decisions/entries/D-ACW-050-acw-substrate-under-dotfolder-and-instance-types.md
  content_template: tools/templates/migration-decision.md.tmpl
  content_tokens:
    DECISION_ID: D-ACW-050
    DATE: "<DATE>"
```

### `remove_gitignore_rule`

Edit `.gitignore` to remove a specific line. For cases like v0.10.0 where `.acw/` was previously ignored and the rule must be retired.

```yaml
- kind: remove_gitignore_rule
  rule: ".acw/"
  reason: "v0.10.0 flips .acw/ from runtime-cache to canonical substrate; ignore rule must be retired."
```

### `run_hook`

Execute a script from `tools/migration-hooks/<name>.py`. Use sparingly — declarative steps are preferred. Hooks exist only for migrations that genuinely can't be expressed declaratively.

```yaml
- kind: run_hook
  script: tools/migration-hooks/v0.10.0-frontmatter-confidence-tagging.py
  rationale: "Walks every wiki entry and adds default INFERRED tags to cross-refs that don't carry an explicit tag. Pure data; declarative form would require per-entry step listing."
```

## Operator interaction during migration

Some steps require operator input that can't be hard-coded in the manifest. The executor pauses at these points, presents the question, and resumes with the answer.

Currently in v0.10.0:

- **`profile:` declaration.** The `update_acw_state::add_fields::profile` value is a default; the executor presents the profile enum (`org-brain | spec-project | coding-project | library | custom`) and asks the operator to confirm or override before writing.
- **`modules:` declaration.** If the operator selected `custom`, the executor prompts for the explicit module list.

Operator-interaction points are documented per manifest in a top-level `operator_prompts:` block:

```yaml
operator_prompts:
  - field: profile
    prompt: "Instance type for this workspace?"
    enum: [org-brain, spec-project, coding-project, library, custom]
    default: spec-project
    affects: update_acw_state.add_fields.profile

  - field: modules
    prompt: "If profile is custom, declare the explicit module list (one per line, empty to abort)."
    type: list
    only_if: { field: profile, equals: custom }
    affects: update_acw_state.add_fields.modules
```

## Audit before upgrade

`/acw-instance audit` reads the appropriate manifest for the instance's current version and produces a per-step plan with the current state, the post-step state, and any operator prompts. The plan is reviewable before upgrade executes.

`/acw-instance upgrade` is plan-execution under a single approval gate. After the operator approves the plan, the executor walks steps serially.

## Recovery on failure

If a step fails mid-migration, the executor:

1. Stops immediately. Does not attempt remaining steps.
2. Emits the failure context: which step, what input, what error.
3. Leaves the partial state visible (no rollback; rollback is operator's choice via git).
4. Emits a recovery instruction: typical fix is `git restore --staged .` + `git checkout .` to reset to pre-migration state, then re-run upgrade after fixing the underlying issue.

The executor does NOT auto-rollback. Rollback decisions are the operator's call.

## Authoring new migrations

When canonical ships a new version:

1. Write the manifest at `migrations/<from>-to-<to>.yaml`.
2. Walk each step kind the manifest uses; verify each is in the executor's supported set. If a new kind is needed, propose it via a decision-log entry first.
3. Test the manifest by running `/acw-instance audit` against a copy of an instance at the `from_version`.
4. Bump `acw-state.yaml::version` in canonical to the `to_version`.
5. Update `migrations/README.md` index.
6. Land the decision-log entry that names the migration's authority.

## Step kinds reserved for future

These are documented as forward-compatible reservations; not yet implemented in v0.10.0:

- `delete_file` — for substrate file retirements
- `delete_dir` — for directory retirements
- `validate_invariant` — runs a check (e.g., "every decision entry has frontmatter `id:` matching its filename") before allowing the next step
- `archive_to` — moves a file into `.acw/archives/` rather than deleting

Reserve step-kind names now to avoid future collisions. Defer implementation until earned by incident.
