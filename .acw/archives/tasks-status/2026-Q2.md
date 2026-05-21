---
class: archive
authority: derived
stability: stable
loaded_by_agent: no
---

# Tasks Status Archive — 2026 Q2

Archived Done entries from `tasks-status.md`. Sessions 1–11. Sessions 12+ stay inline in `tasks-status.md` per the rolling-window discipline in `rules/task-tracking.md`. Build-log narrative for the same period lives in `build-log.md`.

This file is not auto-loaded. Read on demand when historical context is needed.

## Done (archived)

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
- Refreshed `README.md` end-to-end: 60-second scaffold quickstart up front; four operator commands table; current directory map; current load-bearing files; current Tools quickstart.
- Backfilled `CHANGELOG.md` for v0.3.0, v0.4.0, v0.5.0, v0.5.1.
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
  - `integrations/` (instance_layer with templated README) — external-system docs.
  - `briefings/` (empty_dir, .gitkeep) — agent-generated dated snapshots; universal pattern.
- Calendar / tasks / email stay external (D-ACW-028); briefings is the snapshot mechanism when aggregation is wanted.
- `/acw-instance upgrade` adds v0.5.0 migration step: detects legacy `_inbox/`, proposes rename to `_buffer/` with operator confirmation.
- Bumped ACW version `0.4.0` → `0.5.0`. Bumped `last_reconciled_version` to `0.5.0`. Updated template baseline to `0.5.0`.

### 2026-05-02 — v0.4.0: command-routed skills, full audit verb, absorption mechanics (Session 7)

- Tightened `rules/skill-format.md`: ported command-routed orchestrator material from synapse global into ACW canonical with three corrections — reframed "same invariant workflow" as "same shared spine"; split strongest-version rule by orientation; scoped deltas-are-configuration to the spine. D-ACW-016.
- Expanded `rules/multi-instance-topology.md`: three-flow resolution model (adopt / absorb / instance-specific), absorption candidate format (`_inbox/` payload schema), divergence markers, re-adoption flow, cross-repo write governance. D-ACW-017.
- Added four registry entries to `rules/instance-current-manifest.md` (all earned in v0.4.0): `_inbox` directory in `empty_dirs`, `divergent_pending_review`, `instance_specific_substrate`, `adopt_mode_organic_threshold` (default 5).
- Built `skills/acw-instance/` (object-centered command-routed orchestrator). D-ACW-018.
- Built `skills/acw-session/` (object-centered command-routed orchestrator). D-ACW-019.
- Marked old skills as `status: superseded`; moved to `meta_layer` awaiting manual delete.
- D-ACW-020: Mode B ships in v0.4.0 as operator-routed organic substrate discovery.
- D-ACW-021: audit Mode A uses ACW rules + templates as schema; no new artifact.
- D-ACW-022: hard-stop threshold set at 5 non-canonical markdown files.
- User-level junctions swapped: deleted old; created `~/.claude/skills/acw-instance,acw-session`.
- Bumped ACW version `0.3.0` → `0.4.0`. Bumped `last_reconciled_version` to `0.4.0`.

### 2026-05-02 — RC4 → v0.3.0: multi-instance topology, GitHub-first canonical, adopt mode (Session 6)

- Wrote `research/10-multi-instance-topology.md` (meta_layer) — lattice model, knowledge-placement rules, coordination primitive status, Phase 1 spinoff spec.
- Promoted canonical statement to `rules/multi-instance-topology.md` (template_layer). D-ACW-012.
- Added `is_canonical_source` flag to `acw-state.yaml`. D-ACW-013.
- Updated `rules/instance-current-manifest.md`: new entries for `is_canonical_source` and `rules/multi-instance-topology.md` (both earned in v0.3.0).
- Rewrote `skills/upgrade-instance/SKILL.md`: GitHub fetch via `gh` CLI, registration check + substance scan + adoption flow. D-ACW-014.
- Added canonical-edit detection step to `capture-and-metabolize` Phase 2. D-ACW-015.
- Bumped ACW version `0.2.0-rc4` → `0.3.0`. Bumped `last_reconciled_version` to `0.3.0`.
- Push to `origin/master` retired the 8-commits-ahead parked task.

