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

### D-ACW-043 — v0.9.3: weekly cadence + wiki-shape as sanctioned mode + bookend mode-portability + bookend arch improvements + tasks-status Pending-only

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

### D-ACW-042 — v0.9.1: bi-weekly rolling-window discipline for decision-log; doctrine completion + global synapse trim

**Date:** 2026-05-05

**Decision:** Five changes ship together as v0.9.1, a doctrine-completion patch on v0.9.0:

1. **`rules/decision-tracking.md`** gains a "Rolling-window discipline" section parallel to the v0.9.0 addition in `rules/task-tracking.md`. Cadence: **bi-weekly** (every two weeks). Mechanism: entries dated > 14 days old archive to `decisions/decision-log-YYYY-Q*.md` (meta_layer, frontmatter `class: archive, authority: derived, stability: stable, loaded_by_agent: no`). Replace archived content in the live file with a one-line pointer. Threshold trigger from `rules/auto-load-discipline.md` (~15k tokens) is the secondary fire condition: archive aggressively whenever the live file crosses threshold even if entries are < 14 days old. Open Questions, Constraints and Gotchas, and Resolved Questions sections do not archive — they're active surfaces, not historical narrative.

2. **`rules/task-tracking.md`** rolling-window section updated: cadence aligns to **bi-weekly** (was "Sessions ≥ N-2"). The session-count heuristic was a v0.9.0 placeholder when the cadence question was unresolved; bi-weekly gives a clean date-based cutoff that works across both decision-log and tasks-status under one rule shape. Archive file pattern unchanged (`tasks-status-YYYY-Q*.md`).

3. **`rules/auto-load-discipline.md`** caveats updated: both `decisions/decision-log.md` and `tasks-status.md` canonical-recommendation caveats now reference the bi-weekly cadence and point at the appropriate tracking rule for the mechanism.

4. **`rules/instance-current-manifest.md`** gains a new earned-in-0.9.1 entry for `decision-log-YYYY-Q*.md` archive shape; existing tasks-status archive entry text updated to bi-weekly cadence (earned-in-0.9.0 unchanged).

5. **ACW substrate split applied:** entries D-ACW-034 down through D-004 (dated 2026-04-30 to 2026-05-02) moved to `decisions/decision-log-2026-Q2.md`. Live file retains D-ACW-035 onward (8 entries inline). Archive file added to `acw-state.yaml::meta_layer`. **Companion global-layer trim:** moved six ACW-canonical duplicates from `~/synapse/Rules/` (auto-loaded globally via the `~/.claude/rules` junction) to `~/synapse/Reference/acw-canonical/` (sibling, not auto-loaded). ~85k off global memory load on every workspace, every session. Files moved: `instance-current-manifest.md`, `auto-load-discipline.md`, `Procedures/{skill-format, pipeline-roles, capability-broker, decision-tracking}.md`. Global `~/.claude/CLAUDE.md` Rules Index updated to reflect the new location. Five citation references in `cs-copilot/` now point at the old path; doc-only, fix-on-touch.

**Rationale:** The cost-friction incident from v0.9.0 (operator hit halfway through Max-plan weekly budget after 2 days) attacked the bookend's per-invocation cost. v0.9.0 then attacked the structural per-session-load cost via auto-load discipline. v0.9.1 closes two follow-on gaps surfaced this session:

- **Decision-log doctrine gap.** v0.9.0's `rules/auto-load-discipline.md` named the threshold for `decisions/decision-log.md` (~15k tokens) but pointed at `rules/decision-tracking.md` for the mechanism. That mechanism wasn't there — `decision-tracking.md` only described splitting into four files when the log gets too big to navigate. The threshold was canon; the rolling-window mechanism analogous to `task-tracking.md` v0.9.0 was missing. v0.9.1 adds it.

- **Global-layer bloat.** Operator screenshot showed 79.2k of memory files at session start, with synapse/Rules/instance-current-manifest.md (35.8k!) loading globally via the `~/.claude/rules` junction even when in non-ACW workspaces. The synapse copies were stale duplicates of ACW canonical (Pending item from v0.8.0). Moving them out of the auto-load path closes the bloat without losing reference access.

