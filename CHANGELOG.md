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
