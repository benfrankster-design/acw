---
id: D-ACW-050
title: "v0.10.0 — .acw/ dotfolder convention, instance types, codemap module, confidence tagging"
date: 2026-05-21
status: accepted
kind: decision
updated: 2026-05-21
---

# D-ACW-050 — v0.10.0: .acw/ dotfolder + instance types + codemap + confidence tagging

## Decision

ACW canonical absorbs four cross-cutting changes, shipping together as v0.10.0:

1. **`.acw/` dotfolder convention.** All ACW operator-metadata substrate (decisions, glossary, sessions, raw, plans, briefings, inbox, archives, deferred, tasks-status.md, build-log.md, incidents.jsonl, DEFERRED.md, CHANGELOG.md, acw-state.yaml) moves under `.acw/` at the workspace root. Rules, project artifacts (research/, threat-model.md, runbooks/, code directories), and entry-point docs (AGENTS.md, CLAUDE.md, README.md) stay at root.

2. **`_buffer/` → `raw/` rename.** Companion rename to align with the enrichment-vs-memory principle (raw → metabolize → enriched). `acw-state.yaml` path key `buffer_dir:` renamed to `raw_dir:`.

3. **Instance types with profile + modules declaration.** `acw-state.yaml` gains top-level `profile:` (enum: `org-brain | spec-project | coding-project | library | custom`) and optional `modules:` list. Skills consult these to know which substrate modules to operate on. Defaults per profile codified in `rules/instance-types.md`.