The unified bi-weekly cadence across decision-log and tasks-status closes a smaller doctrinal inconsistency: v0.9.0 used "Sessions ≥ N-2" for tasks-status (placeholder when the cadence question was unresolved); the underlying need is the same — keep the file lean, archive what's stale. Bi-weekly works as a date-based cutoff for both files under one rule shape.

**Source:** Operator session 2026-05-05 immediately after v0.9.0 ship. Operator surfaced context-budget bloat via screenshot showing 79.2k memory files. Operator quote: *"for the decisions doctrine Im noticing this is already a problem. lets do this bi-weekly actually (every two weeks) rolling window with the decision logs. and we were supposed to split tasks status. lets just do it now. make it canon so every instance gets the update."*

**Open follow-ups:**

- **Downstream propagation.** Doctrine flows to instances via `/acw-instance upgrade`: the new `rules/decision-tracking.md` section + revised `rules/task-tracking.md` cadence + revised `rules/auto-load-discipline.md` caveats land in template_layer; the v0.9.1 manifest registry entry surfaces drift on instances at `last_reconciled_version` < 0.9.1. The audit verb walks each instance's decision-log and tasks-status against the bi-weekly cutoff and proposes archive splits when entries exceed the window.
- **`tasks-status.md` rolling window for ACW already-applied (v0.9.0).** Sessions 12–14 inline are within the bi-weekly window (dates 2026-05-03 through 2026-05-05; today 2026-05-05). Bi-weekly cadence change is forward-looking; ACW's tasks-status doesn't need a re-split.
- **Cs-copilot citation refresh.** Five files in `~/projects/cs-copilot/` cite `~/.claude/rules/Procedures/{skill-format, capability-broker, decision-tracking}.md` paths that no longer exist post-trim. Citation-only, not load-bearing. Fix when cs-copilot is touched next.
- **v1.0.0 promotion timing.** Per operator directive in v0.9.0, nothing new ships before 1.0.0 promotion. v0.9.1 is a doctrinal patch completing v0.9.0 — does not extend scope, just closes specification gaps. Soak window continues.

**Risks:**

- **Risk: bi-weekly cutoff removes decisions in active reference.** Mitigation: the live file's pointer line names the archive file; agents reading recent decisions see the redirect immediately. Archive file is in `meta_layer` so it stays in the workspace; only loses auto-load.
- **Risk: cs-copilot stale citations.** Already noted. Doc-only.
- **Risk: synapse trim breaks downstream skill.** Already verified — the only references in the codebase are the five cs-copilot citations. No skill or script reads the moved paths programmatically.

### D-ACW-037 — v0.8.0: bookend efficiency cluster (Haiku, subagent isolation, quick/full modes, /acw-session update verb, .current-session tracker, sessions/ at root, retire 4 superseded skills)

**Date:** 2026-05-04

**Decision:** Six changes ship together as v0.8.0:

1. `skills/acw-session/SKILL.md` declares `model: claude-haiku-4-5` in frontmatter. Phase steps that need real reasoning (Phase 3 operator-confirm proposals, Phase 5 research-prompt construction, meta-layer trigger proposed-edit text) escalate to Sonnet inline.
2. Bookend invokes a fresh subagent context to avoid inheriting the parent session's Opus 4.7 1M pricing.
3. `/acw-session end` defaults to **quick mode** (Phase 1 capture + minimal Phase 2 append-only writes + Phase 3 auto-update sweep). `full` argument runs all phases as previously documented. Phase 4 conditional on `--synapse` flag (quick) or `synapse_log_path` set (full); Phase 5 conditional on `--research` flag (quick) or operator confirmation (full).
4. New `/acw-session update` verb for mid-session checkpoints. Reads `.current-session`, appends timestamped note. Self-bootstraps if no tracker exists.
5. `paths.session_captures_dir` migrates from `research/sessions` to `sessions/` at root. Sessions are operational logs, not research artifacts. Existing capture files moved via `git mv`. `empty_dirs` swap.
6. The four superseded skills marked in `meta_layer` since v0.4.0 (`capture-session/`, `capture-and-metabolize/`, `resume-session/`, `upgrade-instance/`) are deleted from disk; their entries removed from `meta_layer`.
7. New `plans/` directory at workspace root for plan artifacts. Operational outputs from planning agents (or operator hand-written plans) save here as dated markdown (`plans/YYYY-MM-DD--<slug>.md`). Empty `.gitkeep` at scaffold time. New canonical default path `plans_dir: plans` in `acw-state.yaml::paths`. Convention only in v0.8.0 — no automatic writer skill; operator drops plans here manually. Earn-by-content reasoning: cheap to pre-create the directory; the writer skill earns its build only when convention demands automation.

