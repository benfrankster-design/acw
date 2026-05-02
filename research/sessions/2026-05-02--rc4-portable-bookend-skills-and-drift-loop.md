---
date: 2026-05-02
participants: [ben, claude]
topic: rc4 portable bookend skills and drift loop
decisions_made: [D-ACW-008, D-ACW-009, D-ACW-010]
conceptual_shifts: yes
linked_files:
  - acw-state.yaml
  - CLAUDE.md
  - CHANGELOG.md
  - rules/manifest-discipline.md
  - rules/instance-current-manifest.md
  - tools/manifest.py
  - tests/test_manifest.py
  - skills/capture-and-metabolize/SKILL.md
  - skills/capture-and-metabolize/gotchas.md
  - skills/capture-and-metabolize/references/distribution-rules.md
  - skills/capture-and-metabolize/references/metabolize-rules.md
  - skills/capture-and-metabolize/references/metabolize-report-format.md
  - skills/capture-and-metabolize/references/research-prompt-format.md
  - skills/capture-and-metabolize/references/session-capture-format.md
  - skills/capture-and-metabolize/references/incidents-format.md
  - skills/capture-and-metabolize/references/synapse-log-format.md
  - skills/capture-and-metabolize/references/sub-step-discipline.md
  - skills/capture-and-metabolize/references/transcript-cleaning-rules.md
  - skills/resume-session/SKILL.md
  - skills/resume-session/gotchas.md
  - skills/upgrade-instance/SKILL.md
  - skills/upgrade-instance/gotchas.md
  - decisions/decision-log.md
  - tasks-status.md
  - build-log.md
  - research/evolution.md
  - tools/templates/acw-state.yaml.tmpl
  - tools/templates/decision-log.md.tmpl
  - tools/templates/tasks-status.md.tmpl
  - tools/templates/evolution.md.tmpl
duration_minutes: ~180
---

# Session — RC4: Portable Bookend Skills + Drift Loop

## 1. Topic & Goal

Make the bookend skills (`/capture-and-metabolize`, `/resume-session`) framework-agnostic, runtime-agnostic, modular, and decoupled — so the logic applies regardless of the host environment and reuses across any ACW-derived workspace without ties to specific file paths or the current local context. Add drift detection so existing instances can learn they're behind when ACW evolves, plus an `/upgrade-instance` skill that walks operators through reconciliation. Ship the work with maximum reliability per operator's "money is not a problem; no missteps, no hallucinations" directive — execute in atomic phases with subagent verification at each gate.

Started by adding ACW's own `CLAUDE.md` (host-specific implementation of `AGENTS.md` directive 7) since ACW is now formally an instance of itself per rc3's D-ACW-006. Then scoped the framework-agnostic skill work as a 7-phase plan; operator confirmed scope and decision points; executed.

## 2. What was decided

- **D-ACW-008 — Paths block + manifest-tooling spec.** `acw-state.yaml::paths` declares every substrate file path; bookend skills read at runtime with fallback to canonical defaults documented in `rules/manifest-discipline.md`. Four-operation manifest-tooling spec (load, append, contains, validate) ships in the same rule. Stdlib-only Python reference implementation in `tools/manifest.py`. Section heading conventions move to per-file frontmatter via `section_conventions:` key.
- **D-ACW-009 — Drift detection via instance-current-manifest.** New file `rules/instance-current-manifest.md` declares the recommended-blocks registry (project, paths, auto-load list, three layers, empty_dirs, cross_repo_writes, synapse_log_path, voice). Each entry: what / why / required / how-to-add / earned-in. `/resume-session` Step 5 compares each entry's earned-in version against `acw-state.yaml::last_reconciled_version` and surfaces a one-line alert on gaps. Required adding `last_reconciled_version` (semantic version) alongside the existing `last_reconciled` (date) field — subagent caught the conflation during Phase 4 verification.
- **D-ACW-010 — `/upgrade-instance` skill closes the drift loop.** New skill walks operators through gap reconciliation. Pure additive: no demotions, no removals, no shape repair. Bumps `last_reconciled_version` after the pass; logs a decision-log entry. Subagent stress test caught two edge cases (partial blocks treated as deliberate operator choice; malformed blocks halt the pass).

