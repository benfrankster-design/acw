---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Manifest Discipline

A recurring pattern in ACW-derived workspaces: any list that (a) names "what files matter" or "what terms matter," (b) is consumed by multiple subsystems, (c) changes over time, and (d) has asymmetric failure cost — wants the same shape. **Single source of truth, additive maintenance by skill, removal by ritual, lint as the safety net.**

This rule documents the shape so future authors don't reinvent it.

## When this rule applies

- A list of files that propagate to derived workspaces vs. files that stay
- A list of files agent hosts auto-load at session start
- A list of approved canonical terms in a vocabulary
- Any equivalent enumeration that drives behavior across multiple consumers

## The three-layer manifest (the load-bearing case)

Workspaces that serve as both an instance (have their own substrate) and a template (spawn child workspaces) carry a three-layer classification of every file. The shape is MECE.

| Layer | Definition | Goes to scaffolded children? |
|---|---|---|
| `template_layer` | Same file in this workspace and every child instance | Yes, verbatim |
| `instance_layer` | This workspace has populated content; children get a templated initial form | Yes, rendered from a template |
| `meta_layer` | Exists only in this workspace; never propagated | No |

The discriminator: *does a child instance have this file? if yes, in the same form or a customized form?* Three answers, three buckets.

Working metaphor: think of `create-react-app`. It ships dotfiles every new project gets verbatim (template_layer), files like `package.json` that get token-substituted per project (instance_layer), and the CRA repo's own README and CHANGELOG that aren't part of any spawned project (meta_layer).

A workspace that does NOT spawn children (a one-off project) ships with the manifest blocks present but empty. The classification machinery is available; the use is conditional.

## Where the manifest lives

`acw-state.yaml` carries the classification:

```yaml
template_layer:
  - rules/pipeline-roles.md
  - tools/lint-vocab.py
  # ... one line per file or directory

instance_layer:
  - path: decisions/decision-log.md
    template: tools/templates/decision-log.md.tmpl
  - path: incidents.jsonl
    template: null    # empty initial state, no token substitution
  # ... per-file template pairing

meta_layer:
  - LINEAGE.md
  - CHANGELOG.md
  # ... one line per file
```

`empty_dirs` is a sibling block listing directories the scaffolder creates with `.gitkeep` markers.

## How the system uses it

Three consumers read the manifest. None carry a second copy.

**`tools/scaffold-instance.py`** reads `template_layer` and `instance_layer`. For each `template_layer` entry it copies verbatim. For each `instance_layer` entry it renders the named template (or writes empty if `template: null`) with token substitution. `meta_layer` is intentionally not iterated. The script is a thin renderer over the manifest, not a second source of truth.

**`capture-and-metabolize` Phase 2** maintains the lists additively. When a session creates a new file at a tracked path (root, `rules/`, `tools/`, `skills/`), the skill surfaces "template_layer or instance_layer or meta_layer?" to the operator and appends the answer. Default is `instance_layer` (see asymmetry rationale below). Removal or layer-demotion (template → instance, template → meta) is forbidden by the skill; both go through `decisions/decision-log.md`.

**The lint** walks the filesystem and warns on any unclassified file at root or in `rules/`, `tools/`, `skills/`. Warns rather than blocks until enforcement is earned by an incident.

## Why default-to-instance

The asymmetry of mistakes drives the asymmetry of the default.

- **Wrong direction (template → instance promotion):** a child instance that needed a file doesn't get it. The operator notices when something downstream fails. Recoverable: edit the manifest, re-scaffold, or copy the file in.
- **Wrong direction (instance → template misclassification, or default-to-template):** this workspace's history ships into a child's project. The child operator may not notice for weeks. Embarrassing in a consulting context, leakage in a security context.

Defaulting new files to `instance_layer` keeps the costly mistake far away. Promoting a file to `template_layer` is an explicit decision-log entry, which is the right friction for the right direction.

## Operator quick-reference

When you create a new file at the workspace root or in `rules/`, `tools/`, `skills/`:

1. Decide its layer: does the file describe this workspace itself (meta), or generic doctrine every child should get (template), or this workspace's own substrate that children will customize (instance)?
2. Add it to the right block in `acw-state.yaml`.
3. If it's `instance_layer`, also write a template form in `tools/templates/` (unless the file should ship empty, in which case use `template: null`).
4. Run the scaffolder with `--dry-run` to verify the file appears in scaffolded output (or correctly does not, if meta).

When you delete or demote a file across layers:

1. Open `decisions/decision-log.md` and write an entry naming the change and the reason.
2. Then edit the manifest.

When the lint warns about an unclassified file: pick its layer, add it to the manifest, don't `--no-verify`.

## Canonical default paths

The bookend skills and any other consumer that needs to locate substrate read paths from `acw-state.yaml::paths`. If a key is absent from that block, consumers fall back to the canonical defaults below. Defaults match the layout produced by `tools/scaffold-instance.py` for a fresh instance.

