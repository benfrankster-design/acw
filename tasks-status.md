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
- [ ] Re-dogfood `/acw-instance audit` against `_Command` after v0.5.0 ships (the audit verb fixes should now produce interactive Mode B prompts and surface absorption candidates correctly; runbooks/integrations/briefings should be marked as canonical-shape OK now that they're absorbed).
- [ ] Dogfood `/acw-instance audit` against cs-copilot (substrate-shaped, below organic threshold; should adopt cleanly).
- [ ] Dogfood `/acw-instance upgrade` against gsg-copilot (older registered instance; should fetch canonical and walk v0.3.0/v0.4.0/v0.5.0 gaps; the v0.5.0 migration step should propose `_inbox/` → `_buffer/` rename).
- [ ] Manually delete superseded skills after dogfood validates v0.4.0: `skills/capture-session/`, `skills/upgrade-instance/`, `skills/resume-session/`, `skills/capture-and-metabolize/` (careful guardrail blocks automated `rm -rf`).
- [ ] Sync `~/synapse/Rules/Procedures/` copies with ACW canonical (mitigation for D-01). Particularly `skill-format.md` since ACW canonical now has the corrected version.
- [ ] Decide: should `tools/scaffold-instance.py` optionally create user-level skill junctions at scaffold time? (OQ-ACW-006 from Session 5.)
- [ ] Decide: extract the host entry file generation logic from `tools/scaffold-instance.py` into `tools/templates/` for single source of truth.
- [ ] Decide: defer C-04 synthesis-cycle to `DEFERRED.md` or ship now.
- [ ] Add cross-instance write trigger to `DEFERRED.md` for capability broker — three documented cross-instance write incidents earn the broker its ship at lattice scale.
- [ ] Add lint gate (in `release_gates`) for command-routed skills: every command in the table has a matching `references/<command>.md`; reference files don't redeclare the spine. Earned when first violation surfaces.
- [ ] Promote `v0.4.0` to `v1.0.0` after a soak window once lattice-level dogfooding has accumulated evidence.

## Done

### 2026-05-03 — v0.6.1: meta-layer backfill from harness's first run (Session 11)

- Accepted all four proposals surfaced by the v0.6.0 meta-layer maintenance harness on its first invocation post-shipping.
- `README.md` directory map extended with `context/` and `inbox/`.
- `LINEAGE.md` backfilled with primitive-trace entries for the entire v0.2.0+ cluster (substrate categories, architectural primitives, skills, tooling, discipline primitives). Closes the v0.1.0-only-traces gap.
- `ORCHESTRATION.md` gained "v0.2.0+ evolution methodology" section documenting the dogfood-driven loop, the recursive earn-by-incident discipline, the maintenance-harness-alongside-structural-fix rule, and the boundary between the v0.1.0 seven-phase arc and the v0.2.0+ loop.
- `SKEPTIC.md` gained Warning 4 ("Substrate is not static") earned by incident `e167b922`. Existing Warning 4 (Reflexive injection) renumbered to Warning 5; file title updated.
- Bumped ACW version `0.6.0` → `0.6.1`. D-ACW-035 records the rationale.
- Validates the meta-layer harness's first-test correctness (OQ-ACW-010 earn-by-incident path appears clean).

### 2026-05-02 — v0.6.0: operator-centric substrate + meta-layer harness (Session 10)

- Shipped `context/` canonical with four templated files (`goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`). Lightweight pointers to operating reality. ACW's own context populated. D-ACW-031.
- Shipped `inbox/` canonical as operator capture surface (folder of dated files). Distinct from `_buffer/` (system) and `briefings/` (agent-generated snapshots). D-ACW-033.
- Updated `rules/task-tracking.md` framing — `tasks-status.md` is workspace-purpose tracker adapted per workspace type; operator-personal life tasks, calendar, and email stay external. D-ACW-032.
- Shipped meta-layer maintenance harness:
  - `/acw-session end` Phase 2 gained per-file trigger walk (README, CHANGELOG, LINEAGE, ORCHESTRATION, SKEPTIC).
  - `/acw-instance audit` gained "Meta-layer staleness" check (Mode A extension).
  - `/acw-instance upgrade` gained "Resolve meta-layer staleness" step.
  - All three gated on `acw-state.yaml::meta_layer` block presence. D-ACW-034.
- Bumped ACW version `0.5.1` → `0.6.0`. Bumped `last_reconciled_version` and template baseline.
- Backfilled CHANGELOG with v0.6.0 entry.

### 2026-05-02 — v0.5.1: front-door cleanup (Session 9)

- Retired `bootstrap/README.md` (functions absorbed by `tools/scaffold-instance.py` + templated `research/01-problem-framing.md`).
- Retired `migration/README.md` (functions absorbed by `/acw-instance audit` and `/acw-instance upgrade` adopt-mode).
- Retired `LAYERS.md`; folded the ACW-specific three-layer narrative into `README.md` as a "How ACW is layered" section; generic pattern stays in `rules/manifest-discipline.md`.
- Refreshed `README.md` end-to-end: 60-second scaffold quickstart up front; four operator commands table (`/acw-session start|end`, `/acw-instance audit|upgrade`); current directory map (runbooks/, integrations/, briefings/, _buffer/); current load-bearing files; current Tools quickstart.
- Backfilled `CHANGELOG.md` for v0.3.0, v0.4.0, v0.5.0, v0.5.1 — each entry summarizes Added / Changed / Decisions per Keep a Changelog format.
- Updated `acw-state.yaml::template_layer` and `meta_layer` to remove the retired files.
- Bumped ACW version `0.5.0` → `0.5.1`. D-ACW-030 records the rationale.

### 2026-05-02 — v0.5.0: audit verb fixes from `_Command` dogfood + new canonical substrate (Session 8)

- First `/acw-instance audit` dogfood run against `_Command` (4/6 substrate signals, unregistered, substantial organic substrate). Audit ran but exposed five v0.4.0 bugs.
- Audit/upgrade verb fixes (D-ACW-023, D-ACW-024, D-ACW-026):
  - Hard-stop scan widened to count root-level organic substrate, not just `decisions/` and `rules/`.
  - Mode B walk made interactive: prompt per finding, write absorption candidates immediately on `[b]`, no static-report shortcut.
  - Mode B default routing changed from `[s] instance-specific` to "ask, don't guess" with explicit canonical comparison in prompt.
  - Skills audit landed inside the verb spine (SKILL.md frontmatter validation against `rules/skill-format.md`).
  - Absorption flow works for unregistered workspaces: candidates flow upstream during audit before formal adoption.
- `_inbox/` → `_buffer/` rename per DIP vocabulary canon (D-ACW-027). Updated all active substrate; preserved historical references in append-only files. Directory renamed via `git mv`.
- Three new canonical surfaces from `_Command` absorption (D-ACW-025, D-ACW-029):
  - `runbooks/` (empty_dir, .gitkeep) — operator-facing how-to docs.
  - `integrations/` (instance_layer with templated README) — external-system docs (APIs, MCPs, adapters, webhooks).
  - `briefings/` (empty_dir, .gitkeep) — agent-generated dated snapshots; universal pattern across workspace types.
- Calendar / tasks / email stay external (D-ACW-028); briefings is the snapshot mechanism when aggregation is wanted.
- `/acw-instance upgrade` adds v0.5.0 migration step: detects legacy `_inbox/`, proposes rename to `_buffer/` with operator confirmation.
- Bumped ACW version `0.4.0` → `0.5.0`. Bumped `last_reconciled_version` to `0.5.0`. Updated template baseline to `0.5.0`.
- Verified scaffolder dry-run produces correct shape with new directories.

### 2026-05-02 — v0.4.0: command-routed skills, full audit verb, absorption mechanics (Session 7)

- Tightened `rules/skill-format.md`: ported command-routed orchestrator material from synapse global into ACW canonical with three corrections — reframed "same invariant workflow" as "same shared spine"; split strongest-version rule by orientation; scoped deltas-are-configuration to the spine. D-ACW-016.
- Expanded `rules/multi-instance-topology.md`: three-flow resolution model (adopt / absorb / instance-specific), absorption candidate format (`_inbox/` payload schema), divergence markers (`divergent_pending_review`, `instance_specific_substrate`), re-adoption flow, cross-repo write governance. D-ACW-017.
- Added four registry entries to `rules/instance-current-manifest.md` (all earned in v0.4.0): `_inbox` directory in `empty_dirs`, `divergent_pending_review`, `instance_specific_substrate`, `adopt_mode_organic_threshold` (default 5). Declared all four on ACW itself; template baseline matches.
- Built `skills/acw-instance/` (object-centered command-routed orchestrator): `references/audit.md` (Mode A canonical comparison + Mode B operator-routed organic discovery + absorption candidate writes), `references/upgrade.md` (gap-walk with adopt-mode hard-stop, divergence-marker respect, cache refresh, version bump, decision-log entry). D-ACW-018.
- Built `skills/acw-session/` (object-centered command-routed orchestrator): `references/start.md` (load context, drift check, surface inbox), `references/end.md` (five-phase capture-distribute-metabolize-synapse-research). D-ACW-019.
- Sub-references carried over from old `capture-and-metabolize/references/` to `acw-session/references/`.
- Marked old skills `skills/upgrade-instance/`, `skills/resume-session/`, `skills/capture-and-metabolize/` as `status: superseded` with `superseded_by` pointer; moved to `meta_layer` awaiting manual delete.
- Verified `/resume-session` (now `/acw-session start`) reads `_inbox/` per the lattice handoff design — Step 4 of the original skill, ported into `references/start.md` as Step 4.
- D-ACW-020: Mode B ships in v0.4.0 as operator-routed organic substrate discovery.
- D-ACW-021: audit Mode A uses ACW rules + templates as schema; no new artifact.
- D-ACW-022: hard-stop threshold set at 5 non-canonical markdown files in `decisions/` or `rules/`.
- User-level junctions swapped: deleted `~/.claude/skills/upgrade-instance,resume-session,capture-and-metabolize`; created `~/.claude/skills/acw-instance,acw-session`.
- Internal cross-references updated: `AGENTS.md`, `rules/instance-current-manifest.md`, `rules/task-tracking.md`, `tools/templates/README.md.tmpl`.
- Bumped ACW version `0.3.0` → `0.4.0`. Bumped `last_reconciled_version` to `0.4.0`.

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