Operator directive that shaped execution mode: *"money is not a problem. i want this done right. no misteps. no hallucinations."* (turn 84). The protocol that fell out: plan-first / read-before-edit / TDD where applicable / spec-first declarative work / phase boundaries are verification gates / subagent verification at key checkpoints / dogfood at end / atomic commit per phase.

Decision points locked at scope-confirmation:
- Section heading frontmatter shape: dedicated YAML key per heading (option A).
- Drift check timing: every `/resume-session` run; suppress when `last_reconciled_version` matches current ACW (option A).
- `/upgrade-instance` lives at `skills/upgrade-instance/` (option A).
- Atomic commits per phase.
- Subagent verification at end of Phase 2, 3, 4, 5, 7.

## 3. What changed in the conception

**Bookend skills decoupled from ACW; manifest-discipline pattern reaches its fourth case.**

The bookend skills used to hardcode ACW's directory layout. That worked for ACW but broke portability: any ACW-derived workspace that wanted to restructure substrate, or any future template evolution that moved a substrate file, would force grep-and-replace across every skill. RC4 replaces the hardcoded paths with a `paths.X` shorthand that resolves at runtime from `acw-state.yaml::paths` (with fallback to canonical defaults). The skills now ship in the template and run in any instance regardless of where it puts its files.

Manifest-discipline (single source of truth in `acw-state.yaml`, additive maintenance by skill, removal by ritual, lint as the safety net) reached its fourth concrete case in this session: auto-load list (rc1), three-layer manifest (rc2), vocabulary canon (existing), and now `paths` (rc4). Operator chose to ship the shared manifest tooling at this fourth case — `tools/manifest.py` becomes the load-bearing helper any consumer can import instead of reinventing the load/validate/append logic.

The drift-detection + upgrade-skill pair completes a previously-missing arc: ACW evolves, instances learn they're behind, instances reconcile. Without this loop, downstream workspaces would silently rot relative to ACW's evolution. With it, drift is visible at session start and fixable through one skill invocation.

Linked entry added to `research/evolution.md`: "2026-05-02 — Bookend skills decoupled from ACW; drift detection earns its build."

## 4. What was built / changed

**Source-file edits (template_layer):**
- `acw-state.yaml`: paths block (14 keys), `last_reconciled_version` field, `tools/manifest.py` and `skills/upgrade-instance/` added to template_layer, `rules/instance-current-manifest.md` added to template_layer + auto_load_at_session_start. Version bumped `0.2.0-rc3` → `0.2.0-rc4`.
- `rules/manifest-discipline.md`: gained "Canonical default paths" section (14-entry fallback table) and "Manifest tooling spec" section (four-operation contract + schema reference for all 8 known blocks including `project`).
- `rules/instance-current-manifest.md` (new): declarative recommended-blocks registry. 9 entries covering project, paths, auto-load list, three manifest layers, empty_dirs, cross_repo_writes, synapse_log_path, voice.
- `tools/manifest.py` (new): stdlib-only reference implementation. ~330 lines, 33 dedicated unit tests in `tests/test_manifest.py`. KNOWN_LISTS, KNOWN_DICTS (paths + project), UNSUPPORTED (instance_layer), CANONICAL_DEFAULTS for paths.
- `tests/test_manifest.py` (new): 33 tests in initial commit, 4 added later for project block; total 46 tests in the suite.
- `skills/capture-and-metabolize/`: SKILL.md + gotchas.md + 9 reference files refactored. Every path now expressed as `paths.X` shorthand. Section conventions read from per-file frontmatter. Project-specific references (gsg-copilot, synapse, Cortex, HR-CP-NNN) generalized to be portable.
- `skills/resume-session/`: SKILL.md gained Step 5 drift check. gotchas.md updated with the same path-resolution preamble.
- `skills/upgrade-instance/` (new directory): SKILL.md walking operator through gap reconciliation; gotchas.md covering version-vs-date semantics, partial-block honoring, malformed-block halt, mid-pass abort safety.