**Rationale:** Operator session 2026-05-04 surfaced acute cost pressure — `/acw-session end` running 7-10 minutes per invocation on Opus 4.7 1M context, burning ~5-8M tokens per session, halfway through Max-plan weekly budget after 2 days. Cost-friction incident logged in `incidents.jsonl` this session. The bookend's work is overwhelmingly mechanical (read transcript, append to file, classify against manifest) — Haiku-grade in 80%+ of phases. Running mechanical bookend work at the most expensive Claude variant is structurally wrong. Quick mode collapses session-end to its append-only essentials, deferring expensive operator-interactive work to explicit `full` invocations at logical boundaries. The `update` verb closes a long-standing gap (binary bookend vs Ian Nuttall's session-update precedent) without paying full session-end cost. Sessions move to root because they are operational logs — `research/` is for design notes and queries. Superseded skill deletion closes a Pending item from v0.4.0 that the careful guardrail blocked from automated removal.

**Source:** Operator session 2026-05-04; deep-research note `research/11-session-continuity-prior-art.md` (Ian Nuttall claude-sessions precedent for `update` verb and `.current-session` tracker pattern; Anthropic Memory Stores filesystem-as-memory validation; ETH Zurich finding on hand-curated substrate); cost-friction incident logged this session.

**Open follow-ups:**

- **v0.9.0 — substrate earn-by-content refactor.** Scaffolder ships discipline floor only; bookend scaffolds substrate files on-demand when content earns them. Threshold table per content type to be argued through in `research/12-substrate-earn-by-content.md` (not yet written).
- **Future — `CLAUDE.md` becomes a thin pointer** ("see `AGENTS.md`"); `AGENTS.md` carries the substantive content currently in `CLAUDE.md` as the instance version of the file. Separate ship; not in v0.8.0 or v0.9.0.
- **Risk: `model:` frontmatter honored?** Field may not be honored by all Claude Code versions. If not honored, the skill still works at whatever model the harness picks; cost-cut is just smaller. No breakage.
- **Risk: quick mode defers operator-interactive work.** Manifest classification, host-entry-file maintenance, canonical-edit detection, meta-layer triggers, cross-repo writes, cross-project notifications accumulate until the next `/acw-session end full` runs them. Long stretches of quick-only mode could let substrate drift. Mitigation: audit verb catches structural gaps; operator instinct picks the heavy session.
- **Risk: self-bootstrap from `update` creates "untitled" capture files.** Mitigation: `end` always renames to topic-from-Phase-1; if operator never runs end, the file stays as-is, harmless.

### D-ACW-035 — Accept all four meta-layer harness proposals; ship as v0.6.1

**Date:** 2026-05-03
**Decision:** Accept all four proposals from the meta-layer harness's first run (post-v0.6.0 `/acw-session end`): extend README directory map with `context/` and `inbox/`; backfill LINEAGE with v0.2.0+ primitive-trace entries; add ORCHESTRATION "v0.2.0+ evolution methodology" section documenting the dogfood-driven loop; add SKEPTIC Warning 4 ("Substrate is not static") earned by incident `e167b922`. Ship as v0.6.1 patch.
**Rationale:** Operator approved with single word ("ship") immediately after the harness surfaced the proposals. The harness earned its build by finding real staleness on its first run; declining the proposals would surface them again on next audit anyway. Better to absorb now while context is warm than to defer and re-discover. The four files together represent the meta-layer's full backfill from the v0.2.0+ cluster — LINEAGE alone has nine primitive-trace gaps closed, ORCHESTRATION gains a major new section, SKEPTIC gains a fifth warning grounded in a documented incident. Validates the harness's first-test correctness (OQ-ACW-010 earn-by-incident path appears clean).
**Source:** Operator approval after Phase 2 meta-layer trigger walk in 2026-05-03 session-end; see build-log entry that documented the proposals.

*(Entries D-ACW-034 down through D-004, dated 2026-04-30 to 2026-05-02, archived to `decisions/decision-log-2026-Q2.md` per the bi-weekly rolling-window discipline in `rules/decision-tracking.md`.)*