### 2026-05-02 — Skill registration via user-level junctions (Session 5)

- D-ACW-011 — registered three bookend-arc skills via user-level directory junctions. ACW is the canonical runtime source; child-instance copies are passive.
- Created junctions for `capture-and-metabolize`, `resume-session`, `upgrade-instance`.
- Surfaced OQ-ACW-006 (should scaffold tool optionally create skill junctions at scaffold time) — deferred for second-instance evidence.
- Capture file at `research/sessions/2026-05-02--skill-registration-via-junctions.md`.

### 2026-05-02 — RC4: framework-agnostic bookend skills, drift detection, upgrade skill (Session 4)

- Added `paths:` block to `acw-state.yaml` (14 substrate file path declarations). D-ACW-008.
- Documented canonical default paths and four-operation manifest-tooling spec in `rules/manifest-discipline.md`.
- Built `tools/manifest.py` reference implementation (stdlib only, ~330 lines, 33 unit tests, all passing).
- Refactored `skills/capture-and-metabolize/` and `skills/resume-session/` to read paths from `acw-state.yaml::paths`.
- Added `section_conventions` frontmatter to `decisions/decision-log.md`, `tasks-status.md`, `research/evolution.md`.
- Created `rules/instance-current-manifest.md` (template_layer). D-ACW-009.
- Added `last_reconciled_version` field to `acw-state.yaml`.
- Added Step 5 drift check to `skills/resume-session/SKILL.md`.
- Built `skills/upgrade-instance/` skill. D-ACW-010.
- Bumped version to `0.2.0-rc4`.

### 2026-04-30 — RC3: ACW as instance of itself; manifest-discipline rule extracted (Session 3)

- Added `project:` block to `acw-state.yaml`. D-ACW-006.
- Bumped version to `0.2.0-rc3`.
- Updated `skills/capture-and-metabolize/SKILL.md`: documented config fields as optional with defaults; added Phase 2 conditional manifest-classification step.
- Created `rules/manifest-discipline.md` (template_layer). D-ACW-007.
- Trimmed `LAYERS.md` to ACW-specific narrative (meta_layer); points at `rules/manifest-discipline.md`.
- Added `rules/manifest-discipline.md` to `acw-state.yaml::template_layer` and `auto_load_at_session_start`.
- First real dogfood of `capture-and-metabolize` against the sandbox clone.

### 2026-04-30 — Three-layer manifest shipped (Session 2)

- Added `template_layer`, `instance_layer`, `meta_layer`, `empty_dirs` blocks to `acw-state.yaml`.
- Refactored `tools/scaffold-instance.py` to read from the manifest.
- Added `tools/templates/README.md.tmpl`.
- Added `LAYERS.md` (meta_layer) explaining the three-bucket model.
- Recorded D-005 in `decisions/decision-log.md`.
- All release gates green.

### 2026-04-30 — gsg-copilot instance extensions absorbed (Session 1)

- Wrote `research/09-gsg-copilot-instance-extensions.md` proposing C-01 through C-09.
- Logged incidents D-01 (synapse-rule-sync) and D-02 (instance-bootstrap).
- Shipped `tools/scaffold-instance.py` + `tools/templates/`.
- Added `--category` enum to `tools/log-incident.py` (C-09).
- Added `rules/task-tracking.md` (C-01) and `rules/incident-tracking.md` (C-09).
- Created `tasks-status.md` and `build-log.md` at repo root.
- Added `auto_load_at_session_start` to `acw-state.yaml` (C-06).
- Added directive 7 to `AGENTS.md`.
- Ported `capture-and-metabolize` and `resume-session` from gsg-copilot.
- Bumped `acw-state.yaml::version` to `0.2.0-rc1`.