4. **Codemap substrate module + confidence tagging discipline.** New substrate module `codemap` for `coding-project` and `library` instance types, modeled on Graphify (https://graphify.net). Codemap edges and all cross-substrate references adopt the EXTRACTED / INFERRED / AMBIGUOUS confidence-tagging discipline. Codified in `rules/codemap.md` and `rules/confidence-tagging.md`.

## Rationale

**Why `.acw/`.** Substrate is metadata about the project, not the project itself. Dotfolders signal "tooling state" universally (`.git/`, `.github/`, `.vscode/`, `.claude/`). Hiding substrate under `.acw/` makes the public-facing repo legible to consumers (engineers cloning a library see only the library, not the operator's journal). Skills that read paths from config keep working unchanged.

**Why `raw/` over `_buffer/`.** "Buffer" suggests transient holding; "raw" matches the actual semantic — unmetabolized inputs awaiting routing through the enrichment principle. The new name makes the principle visible in the folder shape.

**Why instance types.** ACW is becoming the substrate convention for any directory-based work where humans and AI both read and write. Org brains, spec projects, coding projects, libraries — each has different substrate needs. A library shouldn't carry briefings/. A coding project needs codemap that the spec project doesn't. Profile-driven module declaration lets ACW serve all instance types without forcing one shape on everything.

**Why codemap + confidence tagging.** The bottleneck in AI-assisted work on existing codebases is context retrieval, not generation. Pre-computing a navigable code graph (Graphify's approach) collapses 14k-token re-reads into few-hundred-token lookups. Confidence tagging (EXTRACTED / INFERRED / AMBIGUOUS) generalizes beyond code — applied to all substrate cross-references, it distinguishes facts from inferences and makes substrate hygiene auditable.

## Originating evidence

Two downstream instances independently arrived at the `.acw/` convention 2026-05-21:

- **cs-ops-spec:** D-COPS-035 (decision), C-COPS-001 (constraint), OQ-COPS-019 (rules/ migration question).
- **cs-atlas:** D-CATL-001 (in single-file decision log).

Both absorption candidates filed at `.acw/raw/2026-05-21-absorption-acw-substrate-under-dotfolder.md` and `.acw/raw/2026-05-21-absorption-instance-profiles-and-codemap.md`. Both metabolized into this decision; raw artifacts retained under `.acw/raw/` as provenance.

## Scope of changes in v0.10.0

**New rule files:**
- `rules/instance-types.md` — profile enum + default modules per profile + module-to-path mapping
- `rules/confidence-tagging.md` — EXTRACTED / INFERRED / AMBIGUOUS discipline across all substrate
- `rules/substrate-shape.md` — wiki vs flat vs transient shape selection criteria
- `rules/codemap.md` — codemap substrate module contract, Graphify wrapper recommendation

**Updated rule files:**
- `rules/manifest-discipline.md` — `.acw/` paths in canonical defaults, profile/modules fields, raw_dir key
- `rules/instance-current-manifest.md` — profile + modules entries in the recommended-blocks registry
- `rules/substrate-boundary.md` — `.acw/` delineation noted; project artifacts vs substrate clarified

**Canonical substrate migration (ACW itself as reference implementation):**
- `decisions/`, `glossary/`, `sessions/`, `_buffer/`, `plans/`, `briefings/`, `inbox/`, `archives/`, `deferred/`, `build-log.md`, `incidents.jsonl`, `tasks-status.md`, `DEFERRED.md`, `CHANGELOG.md`, `acw-state.yaml` all moved to `.acw/` via `git mv` (history preserved).
- `_buffer/` renamed to `raw/` after move.
- `.acw/acw-state.yaml` updated: paths, auto_load_at_session_start, template_layer, instance_layer, meta_layer, empty_dirs all re-pointed with `.acw/` prefixes where applicable.
- Profile and modules fields added.
- Version 0.9.9 → 0.10.0.

**Deferred to v0.10.1+:**
- `/acw-instance upgrade` skill mechanics to execute this migration on downstream instances (currently the skill doesn't know how to create `.acw/`, git-mv substrate, rename buffer→raw, or add profile/modules declarations). This is the immediate next work after canonical lands.
- `/codemap` skill implementation (wrap Graphify CLI, route output to `.acw/codemap/`).
- `/substrate-map` skill (render the implicit cross-reference graph as an on-demand view).
- `rules/` migration question (OQ-COPS-019) — does rules/ also move to `.acw/rules/`? Recommendation: keep at root for now (load-bearing convention for skill discovery); revisit if instance-type scaling makes it costly.
- Skill audit pass: every existing skill that reads substrate paths must be verified to read from `acw-state.yaml::paths` rather than hardcoding. Hardcodes patched.

## Consequences

**For ACW canonical:**
- v0.10.0 is a breaking schema change (paths shifted). Pre-0.10.0 instances cannot be drift-checked against v0.10.0 directly; they must upgrade first.
- Scaffolder (`tools/scaffold-instance.py`) generates new instances with `.acw/` shape from this version forward.
- AGENTS.md updated to describe the new shape.

**For downstream instances:**
- Two instances already migrated independently (cs-ops-spec, cs-atlas) and absorbed cleanly into the canonical convention.
- Three instances pending migration in subsequent sessions: `_command`, `cs-copilot`, `frank-context` (operator-confirmed scope; requires `/acw-instance upgrade` skill mechanics to land first).
- `synapse` may also adopt depending on operator call; declared profile would be `org-brain`.

**For skills:**
- Skills that read substrate paths from `acw-state.yaml::paths` continue working unchanged after instance upgrade.
- Skills that hardcode substrate paths (e.g., literal `decisions/INDEX.md` instead of `paths.decisions_index`) need patches. Audit pass scheduled.

## Cross-references

- Absorption recommendation 1: `.acw/raw/2026-05-21-absorption-acw-substrate-under-dotfolder.md`
- Absorption recommendation 2: `.acw/raw/2026-05-21-absorption-instance-profiles-and-codemap.md`
- Downstream evidence: cs-ops-spec D-COPS-035, C-COPS-001, OQ-COPS-019; cs-atlas D-CATL-001
- Influence: Graphify (https://graphify.net) — codebase knowledge graph approach
- Influence: synapse/Rules/Procedures/enrichment-vs-memory.md — the principle the `_buffer/→raw/` rename surfaces

## Supersedes

None directly. Extends D-ACW-048 (wiki-mode canonical) by adding the dotfolder location convention. Extends D-ACW-049 (v0.9.9 buffer sweep) by codifying the raw/ shape that replaces _buffer/.
