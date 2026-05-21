---
class: archive
authority: canonical
stability: stable
loaded_by_agent: no
---

# Changelog

All notable changes to ACW (Agentic Contract Workspace) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.0] — 2026-05-21

**Breaking schema change.** ACW operator-metadata substrate relocates under `.acw/` dotfolder. Instance types become first-class. New substrate modules and tagging discipline introduced.

### Changed (breaking)

- **All substrate paths now prefix `.acw/`.** `decisions/`, `glossary/`, `sessions/`, `_buffer/`, `plans/`, `briefings/`, `inbox/`, `archives/`, `deferred/`, `acw-state.yaml`, `build-log.md`, `incidents.jsonl`, `tasks-status.md`, `DEFERRED.md`, `CHANGELOG.md` move under `.acw/`. Rules, project artifacts (`research/`, `threat-model.md`), and entry-point docs stay at root. Pre-0.10.0 instances upgrade via `/acw-instance upgrade` (skill mechanics pending in v0.10.1).
- **`_buffer/` renamed to `raw/`.** The `acw-state.yaml::paths` key `buffer_dir:` renamed to `raw_dir:`. New name aligns with the enrichment-vs-memory principle (raw → metabolize → enriched).
- `rules/manifest-discipline.md` — canonical default paths re-pointed to `.acw/`; `raw_dir` documented; profile + modules fields introduced.
- `rules/instance-current-manifest.md` — `profile` and `modules` entries added to recommended-blocks registry; paths examples updated.
- `rules/substrate-boundary.md` — `.acw/` convention noted; substrate vs project-artifact delineation clarified.
- ACW's own substrate migrated via `git mv` (history preserved); serves as the canonical reference implementation.

### Added

- `rules/instance-types.md` — profile enum (`org-brain | spec-project | coding-project | library | custom`), default modules per profile, module-to-path mapping, skill consumption contract.
- `rules/confidence-tagging.md` — EXTRACTED / INFERRED / AMBIGUOUS tagging discipline applied to all substrate cross-references. Borrowed from Graphify, generalized across substrate.
- `rules/substrate-shape.md` — wiki vs flat vs transient shape selection criteria; per-module canonical shape assignments.
- `rules/codemap.md` — codemap substrate module contract for coding-project and library instances. Two-stage extraction (Tree-sitter AST + LLM semantic), confidence-tagged edges, file-level cache for incremental rebuilds. Wraps Graphify rather than reinventing.
- `acw-state.yaml::profile` — top-level field declaring instance type. Defaults to `spec-project` with warning if absent.
- `acw-state.yaml::modules` — optional explicit override of profile defaults.

### Influence

