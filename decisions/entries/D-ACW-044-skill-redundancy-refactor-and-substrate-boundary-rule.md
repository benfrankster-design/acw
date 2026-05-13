---
id: D-ACW-044
title: "v0.9.4: skill-redundancy refactor for /acw-instance + new rules/substrate-boundary.md"
date: 2026-05-13
status: accepted
kind: decision
tags: [acw-instance, skills, refactor, canon-discipline]
updated: 2026-05-13
---

# D-ACW-044 — v0.9.4: skill-redundancy refactor for /acw-instance + new rules/substrate-boundary.md

**Date:** 2026-05-13

**Decision:** Operator-directed audit of `skills/acw-instance/` (SKILL.md + audit.md + upgrade.md) for sites where the skill restated content that lives authoritatively in `rules/`, `acw-state.yaml`, or `tools/templates/`. 10 redundancy sites identified; all collapsed to pointers to the authoritative source. New rule `rules/substrate-boundary.md` shipped to own the in-scope / out-of-scope partition (including the project-content exclusion list — build/dep directories, package manifests, source file extensions) that previously lived only in skill prose.

**Rationale:** Every restatement of canon in skill prose is a drift surface. When the authoritative source changes (e.g., a new ecosystem's build output gets added, the decision-log entry format changes, the auto-load discipline's canonical-recommendation list shifts), the skill prose silently rots. The fix is to make the skill a pure consumer of canonical sources: read state-file blocks at runtime, fetch rules on demand, and never carry an inline copy of content that has a canonical home.

The 10 sites collapsed:

1. **SKILL.md substance scan** — canonical-shape signals now derived from canonical `acw-state.yaml::template_layer + instance_layer + paths` + mode keys; no hardcoded path list.
2. **SKILL.md canonical fetch** — templates and rules named by `instance_layer[].template` + the recommended-blocks registry; no inline enumeration per mode.
3. **SKILL.md substrate boundary** — in-scope paths derived from state-file blocks; project-content exclusion list moved to `rules/substrate-boundary.md`.
4. **audit.md canonical comparison** — per-type shape spec (frontmatter, sections, id prefixes) replaced with pointer to the rule that owns each shape (`rules/decision-tracking.md`, `rules/task-tracking.md`, `rules/manifest-discipline.md`, `rules/skill-format.md`, `rules/incident-tracking.md`, `rules/substrate-boundary.md`) plus state-file mode keys.
5. **audit.md auto-load discipline** — canonical recommendations + demotion list collapsed to pointer; verdict table (skill's actual contribution) preserved.
6. **upgrade.md decision-log templates** — inline format blocks for both modes replaced with body-field spec; format authority is `rules/decision-tracking.md` + `acw-state.yaml::decision_tracking.entry_frontmatter_required / status_values / kind_values`.
7. **upgrade.md v0.9.0 auto-load migration** — collapsed to verdict-application + pointer.
8. **upgrade.md adopt-mode write-canonical rows** — derived from `template_layer + instance_layer + recommended_blocks`.
9. **upgrade.md initial acw-state.yaml block** — rendered from `tools/templates/acw-state.yaml.tmpl`; only computed fields (`version`, `last_reconciled`, `last_reconciled_version`, `is_canonical_source`, `project.*`) specified inline.
10. **Project-content exclusion list** — promoted from SKILL.md prose to `rules/substrate-boundary.md` as the authoritative source.

Net diff: **–74 lines** across the three skill files. When canon changes now, only the authoritative source needs editing; the skill picks up the change on next canonical fetch.

**Edit discipline:** pattern A (operator IS the reviewer). Direct rule edits + skill refactor in one pass; this entry is the durable receipt.

**Source:** Operator directive 2026-05-13: *"For the ACW instance references, there should be no need for redundancy. Whether auditing an instance or updating an instance, the most authoritative source should be used to compare against canon. That way when changes are made to acw template build, we wont have to update stale references all over the place in the acw instance skill if we dont have to. Find where an authoritative source exists, such as rules, ACW state, tools, etc, and audit where the skill is load bearing where it shouldnt be."*

**Companion ship:** ACW also self-adopted wiki-shape decisions + glossary in the same session (per D-ACW-043's Path B opt-in; ACW now dogfoods what it sanctioned). This entry is the first decision written native in the wiki shape via `tools/migrate_to_wiki.py`-rendered INDEX flow.

**Open follow-ups:**

- **Manifest registry entry for `rules/substrate-boundary.md`.** Earned-in-0.9.4 entry landed in `rules/instance-current-manifest.md` this session; downstream instances at `last_reconciled_version` < 0.9.4 will see this as drift on next `/acw-instance audit` run.
- **Template paths for wiki-mode scaffolding.** `instance_layer` rows for `decisions/decision-log.md` and `glossary.md` still point at single-file templates (correct, since new instances default to single-file). When wiki becomes a sanctioned scaffold mode (Path A), `instance_layer` rows for wiki entries need new template references.
- **`tools/manifest.py` validation extension.** The state-file blocks the skill now reads at runtime (e.g., recommended_blocks registry walked from `rules/instance-current-manifest.md`) could earn a structural validator. Earned when a malformed block surfaces as friction.
- **Audit prose body fields in upgrade.md decision-log entries.** The body-field spec is prose ("Title:", "Date:", "Decision:") rather than a structured schema. If a second consumer (downstream instance audit running automatically) parses these, the schema should formalize. Earn-by-incident.

**Risks:**

- **Risk: skill depends on canonical fetch succeeding.** Now load-bearing on `gh` CLI or `GITHUB_TOKEN`. Mitigation: skill already fails closed on neither path (existing safety in Step 3). No regression.
- **Risk: instance at `last_reconciled_version` < 0.9.4 sees drift on `rules/substrate-boundary.md`.** Mitigation: this is the intended propagation mechanism. Audit will surface the gap as a `write-canonical` plan row; upgrade lands the rule under the existing approval gate.
- **Risk: prose body-field spec in upgrade.md is less precise than the inline templates it replaced.** Mitigation: the authoritative format lives in `rules/decision-tracking.md`; skill bodies just enumerate which fields the verb fills in. If precision matters at adoption time, the rule (not the skill) is where to tighten.