### D-ACW-041 — Buffer lifecycle: `read:` flag + `_buffer/_read/` archive subdirectory

**Date:** 2026-05-05

**Decision:** After an absorption candidate is processed, the operator flips `read: false` → `read: true` in the file's frontmatter, adds an `absorbed_in:` pointer naming where it landed, and moves the file from `_buffer/` to `_buffer/_read/`. The session-start spine already excludes `_read/` from its walk (per spine convention), so processed notifications stop surfacing as drift. History preserved via git. Documented in `rules/multi-instance-topology.md` § "Buffer lifecycle." Applied retroactively — five existing files moved this session (3 backfilled with `read: true` + `absorbed_in:` pointers; 2 already flipped earlier today).

**Rationale:** Convention gap surfaced when operator asked "what happens to files in the buffer once they've been consumed?" The honest answer was: nothing, today. Three older absorbed-but-never-flipped files (D-001 source, cs-copilot rename FYI, Kashef YT note) would still surface as unread notifications on every `/acw-session start` if the spine took the read flag seriously — noise that defeats the buffer's purpose. The session-start spine already documents "do not descend into a `_read/` subdirectory," implying the convention was envisioned but never operationalized. This decision operationalizes it. Cheap form factor (one paragraph in the topology rule + one mkdir + git mv); structural prevention (every absorbed candidate stops surfacing as drift, every session, forever).

