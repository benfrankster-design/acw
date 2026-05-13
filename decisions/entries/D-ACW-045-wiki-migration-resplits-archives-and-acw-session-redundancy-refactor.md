---
id: D-ACW-045
title: "v0.9.6: wiki migration re-splits archives + /acw-session redundancy refactor"
date: 2026-05-13
status: accepted
kind: decision
tags: [decisions, wiki, skill-refactor, canon-discipline]
updated: 2026-05-13
supersedes: D-ACW-043
---

# D-ACW-045 — v0.9.6: wiki migration re-splits archives + /acw-session redundancy refactor

**Date:** 2026-05-13

**Decision:** Three coupled changes ship as v0.9.6:

1. **Doctrine: single-file → wiki migration re-splits historical archives.** Supersedes the "archives stay archived; wiki form starts at the live cutover" expedient from D-ACW-043. In wiki mode, ALL decisions live in `decisions/entries/` — no carve-out for pre-migration entries. The auto-load surface (`decisions/INDEX.md`) sorts by date descending; cold pre-migration entries fall to the bottom of a sorted list rather than cluttering. `tools/migrate_to_wiki.py --archive=<path>` performs the re-split; canonical via `rules/decision-tracking.md`.

2. **ACW dogfood: Q2 archive re-split.** ACW's `decisions/decision-log-2026-Q2.md` (34 entries: D-001 through D-005, D-ACW-006 through D-ACW-034) re-split into per-entry wiki files in `decisions/entries/`. The Q2 archive file deleted. `acw-state.yaml::meta_layer` reference removed. `decisions/INDEX.md` regenerated; now lists all 44 decisions in date order.

3. **`/acw-session` redundancy audit.** Same exercise applied to `skills/acw-session/` as D-ACW-044 did for `skills/acw-instance/`. 7 redundancy sites identified and collapsed:
   - `SKILL.md` state-file block enumeration → pointer to `rules/instance-current-manifest.md`
   - `distribution-rules.md` decision body fields (single-file + wiki) → pointer to `rules/decision-tracking.md` + `acw-state.yaml::decision_tracking.entry_frontmatter_required`
   - `distribution-rules.md` tasks-status session-block format → moved canonical to `rules/task-tracking.md`; skill points there
   - `distribution-rules.md` HR id-numbering pattern → pointer to `rules/decision-tracking.md` (same convention)
   - Stale archive path `tasks-status-YYYY-Q*.md` → `archives/tasks-status/YYYY-MM.md` (v0.9.5 path) fixed in `SKILL.md`, `distribution-rules.md`, `metabolize-rules.md`, `end.md`
   - `end.md` symmetric archive-registration → mode-gated; wiki mode treats decision-log archive registration as dead branch (skip silently)
   - Net: similar shape to D-ACW-044 — skill describes mechanism, not content; format authority lives in rules + state-file blocks

4. **`/acw-instance upgrade` reference extended** with v0.9.6 "single-file → wiki mode migration" section: 8 steps under the same approval gate covering archive re-split, source deletion, state-file mode flip, paths block update, auto-load mirror, host-entry-file sync. Symmetric for glossary.

5. **`tools/migrate_to_wiki.py` extended** with `--archive=<path>` flag. Flat `### `-entry parsing for quarterly archive shape (no `## ` section headers). Idempotent INDEX regeneration after archive merge.

**Rationale:** The "archives stay archived" doctrine made the wiki promise conditional — readers had to learn that pre-migration decisions lived in a different shape than post-migration ones. Earned-by-incident this session: operator asked "shouldn't we have all decisions in the wiki?" and the answer was unambiguous yes. Doctrine flipped; tooling generalized to support the flip; existing dogfood instance (ACW itself) re-split as proof.

The session-skill redundancy refactor extends D-ACW-044's "skill consumes canon, doesn't restate it" principle from `/acw-instance` to `/acw-session`. Same discipline; same drift-prevention; same net effect (skill prose smaller, canon authority unambiguous).

**Edit discipline:** pattern A. Operator-directed bundled refactor; this entry is the durable receipt.

**Source:** Operator session 2026-05-13. Direct quote: *"yeah, I would just prefer the whole idea of building the wiki was for it to be lighter and have that index so that auto-load was lighter, and this is a better form of memory for what the decision logs are intended for."* Plus: *"Re-split Q2 archive. fix stale. make sure that new instances and upgraded instances get that doctrinal discipline. audit the acw session skill to remove prose where authority already is load bearing just like we did with the acw instance skill. log and ship."*

**Supersedes:** D-ACW-043 — specifically the "archives stay archived. Pre-split decision-log-YYYY-Q*.md rolling-window archives don't get re-split; the wiki form starts at the live cutover" clause in that decision's wiki migration section. All other D-ACW-043 content stands.

**Open follow-ups:**

- **Downstream propagation.** Doctrine flows to instances via `/acw-instance upgrade`. The v0.9.6 migration section in `references/upgrade.md` runs when an instance opts into wiki mode. Instances already on wiki (none yet besides ACW) get the re-split lazily on next upgrade when their `last_reconciled_version` < 0.9.6.
- **Glossary archive symmetry.** Wiki migration for glossary is described symmetrically in `references/upgrade.md`, but no instance has triggered it yet. Earn-by-incident if friction surfaces.
- **Migration tool packaging.** `tools/migrate_to_wiki.py` now ships three paths: initial split, INDEX-only regen, archive re-split. As capabilities grow, may earn its own subcommand structure (`migrate split`, `migrate regen-index`, `migrate archive`). Earn when a fourth path arrives.
- **Skill body-size trim.** `/acw-session` references previously held inline format content; now point to rules. Net reduction is modest (~50 lines). If progressive disclosure into deeper sub-references becomes load-bearing, address then.

**Risks:**

- **Risk: re-split creates noisy INDEX with old entries dominating count.** Mitigation: INDEX sorts by date descending; recent entries surface at top. Operators looking for current state read top of list; archive depth is a non-issue for casual browsing.
- **Risk: archive re-split loses archive-specific frontmatter (`class: archive, authority: derived`).** Mitigation: archive frontmatter doesn't survive translation to per-entry files — each entry gets standard wiki frontmatter (`status: accepted`, etc.). The "archive-ness" is preserved by date (entries older than X days). No information loss; just reclassification.
- **Risk: downstream instances on v0.9.3-v0.9.5 wiki dogfood (none currently, but cs-copilot/gsg-copilot may follow) inherit pre-flip doctrine.** Mitigation: `/acw-instance upgrade` walks against current canonical (0.9.6+); doctrine landing happens automatically on next upgrade.
