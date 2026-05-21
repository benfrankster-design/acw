---
class: operational
authority: canonical
stability: stable
loaded_by_agent: no
date: 2026-05-13
status: accepted
id: D-ACW-048
version: 0.9.8
---

# D-ACW-048 — v0.9.8: wiki mode canonical-only for decisions and glossary; context/contacts/ as earn-by-discipline opt-in

## Context

D-ACW-043 (v0.9.3) sanctioned wiki shape as an opt-in mode alongside single-file mode for decisions and glossary, with `decision_tracking.mode` and `glossary.mode` keys gating the on-disk shape. D-ACW-045 (v0.9.6) added the single-file → wiki migration tooling and retired the "archives stay archived" carve-out. ACW itself migrated to wiki at v0.9.6; cs-copilot, gsg-copilot, and _Command are still single-file.

The dual-mode design carried real cost. The audit verb branched on per-workspace mode keys at multiple steps (substance scan, canonical fetch, plan construction, comparison). The decision-tracking rule documented two parallel formats with different rolling-window mechanics. The scaffolder defaulted new instances to single-file, immediately creating future migration work. Every downstream consumer reading the rule had to learn both modes and the migration path between them.

The wiki shape is strictly better at every scale this instance family targets:
- Atomic per-entry files mean diffs and merges are clean.
- The auto-loaded surface is a thin INDEX, not the bodies — context cost stays bounded regardless of entry count.
- No rolling-window archive ceremony required; cold entries naturally sort to the bottom of INDEX.
- Single-file mode's "split when too large via promotion ritual" was strictly worse than starting wiki.

Separately, ACW canon did not have a contacts pattern. _Command's `context/contacts/` (wiki-shaped per-contact CRM, used by `/enrich`-style flows) is a useful pattern but not universal — most instances don't need it. The right shape is earn-by-discipline: not scaffolded by default, surfaced by audit as an opt-in for any instance that wants it.

## Decision

Wiki mode is the only sanctioned mode for `decisions/` and `glossary/`. Single-file mode is retired. Audit and upgrade detect single-file legacy shape and route it for mandatory migration to wiki.

`context/contacts/` is a canonical optional pattern (wiki-shaped: `context/contacts/INDEX.md` + `entries/<slug>.md`). Audit emits an opt-in plan row when the directory is absent; upgrade scaffolds it on operator acceptance. Not propagated by the scaffolder; earned per instance.

Ship as v0.9.8.

## Rationale

- **Wiki canonical.** Reduces surface area across rules, scaffolder, audit, and upgrade. Eliminates a class of branching logic and migration-state ambiguity. Every instance ends up at the same shape; new instances start there.
- **Mandatory migration on upgrade.** Single-file workspaces (cs-copilot, gsg-copilot, _Command) get migrated to wiki the next time they run `/acw-instance upgrade` — no per-instance mode toggle, no opt-in.
- **Contacts as opt-in.** Generalizes the _Command CRM pattern without forcing it on every instance. Earn-by-discipline matches the rest of the ACW philosophy (DEFERRED.md, recommended-blocks registry, instance-specific declarations).

## Rejected alternatives

- **Keep dual-mode support.** Already costing branching complexity in audit/upgrade and forcing rule-readers to learn two formats. The opt-in path was always a transition state; treating it as a permanent option blocked simplification.
- **Scaffold context/contacts/ by default.** Most instances don't need it. Scaffolding it creates noise for the majority. Earn-by-discipline (opt-in via audit) keeps the canonical shape clean.
- **Add context/contacts/ as instance-specific only (no canonical template).** Loses the wiki-shape convention. Every adopter would reinvent the layout. Canonical template with opt-in scaffolding is the right tradeoff.

## Consequences

- `rules/decision-tracking.md` rewritten: wiki shape only, single-file format documentation removed, rolling-window archive section trimmed to a single paragraph about INDEX sort order.
- `tools/templates/acw-state.yaml.tmpl` updated: wiki-mode `decision_tracking` block, new `glossary` block, wiki `paths`, INDEX-based `auto_load_at_session_start`, INDEX-based `canonical_runtime_files`.
- Main `acw-state.yaml` `instance_layer` rows for `glossary.md` and `decisions/decision-log.md` replaced with `glossary/INDEX.md` and `decisions/INDEX.md`. `empty_dirs` extended with `decisions/entries`, `decisions/open-questions`, `decisions/constraints`, `glossary/entries`. Dual-purpose NOTE removed.
- New templates: `tools/templates/decisions-INDEX.md.tmpl`, `tools/templates/glossary-INDEX.md.tmpl`, `tools/templates/context-contacts-INDEX.md.tmpl`.
- `skills/acw-instance/SKILL.md` step 2 + step 3 stripped of mode branching.
- `skills/acw-instance/references/audit.md` "Mode-dependent substrates" branching replaced with mandatory single-file → wiki migration plan rows. New "Optional patterns (earn-by-discipline)" section for `context/contacts/` opt-in.
- `skills/acw-instance/references/upgrade.md` single-file → wiki section reframed as mandatory; new "Optional patterns" section for contacts execution.
- Downstream instances at `last_reconciled_version < 0.9.8` will see mandatory wiki migration plan rows on next audit/upgrade. The legacy `decision_tracking.mode: single-file` key in their state file is honored as a detection signal and overwritten on upgrade.

## Source

Operator directive (2026-05-13). Synapse memory: dual-mode design was never load-bearing; treat wiki as canonical only.
