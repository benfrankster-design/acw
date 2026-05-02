---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
section_conventions:
  open_questions: "Open Questions"
  decisions: "Decisions and Rationale"
  constraints: "Constraints and Gotchas"
  resolved: "Resolved Questions"
---

# Decision Log

This file tracks all decisions, open questions, constraints, and resolved questions for this ACW instance. See `rules/decision-tracking.md` for entry format. When this file grows too large to navigate, split into four files via the promotion ritual in `rules/promotion-ritual.md`.

## Open Questions

### Q-001 — Defer or ship C-04 synthesis-cycle?

**Date raised:** 2026-04-30
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-04
**Question:** Promote `research/queries/` + `research/queries/_consumed/` single-file synthesis lifecycle into ACW canonical, or wait for second-instance evidence?
**Status:** v0.2.0-rc1 added the directories implicitly (capture-and-metabolize and resume-session reference them) but did NOT add a normative `rules/synthesis-cycle.md`. Effectively partial-shipped pending more evidence.

---

## Decisions and Rationale

### D-001 — Absorb gsg-copilot extensions into v0.2.0-rc1

**Date:** 2026-04-30
**Decision:** Ship C-01 (tasks-status), C-02 (build-log), C-03 (bookend skills), C-06 (auto-load convention), C-09 (incident category enum) into ACW canonical. Defer C-04, C-05, C-07-as-hard-rule, C-08 as recommendations only.
**Rationale:** The shipped set is the minimal cohesive substrate for any new ACW instance to pick up gsg-copilot's three weeks of lived experience. Deferred items are operator-preference-flavored or lack second-instance evidence.
**Source:** `research/09-gsg-copilot-instance-extensions.md`

### D-002 — Supersede `skills/capture-session/` with bookend pair

**Date:** 2026-04-30
**Decision:** Replace the standalone `capture-session` skill with a pair: `capture-and-metabolize` (end-of-session, five phases) and `resume-session` (start-of-session). The four sub-steps of the original skill become Phase 1 internal sub-steps of `capture-and-metabolize`.
**Rationale:** Three weeks of lived experience in `gsg-copilot` proved the bookend shape (paired session-start and session-end skills, with substrate maintained as a side effect of distribution) eliminates manual scaffolding maintenance. The standalone `capture-session` covered only one end of the loop.
**Migration:** The original `skills/capture-session/` directory is marked superseded in-place; manual operator deletion required (the careful guardrail blocked automated removal).
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-03

### D-003 — Single-incident emergency promotion of `tools/scaffold-instance.py`

**Date:** 2026-04-30
**Decision:** Ship `tools/scaffold-instance.py` based on Incident D-02 (uuid `616d435b-ec6d-470a-9cdf-2935b739e4a1`) alone, rather than waiting for two more bootstrap-related incidents.
**Rationale:** The promotion ritual's emergency clause is reserved for severity-`high` incidents. D-02 is `med`, but is structurally severe in a different way: every future ACW instance that does not bootstrap from this tool generates more drift incidents downstream. The tool is the *prevention layer* for an incident class, not a primitive earned by lived friction. Form factor is small (~200 lines, stdlib-only), and the prevented incident class is structural. Discipline prefers cheap prevention over earn-by-incident accumulation when both apply.
**Source:** `research/09-gsg-copilot-instance-extensions.md` (final section)

### D-ACW-010 — `/upgrade-instance` skill closes the drift loop

**Date:** 2026-05-02
**Decision:** New skill `skills/upgrade-instance/` walks the operator through reconciling instance state with the current ACW recommended-blocks registry. Drift detection lives in `/resume-session` Step 5; reconciliation lives here. Together they form the upgrade loop: detect → reconcile → bump `last_reconciled_version` → quiet alert.
**Rationale:** Drift visibility without a path-to-fix is half a feature. Operators shouldn't have to hand-edit `acw-state.yaml` and look up canonical defaults manually. The skill walks each gap with the registry's "How to add" content surfaced inline. Pure additive — no demotions, no removals, no shape repair.
**Source:** Operator instruction, turn 73 of the v0.2.0 absorption arc; subagent stress test informed final shape.

### D-ACW-009 — Drift detection via instance-current-manifest

**Date:** 2026-05-02
**Decision:** New file `rules/instance-current-manifest.md` (template_layer) declares the recommended-blocks registry. Each entry documents what / why / required / how-to-add / earned-in. `/resume-session` Step 5 reads the registry, compares earned-in versions against `acw-state.yaml::last_reconciled_version`, and surfaces a one-line drift alert when gaps exist.
**Rationale:** ACW evolves; existing instances need a way to learn they're behind without manual audit. The registry is the source of truth for "what current ACW expects"; the alert is the prompt; `/upgrade-instance` (D-ACW-010) is the action. Backwards-compatible — instances with no `last_reconciled_version` field default to `"0.0.0"` and get a noisy first run that quiets after one reconciliation.
**Source:** Operator instruction during the "framework-agnostic skills" scoping conversation, turns 67–73.
**Implementation note:** Required adding `last_reconciled_version` (semantic version) alongside the existing `last_reconciled` (date) field in `acw-state.yaml`. Subagent caught the version-vs-date conflation during Phase 4 verification; fixed before commit.