**Substrate updates (instance_layer):**
- `decisions/decision-log.md`: D-ACW-008/009/010 entries.
- `tasks-status.md`: Session 4 dated block under Done; `section_conventions` frontmatter added.
- `build-log.md`: comprehensive rc4 narrative entry covering all seven phases.
- `research/evolution.md`: entry recording the framework-agnostic shift; `section_conventions` frontmatter added.
- `CHANGELOG.md`: full [0.2.0-rc4] entry plus retroactive [0.2.0-rc3] entry that was missing.
- `CLAUDE.md` (new): ACW's host-specific implementation of `AGENTS.md` directive 7. Principle-anchored and pointer-heavy.
- `tools/templates/acw-state.yaml.tmpl`, `decision-log.md.tmpl`, `tasks-status.md.tmpl`, `evolution.md.tmpl`: updated to ship rc4 frontmatter and the `last_reconciled_version` field.

**Verification artifacts:**
- All 46 unit tests passing.
- Vocabulary lint clean.
- Drift check (deferred-library) clean.
- Fresh scaffold to `/tmp/acw-rc4-final` passes its own gates with all rc4 features present.
- Drift simulation against a hypothetical pre-rc4 instance produces expected gap list.

**Subagent verifications:**
- Phase 2: confirmed spec/impl alignment of `tools/manifest.py` against `rules/manifest-discipline.md`.
- Phase 3: confirmed zero hardcoded substrate paths in skill content.
- Phase 4: caught version-vs-date conflation in v1 drift check; fix shipped.
- Phase 5: caught partial-block and malformed-block edge cases in `/upgrade-instance`; fixes shipped.
- Phase 7 (cold-read on full rc4 changeset): caught two criticals (`project` not in KNOWN_DICTS so `/upgrade-instance` would crash adding the project block; `auto_load_at_session_start` canonical default in registry was stale at 5 entries instead of 7) plus four concerns. All fixed before final commit `2d878f5`.

**Commits:**
- `62ba6be` — Phase 1: paths block + manifest-tooling spec
- `dd8c8da` — Phase 2: TDD tools/manifest.py + tests
- `3c1cac8` — Phase 3: bookend skills read paths from manifest
- `9374ccb` — Phase 4: drift detection — instance-current-manifest + resume-session
- `0070938` — Phase 5: /upgrade-instance skill
- `a478516` — Phase 6: substrate updates + CLAUDE.md auto-load
- `2d878f5` — Phase 7 fixes: cold-read subagent fixes (project block + canonical defaults)

## 5. Open questions left — structured

*(None — session closed cleanly.)*

The session was execution-heavy, not design-heavy. Every architectural fork had a decision-point gate before execution, and operator confirmed each. Subagent verification surfaced four real ambiguities mid-flight; each was resolved with a fix that landed in its phase commit. No design questions are pending Track A research.

OQ-ACW-004 (manifest-tooling timing) from the prior session was answered by D-ACW-008 — operator chose to ship the shared tooling at the fourth case rather than continue waiting. Resolution noted in D-ACW-008's rationale.

OQ-ACW-005 (published-README structure for scaffold-only vs template-evolving consumers) from the prior session is still unresolved but is not Phase-5-actionable yet — it's deferred until ACW publishes to GitHub publicly, which has no current timeline.

## 6. Operator directives (verbatim)

> "lets do all now. what is the best way to make sure this all gets done 100% without error? money is not a problem. i want this done right. no misteps. no hallucinations." (turn 84) — established quality-first execution mode for the entire rc4 build; drove the protocol of plan-first / read-before-edit / TDD / spec-first / phase-boundary verification gates / subagent checkpoints / dogfood / atomic commits.

> "1. a. 2. a. 3. a. 4. atomic. 5. That's fine." (turn 88) — confirmed the four decision points (section heading frontmatter shape, drift check timing, /upgrade-instance location, commit cadence) plus subagent verification budget at end of Phases 2, 3, 4, 5, 7.

> "go" (turn 90) — authorized execution from Phase 1.

> "Great. put in synapse" (turn 102) — directed the rc4 session block to be appended to the operator's cross-project synapse log; left `acw-state.yaml::synapse_log_path` null (operator's `/log-session` skill owns synapse format; bookend skill stays out).

> "probably not necessarry when running bookend skill. lets run capture-and-metabolize now." (turn 104) — confirmed `synapse_log_path: null` is the right default for ACW; triggered this capture-and-metabolize run.

## 7. Cleaned transcript excerpt

*(Skipped — operator directives in §6 carry the load-bearing wording; the build itself is exhaustively documented in `build-log.md::2026-05-02 — RC4`.)*
