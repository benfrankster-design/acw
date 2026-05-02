---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Instance Current Manifest

Declarative registry of recommended blocks an ACW instance should carry to be current with this version of ACW. The session-start bookend skill (`/resume-session`) reads this file, compares against the instance's `acw-state.yaml`, and surfaces a one-line drift alert when gaps are detected. The `/upgrade-instance` skill walks the operator through reconciliation.

Each entry below documents one recommended block: what it is, why it helps, whether it's required, how to add it, and the ACW version in which it earned its build. The drift check uses the **earned in** field to suppress alerts for blocks that landed before the instance's `last_reconciled` date.

The current ACW version is declared in `acw-state.yaml::version`. An instance is "current" when every recommended block whose `earned in` is at-or-before the ACW version is present in its state file.

---

## `project` block

- **What:** A `project:` block in `acw-state.yaml` with `name`, `code`, `domain` fields.
- **Why it helps:** Enables `D-{CODE}-NNN` and `HR-{CODE}-NNN` id prefixing in the decision log and hard-rules file. Names the project in narrative output. Without it, ids ship unprefixed and narrative falls back to the repo's directory name.
- **Required:** No. The bookend skill ships unprefixed ids (`D-NNN`, `HR-NNN`) when the block is absent.
- **How to add:** Edit `acw-state.yaml`. Add a top-level block:
  ```yaml
  project:
    name: "<human-readable name>"
    code: "<short identifier, e.g. 'ACW' or 'CP'>"
    domain: "<primary domain>"
  ```
- **Earned in:** `0.2.0-rc3`.

## `paths` block

- **What:** A `paths:` block in `acw-state.yaml` listing every substrate file path.
- **Why it helps:** Decouples the bookend skills from hardcoded paths. The skills read paths from this block at runtime. Future template evolution that moves a substrate file requires only one edit per instance instead of grepping skills.
- **Required:** No. When absent, consumers fall back to canonical defaults documented in `rules/manifest-discipline.md`.
- **How to add:** Edit `acw-state.yaml`. Add a top-level block matching the canonical defaults:
  ```yaml
  paths:
    decisions_log: decisions/decision-log.md
    tasks_status: tasks-status.md
    build_log: build-log.md
    glossary: glossary.md
    threat_model: threat-model.md
    incidents: incidents.jsonl
    evolution: research/evolution.md
    sources: research/sources.md
    research_state: research/research-state.yaml
    problem_framing: research/01-problem-framing.md
    session_captures_dir: research/sessions
    research_queries_dir: research/queries
    research_queries_consumed_dir: research/queries/_consumed
    inbox_dir: _inbox
  ```
  Override any key the instance places elsewhere; omit keys that match the default.
- **Earned in:** `0.2.0-rc4`.

## `auto_load_at_session_start`

- **What:** A list block in `acw-state.yaml` naming files agent hosts auto-load at session start.
- **Why it helps:** The cross-vendor contract per `AGENTS.md` directive 7. Each host implements via its native mechanism (Claude Code: `@`-imports in `CLAUDE.md`).
- **Required:** No. When absent, the host has no canonical auto-load list and either reads nothing automatically or relies on host-specific files only.
- **How to add:** Edit `acw-state.yaml`. Add the block:
  ```yaml
  auto_load_at_session_start:
    - decisions/decision-log.md
    - rules/instance-hard-rules.md
    - tasks-status.md
    - glossary.md
    - incidents.jsonl
  ```
  Add or remove entries as substrate enters/leaves the auto-load discipline.
- **Earned in:** `0.2.0-rc1`.

## `template_layer`, `instance_layer`, `meta_layer`

- **What:** Three list blocks classifying every file in the workspace per `rules/manifest-discipline.md`.
- **Why it helps:** Workspaces that serve as both an instance and a template (i.e., spawn child workspaces) need explicit classification so the scaffold tool knows what to propagate and what to keep local. One-off instances that don't spawn children can leave these blocks empty and absorb no overhead.
- **Required:** No. Blocks may be present-but-empty or absent. The bookend skill's manifest-classification step silently skips when blocks are empty.
- **How to add:** Edit `acw-state.yaml`. See `rules/manifest-discipline.md` for the schema and the default-to-instance discipline.
- **Earned in:** `0.2.0-rc2`.

## `empty_dirs`