---

## Done blocks moved from live file 2026-05-13 (v0.9.3 Pending-only migration)

### 2026-05-05 — v0.9.1: bi-weekly rolling-window discipline for decision-log + global synapse trim (Session 15)

- D-ACW-042 records the bundle. Doctrine-completion patch on v0.9.0; closes the decision-log mechanism gap that v0.9.0 left under-specified.
- `rules/decision-tracking.md` gains "Rolling-window discipline" section: bi-weekly cadence + ~15k threshold trigger; archive shape `decisions/decision-log-YYYY-Q*.md` (meta_layer, archive frontmatter); Open Questions/Constraints/Resolved sections do not archive.
- `rules/task-tracking.md` rolling-window cadence aligned to bi-weekly.
- `rules/auto-load-discipline.md` caveats updated for both `decisions/decision-log.md` and `tasks-status.md` to reference bi-weekly cadence + threshold trigger.
- `rules/instance-current-manifest.md` gains earned-in-0.9.1 entry for `decision-log-YYYY-Q*.md` archive shape.
- ACW substrate split applied: D-ACW-034 down through D-004 moved to `decisions/decision-log-2026-Q2.md`. Live decision-log retains D-ACW-035 onward.
- Companion global-layer trim: moved six ACW-canonical duplicates from `~/synapse/Rules/` to `~/synapse/Reference/acw-canonical/`. ~85k off global memory load.
- Bumped ACW version 0.9.0 -> 0.9.1.

### 2026-05-04 — v0.9.0: auto-load discipline + tasks-status archive (Session 14)

- D-ACW-038 records the bundle. Auto-load bloat incident logged.
- `rules/auto-load-discipline.md` (new template_layer rule): codifies earn-by-incident applied to auto-load.
- `tools/manifest.py` extended with STRUCTURED_LISTS; 8 new unit tests; 54 tests pass.
- `acw-state.yaml::auto_load_at_session_start` migrated to structured form with 4 demotions.
- `tools/templates/acw-state.yaml.tmpl` updated.
- `CLAUDE.md` updated: `@`-imports synced to lean 4 entries.
- `/acw-instance audit` + upgrade references gained auto-load discipline sections.
- `tasks-status.md` Done section trimmed: Sessions 1-11 archived; `rules/task-tracking.md` updated.
- Auto-load context savings ~30k.
- Bumped ACW version 0.8.0 -> 0.9.0.

### 2026-05-04 — v0.8.0: bookend efficiency cluster (Session 13)

- D-ACW-037 records the bundle. Cost-friction incident logged.
- Bookend efficiency: skills/acw-session/SKILL.md declares Haiku model; `/acw-session end` defaults to quick mode; full/synapse/research flags.
- New verb `/acw-session update`.
- `.current-session` tracker.
- Sessions move to root.
- Superseded skill cleanup: deleted 4 retired skill dirs from disk.
- Three new earned-in-0.8.0 manifest entries.
- Bumped ACW version 0.7.0 -> 0.8.0.

### 2026-05-03 — v0.7.0: /acw-instance adopt-and-migrate rewrite + integrations scope (Session 12)

- D-ACW-036 records the bundle.
- Workstream B rewrote skills/acw-instance/SKILL.md + references/audit.md + references/upgrade.md to adopt-and-migrate model.
- integrations/<system>/ scope refined to cover docs + integration-specific tooling.
- Bumped ACW version 0.6.1 -> 0.7.0.

## Parked section retired 2026-05-13 (v0.9.3); content below frozen for historical reference

- C-04 synthesis-cycle: single cycle of evidence is too thin. Defer to DEFERRED.md or wait.
- C-05 runbooks layer: operator-preference-flavored. Document as recommended, not normative.
- C-07 vault-boundary as hard rule: include as suggested starting rule in instance-hard-rules template, not normative globally.
- C-08 backlog triple-tag: recommended convention only, not normative.
