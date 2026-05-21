---
id: D-ACW-043
title: "v0.9.3: weekly cadence + wiki-shape as sanctioned mode + bookend mode-portability + bookend arch improvements + tasks-status Pending-only"
date: 2026-05-12
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-043 — v0.9.3: weekly cadence + wiki-shape as sanctioned mode + bookend mode-portability + bookend arch improvements + tasks-status Pending-only

**Date:** 2026-05-12

**Decision:** Bundled absorption of three `_buffer/` proposals from `_Command` (2026-05-11 cadence note + two 2026-05-12 substrate/portability proposals; the second 5/12 proposal supersedes the first per its own declaration). Five coupled changes ship as v0.9.3:

1. **Cadence tightened bi-weekly → weekly** for both `decisions/decision-log.md` and `tasks-status.md` rolling-window archive discipline. Cutoff: entries dated > 7 days old. Threshold trigger (~15k tokens) unchanged as the secondary fire condition. `rules/decision-tracking.md`, `rules/auto-load-discipline.md`, `rules/instance-current-manifest.md` edited in place. (Absorbs 5/11 buffer note; supersedes the bi-weekly rule shipped in D-ACW-042.)

2. **Wiki-shape decisions + glossary sanctioned as opt-in mode (Path B).** `acw-state.yaml` schema gains `decision_tracking.mode` (`single-file` default | `wiki` opt-in) and `glossary.mode` (same). Wiki keys: `index`, `entries_dir`, `open_questions_dir`, `constraints_dir`, `archive_pattern`, `regenerate_index_cmd`, `entry_frontmatter_required`, `status_values`, `kind_values`. ACW itself stays `single-file`; instances opt in by setting the mode field. Industry canon (MADR 4.0.0, log4brains, AWS/Azure ADR guidance) has converged on atomic-per-entry; ACW now accommodates without forcing migration.

3. **`/acw-session` and `/acw-instance audit|upgrade` made mode-portable.** Reference files branch on `decision_tracking.mode` / `glossary.mode`. Single doc, two branches; never two skills. Spine Step 1 cross-checks key presence against mode. Audit canonical-shape signals accept both shapes (decisions/decision-log.md OR decisions/INDEX.md OR decisions/entries/; same for glossary).

4. **Bookend architectural improvements (Pass 1 + Pass 2).** Sonnet subagent for Phase 3/5 judgment via `session-end-judgment.md` (bounded ≤1500-token return contract); named profiles (`end | end full | end log-only | end synapse-only | end research-only`) replace flag combinatorics; per-phase status emission (`[phaseN] RAN | SKIPPED(reason) | FAILED(error)`); Phase 5 empty-tracks gate; pre-flight context-budget check at spine Step 0 (abort if >70% on verb `end`); batched operator-confirm proposals at Phase 3 end; resume-token in `.current-session` (`{file, session_hash, last_completed_phase}`); symmetric archive-registration in Phase 2 (detects new `*-YYYY-Q*.md` archive files and proposes `meta_layer` append); parallel Phase 4 + 5 dispatch when both fire.

