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