| Key | Default path |
|---|---|
| `decisions_log` | `decisions/decision-log.md` |
| `tasks_status` | `tasks-status.md` |
| `build_log` | `build-log.md` |
| `glossary` | `glossary.md` |
| `threat_model` | `threat-model.md` |
| `incidents` | `incidents.jsonl` |
| `evolution` | `research/evolution.md` |
| `sources` | `research/sources.md` |
| `research_state` | `research/research-state.yaml` |
| `problem_framing` | `research/01-problem-framing.md` |
| `session_captures_dir` | `sessions` |
| `research_queries_dir` | `research/queries` |
| `research_queries_consumed_dir` | `research/queries/_consumed` |
| `buffer_dir` | `_buffer` |
| `plans_dir` | `plans` |
| `runbooks_dir` | `runbooks` |
| `integrations_dir` | `integrations` |
| `briefings_dir` | `briefings` |
| `context_dir` | `context` |
| `inbox_dir` | `inbox` |

An instance that wants to override one or more of these declares the override in its `acw-state.yaml::paths` block. Defaults remain in effect for any key the instance does not override.

## Manifest tooling spec

Any consumer that reads or writes a manifest list in `acw-state.yaml` (the three layer blocks, `auto_load_at_session_start`, `paths`, future blocks) implements the same four operations. The reference implementation lives in `tools/manifest.py`; consumers in other languages or runtimes implement the same contract.

### `load(state_file, list_name)`

Returns the list from the named block, with canonical defaults applied for any missing keys (where the spec defines defaults — see `paths` above). Returns an empty list when the block is absent and no defaults are defined. Never raises on a missing block; raises only on malformed yaml.

For dict-shaped blocks like `paths`, `load` returns a dict where the layered result is `{canonical_defaults, **state_file_overrides}`. For list-shaped blocks like `auto_load_at_session_start` and `template_layer`, `load` returns the list as-is from the state file (or empty if absent); list-shaped blocks have no canonical defaults beyond "empty list."

### `append(state_file, list_name, value)`

Adds `value` to the named list. Refuses duplicates (no-op or raises `ManifestError`, consumer's choice — the spec says no-op is acceptable). Refuses unknown list names. Preserves yaml comments and key ordering on write. Implementations that cannot preserve comments must declare that limitation in their docstring.

For dict-shaped blocks, `append` is interpreted as set/upsert: `append(state_file, "paths", {"key": "new/path"})` adds or updates the `key` entry under `paths`.

### `contains(state_file, list_name, value)`

Returns `True` when `value` appears in the named list (or matches a key in a dict-shaped block). Reads the canonically-defaulted view (so `contains(state_file, "paths", "decisions_log")` returns `True` even if the block is absent, because defaults provide the key).

### `validate(state_file, list_name)`

Raises `ManifestError` when:
- The list contains duplicate entries (for list-shaped blocks).
- An entry's shape does not match the block's expected schema (for example, an `instance_layer` entry missing `path`).
- For `paths`, a value is not a string.

Returns `None` on success. Implementations may extend validation with consumer-specific checks (e.g., the lint may verify that paths in `paths` resolve to existing files); those checks live in the calling consumer, not in the reference `validate`.

### Schema reference

| Block | Shape | Item schema | Defaults |
|---|---|---|---|
| `template_layer` | list | string (path or dir) | none (empty) |
| `instance_layer` | list | dict with `path` (required), `template` (required, may be null), optional `host`, `instance_only` | none (empty) |
| `meta_layer` | list | string (path) | none (empty) |
| `empty_dirs` | list | string (path) | none (empty) |
| `auto_load_at_session_start` | list | string (path) | none (empty) |
| `paths` | dict | string keys, string values | see "Canonical default paths" above |
| `project` | dict | `name`, `code`, `domain` (all string) | none (instance-specific; operator-supplied) |
| `cross_repo_writes` | list | string (absolute path) | none (empty) |
| `voice` | list | string (path) | none (empty) |

A consumer that needs additional schema (e.g., extra fields on `instance_layer` entries) extends this table in its own scope and validates accordingly.

## The recurring pattern

The manifest shape now appears at least three times in ACW:

1. `auto_load_at_session_start` — files agent hosts auto-load at session start
2. `template_layer` / `instance_layer` / `meta_layer` — what propagates and what doesn't
3. The vocabulary canon (per `rules/canon-governance.md`) — terms governed by a state machine, lint as the safety net

Each one shares the four properties named at the top of this rule. Each one wants the same shape: single source of truth, additive maintenance by skill, removal by ritual, lint as the safety net.

When you encounter a fourth case of this pattern, write the new manifest in `acw-state.yaml` (or a sibling state file if scope warrants), wire its consumers to read from it, and add a lint check. Resist the urge to invent a new shape; the same pattern works.

## Recursive instances

Workspaces that themselves serve as templates for further-derived instances apply this same model recursively. A consultancy workspace (e.g., one that scaffolds per-client engagement workspaces) has its own `template_layer` (what every client engagement gets), `instance_layer` (the consultancy's own ops content), and `meta_layer` (about-the-consultancy-only). Its scaffold tool produces clean-palette children just like ACW's does.

The pattern survives recursion because the manifest is local to each workspace. ACW's manifest classifies ACW's files. A derived workspace's manifest classifies its own files. Children of children classify their own files. Each level decouples its own published-state from the children it spawns.
