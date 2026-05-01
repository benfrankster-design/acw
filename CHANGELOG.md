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
