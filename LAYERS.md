---
class: reference
authority: canonical
stability: experimental
loaded_by_agent: no
---

# LAYERS — How ACW Itself Is Layered

ACW is two things at once: a template that scaffolds new agentic-contract workspaces, and its own first instance with three weeks of lived history. This document explains how those two roles coexist in the same repo without confusing each other.

For the **generic pattern** (any workspace classifying its files into a three-layer manifest), see `rules/manifest-discipline.md`. This file is ACW-specific narrative — what's in each ACW layer, why ACW landed on this split, how it earned its build.

## ACW's three layers

### `template_layer` — generic doctrine ACW ships to derived workspaces

- `AGENTS.md`, `DEFERRED.md`
- `bootstrap/`, `migration/`
- `rules/canon-governance.md`, `rules/canon-schema.yaml`, `rules/canon.yaml`
- `rules/capability-broker.md`, `rules/decision-tracking.md`, `rules/incident-tracking.md`
- `rules/pipeline-roles.md`, `rules/promotion-ritual.md`, `rules/skill-format.md`
- `rules/task-tracking.md`, `rules/vocabulary-lint.md`, `rules/manifest-discipline.md`
- `skills/example-skill/`, `skills/capture-and-metabolize/`, `skills/resume-session/`
- `tests/`
- `tools/lint-vocab.py`, `tools/log-incident.py`, `tools/scaffold-instance.py`
- `tools/templates/`

These are copied verbatim into any workspace scaffolded from ACW.

### `instance_layer` — ACW's own substrate with templated initial forms for children

- `acw-state.yaml`, `glossary.md`, `threat-model.md`
- `decisions/decision-log.md`, `rules/instance-hard-rules.md`
- `research/01-problem-framing.md`, `research/evolution.md`, `research/sources.md`, `research/research-state.yaml`
- `tasks-status.md`, `build-log.md`, `incidents.jsonl`
- `README.md` (children get an instance-flavored starter; ACW's own README at root is meta)

ACW's versions of these files hold ACW's history. Each pairs with a `tools/templates/X.tmpl` (or `template: null` for files that ship empty). The scaffolder renders fresh forms into children.

### `meta_layer` — about ACW only, never propagated

- `LINEAGE.md`, `AUTHOR.md`, `SKEPTIC.md`, `ORCHESTRATION.md`
- `CHANGELOG.md`, `LAYERS.md`, `README.md` (ACW's own)
- `LICENSE-CODE`, `LICENSE-CONTENT`
- `research/08-cross-model-audit.md`, `research/09-gsg-copilot-instance-extensions.md`
- `skills/capture-session/` (superseded; awaiting manual delete)

Children scaffolded from ACW do not receive any of this. ACW's lineage, attribution, stress-test record, and rcN history stay with ACW.

## Why ACW landed here

Until v0.2.0-rc2, the template/instance split lived inside `tools/scaffold-instance.py` as five hardcoded Python lists. That worked, but adding a new propagatable file required a paired script edit, and a forgotten edit silently broke instances scaffolded thereafter. The operator surfaced the gap during the v0.2.0-rc1 absorption work; D-005 made the manifest explicit.

The deeper reframing: **ACW is an instance of itself, and also serves as a template.** Earlier framing treated ACW as "the template, period." The accumulated substrate (decisions, tasks-status, build-log, incidents, evolution, glossary, threat-model) gave that framing the lie — ACW had been operating as its own instance from session zero. The three-layer manifest formalizes both roles.

## Why this is a meta_layer document

The general pattern (workspace classifying its files into three buckets, scaffold tool reads from the manifest, skill maintains it additively, lint catches drift, default-to-instance discipline) is generic and ships in `rules/manifest-discipline.md`. Every derived workspace gets that rule.

What stays here is ACW-specific: which exact files live in which exact layer, why ACW arrived at this classification, when each piece earned its build. A consultancy workspace (Frank Context, hypothetically) would have its own `LAYERS.md` documenting the consultancy's own three-layer split, while reading the generic `rules/manifest-discipline.md` for the underlying pattern.

## Changelog

- **2026-04-30** — Initial three-layer manifest shipped in v0.2.0-rc2. Generic pattern extracted into `rules/manifest-discipline.md` in v0.2.0-rc3. ACW gained a `project:` block (`code: ACW`) so it became valid input to `capture-and-metabolize` and the rest of the skill suite. See `decisions/decision-log.md::D-005`.
