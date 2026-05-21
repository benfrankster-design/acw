---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Instance types

ACW supports multiple instance types. Each type names a default substrate module set; instances may deviate by editing `modules:` directly in `acw-state.yaml`. The profile is a starting shape, not a lock-in.

## The enum

| Profile | Mental model | Primary use |
|---|---|---|
| `org-brain` | Personal or organizational knowledge management. Substrate IS the artifact. | Synapse-shaped instances. Decisions, glossary, sessions, build-log, incidents, briefings, archives, inbox, raw. |
| `spec-project` | Design substrate with deliverable. Decision-heavy. | cs-ops-spec, frank-context. Decisions (entries + open-questions + constraints), sessions, glossary, tasks-status, incidents, raw, plans, build-log, research. |
| `coding-project` | Code + substrate hybrid. Library or service with operator-side reasoning. | cs-atlas, gsg-cs-chatbot, gsg-cs-atlas-mcp. Decisions, sessions, tasks-status, incidents, codemap, raw, build-log. |
| `library` | Minimal substrate around a code artifact. | Smaller code projects. Decisions, codemap, raw, build-log. |
| `custom` | Bespoke. Operator declares modules explicitly. | Edge cases that don't fit the four named profiles. |

## Default modules per profile

The skill `/acw-instance audit` consults this table to know which modules to expect when validating an instance.

```yaml
# Canonical defaults — instances may deviate by overriding `modules:` directly.

org-brain:
  - decisions          # entries + open-questions + constraints
  - glossary
  - sessions
  - build-log
  - incidents
  - tasks-status
  - raw
  - plans
  - briefings
  - inbox
  - archives
  - research

spec-project:
  - decisions
  - glossary
  - sessions
  - tasks-status
  - incidents
  - raw
  - plans
  - build-log
  - research

coding-project:
  - decisions
  - sessions
  - tasks-status
  - incidents
  - codemap
  - raw
  - build-log

library:
  - decisions
  - codemap
  - raw
  - build-log

custom:
  # No defaults. Operator declares every module explicitly.
  []
```

## Module → substrate path mapping

When a module is declared, ACW skills consult `acw-state.yaml::paths` for the actual location. Module names are stable; paths can vary per instance.

| Module name | Default path (under `.acw/`) | Path key in acw-state.yaml |
|---|---|---|
| `decisions` | `.acw/decisions/` | `decisions_entries_dir`, `decisions_open_questions_dir`, `decisions_constraints_dir`, `decisions_index` |
| `glossary` | `.acw/glossary/` | `glossary_entries_dir`, `glossary_index` |
| `sessions` | `.acw/sessions/` | `session_captures_dir` |
| `tasks-status` | `.acw/tasks-status.md` | `tasks_status` |
| `incidents` | `.acw/incidents.jsonl` | `incidents` |
| `build-log` | `.acw/build-log.md` | `build_log` |
| `raw` | `.acw/raw/` | `raw_dir` |
| `plans` | `.acw/plans/` | `plans_dir` |
| `briefings` | `.acw/briefings/` | `briefings_dir` |
| `inbox` | `.acw/inbox/` | `inbox_dir` |
| `archives` | `.acw/archives/` | `archives_dir` |
| `research` | `research/` (project artifact, NOT under .acw/) | `research_state`, `research_queries_dir`, etc. |
| `codemap` | `.acw/codemap/` | `codemap_dir`, `codemap_report` |

`research/` stays at root because it's a project artifact in spec-project and org-brain instances, not ACW metadata. See `rules/substrate-boundary.md` for the substrate-vs-artifact distinction.

## Declaring profile and modules

`acw-state.yaml` gains two top-level fields:

```yaml
profile: coding-project          # one of: org-brain | spec-project | coding-project | library | custom
modules:                         # explicit module list; overrides profile defaults if both set
  - decisions
  - sessions
  - tasks-status
  - incidents
  - codemap
  - raw
  - build-log
```

If `profile:` is set and `modules:` is omitted, the profile defaults apply.
If `modules:` is set explicitly, it supersedes profile defaults.
If neither is set, the instance is treated as `spec-project` (closest match to pre-0.10.0 canonical shape) with a warning surfaced at audit time prompting the operator to declare explicitly.

## How skills consume this

Every ACW skill that touches substrate must:

1. Read `acw-state.yaml::profile` and `acw-state.yaml::modules` at session start (via `tools/manifest.py::load`).
2. Resolve the effective module list (profile defaults + explicit overrides).
3. Skip operations on modules not in the effective list. Do not error on absence — absence is a declared choice.
4. Validate operations against the module's path declaration in `paths:`. Never hardcode a substrate path.

## When the canonical enum changes

Adding a new profile or module type is a breaking schema change:

1. Add the profile or module to this file.
2. Update `rules/manifest-discipline.md` with the path key contract.
3. Update `rules/substrate-shape.md` if the new module has a non-default shape (wiki vs flat).
4. Bump `acw-state.yaml::version` minor (breaking schema) or patch (additive).
5. Log a decision-log entry.

Removing a profile or module is a major version bump and requires migration path documentation.
