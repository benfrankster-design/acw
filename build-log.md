---
class: archive
authority: derived
stability: stable
loaded_by_agent: no
---

# Build Log — ACW

Append-only, newest-first narrative of build progress per session.

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