- **What:** A list block naming directories the scaffold tool creates with `.gitkeep` markers when scaffolding a child instance.
- **Why it helps:** Ensures the canonical directory layout is present in scaffolded children from session zero, even when the directories start empty.
- **Required:** No. Workspaces that don't spawn children can leave the block empty or absent.
- **How to add:** Edit `acw-state.yaml`. Typical defaults:
  ```yaml
  empty_dirs:
    - research/sessions
    - research/queries
    - research/queries/_consumed
    - skills
    - deferred
  ```
- **Earned in:** `0.2.0-rc2`.

## `cross_repo_writes`

- **What:** A list block enumerating absolute paths outside the project repo that the bookend skill is allowed to write to.
- **Why it helps:** Vault-boundary discipline. By default the skill refuses to write outside the project repo. Instances that legitimately need cross-repo writes (e.g., publishing to a docs site, dropping notifications into a shared inbox) declare those targets explicitly here.
- **Required:** No. Empty list or absent block means no external writes allowed.
- **How to add:** Edit `acw-state.yaml`. List paths the skill may write to.
- **Earned in:** `0.2.0-rc1`.

## `synapse_log_path`

- **What:** A scalar string declaring an operator-personal cross-project day-index directory. The bookend skill's Phase 4 appends a session block there.
- **Why it helps:** Provides a per-day cross-project index for operators who work across many projects. Optional convenience.
- **Required:** No. `null` or absent disables Phase 4 entirely; the skill skips silently.
- **How to add:** Edit `acw-state.yaml`. Set `synapse_log_path: <absolute path>` for the operator's personal day-index directory.
- **Earned in:** `0.2.0-rc1`.

## `voice`

- **What:** A list block declaring voice-reference files applied during transcript cleanup in Phase 1.
- **Why it helps:** Lets the skill enforce the operator's voice conventions (brand voice, customer voice, etc.) when cleaning the transcript before persistence.
- **Required:** No. Empty list or absent means no voice opinion.
- **How to add:** Edit `acw-state.yaml`. List paths to voice-reference files.
- **Earned in:** `0.2.0-rc1`.

---

## How `/resume-session` reads this file

At session start, the skill walks each entry above. For each entry, the skill compares the entry's **earned in** version against `acw-state.yaml::last_reconciled_version` (NOT against `last_reconciled`, which is a date). Version comparison uses semantic-version ordering with rc-suffixes treated as pre-release (e.g., `0.2.0-rc1 < 0.2.0-rc2 < 0.2.0`).

For each entry whose earned-in version is newer than `last_reconciled_version`, the skill checks whether the block is present in the instance's state file:

- **Block absent from file** → counts as missing; flag.
- **Block present-but-empty** (e.g., `template_layer: []`) → counts as DELIBERATELY OPTED OUT; do not flag. Present-but-empty is the operator's explicit choice.
- **Block present and populated** → not missing; do not flag.

For each entry whose earned-in version is at-or-before `last_reconciled_version`, do not flag regardless of presence. The instance has already been reconciled past that point.

If the gap list is non-empty, the skill emits one alert line:

```
[acw-drift] Your instance is reconciled to ACW <last_reconciled_version> as of <last_reconciled>. Current ACW (<version>) expects N additional blocks: <names>. Run /upgrade-instance to reconcile.
```

Otherwise the skill stays silent on drift.

If `last_reconciled_version` is absent from the state file, the skill treats it as `"0.0.0"` — every recommended block whose earned-in version is set will be flagged. This produces a noisy first run for very old instances; running `/upgrade-instance` once quiets the alert.

`last_reconciled` is the human-friendly date the reconciliation happened. `last_reconciled_version` is the semantic ACW version the reconciliation synced to. Both are bumped automatically by `/upgrade-instance` after a successful reconciliation pass.

## How `/upgrade-instance` reads this file

The upgrade skill walks each entry, detects gaps, and surfaces the canonical default content alongside the operator's three options (add as proposed / modify / skip). On confirmation, the skill writes the chosen blocks via `tools/manifest.py::append`, bumps `last_reconciled`, and logs a decision-log entry recording the reconciliation.

## Maintenance

When ACW ships a new recommended block in a future version, append a new entry to this file with the same fields (What / Why it helps / Required / How to add / Earned in). The earned-in version sets the floor for when existing instances start seeing the block as drift.

Adding an entry to this file is itself a substrate shift. The bookend skill's Phase 2 host-entry-file maintenance step may propose updates to `CLAUDE.md` (or other host entry files) when a new block enters the recommended registry.
