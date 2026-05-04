---
date: 2026-05-04
participants: [operator, agent]
topic: v0.8.0 bookend efficiency cluster + plans folder + Kashef research
decisions_made: [D-ACW-037]
conceptual_shifts: yes
linked_files:
  - decisions/decision-log.md
  - incidents.jsonl
  - skills/acw-session/SKILL.md
  - skills/acw-session/references/start.md
  - skills/acw-session/references/end.md
  - skills/acw-session/references/update.md
  - acw-state.yaml
  - tools/templates/acw-state.yaml.tmpl
  - rules/manifest-discipline.md
  - rules/instance-current-manifest.md
  - tasks-status.md
  - sessions/ (migration target — 8 files renamed from research/sessions/)
  - skills/capture-session/ (deleted)
  - skills/capture-and-metabolize/ (deleted)
  - skills/resume-session/ (deleted)
  - skills/upgrade-instance/ (deleted)
  - research/11-session-continuity-prior-art.md (created in Session 12, retained as meta_layer)
  - research/12-kashef-hive-mind-comparison.md (created this session)
  - plans/ (new directory; .gitkeep)
duration_minutes: ~180
---

# Session 13 — v0.8.0 bookend efficiency + plans folder + Kashef research

## 1. Topic & Goal

Two things happened in this session, in sequence. First: ship v0.8.0 bookend efficiency cluster — operator surfaced acute cost pressure (`/acw-session end` running 7-10 minutes per invocation on Opus 4.7 1M context, halfway through Max-plan weekly budget after 2 days). The session translated that into a six-change ship: Haiku-default model frontmatter, fresh-subagent isolation, quick/full mode split with quick as default, `/acw-session update` mid-session checkpoint verb, `.current-session` tracker, sessions/ migrated to root, retire 4 superseded skills. Plus a 7th change folded in mid-execution: `plans/` directory at workspace root for plan artifacts.

Second: deep research on Mark Kashef's "ClaudeClaw V3 / Hive Mind" Claude Code setup, framed as *"what scaffolding could ACW absorb that would be earn-shippable?"*. Two parallel research lanes returned with strong findings: zero patterns original to Kashef; ACW occupies the substrate layer of the agentic-OS stack uniquely; three weak earn-ship candidates worth `DEFERRED.md` rows but no immediate ship.

## 2. What was decided

- **D-ACW-037 — v0.8.0: bookend efficiency cluster** (newly created this session). Six original changes plus `plans/` folder added as 7th item mid-execution. Records cost-friction incident `a8e771f0-7686-484d-b89e-cc25e96f8c93` as the activation evidence. Five open follow-ups documented inline.
- **Quick mode is the default for `/acw-session end`.** `full` is the verb argument. `--synapse` and `--research` flags surface those phases inside quick mode. Operator can pick the heavy session at logical boundaries; quick handles routine sessions cheaply.
- **`/acw-session update` ships as a third bookend verb.** Mid-session checkpoint, Haiku-grade end-to-end, self-bootstraps if no `.current-session` tracker exists.
- **`sessions/` lives at root, not under `research/`.** Sessions are operational logs, not research artifacts. Naming with their actual purpose clears semantic space in `research/` for what `research/` actually holds.
- **Four superseded skills deleted from disk** (`capture-session/`, `capture-and-metabolize/`, `resume-session/`, `upgrade-instance/`). Closes v0.4.0 Pending item the careful guardrail blocked from automated removal.
- **`plans/` directory canonical** with `paths.plans_dir: plans` default. Convention only in v0.8.0 — no automatic writer skill; operator drops plans there manually. Earn-by-content reasoning: cheap to pre-create the directory; the writer skill earns its build only when convention demands automation.
- **Three new earned-in-0.8.0 manifest registry entries** plus `plans/` as the fourth: `sessions/` at root, `.current-session` tracker, `model:` frontmatter for bookend skills, `plans/` directory.
- **Operator directive on AGENTS.md / CLAUDE.md future shape (captured for separate ship):** *"AGENTS.md is going to be the entry file. The CLAUDE.md should just be a pointer to that AGENTS.md, for people who are using CLAUDE instances, just because CLAUDE looks for the CLAUDE.md."* Future state: AGENTS.md carries the substantive content currently in CLAUDE.md as the instance version; CLAUDE.md becomes a "see AGENTS.md" stub. Not in v0.8.0 or v0.9.0 — separate ship.
- **Kashef research filtered through earn-ship lens.** Three candidates surfaced as substrate-shaped (worth `DEFERRED.md` rows, not immediate ship): `/acw-session standup` verb, briefing skill, suggestions/drift surfacer. Hold list: 3D visualization, Mission Control UI, "back of house" terminology, Telegram bridge, mega-prompt install pattern.
- **ACW positioning in agentic-OS stack named explicitly.** ACW occupies the substrate/governance layer; UI/Mission Control, orchestration runtime, memory/retrieval are separate layers. ACW is the only published framework occupying its layer with this discipline. Worth folding into `LINEAGE.md` (deferred to next session).

