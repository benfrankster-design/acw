---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
section_conventions:
  pending: "Pending"
  done: "Done"
  parked: "Parked"
---

# Tasks Status — ACW

Three-section task tracker. See `rules/task-tracking.md` for format and discipline.

## Pending

- [ ] Decide: extract the host entry file generation logic from `tools/scaffold-instance.py` into `tools/templates/` (Option B from the CLAUDE.md follow-up discussion) for single source of truth, or leave as-is.
- [ ] Manually delete `skills/capture-session/` (superseded; careful guardrail blocks automated `rm -rf`).
- [ ] Sync `~/synapse/Rules/Procedures/` copies with ACW canonical (mitigation for D-01).
- [ ] Decide: defer C-04 synthesis-cycle to `DEFERRED.md` (only one cycle of evidence) or ship now.
- [ ] Dogfood `/upgrade-instance` adopt mode against cs-copilot (its substrate-shaped workspace pre-dates registration; should now adopt cleanly).
- [ ] Dogfood `/upgrade-instance` reconcile path against gsg-copilot (older registered instance; should fetch canonical from GitHub and walk gaps).
- [ ] Decide: should `tools/scaffold-instance.py` optionally create user-level skill junctions at scaffold time? (Surfaced by D-ACW-011 session.)
- [ ] Decide: defer C-04 synthesis-cycle to `DEFERRED.md` (only one cycle of evidence) or ship now.
- [ ] Decide: extract the host entry file generation logic from `tools/scaffold-instance.py` into `tools/templates/` for single source of truth, or leave as-is.
- [ ] Manually delete `skills/capture-session/` (superseded; careful guardrail blocks automated `rm -rf`).
- [ ] Sync `~/synapse/Rules/Procedures/` copies with ACW canonical (mitigation for D-01).
- [ ] Add cross-instance write trigger to `DEFERRED.md` for capability broker — three documented incidents earn the broker its ship at lattice scale (per research/10).
- [ ] Promote `v0.3.0` to `v1.0.0` after a soak window once lattice-level dogfooding has accumulated evidence.

## Done

### 2026-05-02 — RC4 → v0.3.0: multi-instance topology, GitHub-first canonical, adopt mode (Session 6)

- Wrote `research/10-multi-instance-topology.md` (meta_layer) — lattice model, knowledge-placement rules, coordination primitive status, Phase 1 spinoff spec.
- Promoted canonical statement to `rules/multi-instance-topology.md` (template_layer). D-ACW-012.
- Added `is_canonical_source` flag to `acw-state.yaml` (set true on ACW; default false in template). D-ACW-013.
- Updated `rules/instance-current-manifest.md`: new entries for `is_canonical_source` and `rules/multi-instance-topology.md` (both earned in v0.3.0). Updated "How `/upgrade-instance` reads this file" to document GitHub-first canonical fetch and adopt mode.
- Rewrote `skills/upgrade-instance/SKILL.md`: GitHub fetch via `gh` CLI (private repo), Step 0/0a registration check + substance scan + adoption flow, fail-closed on GitHub unreachable, write fetched canonical to local cache after each successful pass. D-ACW-014.
- Added canonical-edit detection step to `capture-and-metabolize` Phase 2: computes intersection of `auto_load_at_session_start` and `template_layer`, branches on `is_canonical_source` (publisher gets version-bump-and-push prompt; consumer gets local-edit warning). D-ACW-015.
- Bumped ACW version `0.2.0-rc4` → `0.3.0`. Bumped `last_reconciled_version` to `0.3.0`. Updated template baseline `last_reconciled_version` to `0.3.0`.
- Wired `rules/multi-instance-topology.md` into `template_layer` and `auto_load_at_session_start` in `acw-state.yaml`.
- Push to `origin/master` retired the 8-commits-ahead parked task by landing rc1-rc4 + v0.3.0 in one batch.

### 2026-05-02 — Skill registration via user-level junctions (Session 5)

- D-ACW-011 — registered three bookend-arc skills via user-level directory junctions in `~/.claude/skills/<name>/` pointing at `acw/skills/<name>/`. ACW is the canonical runtime source; child-instance copies are passive.
- Created junctions for `capture-and-metabolize`, `resume-session`, `upgrade-instance`. Verified via `dir /AL ~/.claude/skills/`.
- Surfaced OQ-ACW-006 (should scaffold tool optionally create skill junctions at scaffold time) — deferred for second-instance evidence.
- Logged process-gap incident: ACW skills shipped at `acw/skills/` were not auto-discovered by Claude Code on a fresh operator machine; manual junction setup required. Future scaffold tooling could close the gap.
- Capture file at `research/sessions/2026-05-02--skill-registration-via-junctions.md`.

### 2026-05-02 — RC4: framework-agnostic bookend skills, drift detection, upgrade skill (Session 4)

- Added `paths:` block to `acw-state.yaml` (14 substrate file path declarations). D-ACW-008.
- Documented canonical default paths and four-operation manifest-tooling spec in `rules/manifest-discipline.md`.
- Built `tools/manifest.py` reference implementation (stdlib only, ~330 lines, 33 unit tests, all passing).
- Refactored `skills/capture-and-metabolize/` and `skills/resume-session/` to read paths from `acw-state.yaml::paths` instead of hardcoding. Audited 11 reference files; subagent verified zero hardcoded substrate paths remain in skill content.
- Added `section_conventions` frontmatter to `decisions/decision-log.md`, `tasks-status.md`, `research/evolution.md` (and to their templates so new instances ship with them).
- Created `rules/instance-current-manifest.md` (template_layer) — declarative registry of recommended blocks with what / why / required / how-to-add / earned-in fields. D-ACW-009.
- Added `last_reconciled_version` field to `acw-state.yaml` (and template) for semantic version tracking alongside `last_reconciled` date.
- Added Step 5 drift check to `skills/resume-session/SKILL.md`. Compares each registry entry's earned-in against instance's `last_reconciled_version`; surfaces one-line alert on gaps.
- Built `skills/upgrade-instance/` skill. Walks operator through gap reconciliation; bumps `last_reconciled_version` after pass; logs decision-log entry. D-ACW-010.
- Bumped version to `0.2.0-rc4`.
- Subagent verifications at end of Phase 2, 3, 4, 5 — all caught real ambiguities (spec/impl alignment, hardcoded path scan, version-vs-date conflation, partial-block + malformed-block edge cases). Each fix landed before its phase commit.

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
