---
id: D-ACW-038
title: "v0.9.0: auto-load discipline (earn-by-incident applied to auto-load) + tasks-status rolling-window archive; final pre-1.0.0 substantive ship"
date: 2026-05-04
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-038 — v0.9.0: auto-load discipline (earn-by-incident applied to auto-load) + tasks-status rolling-window archive; final pre-1.0.0 substantive ship

**Date:** 2026-05-04

**Decision:** Eight changes ship together as v0.9.0. Per operator directive ("there should be nothing for 1.0.0"), v0.9.0 is the final pre-promotion substantive ship; v1.0.0 is the soak/promotion.

1. **`rules/auto-load-discipline.md`** ships as new template_layer rule. Codifies earn-by-incident applied to `auto_load_at_session_start`: every entry MUST declare a structured claim ("what fails if not loaded every session?") and an `earned_by` field. The rule names canonical recommendations (the four files ACW recommends with stated claims) and declared demotion candidates (paths that fail the gate, with reasons).

2. **`tools/manifest.py`** extended: new `STRUCTURED_LISTS = {"auto_load_at_session_start"}` set; parser handles dict-shaped entries (`- path: ... / claim: ... / earned_by: ...`); `load()` returns paths only (legacy backward compat — existing consumers and the drift check work unchanged); `load_structured()` returns full dict per entry; `validate()` enforces no duplicate paths and required `path` field on dict entries. 8 new unit tests; all 54 tests pass.

3. **`acw-state.yaml::auto_load_at_session_start`** migrated to structured form with 4 demotions: `rules/manifest-discipline.md`, `rules/instance-current-manifest.md`, `rules/multi-instance-topology.md`, `incidents.jsonl` removed (each consumer-skill loads them directly when needed; no agent-context value justifies auto-load). 4 entries kept with structured claims: decision-log, instance-hard-rules, tasks-status, glossary.

4. **`tools/templates/acw-state.yaml.tmpl`** updated: new instances scaffolded by `tools/scaffold-instance.py` inherit the lean 4-entry structured-form default. Bumped baseline `last_reconciled_version` to `0.9.0`.

5. **`CLAUDE.md`** synced: `@`-imports reduced to the 4 canonical entries; "Other substrate is read on demand" section names the demoted files and their consumer-skills.

6. **`/acw-instance audit`** reference (`skills/acw-instance/references/audit.md`) gained "Auto-load discipline" section: walks `auto_load_at_session_start`, classifies entries (KEEP / KEEP-migrate-to-structured / KEEP-instance-specific / DEMOTE / REVIEW), proposes consolidated `reshape` plan row with verdicts applied per entry. Also proposes `write-canonical` for the discipline rule itself when missing.

7. **`/acw-instance upgrade`** reference (`skills/acw-instance/references/upgrade.md`) gained "v0.9.0 migration: auto-load discipline" section: applies the audit's verdicts under the existing single approval gate; converts bare entries to structured form using canonical claims; removes demotion entries; resolves REVIEW entries interactively; updates host entry files to mirror.

8. **`tasks-status.md` rolling-window archive**: Sessions 1–11 archived to `tasks-status-2026-Q2.md` (meta_layer); Sessions 12–14 stay inline. `rules/task-tracking.md` updated with rolling-window discipline declaring inline ≤ 2–3 sessions and quarterly archive convention. New earned-in-0.9.0 entry in `rules/instance-current-manifest.md` documents the archive shape.

**Rationale:** The cost-friction incident `a8e771f0-7686-484d-b89e-cc25e96f8c93` (logged 2026-05-04 against v0.8.0) attacked the bookend's per-invocation cost (Haiku default, quick mode). v0.9.0 attacks the structural per-session-load cost. Operator opened this session by surfacing context-budget bloat: 113.2k at session start, with `Memory files` consuming 83.1k (mostly from the 8-entry auto-load list). Audit of each auto-load file against an earn-by-incident gate ("what fails if this isn't loaded every session?") revealed that 4 of 8 entries failed the gate — their consumer-skills load them directly, single-operator workspaces don't need the multi-instance lattice rule, and the incidents log is consumed only by audit and promotion-ritual review.

The doctrine extension ("earn-by-incident applied to auto-load") generalizes ACW's existing earn-by-incident discipline (governing the deferred library and the recommended-blocks registry) to the most expensive substrate surface in the workspace. Bringing this surface under the same gate closes a structural blind spot.

The discipline propagates to downstream instances via `/acw-instance upgrade`: the new rule lands in template_layer and instance-current-manifest; the demotions DO NOT auto-propagate (each instance owns its own auto-load list); the audit verb's per-instance walk proposes demotions when an instance's bloated list contains canonical-demotion candidates. This separation is correct — doctrine flows downstream automatically; list curation stays operator-driven per workspace.

**Source:** Operator session 2026-05-04 immediately following v0.8.0 ship. Operator surfaced context-budget bloat via screenshot, then directed: "I'd like somehow for the 'Project substrate (auto-loaded every session)' to earn its ship." Then: "instances doing acw instance audit should be audited for demotions." Then: "Get it all done. there should be nothing for 1.0.0."

**Auto-load context savings:** ~30k off session-load when fully applied:
- `rules/manifest-discipline.md` (5.2k)
- `rules/instance-current-manifest.md` (11.5k)
- `rules/multi-instance-topology.md` (5.2k)
- `incidents.jsonl` (~3k current; grows unboundedly)
- `tasks-status.md` Done section (~7k via archive split)

**Open follow-ups:**

- **Backward-compat soak.** Bare-path entries remain valid in v0.9.0 (parser accepts both shapes; audit flags as `legacy-pending-review`). If parser ambiguities surface in the wild, fix forward; do not roll back.
- **`rules/auto-load-discipline.md` canonical recommendations may need expansion.** Today's recommendation list is four entries. If a future incident demonstrates a path that materially earns auto-load (skill X failed because file Y was not in context, consistently, across N sessions), expand canonical recommendations and document the incident as the activation evidence.
- **Auto-load enforcement at session-start time.** Currently the discipline gate fires only at audit time. A v0.10.0+ harness could surface a "auto-load discipline drift" warning at session start when the workspace carries entries declared as demotion candidates. Earn-by-incident: surface only after operator runs into the same demotion three times across three audits.
- **Instance-specific override claims may drift.** When an operator declares an instance-specific entry with a claim, the claim doesn't auto-validate over time — the file's content may evolve such that the claim no longer holds. No detection mechanism in v0.9.0; would earn its build if drift surfaces.

**Risks:**

- **Risk: parser accepts both shapes; misformed structured entries may fail silently.** Mitigation: `validate()` raises `ManifestError` on missing `path` field or duplicate paths; release gate runs validate; future audit verb invocation surfaces malformed entries as `[?]` REVIEW rows.
- **Risk: consumer-skill must load demoted files itself.** Already true in current implementation (skills read paths directly from `acw-state.yaml::paths`; the demoted files are read via skill action, not via auto-load context). No change needed.
- **Risk: downstream instances at `last_reconciled_version` < 0.9.0 will see a v0.9.0 drift alert mentioning `rules/auto-load-discipline.md` AND a separate audit-driven proposal to demote their own auto-load entries.** The two are sequential: first run `/acw-instance upgrade` to land the rule + bump last_reconciled_version; second run `/acw-instance audit` to propose demotions. Documented in upgrade reference.
