---
class: archive
authority: derived
stability: stable
loaded_by_agent: no
---

# Build Log — ACW

Append-only, newest-first narrative of build progress per session.

## 2026-05-02 — v0.4.0: command-routed skills, full audit verb, absorption mechanics

Operator opened the session with a session capture from cs-copilot where they had tried to run `/upgrade-instance` and the agent there bailed because cs-copilot is substantively an ACW instance but lacks formal registration. This was already addressed in v0.3.0 via adopt mode, but the operator's question went deeper: what about workspaces with **organic substrate** that's evolved its own conventions (like `_Command`)? Steamrolling those into canonical shape would destroy institutional learning.

The conversation refined the three-flow model: adopt (canonical-shaped, just unregistered), absorb (workspace's pattern is better than canonical; flow upstream via `_inbox/`), and instance-specific (uniquely the workspace's, won't generalize). Operator pressed on permanent divergence as a smell: the gradient should always be toward canonical-shaped. Right answer — `divergent_pending_review` is temporary, pending ACW resolution; `instance_specific_substrate` is permanent but requires a decision-log reference.

Then a structural insight: rename `/upgrade-instance` → `/acw-instance` with verbs `audit` and `upgrade`, fitting the command-routed orchestrator pattern. Operator pushed further: `/resume-session` and `/capture-and-metabolize` should follow the same shape as `/acw-session start|end`. I initially pushed back — the four-test rule reading "same invariant workflow" seemed to prohibit sibling specialist operations. Operator pointed at Impeccable as the precedent: 23+ commands across genuinely different specialist workflows, unified by shared setup. Re-reading the skill-format with that lens, the strict-voice contradicted the permissive-voice (command-count ladder explicitly carves out object-centered workbenches at 10+ commands). The format itself was self-contradictory; that's why I false-flagged the pattern.

Then the synthesis question: is every problem named in this session shippable? It surfaced loose items — absorption candidate format wasn't specified, divergence marker schemas weren't documented, hard-stop threshold had no value, re-adoption flow had no mechanics. Six commits revised: tighten skill-format, expand multi-instance-topology with absorption mechanics, register four new recommended blocks, restructure skills as command-routed, housekeeping.

Two operator pushbacks during execution that produced better answers:
- Mode A doesn't need a new schema artifact; ACW rules + templates ARE the schema in prose form. Audit verb fetches them from GitHub canonical and compares inline.
- Mode B doesn't need sophisticated heuristics; it needs the operator in the loop. Walk for substrate-like patterns; surface to operator with four-option routing.

Both ship in v0.4.0 instead of being deferred.

The skill-format port was bigger than expected. ACW canonical's `rules/skill-format.md` had been shorter than the operator's synapse global rules — the command-routed orchestrator material had only existed in the personal layer. Ported the full content into ACW canonical with the three corrections applied.

User-level junctions swapped at the end. Old skill directories marked superseded in frontmatter (`status: superseded`, `superseded_by`, `superseded_in: 0.4.0`); moved to `meta_layer` awaiting manual delete (careful guardrail blocks automated `rm -rf`).

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 7 dated block. `tasks-status.md::Pending` rebuilt with v0.4.0-shaped tasks (dogfood `/acw-instance audit` against cs-copilot, `_Command`, gsg-copilot; deletion task for four superseded skill directories).
- `decisions/decision-log.md` — added D-ACW-016 through D-ACW-022 (seven entries) in chronological order.
- `acw-state.yaml` — bumped `version` and `last_reconciled_version` to `0.4.0`; added `_inbox` to `empty_dirs`; added `divergent_pending_review`, `instance_specific_substrate`, `adopt_mode_organic_threshold` blocks; updated `template_layer` to list new skills; added superseded skills to `meta_layer`; added `research/10-multi-instance-topology.md` to `meta_layer`.
- `tools/templates/acw-state.yaml.tmpl` — same shape as parent for the four new blocks.
- `incidents.jsonl` — appended `0e4dcc21` (skill-format false-flag, severity low, category process-gap). Resolution shipped in same release via D-ACW-016.
- `research/sessions/2026-05-02--v040-command-routed-skills-and-audit-verb.md` — session capture written by `/acw-session end` at session close.

**Proposed for operator review** (deferred to next session):
- Manual deletion of four superseded skill directories after dogfood validates v0.4.0 against cs-copilot.
- Cross-instance write trigger entry in `DEFERRED.md` for the capability broker.
- Lint gate for command-routed skills.
- OQ-ACW-007: how does ACW notify a workspace when an absorption candidate is rejected? (Three candidates in the session capture; needs lattice-scale evidence.)

## 2026-05-02 — RC4 → v0.3.0: multi-instance topology, GitHub-first canonical, adopt mode

Operator opened the session by feeding back a cs-copilot session where `/upgrade-instance` correctly identified missing registration files and bailed. They pushed back on the "not an ACW instance" verdict, asking what an ACW instance fundamentally **is**. The conversation surfaced the substance-vs-registration distinction: cs-copilot has every load-bearing piece of an ACW instance (decisions, rules, glossary, evolution, research, incidents, bookend skills) but lacks the registration metadata. Verdict: cs-copilot is substantively an ACW instance; the agent ran a registration check rather than a substance check.

That conversation escalated into the larger architectural question: can a full business run from ACW, and if so, what's the structure? Sketched the lattice model (org-brain instance + departmental instances), the knowledge-placement discriminator (who queries it; does the answer need to be the same), the reference-not-duplicate principle, the three coordination primitives needed (handoff protocol, capability broker, admission controller — the broker now has the lattice as its architectural target), the authority model across the lattice, the bootstrapping order (departmental first, org-brain refactored from extraction).

Wrote `research/10-multi-instance-topology.md` formalizing the lattice and naming Phase 1 ship: fix `/upgrade-instance` to support adopt mode for substrate-shaped pre-ACW workspaces.

Operator then asked four sharp follow-up questions that exposed real seams:

1. How do we conceptualize the lattice into the template so a business is informed when ready? **Answer:** promote canonical statement to `rules/multi-instance-topology.md` (template_layer). Research note stays meta_layer as provenance. Add as recommended block earned in v0.3.0.
2. When ACW's canonical registration updates, how do other instances stay current? **Answer:** GitHub as single source of truth. `/upgrade-instance` fetches canonical from `benfrankster-design/acw` on every run via `gh` CLI (private repo). Local copy is write-once cache. Operator rejected local-ACW fallback; one pointer means one place to update if repo ever moves.
3. How do edits inside ACW get captured and metabolized properly? **Answer:** add canonical-edit detection to `capture-and-metabolize` Phase 2. Detect edits to files in the intersection of `auto_load_at_session_start` and `template_layer`; branch on `is_canonical_source`.
4. What happens when child instances inherit the propagation behavior? **Operator caught the bug:** if Phase 2 ships a "version bump + push to GitHub" prompt to every instance, child instances will start trying to push to ACW's GitHub. Solution: add `is_canonical_source` flag to `acw-state.yaml`. ACW sets true; children default false. Phase 2 branches on the flag — publishers get the push prompt; consumers get a "local edits won't propagate" warning.

Shipped six pieces: new rule file, manifest registry entries, flag in state file + template, upgrade-instance rewrite, capture-and-metabolize Phase 2 update, version bump to 0.3.0. Logged D-ACW-012 through D-ACW-015. Updated tasks-status with two adopt-mode dogfood targets (cs-copilot and gsg-copilot) and a note to add the cross-instance write trigger to DEFERRED.md.

Push to `origin/master` retires the 8-commits-ahead parked task by landing rc1-rc4 plus v0.3.0 in a single batch — GitHub goes from 3 weeks stale to current in one move, and the new `/upgrade-instance` works against the live canonical from first run on any instance.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 6 dated block. Pruned the resolved 8-commits-ahead push task from Pending; added two adopt-mode dogfood tasks (cs-copilot, gsg-copilot) and the cross-instance broker trigger task.
- `decisions/decision-log.md` — added D-ACW-012, D-ACW-013, D-ACW-014, D-ACW-015 in chronological order.
- `acw-state.yaml` — bumped `version` and `last_reconciled_version` to `0.3.0`; added `is_canonical_source: true`; added `rules/multi-instance-topology.md` to `template_layer` and `auto_load_at_session_start`.
- `tools/templates/acw-state.yaml.tmpl` — set baseline `last_reconciled_version: "0.3.0"`; added `is_canonical_source: false` default.

**Proposed for operator review** (not executed):
- Whether `CLAUDE.md` needs an edit to reflect v0.3.0 substrate (new `rules/multi-instance-topology.md` in auto-load list); the auto-load list in CLAUDE.md is import-driven via `@`, so adding the file may want a manual import line.
- Whether `research/10-multi-instance-topology.md` should also live in cross-vendor-readable form somewhere downstream (e.g., as a starter template snippet) or whether the rule file is sufficient.

## 2026-05-02 — Skill registration via user-level junctions

Operator surfaced that `/resume-session` wasn't firing — the skills shipped at `acw/skills/<name>/` weren't being discovered by Claude Code, which reads from `.claude/skills/` and `~/.claude/skills/`. Discussed two registration patterns (project-level per workspace vs. user-level single canonical source) and the multi-instance pollution concern when child workspaces also ship the same skills via template_layer. Operator chose the user-level / single-canonical-source pattern: ACW is the registered source for every workspace; child copies stay passive on disk for self-contained distribution. Created three directory junctions in `~/.claude/skills/` pointing at ACW's `skills/<name>/` directories.

D-ACW-011 records the architectural choice. OQ-ACW-006 captures the open question of whether `tools/scaffold-instance.py` should optionally create skill junctions at scaffold time — deferred for second-instance evidence.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 5 dated block.
- `decisions/decision-log.md` — added D-ACW-011.
- `incidents.jsonl` — appended one process-gap incident: skills ship in template_layer but registration is manual, future operators will hit the same friction.

**Proposed for operator review** (not executed):
- *(none)* — session was small and unambiguous.

**Skipped** (intentionally not touched):
- All append-only history (build-log past entries, evolution past entries, incidents prior lines, capture-session past files, decision-log past decisions).
- `paths.research_queries_dir` is empty; nothing to consume.

**Prompts consumed this session:** *(none — `paths.research_queries_dir` is empty.)*

## 2026-05-02 — RC4: portable bookend skills, drift detection, upgrade skill

The bookend skills (`capture-and-metabolize`, `resume-session`) were tightly coupled to ACW's specific directory layout — paths to `decisions/decision-log.md`, `tasks-status.md`, `research/sessions/`, etc. were hardcoded throughout. That worked for ACW but broke portability: instances that wanted to restructure substrate, or future template evolution that moved a file, would force grep-and-replace across every skill. RC4 decouples the skills from paths via a manifest-driven approach, then adds drift detection so existing instances can learn they're behind and reconcile through a guided skill.

Shipped in seven atomic phases with verification at each boundary:

**Phase 1 — Foundations.** Added `paths:` block to `acw-state.yaml` listing 14 substrate file paths. Documented canonical defaults and four-operation manifest-tooling spec (load / append / contains / validate) in `rules/manifest-discipline.md`. Version bumped `0.2.0-rc3 → 0.2.0-rc4`. Commit `62ba6be`.

**Phase 2 — Python tooling (TDD).** Wrote `tests/test_manifest.py` first (33 tests covering existing-list reads, canonical-default fallback, append additivity, dict/list round-trip, comment preservation, error semantics). Implemented `tools/manifest.py` until tests passed first run. Subagent confirmed spec/impl alignment. Commit `dd8c8da`.

**Phase 3 — Skill refactor + references audit.** Refactored both bookend skills to use `paths.X` shorthand throughout. Audited 11 reference files in `capture-and-metabolize/references/`, plus `resume-session/`'s SKILL.md and gotchas. Replaced hardcoded paths with prose-level references resolved at runtime. Generalized project-specific references (gsg-copilot, synapse, Cortex, HR-CP-NNN) to be portable. Added `section_conventions` frontmatter to `decisions/decision-log.md`, `tasks-status.md`, `research/evolution.md` and their templates. Subagent verified zero hardcoded substrate paths remain. Commit `3c1cac8`.

**Phase 4 — Drift detection.** Created `rules/instance-current-manifest.md`, the declarative registry of recommended blocks (project, paths, auto-load list, three-layer manifest, empty_dirs, cross_repo_writes, synapse_log_path, voice). Each entry documents what / why / required / how-to-add / earned-in. Added Step 5 drift check to `resume-session` SKILL.md. Subagent caught a version-vs-date conflation: `last_reconciled` was a date but the comparison needed semantic versions. Fixed by adding `last_reconciled_version` field alongside the date field. Also clarified present-but-empty semantics: a block declared empty is deliberate opt-out, not drift. Commit `9374ccb`.

**Phase 5 — `/upgrade-instance` skill.** Built the reconciliation skill that walks operators through gap closure. Subagent stress test caught two more edge cases: partial blocks (some-but-not-all canonical keys) and malformed blocks (wrong shape). Resolved: partial blocks are honored as deliberate operator choice (runtime defaults fill the rest); malformed blocks halt the pass and ask for hand-edit (skill is reconciliation, not validation cleanup). Commit `0070938`.

**Phase 6 — Substrate updates** (this entry). Decision-log entries D-ACW-008, D-ACW-009, D-ACW-010 record the architectural choices. Tasks-status Session 4 block. CLAUDE.md updated with the new auto-load entry (`rules/instance-current-manifest.md`). Evolution entry recording the framework-agnostic shift.

**Phase 7 — Final dogfood.** Scaffold a fresh instance from rc4. Run release gates inside it. Simulate outdated instance (remove a recommended block); confirm drift alert fires. Run upgrade skill; confirm reconciliation. Final cold-read subagent reviews the rc4 changeset for inconsistencies, hardcoded paths, circular dependencies, backwards-compatibility gaps.

The shape that fell out: ACW now treats every "what files matter" list the same way — single source of truth in `acw-state.yaml`, additive maintenance by the bookend skill, removal by ritual, lint as the safety net. The bookend skills are portable; instances upgrade themselves with a one-line alert and a one-skill walkthrough.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Pending` — removed "Framework-agnostic bookend skills..." item; satisfied by Session 4 Done block.
- `tasks-status.md::Pending` — removed "Decide: ship tools/scaffold-instance.py under emergency clause..." item; decided in rc1 as D-003.
- `tasks-status.md::Pending` — reworded the "Promote v0.2.0-rc1 to v0.2.0" item to reflect the actual current state (multiple rcN have shipped; promotion is now to v0.2.0 final after a clean-soak window).
- `tasks-status.md::Pending` — added "Dogfood /upgrade-instance against an actually-outdated downstream instance" so the upgrade loop earns its build through real friction, not just simulated friction.
- `tasks-status.md::Pending` — added "Push branch to origin/master" since the rc4 work is committed locally only.

**Proposed for operator review** (not executed):
- *(none)* — no items needed operator confirmation this pass. The cleanups above were all unambiguous.

**Skipped** (intentionally not touched):
- `build-log.md` past entries — append-only history.
- `incidents.jsonl` — append-only ledger; rc4 had no new incidents (subagent verification protocol caught issues before commit, which is the protocol working as designed).
- `research/sessions/` past captures — frozen once written.
- `decisions/decision-log.md::section_conventions.decisions` past entries — append-only spirit.
- `tasks-status.md::Done` past dated entries — history.
- `paths.research_queries_dir` — empty; nothing to consume.

**Prompts consumed this session:** *(none — `paths.research_queries_dir` is empty.)*

The session was clean. No drift surfaced beyond the satisfied/stale Pending items above. No new incidents. Subagent verifications at four phase boundaries plus a final cold-read all surfaced fixable issues that landed before commit, exactly as the protocol intends.

## 2026-04-30 — RC3: ACW as instance of itself; manifest-discipline rule extracted

Resolved two configuration gaps surfaced in the prior dogfood (OQ-001 missing `project:` block, OQ-002 manifest-classification step not wired into Phase 2). Operator pressed on the framing — "doesn't the fact that ACW exists in 3 layers prove it is in fact an instance with a template layer and a meta layer?" — and that reframe locked D-ACW-006.

Shipped:

- **`project:` block** in `acw-state.yaml` (`name: ACW`, `code: ACW`, `domain: meta-template`). D-ACW-006. Reframes ACW as an instance of itself. Existing legacy ids `D-001..D-005` stay unprefixed; new entries use `D-ACW-NNN`. The skill suite now runs on ACW.
- **`rules/manifest-discipline.md`** (template_layer) — generic pattern documentation extracted from LAYERS.md. D-ACW-007. Covers when the rule applies, the three-layer model, manifest mechanics, why-default-to-instance, operator quick-reference, recurring-pattern naming, recursive-instances note.
- **`LAYERS.md`** trimmed to ACW-specific narrative (meta_layer): exact files in each ACW layer, why ACW landed here, rcN changelog. Points at the new generic rule.
- **`skills/capture-and-metabolize/SKILL.md`** — Configuration section documents all fields as optional with defaults; Phase 2 gained the conditional manifest-classification step.
- **Version bumped** to `0.2.0-rc3`.

First real dogfood of `capture-and-metabolize` ran cleanly on the sandbox: Phase 1 produced this session's capture file, Phase 2 wrote D-ACW-006/007 plus this build-log entry plus a tasks-status Session 3 block plus an evolution entry, Phase 3 metabolize swept the empty queries directory and reported nothing else stale, Phase 4 correctly skipped (`synapse_log_path: null`), Phase 5 prompted for research-prompt build and exited cleanly when no operator was present. Then operator instructed to fire the same skill in ACW directly — this entry is the result.

## 2026-04-30 — Three-layer manifest

Followed the v0.2.0-rc1 absorption pass with the manifest discipline that makes the template-vs-instance split explicit. Without a manifest, the classification lived as five hardcoded lists inside `tools/scaffold-instance.py`; every new propagatable file required a paired script edit, and a forgotten edit silently broke instances scaffolded thereafter.

Shipped:

- **Three blocks in `acw-state.yaml`** — `template_layer` (verbatim copies), `instance_layer` (templated initial form, per-file `path` + `template` declaration), `meta_layer` (about-ACW only, never propagated). Plus `empty_dirs` for `.gitkeep` initialization.
- **Refactored `tools/scaffold-instance.py`** — reads the manifest, stdlib-only mini-yaml parser. The hardcoded `VERBATIM_FILES` / `VERBATIM_RULES` / `TEMPLATED_FILES` constants are gone. Skips `__pycache__/` and `.pyc` files when copying directories.
- **`tools/templates/README.md.tmpl`** — instances now ship with an operator-facing README explaining what the workspace is and the first-session checklist.
- **`LAYERS.md`** (meta_layer) — explainer document with the three-bucket table, the why, the how, and the operator quick-reference. Names manifest-discipline as a recurring pattern (third application in ACW after `auto_load_at_session_start` and the canon governance state machine).
- **D-005 in the decision log** — records the architectural choice and the default-to-instance discipline.
- **Release gate added** — every file at root, `rules/`, `tools/`, `skills/` must be classified in one of the three layers.

Verification: scaffolded a fresh instance to `/tmp/acw-scaffold-v2`, confirmed it renders correctly, passes its own lint and test suite, and excludes meta_layer files (no `LINEAGE.md`, `AUTHOR.md`, `LAYERS.md`, etc. in the scaffolded output).

## 2026-04-30 — v0.2.0-rc1: gsg-copilot extensions absorbed

First absorption pass from the first ACW instance (`gsg-copilot`). Three weeks of single-operator lived experience surfaced nine candidate primitives (C-01 through C-09) and two staleness incidents (D-01 synapse-rule-sync, D-02 instance-bootstrap).

Shipped this session:

- **`tools/scaffold-instance.py`** — closes the bootstrap gap. Stdlib-only, ~200 lines, refuses to clobber, supports `--dry-run`. Templates live in `tools/templates/`.
- **`rules/task-tracking.md`** — codifies the three-section `tasks-status.md` model (Pending / Done / Parked) with dated session blocks under Done and pinned-marker convention at the top of Pending. Promoted from C-01.
- **`rules/incident-tracking.md`** — codifies the incident schema, severity ladder, and category vocabulary. Documents `incidents.jsonl` as default-on substrate that does not earn its build.
- **`tools/log-incident.py`** — gained `--category` flag with the seven-value enum from C-09.
- **`tasks-status.md` and `build-log.md`** — added at repo root and to `canonical_runtime_files` per C-01/C-02.
- **`acw-state.yaml::auto_load_at_session_start`** — new array per C-06. Names the canonical file list any agent host should pull at session start.
- **`AGENTS.md` directive 7** — declares the auto-load convention as the cross-vendor contract. Host-specific entry files implement via native syntax.
- **`skills/capture-and-metabolize/` and `skills/resume-session/`** — bookend skill pair ported from gsg-copilot. Adapted to read project code, synapse log path, voice references, and cross-repo writes from `acw-state.yaml`. Replaces `skills/capture-session/`.

Deferred:

- C-04 synthesis-cycle (only one cycle of evidence). Will revisit after second instance or third cycle.
- C-05 runbooks layer, C-07 vault-boundary as hard rule, C-08 backlog triple-tag — operator-preference-flavored. Documented as recommendations, not normative.

Version bumped: `0.1.0` → `0.2.0-rc1`. Tag earns promotion to `0.2.0` after release-gate verification.