## 3. What changed in the conception

Three conceptual shifts worth naming.

**Conceptual shift 1: bookend skills are model-tiered work.** Earlier ACW thinking treated the bookend as one homogeneous skill that runs at whatever the parent session's model is. v0.8.0 split it into tiered work — most phases are mechanical (Haiku-grade), specific steps need judgment (Sonnet for Phase 3 operator-confirm proposals and Phase 5 research-prompt construction; meta-layer trigger edits). The `model:` frontmatter declaration is the mechanism; subagent isolation is the cost discipline. This generalizes — any future ACW skill that does mostly mechanical work over substrate should declare its model floor.

**Conceptual shift 2: substrate creation is itself earn-by-incident.** Operator surfaced this question late in the session, and it grounds v0.9.0 (substrate earn-by-content refactor — scaffolder ships discipline floor only; bookend scaffolds substrate files on-demand when content earns them). The Kashef research reinforced the framing: Kashef's "salience and recency" framing is the *consumer-side* of substrate retrieval; v0.9.0's earn-by-content is the *producer-side*. Complementary halves of the same retrieval-quality problem.

**Conceptual shift 3: ACW occupies the substrate layer of the agentic-OS stack.** Kashef research surfaced the layer breakdown explicitly (UI / orchestration runtime / memory / **substrate** / skills / model routing). ACW is the only published framework occupying the substrate layer with this discipline. Closes a citation gap — ACW currently doesn't name its layer relative to the field; doing so makes its complementarity (vs. competitive overlap) legible.

## 4. What was built / changed

**Skill edits:**

- `skills/acw-session/SKILL.md` — `model: claude-haiku-4-5` frontmatter; description rewritten for three verbs; command table updated with `update` row; tracker convention section added.
- `skills/acw-session/references/start.md` — Step 0 added before existing steps; creates capture file with frontmatter and `## Updates` section, writes relative filename to `<sessions_dir>/.current-session`.
- `skills/acw-session/references/end.md` — Mode dispatch table; Quick mode behavior section; Full mode behavior section; per-phase mode notes; Sonnet escalation notes for Phase 3 and Phase 5; tracker cleanup section.
- `skills/acw-session/references/update.md` — NEW. Reads `.current-session`; appends timestamped note under `## Updates`; self-bootstraps with topic-from-note slug if no tracker.

**Substrate writes:**

- `decisions/decision-log.md` — D-ACW-037 added at top of Decisions section (post-`plans/` fold-in: 7-item change list, 5 open follow-ups).
- `incidents.jsonl` — cost-friction incident appended (`a8e771f0-7686-484d-b89e-cc25e96f8c93`).
- `tasks-status.md` — Session 13 Done block added; v0.4.0 superseded-skills Pending item closed.

**State / manifest:**

- `acw-state.yaml` — version 0.7.0 → 0.8.0; `last_reconciled_version` bumped; `paths.session_captures_dir: sessions`; `paths.plans_dir: plans` added; `empty_dirs` swap (`research/sessions` → `sessions`; `plans` appended); meta_layer cleanup of 4 superseded skill entries; `research/11-session-continuity-prior-art.md` added to meta_layer.
- `tools/templates/acw-state.yaml.tmpl` — `last_reconciled_version: "0.8.0"` for fresh instances. (No empty_dirs/paths blocks in this template; canonical defaults flow from rules/manifest-discipline.md at scaffold time.)
- `rules/manifest-discipline.md` — canonical default-paths table updated: `session_captures_dir` → `sessions`; `plans_dir` → `plans` row added.
- `rules/instance-current-manifest.md` — four new earned-in-0.8.0 entries: `sessions/` at root, `.current-session` tracker, `plans/` directory, `model:` frontmatter for bookend skills.

**Filesystem moves / deletes:**

- `git mv research/sessions sessions` — 8 capture files migrated.
- `mkdir plans && touch plans/.gitkeep` — new directory with .gitkeep.
- `rm -rf skills/capture-session skills/capture-and-metabolize skills/resume-session skills/upgrade-instance` — four superseded skill directories deleted.

**Research artifacts:**