### D-ACW-008 — Paths block + manifest-tooling spec

**Date:** 2026-05-02
**Decision:** `acw-state.yaml::paths` declares every substrate file path. The bookend skills read paths from this block at runtime; canonical defaults documented in `rules/manifest-discipline.md`. The manifest-tooling spec (four operations: load, append, contains, validate) ships in `rules/manifest-discipline.md` with a stdlib-only Python reference implementation in `tools/manifest.py`.
**Rationale:** Decouples bookend skills from hardcoded paths. Future template evolution (moving a substrate file) requires editing one yaml block per instance instead of grepping skills. Manifest-tooling spec is the fourth application of the manifest-discipline pattern (after auto_load_at_session_start, three-layer manifest, vocabulary canon) — the operator chose to ship the shared tooling now rather than wait for a fifth case. Section heading conventions also moved to per-file frontmatter (`section_conventions` key).
**Source:** Operator scoping conversation, turns 67–73. Reference implementation is 33-test TDD; subagent verified spec/impl alignment before commit.

### D-ACW-007 — Generic manifest-discipline rule extracted; LAYERS.md trimmed to ACW-specific narrative

**Date:** 2026-04-30
**Decision:** The generic three-layer pattern ships as `rules/manifest-discipline.md` in `template_layer`. ACW's own `LAYERS.md` stays in `meta_layer` with ACW-specific content only.
**Rationale:** Operator question surfaced that LAYERS.md as written carried both the generic pattern (would be useful in every derived workspace) and ACW-specific narrative (only useful in ACW). Splitting on that axis makes the pattern reusable; recursive instances (Frank Context, hypothetically) get the same machinery and write their own narrative on top.
**Source:** Operator question on three-layer model shipping behavior; turn 35–37.

### D-ACW-006 — ACW becomes instance of itself; gains `project:` block

**Date:** 2026-04-30
**Decision:** `acw-state.yaml` carries `project:` block (`name: "ACW"`, `code: "ACW"`, `domain: "meta-template"`). Existing legacy ids `D-001` through `D-005` stay unprefixed; new entries use `D-ACW-NNN`.
**Rationale:** Operator pressed on the framing that "ACW is the template, not an instance" — the accumulated substrate gave the lie to that framing. ACW had been operating as its own instance from session zero. The reframe formalizes ACW = instance + template, both at once. The `project.code` derivation in capture-and-metabolize now works on ACW; the missing-block fallback (skill ships unprefixed ids) remains for downstream one-off instances.
**Source:** Operator-surfaced framing question, turn 37.

### D-005 — Three-layer manifest replaces hardcoded scaffold lists

**Date:** 2026-04-30
**Decision:** `acw-state.yaml` now carries three blocks — `template_layer`, `instance_layer`, `meta_layer` — that classify every file in ACW. The scaffold tool reads from this manifest instead of carrying hardcoded `VERBATIM_FILES` / `VERBATIM_RULES` / `TEMPLATED_FILES` lists. Default for new files is `instance_layer`; promotion to `template_layer` or `meta_layer` requires an explicit decision-log entry.
**Rationale:** ACW is both a template and its own first instance. Without explicit classification, the template-vs-instance split lived inside scaffold-instance.py as five hardcoded lists — adding a new propagatable file required a paired script edit, and a forgotten edit silently broke instances scaffolded thereafter. The asymmetry of mistakes (instance content shipping as template > template missing from instance) drives the default-to-instance discipline. This is the third application of the manifest-discipline pattern in ACW (after `auto_load_at_session_start` and the canon governance state machine), making the pattern itself worth naming.
**Source:** Operator-flagged during v0.2.0-rc1 absorption work; classified as the actionable form of D-01/D-02 follow-up.
**See also:** `LAYERS.md` (the meta_layer explainer).

### D-004 — Auto-load convention is vendor-agnostic

**Date:** 2026-04-30
**Decision:** AGENTS.md directive 7 declares the auto-load convention as the cross-vendor contract. The canonical file list lives in `acw-state.yaml::auto_load_at_session_start`. Each agent host implements via its native mechanism (Claude Code: `@`-imports in `CLAUDE.md`; agents reading `acw-state.yaml` directly need no host-specific file).
**Rationale:** ACW is designed to outlive any single vendor. Coupling the convention to `@`-imports would couple ACW to Claude Code. Splitting the convention across three layers (prose contract, machine-readable list, host-specific implementation) preserves portability.
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-06

---

## Constraints and Gotchas

### C-001 — `skills/capture-session/` directory still exists on disk

`skills/capture-session/` is marked superseded in its SKILL.md frontmatter (`status: superseded`, `superseded_by: skills/capture-and-metabolize/`) but the directory itself was not removed. The careful guardrail blocked automated `rm -rf`. Operator must delete manually before the v0.2.0 tag.

### C-002 — Synapse copies still stale

Per Incident D-01, `~/synapse/Rules/Procedures/` copies are still stale relative to `/Projects/acw/rules/`. Mitigation deferred to a separate session.

---

## Resolved Questions

*(No entries yet.)*
