---
from_instance: _Command
date: 2026-05-12
proposing:
  - Wiki-shape substrate as a sanctioned ACW canonical mode (decisions, glossary)
  - Substrate-shape portability across acw-session, acw-instance audit/upgrade
  - /acw-session architectural improvements (Pass 1 + Pass 2: model-tier subagent, status emission, named profiles, pre-flight context check, batch confirmations, resume token, parallel phases 4+5)
  - Tasks-status simplified to Pending-only — Done/Parked retired; archive-on-completion replaces rolling-window cadence (supersedes D-CMD-024's tasks-status cadence rule)
related: D-CMD-025, D-CMD-026, D-CMD-030 (in _Command/decisions/entries/)
edit_discipline: pattern A — canonical rules edited in place; this buffer file is the after-the-fact absorption note. Operator IS the reviewer.
companion_proposals:
  - 2026-05-12-cmd-wiki-shape-substrate-proposal.md (earlier today; substrate-only)
  - 2026-05-11-cmd-rolling-window-cadence-bi-weekly-to-weekly.md (5/11; cadence + 3 carry-forwards)
read: true
absorbed_in: decisions/decision-log.md::D-ACW-043 (v0.9.3 bundle — Tier 4 adopted, 2026-05-12)
status: absorbed
research:
  - Cortex/Resources/research/2026-05-12--acw-session-skill-problems-and-improvements.md (95 sources)
  - Cortex/Resources/research/2026-05-12--decision-log-as-llm-wiki-synthesis.md (62 sources)
---

# Comprehensive proposal — wiki-shape substrate + portable session/instance skills + architectural improvements

This proposal **supersedes** the earlier 2026-05-12 wiki-shape proposal (which covered substrate only) and **rolls forward** the 5/11 cadence-tightening proposal's three carry-forward candidates. Sending as one bundle because the changes are coupled: a skill improvement that doesn't handle wiki-shape substrate is incomplete; a substrate-shape change without skills that read both shapes is unshippable upstream.

## Why one bundle

Four threads converge:

1. **Substrate shape:** `_Command` migrated decisions + glossary from monolithic single-file to atomic-per-entry Karpathy-wiki shape (D-CMD-025). The motivating evidence is auto-load bloat — same failure mode that drove D-CMD-024 (cadence tightening 5/11). Industry canon (MADR 4.0.0, log4brains, AWS, Azure WAF) has converged on atomic per-entry shape; ACW's current `decision_tracking.mode: single-file` is at odds with where the broader practice sits.

2. **Skill portability:** if ACW absorbs wiki-shape, the canonical session and instance skills must read both shapes. `_Command` has done the work: `acw-session` and `acw-instance audit | upgrade` now branch on `acw-state.yaml::decision_tracking.mode` and `glossary.mode`. Same skill, two substrate shapes, single mode-field dispatch.

3. **Skill architecture:** independent of substrate shape, `/acw-session` has structural issues exposed by today's "Prompt is too long" hit. The architectural improvements (Pass 1 + Pass 2 in the research artifact) earn their place independent of the wiki migration but ship cleanly together because they touch the same files.

4. **Tasks-status simplification (D-CMD-030, added later 2026-05-12):** the prior three-section shape (Pending / Done / Parked) carried the same auto-load bloat failure mode the wiki-shape fix addressed for decisions/glossary. `_Command` retired Done and Parked from the live file: Pending-only, with completed work archiving immediately to `tasks-status-YYYY-Q*.md` (event-driven, not interval cadence) and deferred ideas routing to `inbox/ideas/` or decision-log. Supersedes the tasks-status side of D-CMD-024's cadence rule (decision-log side stands independently for single-file-mode instances). Canonical `Projects/acw/rules/task-tracking.md` rewritten in place under pattern A; this is the absorption note.

ACW can absorb in tiers (substrate only → substrate + portability → all three → all four) — see §6.

---

## 1. Substrate shape — wiki as a sanctioned mode

### Schema additions

Add to `acw-state.yaml` schema definition in `rules/manifest-discipline.md` (or wherever canonical lives):

```yaml
decision_tracking:
  mode: single-file  # default. wiki is opt-in.
  # single-file mode keys:
  file: decisions/decision-log.md
  sections:
    - "Open Questions"
    - "Decisions and Rationale"
    - "Constraints and Gotchas"
    - "Resolved Questions"
  # wiki mode keys (only when mode == wiki):
  index: decisions/INDEX.md
  entries_dir: decisions/entries
  open_questions_dir: decisions/open-questions
  constraints_dir: decisions/constraints
  archive_pattern: "decisions/decision-log-YYYY-Q*.md"
  regenerate_index_cmd: "python tools/migrate_to_wiki.py"   # optional
  entry_frontmatter_required: [id, title, date, status, kind, updated]
  status_values: [proposed, accepted, superseded, deprecated, rejected, open, partial-resolved, resolved]
  kind_values: [decision, open-question, constraint]

glossary:
  mode: single-file  # default. wiki is opt-in.
  # single-file mode:
  file: glossary.md
  # wiki mode:
  index: glossary/INDEX.md
  entries_dir: glossary/entries
  regenerate_index_cmd: "python tools/migrate_to_wiki.py"   # optional
  entry_frontmatter_required: [term]
  status_values: [active, deprecated]
```

### Wiki-shape conventions

For decisions:
- One file per atomic entry at `<entries_dir>/<id>-<slug>.md`
- `slug = slugify(title)[:60]`, kebab-case ASCII
- Legacy ids preserve verbatim (`D-CMD-024-…`); never renumber
- Open questions live at `<open_questions_dir>/<oq-id>-<slug>.md` (kind: open-question)
- Constraints at `<constraints_dir>/<cg-id>-<slug>.md` (kind: constraint)
- Resolved OQ becomes a kind:decision entry; the file moves from open-questions/ → entries/ but **keeps its OQ id as filename** (the resolution is tracked in frontmatter; renaming would break in-flight references)
- Supersession via frontmatter (`status: superseded`, `superseded_by: <id>`). Never delete files.
- INDEX is the auto-loaded summary; bodies load on demand by id

For glossary:
- One file per term at `<entries_dir>/<slug>.md` with `term`, `status` frontmatter
- INDEX lists term + link per entry
- Living-document mutability for glossary (terms are definitions, not history)

### Adoption mechanism

The migration is a one-shot script (`tools/migrate_to_wiki.py` in `_Command` is the reference implementation — ~250 lines Python). Idempotent for INDEX regeneration after initial split. ACW canonical could ship a generalized version under `tools/` that takes a workspace path argument.

### Migration semantics

- **Never renumber.** D-CMD-024 stays `D-CMD-024-…` in the new filename.
- **Living-document mutability** (date-stamped amendments in place; git as audit; supersession reserved for genuine reversals) — rejected AWS/MADR strict-immutable for single-operator instances. Multi-operator instances may want immutable; could be a `decision_tracking.mutability` field if needed.
- **Archives stay archived.** Pre-split `decision-log-YYYY-Q*.md` rolling-window archives don't get re-split; the wiki form starts at the live cutover. INDEX references the archive file as historical pointer.

### Choice posture

The two-mode design lets ACW canonical default to `single-file` (no breakage for existing instances) while sanctioning `wiki` as a documented variant. **Path B from the research artifact.** Path A (wiki as new default) was the cleaner long-term answer but Path B is the lower-risk first step.

---

## 2. Skill portability across both substrate modes

`_Command` has updated `acw-session` and `acw-instance` to branch on `decision_tracking.mode` and `glossary.mode`. Reference implementation lives in `~/.claude/skills/{acw-session,acw-instance}/`. Key portability principles:

### Mode dispatch in skill prose

Every reference file that writes to decisions or glossary now has two-mode dispatch. Example from `distribution-rules.md`:

```markdown
## Decisions

### Mode: `single-file` (canonical default)
[existing behavior — section-based]

### Mode: `wiki`
- Create file at `<entries_dir>/<id>-<slug>.md` with frontmatter
- Regenerate INDEX via `regenerate_index_cmd` or append directly
[etc.]
```

Same pattern for metabolize, audit, upgrade. The skill text is one document with two branches; never two skills.

### Spine portability

`acw-session/SKILL.md` Step 1 (config read) now declares both key sets supported in `paths`:
- Single-file shape: `decisions_log`, `glossary` keys
- Wiki shape: `decisions_index`, `decisions_entries_dir`, `decisions_open_questions_dir`, `decisions_constraints_dir`, `glossary_index`, `glossary_entries_dir` keys

The presence of keys cross-checks against `decision_tracking.mode` / `glossary.mode`. Mismatch warns; doesn't silently pick.

### Substance scan portability (acw-instance)

`acw-instance/SKILL.md` Step 2 canonical-shape signals updated:
- "any decisions surface (`decisions/decision-log.md` OR `decisions/INDEX.md` OR `decisions/entries/`)"
- "any glossary surface (`glossary.md` OR `glossary/INDEX.md` OR `glossary/entries/`)"

Threshold (3-of-6 signals) unchanged.

### Audit-side mode-portability

`acw-instance/references/audit.md` Canonical-shape compare step now reads `decision_tracking.mode` / `glossary.mode` and branches the shape it expects to find.

### Upgrade-side mode-portability

`acw-instance/references/upgrade.md` decision-log entry write step now dispatches:
- Single-file mode: append to `paths.decisions_log` under section
- Wiki mode: write file to `<entries_dir>/D-<CODE>-NNN-<slug>.md`, then regenerate INDEX

Same for instance-specific rationale entries.

### Adoption cost

Drop-in patches; no new skills, no breaking changes to single-file instances. Tested against `_Command`'s wiki-shape substrate today (D-CMD-025 written in new shape, INDEX regeneration works).

---

## 3. /acw-session architectural improvements

Independent of substrate shape. From the 95-source research artifact (saved at `Cortex/Resources/research/2026-05-12--acw-session-skill-problems-and-improvements.md`):

### Pass 1 — Tier A (high leverage)

**Sonnet subagent for Phase 3 + 5 judgment.** `model: claude-haiku-4-5` on parent; judgment phases dispatch to subagent `.claude/agents/session-end-judgment.md` (`model: sonnet`). Removes the "Sonnet escalation" prose fiction — Claude Code doesn't ship per-step model selection (anthropics/claude-code#23462 still open). Bounded return contract (≤800 / ≤1500 tokens) prevents subagent-overflow (anthropics/claude-code#23463).

**Named profiles replace flag soup.** `end | end full | end log-only | end synapse-only | end research-only` instead of 8-cell `quick/full × --synapse/--research/--no-synapse/--no-research` matrix. Greppable; operator memorizes 5 names instead of flag combinatorics.

**Per-phase status emission.** Every phase emits `[phaseN] RAN | SKIPPED(reason) | FAILED(error)` line. End-of-run banner lists all phases. Adopted from Airflow/Prefect/Dagster discipline (skipped tasks as first-class run state, not absence).

**Phase 5 empty-tracks gate.** Don't surface "Build research prompt now?" when both Track A and Track B are empty. Emit `[phase5] SKIPPED(empty-tracks)` and exit. Closes the long-standing gotcha.

### Pass 2 — Tier B (medium leverage)

**Pre-flight context-budget check (spine Step 0).** Heuristic-estimate context %. If >70% AND verb is `end`, abort with operator-facing message: "/compact first, then retry. For minimal capture: /acw-session end log-only." Closes 5/11 absorption-note carry-forward (a).

**Batch operator-confirm proposals.** Phase 3 collects all operator-confirm proposals into a single approval batch at phase end. Replaces N inline prompts. Reduces approval fatigue.

**Resume token in `.current-session`.** Schema becomes `{file, session_hash, last_completed_phase}`. End updates after each phase. Re-running end with matching hash skips already-completed phases (idempotency). Backward-compatible: plain single-line filename still accepted.

**Symmetric archive registration in Phase 2.** Detect new `decision-log-YYYY-Q*.md` or `tasks-status-YYYY-Q*.md` files; propose `meta_layer` append. Closes 5/11 carry-forward (c).

**Phases 4 + 5 parallel when both fire.** They don't depend on each other. Two-Task-call parallel dispatch. AgentEval (arxiv 2604.23581) finding: 88% of agent traces are sequential despite parallel-safe branches.

### What's NOT changing

- Three-verb command table (`start`, `update`, `end`) — bookend contract preserved
- Five-phase structure of `end` — phases stay; mode dispatch and judgment delegation change how they run
- Subdir structure under `references/` — same layout; mode-dispatch is in prose
- Backward compatibility with single-file substrate is non-negotiable; this is the canonical default

---

## 4. Tasks-status simplified to Pending-only (D-CMD-030, added 2026-05-12 PM)

### What changed

Three coupled changes to the canonical tasks-status shape:

1. **Pending-only.** `tasks-status.md` carries one section: Pending. No Done. No Parked.

2. **Archive on completion (event-driven).** When a task completes, the completing session writes a dated session block to `tasks-status-YYYY-Q*.md` immediately and removes the item from Pending. No weekly cadence. No interval metabolize.

3. **Parked retired.** Deferred-but-keep ideas route to `inbox/ideas/` (wiki-shaped, one file per idea, frontmatter `type: idea, status: parked, date:`). Architectural deferrals (we considered X and decided not to do it now) earn a decision-log entry. Long-tail noticed-but-not-actionable observations die in conversation.

### Schema implication

No new fields needed in `acw-state.yaml`. The existing `tasks_status` path key continues to point at `tasks-status.md`. The archive file convention (`tasks-status-YYYY-Q*.md` in `meta_layer`) stays the same; what changes is *when* writes happen (on completion, not on cadence).

### Canonical rewrite (pattern A — already landed)

`Projects/acw/rules/task-tracking.md` rewritten in place this session. Key changes:

- "Three sections" framing replaced with "Pending-only (v0.9.3+ canonical shape)".
- "Rolling-window discipline" section replaced with "Done — archive on completion (no interval cadence)".
- "Parked" section title kept as a heading but body rewritten to "retired (v0.9.3+)" with replacement routing documented (`inbox/ideas/` or decision-log).
- "Migration from pre-v0.9.3 instances" section added at the end: 5-step migration procedure for instances on the three-section shape (move Done to archive; move Parked to archive's final frozen block; cherry-pick active items into `inbox/ideas/` or decision-log; rewrite live file Pending-only; log D-CMD-NNN).

### Skill changes (coupled with §2 portability work)

Five skill-reference files updated in `~/.claude/skills/acw-session/`:

- `SKILL.md` — append-only files list updated: tasks-status archive (`tasks-status-YYYY-Q*.md`) replaces "Done blocks" as the append-only target.
- `references/distribution-rules.md::paths.tasks_status` — full rewrite. Pending-only writes (live file); archive-on-completion writes (archive file). "Never" list updated: never write to a Done section or a Parked section in `tasks-status.md` (those sections don't exist in v0.9.3+ shape).
- `references/metabolize-rules.md` — tasks_status row in the metabolize table rewritten: Pending items completed → write to archive + remove from Pending; Pending items superseded by decision → propose removal or move to `inbox/ideas/`.
- `references/end.md` — Phase 1 task identification + Phase 2 distribution updated. Example operator-confirm proposal swapped from "Move Parked item X to deprecated" to "Mark idea X in inbox/ideas/ as superseded (now covered by D-CMD-NNN)".
- `references/metabolize-report-format.md` — example output lines updated: "moved to the new Done block" → "removed from Pending; dated session block written to tasks-status-YYYY-Q*.md archive".

### Local instance state (_Command, applied 2026-05-12)

- Live `tasks-status.md` rewritten as Pending-only (~150 active items preserved).
- Done blocks (3 sessions: 2026-05-12, 05-05/06, 05-04) moved to `tasks-status-2026-Q2.md`.
- Full Parked section (~85 items across 4 sub-blocks: main + AI CS Copilot PRD + ATL AI Week + 2026-04-27 session) moved to `tasks-status-2026-Q2.md` as a frozen final block (clearly marked: "Parked section retired 2026-05-12; content below frozen for historical reference").
- `_Command/rules/auto-load-discipline.md::tasks-status.md` caveat rewritten for v0.9.3+ language.
- `_Command/rules/instance-current-manifest.md::tasks-status-YYYY-Q*.md archive` entry rewritten: archive-on-completion, not rolling-window.
- `_Command/CLAUDE.md::Operator's untriaged items` updated: `inbox/ideas/` is the explicit replacement for the retired Parked section.
- `_Command/acw-state.yaml::auto_load_at_session_start::tasks-status.md` claim updated to reference D-CMD-030.

### Rationale (condensed; full version in D-CMD-030)

The prior three-section shape carried two failure modes:

1. **Done as live-file resident is wrong abstraction.** Done is write-once historical, not a work-queue state. Keeping it in the live file costs auto-load context every chat without operational value. `build-log.md` already covers the same period in fuller form. D-CMD-024's weekly cadence treated the symptom; D-CMD-030 treats the root (Done shouldn't live in active work-queue file at all). _Command hit "Prompt is too long" twice in a week (5/11 + 5/12) partly because Done sat in the live file even with weekly cadence.

2. **Parked accumulated without consumer.** Grew to ~85 items at retirement time across multiple sub-blocks with no review cadence and no consumer skill. Most entries never came back into scope. The right routing was always `inbox/ideas/` (deferred-but-keep, wiki-shaped) or decision-log (architectural deferral); Parked was the middle category that bloated the file.

The cadence change is event-driven, not time-driven. Cadence was a symptom-management pattern for the original shape; Pending-only makes cadence meaningless.

### Supersession

**Supersedes D-CMD-024's tasks-status cadence rule.** D-CMD-024 ships in two halves:
- Tasks-status weekly cadence → **moot under Pending-only**.
- Decision-log weekly cadence → **stands independently** for single-file-mode instances. Wiki-mode instances don't need a Done-style archive (each entry is its own file).

The decision-log archive registration discipline (5/11 carry-forward c, closed by Pass 2's symmetric archive-registration in §3) still applies — that's about *registering* archive files in `meta_layer`, orthogonal to *when* archive writes happen.

### Adoption posture

This thread is the lowest-risk of the four — no schema additions, no new keys in `acw-state.yaml`. The change is in `rules/task-tracking.md` prose + 5 skill-reference files. Migration mechanics for existing instances are documented in `rules/task-tracking.md` § "Migration from pre-v0.9.3 instances".

---

## 5. The 5/11 carry-forwards — status update

The 5/11 absorption note flagged three items:

| Carry-forward | Status |
|---|---|
| (a) Cadence-friction telemetry in `/acw-session start` to catch "Prompt is too long" before operator does | **Addressed by Pass 2 P-10 (pre-flight context check).** Lands in spine Step 0; runs in every verb but with verb-dependent abort thresholds. |
| (b) Re-evaluate weekly as default for new instances | **Moot under D-CMD-030 for tasks-status** (no cadence). For decision-log single-file mode, the weekly default still stands. |
| (c) Symmetric archive-registration check for `decision-log-Q*.md` | **Addressed by Pass 2 P-13 (Phase 2 archive registration).** Phase 2 detects new archive files matching `decision_tracking.archive_pattern` and proposes `meta_layer` append. |

---

## 6. Adoption tiers (ACW's choice)

ACW can adopt these in four tiers depending on risk appetite:

### Tier 1 — Substrate shape only

Add `decision_tracking.mode` and `glossary.mode` to schema. Document wiki mode as opt-in. Ship reference migration script in `tools/`. Skills stay single-file-only. Result: instances can adopt wiki shape locally; canonical session skill won't write to wiki-shape decisions correctly but won't actively break (logs warning).

Risk: low. Schema-only change. No skill changes.

### Tier 2 — Substrate shape + skill portability

Tier 1 + mode-dispatch in `acw-session` distribution/metabolize and `acw-instance` audit/upgrade. Single-file mode stays default; wiki opt-in works end-to-end.

Risk: medium. Touches skill files but adds branches; doesn't change single-file behavior.

### Tier 3 — Substrate + portability + Pass 1/2 architecture

Tier 2 + Pass 1 + Pass 2 architectural improvements to `/acw-session`. Sonnet subagent, named profiles, status emission, pre-flight check, batch confirmations, resume token, parallel 4+5, archive-registration.

Risk: medium-high. Substantial rewrite of `end.md` and SKILL.md. Test against existing single-file instances to confirm backward compat before merging.

### Tier 4 — All four threads (Tier 3 + tasks-status Pending-only)

Tier 3 + D-CMD-030 changes: `rules/task-tracking.md` rewrite (Pending-only, archive-on-completion, Parked retired), plus the 5 skill-reference file updates that ship coupled with it. Migration mechanics for pre-v0.9.3 instances documented in the rewritten rule.

Risk: low-to-medium. The rule rewrite is prose-only; no schema additions. Skill changes are localized to tasks-status write paths. The migration is mechanical (move Done to archive, move Parked to archive's final frozen block, rewrite live file). Existing instances on the three-section shape continue to work until they choose to migrate — the rule documents both shapes during the transition window if needed.

**_Command's lean:** Tier 4 in one PR — all four threads share the same root cause (auto-load shape vs. cadence) and shipping them separately leaves the same failure mode partially unaddressed. Reference implementation already lives at `~/.claude/skills/{acw-session,acw-instance}/` and `Projects/acw/rules/task-tracking.md` post-2026-05-12 and is in active use against `_Command`.

---

## 7. Reference implementation receipts

All files at consumer paths (`~/.claude/skills/...`); backing store is `~/synapse/skills/...`.

**acw-session:**
- `SKILL.md` — spine pre-flight (Step 0), tracker resume-token schema, mode-detection in Step 1, verb-scoped reference loading principle
- `references/end.md` — profile dispatch (5 profiles), mode-portable Phase 2 + 3, Sonnet subagent dispatch for judgment, parallel 4+5, empty-tracks gate, status emission per phase, resume-token updates
- `references/distribution-rules.md` — mode-portable for decisions + glossary; cross-file consistency rules updated
- `references/metabolize-rules.md` — mode-portable
- `references/metabolize-report-format.md` — examples for both modes
- `references/research-prompt-format.md` — OQ update path mode-portable
- `references/session-capture-format.md` — language for both modes
- `gotchas.md` — updated for new realities

**acw-instance:**
- `SKILL.md` — canonical-shape signals accept both modes; template-fetch dispatch on mode
- `references/audit.md` — canonical-shape compare branches on mode; auto-load surface language mode-aware
- `references/upgrade.md` — decision-log write dispatches on mode; write-canonical row language mode-aware

**Subagent definition:**
- `~/.claude/agents/session-end-judgment.md` — Sonnet-bound subagent for Phase 3 + 5 judgment dispatch

**Canonical edits already landed (pattern A):**
- `Projects/acw/rules/task-tracking.md` — full rewrite for D-CMD-030 (Pending-only, archive-on-completion, Parked retired, migration steps)

**_Command-side state (proof of working integration):**
- `_Command/acw-state.yaml::decision_tracking.mode: wiki` + populated wiki-mode keys
- `_Command/acw-state.yaml::glossary.mode: wiki` + populated wiki-mode keys
- `_Command/decisions/INDEX.md` + entries/ + open-questions/ + constraints/
- `_Command/glossary/INDEX.md` + entries/
- `_Command/decisions/entries/D-CMD-025-substrate-migrated-to-karpathy-wiki-shape.md` — first decision written native in new shape (dogfood gate)
- `_Command/decisions/entries/D-CMD-026-acw-session-and-instance-skills-made-substrate-mode-portable.md` — skill rewrite decision in wiki shape
- `_Command/decisions/entries/D-CMD-030-tasks-status-pending-only-parked-retired.md` — tasks-status simplification decision in wiki shape; supersedes D-CMD-024's tasks-status side
- `_Command/tasks-status.md` — rewritten Pending-only (proof of v0.9.3+ shape working)
- `_Command/tasks-status-2026-Q2.md` — gained 3 archived Done blocks + retired Parked section as frozen final block
- `_Command/rules/auto-load-discipline.md` + `_Command/rules/instance-current-manifest.md` — local rule mirrors updated for v0.9.3+ language
- `_Command/CLAUDE.md::Operator's untriaged items` — `inbox/ideas/` named as explicit replacement for retired Parked section

---

## 7a. Edit discipline used in this absorption (pattern A)

Operator directive 2026-05-12: pattern A is the going-forward rule for ACW canonical edits where operator is the reviewer.

**Pattern A:** Edit canonical rules in place; file an absorption note in `_buffer/` documenting what changed and why. Operator IS the reviewer, so the buffer's review-gate function is satisfied by the operator's own awareness of the change set. The buffer note is the durable receipt.

**Pattern B** (rejected for this kind of work): Write the proposal first, get external review, then edit canonical. Reserved for cases where reviewers external to the operator need to weigh in before canonical changes land.

For this session's work:
- 5/11 cadence tightening (D-CMD-024) used pattern A — direct rule edits, absorption note filed after.
- This morning's substrate/portability/architectural work used pattern B — buffer proposal written first, canonical edits to follow once operator confirmed scope.
- This afternoon's tasks-status simplification (D-CMD-030) used pattern A — direct rule edit in `Projects/acw/rules/task-tracking.md`, with this buffer note extended after the fact to document.

Going forward: pattern A unless reviewers external to the operator need to weigh in. Document the discipline in each absorption note's frontmatter (`edit_discipline:` field — added to this proposal's frontmatter today).

---

## 8. Open questions for ACW

1. **Default mode for new instances.** `single-file` (backward compat) or `wiki` (industry canon)? _Command leans `single-file` default, `wiki` documented as sanctioned variant — Path B from the research.
2. **Mutability convention.** Living-document with date-stamped amendments (_Command's choice; pragmatic for single-operator) or strict-immutable-supersede-only (AWS/MADR canon; better for multi-author)? Could be a `decision_tracking.mutability` field.
3. **INDEX regeneration mechanism.** `regenerate_index_cmd` invokes an external script (current _Command approach). Alternative: skill-side INDEX rendering (no external tool dependency) — could ship as ACW canonical Python in `tools/`.
4. **Filename convention in wiki mode.** Legacy id in filename (`D-CMD-024-slug.md`, _Command's choice) or MADR sequential (`0024-slug.md` + `aliases:` frontmatter, ADR canon)? _Command picked legacy-id-in-filename — zero-friction for in-flight cross-references — but the choice is debatable.
5. **Subagent registry.** `.claude/agents/session-end-judgment.md` lives in user-level Claude Code today. If ACW ships canonical skills, should subagent definitions ship alongside in canonical `agents/` for instances to junction onto? Or should canonical skills assume the subagent exists and instances are responsible for shipping it?
6. **Skill body size.** `acw-session/references/end.md` is now ~250 lines (was 191). Anthropic's <500-line skill-body target still holds, but progressive disclosure into more sub-references could trim further. Probably defer until friction surfaces.
7. **Tasks-status migration cadence for existing instances.** New instances on v0.9.3+ canonical get Pending-only by default. Existing instances on the three-section shape need a one-time migration. Should `/acw-instance upgrade` detect the three-section shape and offer the migration as a row in the migration plan? Or should it be operator-driven via a `python tools/migrate_tasks_status.py` style script? _Command's lean: detect + offer in `/acw-instance upgrade` (consistent with how other v0.9.x migrations have shipped).
8. **Edit discipline going forward.** Pattern A (edit canonical in place, absorption note as receipt) declared as going-forward default for ACW canonical edits where operator IS the reviewer. Does ACW want this codified in `rules/` somewhere (e.g., a `canonical-edit-discipline.md` in rules/)? Or stays as convention?

ACW reviews on its own cadence; _Command will keep operating on the wiki shape + portable skills + Pending-only tasks-status regardless.