- `research/11-session-continuity-prior-art.md` — landed in Session 12 (yesterday); 95-source survey of session-continuity prior art across Anthropic native, memory frameworks, workspace conventions, multi-agent orgs, and academic/thought-leader output.
- `research/12-kashef-hive-mind-comparison.md` — created this session; 25-source synthesis filtering Kashef's Hive Mind setup through ACW's earn-by-incident lens. Three earn-ship candidates documented; ACW positioned in agentic-OS substrate layer.

**Release gates (post fold-in):** vocab lint exit 0, drift check clean, 46/46 tests pass.

## 5. Open questions left — structured

#### OQ-080-A — Will `model:` frontmatter on SKILL.md actually be honored at runtime?

**Question:** v0.8.0 ships `model: claude-haiku-4-5` in `skills/acw-session/SKILL.md` frontmatter expecting Claude Code to use Haiku for the skill's work. The field may not be honored by all Claude Code versions; documentation isn't fully clear on the field's status. If not honored, the skill still works at whatever model the harness picks; the cost-cut is just smaller. Need empirical confirmation that the field works as designed.

**Candidates considered:** Wait for first invocation post-restart and observe; alternative is pre-emptively wrapping bookend in subagent invocation that explicitly sets model.

**Why unresolved:** Needs first real invocation of `/acw-session end quick` with the new SKILL.md to confirm model selection. Operator will test on next session boundary.

**Who needs to weigh in:** Operator (empirical test); fallback is Anthropic Claude Code documentation if the field is documented somewhere I haven't found.

#### OQ-080-B — Should the three Kashef-research earn-ship candidates land in DEFERRED.md or wait?

**Question:** The Kashef research surfaced three substrate-shaped candidates: `/acw-session standup` verb, briefing skill, suggestions/drift surfacer. Each has an activation trigger. Should they land in `DEFERRED.md` now (declarative documentation of intent + activation criteria) or wait for first incident before even being recorded?

**Candidates considered:** Land all three in `DEFERRED.md` now with activation triggers — keeps the design slot warm, documents the thinking; or hold until first incident — keeps `DEFERRED.md` from accumulating speculative entries.

**Why unresolved:** Requires operator call. The earn-by-incident discipline argues for the latter (don't document what hasn't earned its evidence); the deferred-library philosophy argues for the former (document the design slot so future operators don't re-derive).

**Who needs to weigh in:** Operator preference + read of how `DEFERRED.md` has grown so far.

#### OQ-080-C — When does v0.9.0 (substrate earn-by-content) land?

**Question:** v0.9.0 was discussed as the next substantive design pass — scaffolder ships discipline floor only; bookend scaffolds substrate files on-demand when content earns them. Operator approved the direction but hasn't picked a ship date. Some open design questions remain (threshold table, retroactive behavior on existing instances, manifest registry shape).

**Candidates considered:** Ship v0.9.0 next session; defer until v0.8.0 has soaked for a week+ to see if cost-cut works as designed; spawn a research note (`research/13-substrate-earn-by-content.md`) first to pressure-test the threshold table before code lands.

**Why unresolved:** Operator preference; also depends on whether v0.8.0's cost-cut is empirically validated first.

**Who needs to weigh in:** Operator.

## 6. Operator directives (verbatim)

> "Use haiku where haiku can do it and sonnet where haiku can't."

> "I'm down to make phase 4 and phase 5 opt-in, not default."

> "Sessions should actually be a folder at the root. It doesn't really belong in research."

> "I'm reading the capen, I'm reading the promotion ritual how primitives earn the deferred ship move. I feel like out of the box an instance how. Look, not every instance needs everything that ACW has."

> "The agents.md is going to be the entry file. The CLAUDE.md should just be a pointer to that agents.md, for people who are using CLAUDE instances, just because CLAUDE looks for the CLAUDE.md. It would be a quick, simple: CLAUDE goes to the CLAUDE.md, the CLAUDE.md says go to see agents.md, immediately goes to agents.md, and there is the entry file. That's how I want it to work in the future. The agents.md should look like the CLAUDE.md looks like now. That would be an instance version of the agents.md, not a template version."

> "Let's get rid of capture and metabolize. Capture session, resume session, and upgrade instance. Those have already been absorbed by ACW instance and ACW session."

> "I'm actually interested in seeing what other scaffolding we could put into ACW that would be earnship."

> "Add this to eight... fold it in. then acw-session end" — re: `plans/` directory.

## 7. Cleaned transcript excerpt

Skipped — this session was build-heavy, transcript-light. Operator directives in §6 carry the load-bearing wording; rationale lives in D-ACW-037.
