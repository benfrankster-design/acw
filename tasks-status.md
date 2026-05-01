---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Tasks Status — ACW

Three-section task tracker. See `rules/task-tracking.md` for format and discipline.

## Pending

- [ ] Decide: ship `tools/scaffold-instance.py` under emergency clause (D-02 single incident) or wait for two more bootstrap-related incidents.
- [ ] Sync `~/synapse/Rules/Procedures/` copies with ACW canonical (mitigation for D-01).
- [ ] Decide: defer C-04 synthesis-cycle to `DEFERRED.md` (only one cycle of evidence) or ship now.
- [ ] Promote v0.2.0-rc1 to v0.2.0 after release-gate verification (lint, tests).

## Done

### 2026-04-30 — RC3: ACW as instance of itself; manifest-discipline rule extracted (Session 3)

- Added `project:` block to `acw-state.yaml` (`code: ACW`, `domain: meta-template`). D-ACW-006.
- Bumped version to `0.2.0-rc3`.
- Updated `skills/capture-and-metabolize/SKILL.md`: documented config fields as optional with defaults; added Phase 2 conditional manifest-classification step.
- Created `rules/manifest-discipline.md` (template_layer) — generic pattern documentation. D-ACW-007.
- Trimmed `LAYERS.md` to ACW-specific narrative (meta_layer); points at `rules/manifest-discipline.md`.
- Added `rules/manifest-discipline.md` to `acw-state.yaml::template_layer` and `auto_load_at_session_start`.
- First real dogfood of `capture-and-metabolize` against the sandbox clone: all five phases fired. Capture at `research/sessions/2026-04-30--rc3-acw-as-instance.md`.
- Logged process-gap incident: agent skipped Phase 2 in initial dogfood; corrected by operator (turn 37).

### 2026-04-30 — Three-layer manifest shipped (Session 2)

- Added `template_layer`, `instance_layer`, `meta_layer`, `empty_dirs` blocks to `acw-state.yaml`.
- Refactored `tools/scaffold-instance.py` to read from the manifest. Hardcoded constants removed; script is ~30 lines of logic over the yaml instead of ~100 lines of lists.
- Added `tools/templates/README.md.tmpl` so new instances ship with an operator-facing README.
- Added `LAYERS.md` (meta_layer) explaining the three-bucket model.
- Recorded D-005 in `decisions/decision-log.md`.
- All release gates green: scaffold dry-run + real, lint, tests, drift check.

### 2026-04-30 — gsg-copilot instance extensions absorbed (Session 1)

- Wrote `research/09-gsg-copilot-instance-extensions.md` proposing C-01 through C-09.
- Logged incidents D-01 (synapse-rule-sync) and D-02 (instance-bootstrap).
- Shipped `tools/scaffold-instance.py` + `tools/templates/` (single-incident emergency promotion for D-02).
- Added `--category` enum to `tools/log-incident.py` (C-09).
- Added `rules/task-tracking.md` (C-01) and `rules/incident-tracking.md` (C-09).
- Created `tasks-status.md` and `build-log.md` at repo root, added to canonical_runtime_files (C-01, C-02).
- Added `auto_load_at_session_start` to `acw-state.yaml` (C-06).
- Added directive 7 to `AGENTS.md` documenting the auto-load convention (C-06).
- Ported `capture-and-metabolize` and `resume-session` from gsg-copilot; retired `skills/capture-session/` (C-03).
- Bumped `acw-state.yaml::version` to `0.2.0-rc1`.

## Parked

- C-04 synthesis-cycle: single cycle of evidence is too thin. Defer to DEFERRED.md or wait.
- C-05 runbooks layer: operator-preference-flavored. Document as recommended, not normative.
- C-07 vault-boundary as hard rule: include as suggested starting rule in instance-hard-rules template, not normative globally.
- C-08 backlog triple-tag: recommended convention only, not normative.