5. **`tasks-status.md` Pending-only (supersedes D-CMD-024's tasks-status side; supersedes the three-section shape canonical since v0.9.0).** Live file carries one section: Pending. Done archives on completion (event-driven, not interval) to `tasks-status-YYYY-Q*.md`. Parked retired — deferred-but-keep routes to `inbox/ideas/` (wiki-shaped, frontmatter `type: idea, status: parked, date:`); architectural deferrals earn a decision-log entry; noticed-but-not-actionable observations die in conversation. `rules/task-tracking.md` rewritten in place with migration steps for pre-v0.9.3 instances. The cadence change in (1) still applies to decision-log; for tasks-status it's moot under Pending-only.

**Rationale:** All four threads share one root cause — auto-loaded substrate growing past Claude Code's prompt limit. `_Command` hit "Prompt is too long" twice in a week (5/11 + 5/12). Rolling-window cadence (D-ACW-042) treated the symptom; this bundle treats the shape: cadence tightened where the symptom-management is still load-bearing (decision-log single-file mode); wiki shape sanctioned where the shape-change attacks the root (atomic entries dissolve the auto-load-bloat problem entirely); tasks-status Pending-only because Done is write-once historical, not a work-queue state, and shouldn't live in the live file regardless of cadence. Bookend arch improvements ship coupled because they touch the same files and the pre-flight context check + per-phase status emission close the 5/11 carry-forwards. Per operator: most-recent proposals supersede on conflict — the 5/12 comprehensive proposal is the master spec; the 5/12 wiki-only proposal is subsumed.

**Edit discipline:** pattern A (operator IS the reviewer). Canonical rules + skill references edited in place over multiple sessions before this absorption note landed; this entry is the durable receipt and version-bump bookkeeping.

**Source:** `_buffer/2026-05-11-cmd-rolling-window-cadence-bi-weekly-to-weekly.md`, `_buffer/2026-05-12-cmd-wiki-shape-substrate-proposal.md`, `_buffer/2026-05-12-cmd-acw-session-and-substrate-portability-proposal.md`. Companion entries: `_Command/decisions/entries/D-CMD-024`, `D-CMD-025`, `D-CMD-026`, `D-CMD-030`. Research: `Cortex/Resources/research/2026-05-12--acw-session-skill-problems-and-improvements.md` (95 sources), `Cortex/Resources/research/2026-05-12--decision-log-as-llm-wiki-synthesis.md` (62 sources).

**Open follow-ups:**

- **Stray scaffolding in ACW workspace.** `decisions/INDEX.md`, `glossary/INDEX.md`, `glossary/entries/`, `inbox/ideas/`, `context/contacts/`, `research/historical/`, `tools/migrate_to_wiki.py` are untracked in ACW. The INDEX files reference "_Command" in their headings — accidental leakage from `_Command` migration testing, not adopted ACW state. ACW canonical stays `single-file`. Operator decision needed: remove the stray files, gitignore them, or move to a sibling location.
- **Default mode for new instances.** Path B today (single-file default, wiki opt-in). Revisit defaulting to wiki after a second instance adopts and the migration friction earns its named incident.
- **MADR 4.0.0 frontmatter alignment.** Open question 1 in 5/12 proposal — adopt MADR verbatim or keep the ACW-flavored extension (`kind`, `related`, `supersedes`, `superseded_by`, `updated`)? Earned when a multi-author instance hits friction.
- **INDEX regeneration mechanism.** Today instances run `python tools/migrate_to_wiki.py` (script lives in each instance). Skill-side INDEX rendering (no external tool) could ship as canonical `tools/` Python. Earn when second instance adopts and operator hits the regen friction.
- **Subagent canonical shipping.** `.claude/agents/session-end-judgment.md` lives at user-level today. Whether ACW canonical ships `agents/` for instances to junction onto is deferred — earn when a host other than Claude Code needs the same dispatch pattern.
- **Generalize `tools/migrate_to_wiki.py`.** `_Command`'s reference implementation hardcodes ROOT. Earned for canonical ship when second instance adopts wiki and asks for tooling.
- **`/acw-instance upgrade` migration plan rows.** Should detect three-section `tasks-status.md` and propose Pending-only migration as a plan row. Same for single-file `decision-log.md` → wiki when an instance opts in. Earn-by-second-adopter.
- **`v1.0.0` promotion.** v0.9.0 was declared "final pre-1.0.0 substantive ship" per D-ACW-038; v0.9.1 (D-ACW-042) and v0.9.3 (this entry) extended that as doctrine-completion patches. The "nothing new before 1.0.0" directive still holds — promotion gated on lattice-level dogfooding.

**Risks:**

- **Risk: weekly cadence too tight for low-density instances.** Mitigation: cadence fires more often with fewer entries per run; no instance is worse off. Override possible in local `rules/` if surfaced as friction.
- **Risk: stray INDEX/glossary/inbox files in ACW workspace confuse session-start drift checks.** Mitigation: flagged as follow-up above; not load-bearing (decision-log.md is still canonical single-file in ACW).
- **Risk: subagent dispatch fails if `session-end-judgment.md` not present.** Mitigation: bookend skill prose names the dispatch target; if missing, phase falls back to inline judgment at parent's model.