- Graphify (https://graphify.net) — codebase knowledge graph approach; source of confidence tagging discipline and codemap shape.
- Karpathy LLM-wiki framing — substrate-as-wiki pattern already in place; this release codifies where it applies (wiki shape) vs doesn't (flat / transient shapes).
- synapse/Rules/Procedures/enrichment-vs-memory.md — principle the `raw/` rename surfaces.

### Originating evidence

Two downstream instances independently arrived at the `.acw/` convention 2026-05-21:
- cs-ops-spec: D-COPS-035, C-COPS-001, OQ-COPS-019
- cs-atlas: D-CATL-001

Both absorption candidates filed to ACW canonical, metabolized into D-ACW-050.

### Decisions

- D-ACW-050 — v0.10.0: `.acw/` dotfolder + instance types + codemap + confidence tagging

### Constraints

- C-003 — ACW operator-metadata substrate must live under `.acw/` (authority: D-ACW-050)

### Deferred to v0.10.1+

- `/acw-instance upgrade` skill mechanics to execute the migration on downstream instances. Without this, downstream upgrade is manual.
- `/codemap` skill implementation (Graphify CLI wrapper, output routed to `.acw/codemap/`).
- `/substrate-map` skill — rendered cross-reference graph view on demand.
- Skill audit pass — verify all existing skills read substrate paths from `acw-state.yaml::paths` rather than hardcoding. Patch any hardcodes.
- `rules/` migration question (OQ-COPS-019) — recommendation is keep at root for now.

## [0.9.7] — 2026-05-13

CLAUDE.md becomes a thin pointer. Auto-load moves to a Claude Code SessionStart hook. Drift surface eliminated.

### Changed

- `tools/scaffold-instance.py` — Claude Code host branch now writes `CLAUDE.md` as a one-line pointer (`See AGENTS.md.\n`) instead of hardcoded `@`-imports. Additionally writes `.claude/settings.json` and `.claude/hooks/load-context.py` to register the SessionStart hook. Hook reads `acw-state.yaml::auto_load_at_session_start` at runtime, eliminating drift between CLAUDE.md and the manifest.
- `AGENTS.md` — directive 7 rewritten to point at the SessionStart hook as the Claude Code implementation. Added **Auto-load (Resource / When / Why)** table and **What NOT to Load** section, both adopted from JEVanClief's Interpreted Context Methodology.
- `rules/auto-load-discipline.md` — added "Implementation: SessionStart hook (Claude Code host)" subsection naming the hook path, runtime contract, and rationale.

### Added

- `tools/templates/load-context.py.tmpl` — stdlib-only Python SessionStart hook. Emits `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "<contents>"}}` JSON to stdout. Reads manifest at runtime.
- `tools/templates/settings.json.tmpl` — Claude Code settings.json with SessionStart hook registered for matchers `startup|resume|clear`.

### Decisions

- D-ACW-047 — full rationale. Drift incident earned by `cs-ops-spec` scaffold producing nine unearned `@`-imports against four earned manifest entries.

### Migration

Pre-v0.9.7 instances: `/acw-instance upgrade` proposes the migration (CLAUDE.md trim + hook write + AGENTS.md update). Manual path documented in D-ACW-047.

## [0.6.1] — 2026-05-03

Meta-layer backfill — the v0.6.0 maintenance harness's first run surfaced four staleness proposals on its first walk. Operator accepted all four. v0.6.1 ships the meta-file updates that close the v0.2.0+ backfill gap.

### Changed
- `README.md` — directory map extended with `context/` (and its four canonical files) and `inbox/`. Previously listed only the v0.5.0 surfaces.
- `LINEAGE.md` — added "v0.2.0+ primitives" section with primitive-trace entries for: substrate categories (`tasks-status.md`, `build-log.md`, `runbooks/`, `integrations/`, `briefings/`, `context/`, `inbox/`), architectural primitives (three-layer manifest, multi-instance topology, command-routed orchestrator, GitHub-first canonical, `is_canonical_source` + absorption mechanics), skills (`/acw-session start|end`, `/acw-instance audit|upgrade`), tooling (`tools/scaffold-instance.py`, `tools/manifest.py`), and discipline primitives (`rules/instance-current-manifest.md`, meta-layer maintenance harness, earn-by-incident applied recursively).
- `ORCHESTRATION.md` — added "v0.2.0+ evolution methodology" section documenting the recurring dogfood-driven loop that produced v0.2.0–v0.6.0. Names the discipline (earn-by-incident applies recursively; maintenance harnesses ship alongside structural fixes; append-only history is sacred) and the boundary (v0.2.0+ loop runs *after* v0.1.0-style structured research produces a coherent foundation).
- `SKEPTIC.md` — Warning 4 added: "Substrate is not static." Earned 2026-05-03 via incident `e167b922`. Names the asymmetric-build anti-pattern. Existing Warning 4 (Reflexive injection) renumbered to Warning 5; file title updated.

### Decisions
D-ACW-035. See `decisions/decision-log.md`.

## [0.6.0] — 2026-05-02

Operator-centric substrate cluster + meta-layer maintenance harness. The substrate cluster fills the operator-context gap (context/, inbox/, tasks-status framing). The harness closes the staleness gap that produced v0.5.1 — substrate had Phase 2 distribution; meta-layer now has the same.

### Added
- `context/` canonical (instance_layer with four templated files: `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`). Lightweight pointers to operating reality, read on demand by agents that need context. Templates ship in `tools/templates/context-*.md.tmpl`.
- `inbox/` canonical (empty_dir) — operator's untriaged-items surface. Folder of dated markdown files plus loose entries. Items get processed and removed: routed to `tasks-status::Pending` (committed work), parked, sent to external task app (personal life), or deleted.
- `acw-state.yaml::paths` keys for `context_dir` and `inbox_dir`. Mirrored in `rules/manifest-discipline.md` and `tools/manifest.py`.
- `rules/instance-current-manifest.md` — two new registry entries earned in v0.6.0 (`context/`, `inbox/`).
- Meta-layer maintenance harness:
  - `/acw-session end` Phase 2 gains a "Meta-layer maintenance" step. Walks per-file triggers (README on substrate-shape change, CHANGELOG on version bump, LINEAGE on new primitive, ORCHESTRATION on new methodology, SKEPTIC on med+ incident). Surfaces proposed edits; operator confirms.
  - `/acw-instance audit` gains a "Meta-layer staleness" check (Mode A extension). Compares meta-files against the same trigger table; flags stale ones in the report.
  - `/acw-instance upgrade` gains a "Resolve meta-layer staleness" step. Walks audit-flagged meta-layer entries with operator-per-file confirmation.
  - All three gated on `acw-state.yaml::meta_layer` block presence — consumer instances without the block pay no cost.

### Changed
- `rules/task-tracking.md` — framing update. `tasks-status.md` tracks workspace purpose adapted per workspace type (cockpit = config + chief-of-staff ops; project = deliverables; full = org coordination). Operator-personal life tasks, calendar, and email explicitly stay external (MCP integrations + briefings for snapshots, never local mirroring).

### Decisions
D-ACW-031 through D-ACW-034 (four entries). See `decisions/decision-log.md`.

## [0.5.1] — 2026-05-02

Front-door cleanup. Retires content functionally absorbed by the v0.4–v0.5 tooling; refreshes the README with current substrate, current operator commands, and a prominent scaffold quickstart so anyone landing on the GitHub repo can stand up an instance in 60 seconds.

### Removed
- `bootstrap/README.md` — the seven-question greenfield instantiation interview. Functionally absorbed by `tools/scaffold-instance.py` (mechanical work) plus `research/01-problem-framing.md` (thinking work; templated for every new instance).
- `migration/README.md` — the brownfield audit guide. Functionally absorbed by `/acw-instance audit` (Mode A canonical comparison + Mode B operator-routed organic discovery) and `/acw-instance upgrade` adopt-mode.
- `LAYERS.md` — ACW-specific narrative on how the three-layer manifest applies to ACW itself. Conceptual content folded into README.md as a "How ACW is layered" section; the generic pattern lives (and continues to live) in `rules/manifest-discipline.md`.

### Changed
- `README.md` — full refresh. New "Scaffold a new instance (60 seconds)" quickstart up front. New "Four operator commands" table covering `/acw-session start|end` and `/acw-instance audit|upgrade`. Directory map reflects current substrate (runbooks/, integrations/, briefings/, _buffer/). Load-bearing files updated to current architecture (skill-format, multi-instance-topology, instance-current-manifest, the bookend orchestrators). LAYERS.md content absorbed.
- `acw-state.yaml::template_layer` — removed `bootstrap/` and `migration/`.
- `acw-state.yaml::meta_layer` — removed `LAYERS.md`.

## [0.5.0] — 2026-05-02

Audit verb fixes earned by the first `/acw-instance audit` dogfood against `_Command`, plus three new universal canonical surfaces absorbed from the same dogfood, plus the system buffer rename. v0.5.0 closes the loop between the audit verb's intent and its actual behavior.

### Added
- `runbooks/` — canonical surface for operator-facing how-to docs. Empty dir, ships with `.gitkeep`. Universal pattern.
- `integrations/` — canonical surface for external-system documentation (APIs, MCPs, adapters, webhooks). Ships with a templated `README.md` (`tools/templates/integrations-README.md.tmpl`) explaining the convention. Universal pattern.
- `briefings/` — canonical surface for agent-generated dated snapshots. Universal pattern; content varies by workspace type (cockpit aggregates calendar+tasks+email; project aggregates PR+build+issues; full/org-brain aggregates cross-domain rollups).
- `acw-state.yaml::paths` keys for `runbooks_dir`, `integrations_dir`, `briefings_dir`, `buffer_dir` (canonical defaults in `rules/manifest-discipline.md` and `tools/manifest.py`).
- `rules/instance-current-manifest.md` — three new registry entries earned in v0.5.0 (runbooks, integrations, briefings) plus updated `_buffer` entry with rename history.
- `/acw-instance upgrade` — v0.5.0 migration step that detects legacy `_inbox/` and proposes rename to `_buffer/`.

### Changed
- `skills/acw-instance/references/audit.md` — Mode B walk made interactive. Each finding prompts the operator with the four-option route (`[a]/[b]/[s]/[n]`); writes happen during the walk on `[b]`, no static-report shortcut. Default routing changed from `[s] instance-specific` to "ask, don't guess" with explicit canonical comparison surfaced in the prompt. Skills audit landed inside the verb spine (SKILL.md frontmatter validation against `rules/skill-format.md`). Absorption flow works for unregistered workspaces — candidates flow upstream during audit before formal adoption.
- `skills/acw-instance/references/upgrade.md` — hard-stop scan widened to count root-level organic substrate (briefings/, runbooks/, integrations/, custom-named directories) plus root-level non-canonical markdown files, in addition to the v0.4.0 logic that counted only `decisions/` and `rules/`. The threshold (default 5) applies to the total. Caught the case the threshold was designed to catch — workspaces like `_Command` accumulate organic substrate at root.
- `_inbox/` → `_buffer/` rename across all active substrate. Per the operator's DIP vocabulary canon ("buffer" replaces inbox/queue/staging) and to clear semantic space for the operator-facing `inbox/` arriving in v0.6.0. Active files updated; append-only history retained historical references.

### Decisions
D-ACW-023 through D-ACW-029 (seven entries). See `decisions/decision-log.md`.

## [0.4.0] — 2026-05-02

Skills restructured as object-centered command-routed orchestrators. Multi-instance topology baked into canonical with absorption mechanics specified. Skill-format rule tightened to reconcile its strict-voice with the object-centered carve-out.

### Added
- `skills/acw-instance/` — orchestrator with verbs `audit` (read-only routing-table report) and `upgrade` (interactive reconciliation). Replaces `skills/upgrade-instance/`.
- `skills/acw-session/` — orchestrator with verbs `start` (load context, drift check, surface buffer) and `end` (five-phase capture-distribute-metabolize). Replaces `skills/resume-session/` and `skills/capture-and-metabolize/`.
- `rules/multi-instance-topology.md` (template_layer) — lattice model + knowledge-placement discriminator + reference-not-duplicate principle + three-flow resolution model (adopt / absorb / instance-specific) + absorption candidate format + divergence markers + re-adoption flow + cross-repo write governance.
- `rules/instance-current-manifest.md` — new registry entries: `_inbox` directory in `empty_dirs` (renamed `_buffer` in v0.5.0), `divergent_pending_review`, `instance_specific_substrate`, `adopt_mode_organic_threshold` (default 5).

### Changed
- `rules/skill-format.md` — three corrections to reconcile strict-voice with object-centered carve-out. Reframed "same invariant workflow" as "same shared spine"; split strongest-version rule by orientation; scoped deltas-are-configuration to spine only. Ported the full command-routed orchestrator material from the operator's synapse global rules into ACW canonical.

### Decisions
D-ACW-016 through D-ACW-022 (seven entries). See `decisions/decision-log.md`.

### Superseded
- `skills/upgrade-instance/` (→ `skills/acw-instance/`)
- `skills/resume-session/` (→ `skills/acw-session/`, verb `start`)
- `skills/capture-and-metabolize/` (→ `skills/acw-session/`, verb `end`)

## [0.3.0] — 2026-05-02

Multi-instance topology shipped as canonical rule + research note. GitHub-first canonical fetch closes the loop on instance reconciliation. Adopt mode lets pre-ACW substrate-shaped workspaces register without manual scaffolding.

### Added
- `rules/multi-instance-topology.md` (initial version, expanded in v0.4.0).
- `research/10-multi-instance-topology.md` — provenance/derivation note.
- `acw-state.yaml::is_canonical_source` flag — gates `capture-and-metabolize` Phase 2 propagation behavior. ACW sets `true`; every child instance defaults `false`.
- `/upgrade-instance` adopt-mode — when `acw-state.yaml` is missing but ≥3 substrate signals are present, offers to register the workspace as a formal instance.
- `capture-and-metabolize` Phase 2 canonical-edit detection — branches on `is_canonical_source`. Publishers prompt for version bump and push to GitHub; consumers warn that local edits won't propagate.

### Changed
- `/upgrade-instance` now fetches `rules/instance-current-manifest.md` from the ACW GitHub repo on every run via `gh` CLI (private repo). Single source of truth: GitHub. Local cache refreshed after each successful pass. Fail-closed if GitHub unreachable.

### Decisions
D-ACW-012 through D-ACW-015. See `decisions/decision-log.md`.

## [0.2.0-rc4] — 2026-05-02

Framework-agnostic bookend skills, drift detection, and the upgrade skill that closes the loop. Seven atomic phases with subagent verification at four checkpoints. The bookend skills are now portable across any ACW-derived workspace; existing instances learn they're behind via a one-line alert at session start and reconcile through `/upgrade-instance`.

### Added
- `acw-state.yaml::paths` — declares substrate file paths; bookend skills read from this block at runtime with fallback to canonical defaults documented in `rules/manifest-discipline.md`. 14 keys covering decisions log, tasks-status, build-log, glossary, threat-model, incidents, evolution, sources, research-state, problem-framing, session-captures dir, research-queries dir, research-queries-consumed dir, inbox dir.
- `acw-state.yaml::last_reconciled_version` — semantic version this instance is synced to in the recommended-blocks registry.
- `rules/manifest-discipline.md` — gained "Canonical default paths" section and "Manifest tooling spec" section (four-operation contract: load, append, contains, validate).
- `tools/manifest.py` — stdlib-only reference implementation of the manifest-tooling spec. ~330 lines, 33 unit tests. Subagent-verified spec/impl alignment.
- `tests/test_manifest.py` — TDD test suite.
- `rules/instance-current-manifest.md` — declarative registry of recommended blocks. Each entry: what / why / required / how-to-add / earned-in.
- `skills/resume-session/SKILL.md` Step 5 — drift check that compares each registry entry's earned-in version against the instance's `last_reconciled_version`; surfaces a one-line alert on gaps.
- `skills/upgrade-instance/` — new skill that walks operators through reconciling instance state with the recommended-blocks registry. Pure additive: no demotions, no removals, no shape repair.
- `section_conventions` frontmatter on `decisions/decision-log.md`, `tasks-status.md`, `research/evolution.md` (and on the corresponding templates).

### Changed
- `acw-state.yaml::version` bumped from `0.2.0-rc3` to `0.2.0-rc4`.
- `acw-state.yaml::auto_load_at_session_start` now includes `rules/instance-current-manifest.md`.
- `acw-state.yaml::template_layer` now includes `rules/instance-current-manifest.md` and `skills/upgrade-instance/`.
- `skills/capture-and-metabolize/` and `skills/resume-session/` — every reference to a substrate path replaced with `paths.X` shorthand. Section heading conventions read from per-file frontmatter via `section_conventions.X`. Project-specific references (gsg-copilot, synapse, Cortex, HR-CP-NNN) generalized. 11 reference files audited; subagent verified zero hardcoded substrate paths remain.
- `tools/templates/decision-log.md.tmpl`, `tasks-status.md.tmpl`, `evolution.md.tmpl`, `acw-state.yaml.tmpl` — updated to ship the new frontmatter and the `last_reconciled_version` field.
- `CLAUDE.md` — auto-load list updated per the bookend skill's host-entry-file maintenance rule.

### Earned
- D-ACW-008 — paths block + manifest-tooling spec.
- D-ACW-009 — drift detection via instance-current-manifest.
- D-ACW-010 — `/upgrade-instance` skill closes the drift loop.

### Backwards compatibility
- All new blocks and fields are optional. Instances missing `paths`, `project`, manifest layers, etc. fall back to canonical defaults documented in the rules.
- Instances missing `last_reconciled_version` default to `"0.0.0"` and get a noisy first run of the drift alert; one `/upgrade-instance` pass quiets it.
- Existing legacy id formats (`D-NNN`, `HR-NNN` without project code prefix) continue to work; the bookend skill respects whatever the instance's decision log already uses.

---

## [0.2.0-rc3] — 2026-05-02

ACW formally reframes itself as an instance of itself (not just a template). Splits `LAYERS.md` into a generic rule (`rules/manifest-discipline.md`, template_layer) plus ACW-specific narrative (`LAYERS.md`, meta_layer). Gives the bookend skills a `project:` block so the skill suite runs on ACW like any other instance.

### Added
- `acw-state.yaml::project` block (`name: "ACW"`, `code: "ACW"`, `domain: "meta-template"`). Existing legacy ids `D-001..D-005` stay unprefixed; new entries use `D-ACW-NNN`.
- `rules/manifest-discipline.md` — generic three-layer pattern documentation extracted from LAYERS.md. Covers when the rule applies, the three-layer model, manifest mechanics, why-default-to-instance, operator quick-reference, recurring-pattern naming, recursive-instances note.
- `skills/capture-and-metabolize/SKILL.md` — Configuration section documents all fields as optional with defaults; Phase 2 gained the conditional manifest-classification step.

### Changed
- `acw-state.yaml::version` bumped from `0.2.0-rc2` to `0.2.0-rc3`.
- `LAYERS.md` trimmed to ACW-specific narrative (meta_layer); points at `rules/manifest-discipline.md` for the generic pattern.

### Earned
- D-ACW-006 — ACW becomes instance of itself; gains `project:` block.
- D-ACW-007 — Generic manifest-discipline rule extracted; LAYERS.md trimmed to ACW-specific narrative.

---

## [0.2.0-rc2] — 2026-04-30

### Added
- Three-layer manifest in `acw-state.yaml`: `template_layer`, `instance_layer`, `meta_layer`, `empty_dirs`. Replaces the hardcoded lists in `tools/scaffold-instance.py`. See `LAYERS.md` and `decisions/decision-log.md::D-005`.
- `LAYERS.md` (meta_layer) — the three-bucket explainer with operator quick-reference.
- `tools/templates/README.md.tmpl` — instance-layer README starter.
- Release gate: every file at root, `rules/`, `tools/`, `skills/` must be classified in the manifest.

### Changed
- `tools/scaffold-instance.py` refactored to read from the manifest. Stdlib-only mini-yaml parser. Skips `__pycache__/` and `.pyc` when walking `template_layer` directories.
- `acw-state.yaml::version` bumped from `0.2.0-rc1` to `0.2.0-rc2`.

---

## [0.2.0-rc1] — 2026-04-30

First absorption pass from the first ACW instance (`gsg-copilot`). Three weeks of single-operator lived experience surfaced nine candidate primitives (C-01 through C-09) and two staleness incidents (D-01 synapse-rule-sync, D-02 instance-bootstrap), documented in `research/09-gsg-copilot-instance-extensions.md`.

### Added
- `tools/scaffold-instance.py` — bootstrap a canonical ACW instance into a target directory. Stdlib-only, refuses to clobber, supports `--dry-run` and `--host`. Closes the bootstrap gap surfaced by Incident D-02.
- `tools/templates/` — eleven templates with `{{TOKEN}}` placeholders for `acw-state.yaml`, `glossary.md`, `threat-model.md`, `decisions/decision-log.md`, `rules/instance-hard-rules.md`, `research/01-problem-framing.md`, `research/evolution.md`, `research/sources.md`, `research/research-state.yaml`, `tasks-status.md`, `build-log.md`.
- `rules/task-tracking.md` — codifies the three-section `tasks-status.md` model (Pending / Done / Parked) with dated session blocks and pinned-marker convention.
- `rules/incident-tracking.md` — documents incident schema, severity ladder, and the seven-value category vocabulary.
- `tasks-status.md` and `build-log.md` at repo root, added to `canonical_runtime_files`.
- `acw-state.yaml::auto_load_at_session_start` array. Files agent hosts auto-load at session start.
- `acw-state.yaml::project` block (`name`, `code`, `domain`).
- `acw-state.yaml::cross_repo_writes`, `synapse_log_path`, `voice` fields for instance-specific configuration consumed by bookend skills.
- `AGENTS.md` directive 7 — declares the auto-load convention as the cross-vendor contract.
- `skills/capture-and-metabolize/` — five-phase end-of-session bookend ported and generalized from gsg-copilot.
- `skills/resume-session/` — session-start bookend, paired with capture-and-metabolize. Loads recent capture sections §5–§7, queued research prompts, and cross-project `_inbox/` notifications.
- `tools/log-incident.py --category` flag with seven-value enum (`implementation-bug`, `governance-leak`, `environment-state`, `process-gap`, `wrong-assumption`, `scale-vulnerability`, `earn-by-incident`).
- `research/09-gsg-copilot-instance-extensions.md` (the absorption-pass research artifact).

### Changed
- `acw-state.yaml::version` bumped from `0.1.0` to `0.2.0-rc1`.
- `acw-state.yaml::canonical_runtime_files` extended with `rules/task-tracking.md`, `rules/incident-tracking.md`, `tasks-status.md`, `build-log.md`, `tools/scaffold-instance.py`.

### Superseded
- `skills/capture-session/` superseded by `skills/capture-and-metabolize/` + `skills/resume-session/`. The original directory is marked `status: superseded` in its SKILL.md frontmatter; operator must delete manually (the careful guardrail blocks automated removal).

### Earned
- **Incident D-01** (severity: med, primitive: `synapse-rule-sync`) — synapse copies of ACW rules at `~/synapse/Rules/Procedures/` are stale relative to canonical. Mitigation deferred.
- **Incident D-02** (severity: med, primitive: `instance-bootstrap`) — `gsg-copilot` did not bootstrap from `/Projects/acw/bootstrap/` because no scaffolding tooling existed. Mitigation: shipped `tools/scaffold-instance.py` under D-003 single-incident emergency promotion.

### Deferred (no ship this release)
- C-04 synthesis-cycle (`rules/synthesis-cycle.md`). Single cycle of evidence; awaiting second instance or third cycle.
- C-05 runbooks layer. Operator-preference-flavored.
- C-07 vault-boundary as hard rule. Included as suggested starting rule in `instance-hard-rules.md.tmpl`, not normative globally.
- C-08 backlog triple-tag. Recommended convention only.

---

## [0.1.0] — 2026-04-11

### Added
- Initial release.
- `rules/pipeline-roles.md` with four role groups (orchestrator, pipeline-worker, guardian, broker-sideband)
- `rules/canon-governance.md` with SKOS-inspired vocabulary schema, N-authority approval model (free-form string with three worked examples), and intra-workspace canonicalization discipline
- `rules/canon-schema.yaml` template for vocabulary canon files
- `rules/canon.yaml` empty instance ready for operator to populate
- `rules/capability-broker.md` design document (implementation deferred per activation trigger)
- `rules/decision-tracking.md` ADR-lite for recording operator decisions
- `rules/vocabulary-lint.md` explaining the lint rule and exit codes
- `rules/promotion-ritual.md` mechanical procedure for promoting deferred primitives
- `rules/instance-hard-rules.md` with worked example
- `tools/lint-vocab.py` stdlib-only regex vocabulary linter
- `tools/log-incident.py` stdlib-only incident ledger writer with three subcommands (log, count, check-drift)
- `glossary.md` seed glossary
- `incidents.jsonl` empty incident ledger
- `DEFERRED.md` canonical deferred library table with activation triggers
- `deferred/` folder with 11 derived subfolder READMEs (one per primitive)
- `threat-model.md` scoped to shipped tools
- `skills/example-skill/SKILL.md` worked reference skill with declared role
- `bootstrap/README.md` for greenfield instantiation (includes seven-question interview)
- `migration/README.md` for brownfield audit methodology (includes pre-import checklist)
- `decisions/decision-log.md` single-file decision log scaffolded with four sections
- `tests/test_lint_vocab.py`, `tests/test_log_incident.py`, fixtures
- `research/` with seven sanitized research files (problem framing, literature survey, synthesis, proposal, ship decision, sources, README)
- `README.md`, `AGENTS.md`, `SKEPTIC.md`, `AUTHOR.md`, `LINEAGE.md` root indexes and guidance
- `ORCHESTRATION.md` documenting the methodology used to produce v0.1.0
- `acw-state.yaml` machine-readable self-contract naming version, canonical runtime files, role schema mode, canon authority mode, decision tracking mode, and release gates
- Every non-code markdown file carries class/authority/stability/loaded_by_agent frontmatter headers for machine-readable classification

### Earned
- **Incident #1** (severity: high) — seed glossary imported an operator-personal vocabulary standard wholesale as canonical terms with aggressive forbidden-synonym blocks on ordinary English words, causing 180+ lint violations on the template's own prose during v0.1.0 verification. Fix: seed ships zero forbidden-synonym blocks. Lesson: regex-based linting cannot distinguish citation from substitution; enforcement earns activation when an instance populates `rules/canon.yaml` with real drift evidence.

### License
- Content: CC BY 4.0 (see `LICENSE-CONTENT`)
- Code: MIT (see `LICENSE-CODE`)