**Why subdirectory and not deletion:** the absorbed candidate is mirrored into the consuming surface (decision-log entry, research note, etc.), so the buffer file IS technically redundant after absorption. But: the buffer file carries source attribution (the `from_session_capture` pointer back to the originating instance's session) that the consuming surface may not preserve. Keeping the buffer file in `_read/` preserves the chain of evidence at zero cost.

**Why not just trust git history:** operator legibility. `git log _buffer/` requires intent; `ls _buffer/_read/` is the natural read. Archive subdirectory is the cheaper UX for "what's been processed?"

**Source:** Operator session 2026-05-05, immediately after the buffer-state inspection that revealed three older files still showing `read: false`. Operator approved option 2 (archive subdirectory) over option 1 (accept accumulation) and option 3 (delete on flip).

**Open follow-ups:**
- `/acw-session end` could optionally surface a "any unprocessed buffer notifications?" prompt during the bookend, prompting the operator to flip-and-move at session-end. Earn-by-incident: surfaces only if buffer accumulates faster than the operator processes manually.
- Cross-instance: downstream instances (cs-copilot, _Command, etc.) inherit the convention via the topology rule (template_layer propagation). Their own `_buffer/` directories follow the same lifecycle.
- `_read/` archive is not pruned. If it grows large enough to bother `git status` or directory listings, an annual archive (e.g., `_buffer/_read/2026/`) would earn its build. Not now.

---

### D-ACW-040 — Promote runtime-code-location from convention to AGENTS.md directive 8 (single-incident emergency promotion)

**Date:** 2026-05-04

**Decision:** Promote the runtime-code-location convention shipped in D-ACW-039 from a "convention only" paragraph in `rules/multi-instance-topology.md` to a normative directive (AGENTS.md #8). AGENTS.md goes from "Seven directives" to "Eight directives." Topology rule paragraph rewritten to drop the "convention only" hedge and point at the directive as the normative source.

**Rationale:** Operator overrode the earn-by-incident framing in D-ACW-039 with a sharper read on what counts as the activating incident. D-ACW-039 framed the absorption note from cx-dashboard-saas as "incident #1, wait for #2 before promoting." Operator's correction: the absorption note is itself meta-evidence; the *real* incident #1 is "agent starts writing runtime code in an instance and has to guess where it goes." That incident fires every time a code-shipping instance spins up. A convention buried in a rule file the agent doesn't read at session start fails to prevent it; the agent guesses, the operator corrects, the friction recurs. The fix has to live in a surface the agent reads at session start.

AGENTS.md is the canonical entry point for any agent opening any ACW workspace, declared `loaded_by_agent: yes`, propagated verbatim to every scaffolded instance via template_layer. Adding a single directive line is the smallest possible form factor for the prevention. This is the structural-prevention single-incident emergency promotion path documented in `rules/promotion-ritual.md` and exercised once before in D-003 (scaffold-instance.py).

**Why this is a structural-prevention class:**
- Form factor: one directive line in AGENTS.md, one paragraph rewrite in topology rule.
- Prevented incident class: agents writing runtime code in an instance without canonical guidance, every session. Recurs by structure, not by accident.
- Cost of waiting for "incident #2": every code-shipping session before #2 fires accumulates the same friction.
- The discipline of earn-by-incident is preserved by the *evidence* requirement (cx-dashboard-saas absorption note is the named, dated, documented incident); operator override applied to the *threshold count*, which is reserved for structural-prevention cases.

**Source:** Operator session 2026-05-04, immediately after D-ACW-039 ship. Operator quote: "the first incident should be writing code runtime code. at acw session start claude should read somewhere about this and if code happens in session it knows what to do."

**Open follow-ups:**
- Schema field `acw-state.yaml::paths::runtime_code_dir` (or similar) — still earn-by-incident. Earns when a skill or audit needs to read the runtime path programmatically.
- Existing instances with runtime code already at root: not retroactively breaking. Migration earns its own decision-log entry per instance if the operator chooses to migrate.
- Other AGENTS.md directive expansions: don't expand on speculation. The eight-directive list is small on purpose. Future directives need the same single-incident emergency promotion or earn-by-incident threshold.

---

### D-ACW-039 — Runtime-code-location convention (subdir, not root) absorbed from cx-dashboard-saas

**Date:** 2026-05-04

**Decision:** Add a "Runtime code in shipping instances" section to `rules/multi-instance-topology.md` documenting the observed convention: instances shipping runtime code locate it under a named subdirectory at instance root (`web/`, `server/`, `agents/`, `app/`), not at instance root itself. Substrate stays at root. Convention only — no schema field in `acw-state.yaml`, no separate rule file, no audit enforcement. Source absorption note marked read.

**Rationale:** Absorption candidate from `cx-dashboard-saas` Phase 0 scaffold (`_buffer/2026-05-04-cx-dashboard-saas-app-code-location-friction.md`) flagged a real gap — ACW canonical scaffolds every instance as pure-substrate, but several active instances (cs-copilot, cx-dashboard-saas, future project workspaces) ship runtime code and have to make an unguided structural decision. The candidate proposed three options: (1) `runtime_code_location` schema field, (2) dedicated `rules/runtime-code-location.md`, (3) light-touch convention note. Option 3 is correct under earn-by-incident discipline: this is incident #1 of this class. Schema fields and dedicated rule files earn their build by being load-bearing for skills or audits; nothing in current ACW canonical reads or enforces the runtime path. The convention paragraph in the topology rule is enough until a second instance trips on the same gap.

**Why subdir over root:** substrate and runtime move on different clocks. Substrate is governance (slow-moving, decision-driven, audit-checked); runtime is operational (fast-moving, build-driven, dependency-managed). Co-locating at one path level conflates the two clocks — build artifacts collide with substrate in `git status`, package managers see substrate as project-root noise, deployment configs (Vercel, Docker) point at a path that also carries decisions/.

**Source:** Absorption candidate from cx-dashboard-saas, 2026-05-04. Operator approved option 3 (convention note) in same session.

**Open follow-ups:**
- If a second consumer instance hits the same friction independently (a different operator scaffolding a project workspace and asking the same "where does code go?" question), the convention has accumulated enough incident evidence to earn promotion. Candidates: structured field in `acw-state.yaml`, a dedicated `rules/runtime-code-location.md`, or a scaffolder flag (`tools/scaffold-instance.py --runtime-code-dir web`).
- Eventual: if/when a skill needs to read the runtime path programmatically (e.g., a build-runner skill that needs to know where to `cd` before `npm run build`), the schema field earns its build at that moment.
- Not v1.0.0 — soak only. v1.1.0+ candidate.

---

### D-ACW-038 — v0.9.0: auto-load discipline (earn-by-incident applied to auto-load) + tasks-status rolling-window archive; final pre-1.0.0 substantive ship

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

### D-ACW-036 — `/acw-instance audit|upgrade` rewritten to adopt-and-migrate model; `integrations/` scope refined; ship as v0.7.0

**Date:** 2026-05-03
**Decision:** Three changes ship together as v0.7.0:

1. `skills/acw-instance/` rewritten to embody the adopt-and-migrate mental model. Audit produces a migration plan (per-file table: source → canonical destination → action) instead of an interactive Mode A/B walk. Upgrade executes the plan under a single approval gate, performing renames, format reshapes, content merges, and source deletions in one bulk operation. Substrate boundary made explicit: migration applies to recognized canonical paths (decisions/, rules/, research/, briefings/, runbooks/, integrations/, context/, inbox/, _buffer/, skills/, tools/, glossary.md, tasks-status.md, build-log.md, incidents.jsonl, CLAUDE.md, AGENTS.md, acw-state.yaml) plus substrate-shaped patterns (frontmatter class/authority/stability, dated capture files, jsonl); everything else (project code, data, configs, tests) stays untouched. For coding projects: substrate scaffolds alongside untouched code. Pre-migration safety commit recommended (offered when workspace is git-untracked); plan approval gate is the load-bearing safety surface. Interactive prompts reserved only for ambiguous routings flagged `[?]`; default behavior makes the routing call from canonical knowledge.

2. `integrations/` scope refined: `integrations/<system>/` covers BOTH documentation AND integration-specific operational scripts that are tightly coupled to one external system (bulk-push tools, sync utilities, data extractors, auth helpers). Boundary with `tools/`: tools/ holds general-purpose utilities; integrations/<system>/ holds tooling that exists only because the integration exists ("if you removed the integration, the script would be deleted with it"). Updated in `tools/templates/integrations-README.md.tmpl` and `rules/instance-current-manifest.md` § integrations entry.

3. ACW version bumped 0.6.1 → 0.7.0 reflecting the substantive `/acw-instance` behavior change. No new manifest registry entries earned; existing recommended-blocks list is unchanged. Downstream instances at `last_reconciled_version` 0.6.1 stay drift-clean (no new earned-in entries to flag).

**Rationale:** Today's `_Command` migration dogfood produced the earned-by-incident evidence for both refinements. The v0.4.0/v0.5.0 interactive Mode B walk forced the operator into nine routing prompts when six of the nine had clear canonical destinations after v0.6.0 absorbed the cockpit cluster. Operator's directive verbatim: *"that's what I want the skill to do. I want the skill to really perfectly ACW can absorb everything we have here, and it's going to do it. We've been doing better when I lose any context. It's going to actually keep it all but make it all better."* The `_Command/integrations/zoho-desk/push_direct.py` finding (an operational direct-HTTP pusher co-located with Zoho integration docs) revealed that `integrations/<system>/` wants both docs and integration-coupled scripts; current canonical README implied scripts did not belong. Migration model proves out under load: 18 file moves, 11 reshapes, 11 new canonical files, 9 deletes, one-shot via subagent-parallelized authoring + sequential write+delete, with pre-migration commit at cb39d32 as rollback path.

**Source:** Operator session 2026-05-03; `_Command` migration commits at cb39d32 (pre-migration), 7ea96e7 (migration), e179bbf (missing template_layer rules backfill). Workstream B subagent rewrite of `skills/acw-instance/SKILL.md`, `references/audit.md`, `references/upgrade.md`. Companion D-CMD-001 in `_Command/decisions/decision-log.md`.

**Open follow-ups (per Workstream B subagent):**
- Plan persistence: not persisted to disk between audit and upgrade (deterministic regeneration). May earn a `--save-plan` flag if substrate races become an incident.
- Adopt-mode hard-stop (D-ACW-022) is now structurally redundant with the plan-approval gate. Schema retained for backward compat; formal retirement deferred to a future decision-log entry.
- "Verify content at destination before deleting source" is documented but not mechanically enforced; may earn a checksum step from a future incident.
- Cross-repo writes still rely on `cross_repo_writes` declaration; capability broker (deferred per `rules/capability-broker.md`) remains the eventual replacement.

---

## Constraints and Gotchas

### C-001 — `skills/capture-session/` directory still exists on disk

`skills/capture-session/` is marked superseded in its SKILL.md frontmatter (`status: superseded`, `superseded_by: skills/capture-and-metabolize/`) but the directory itself was not removed. The careful guardrail blocked automated `rm -rf`. Operator must delete manually before the v0.2.0 tag.

### C-002 — Synapse copies still stale

Per Incident D-01, `~/synapse/Rules/Procedures/` copies are still stale relative to `/Projects/acw/rules/`. Mitigation deferred to a separate session.

---

## Resolved Questions

*(No entries yet.)*
