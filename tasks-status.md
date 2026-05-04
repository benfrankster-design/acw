---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
section_conventions:
  pending: "Pending"
  done: "Done"
  parked: "Parked"
---

# Tasks Status — ACW

Three-section task tracker. See `rules/task-tracking.md` for format and discipline. Done section uses a rolling window — Sessions ≥ N-2 stay inline; older sessions archive to `tasks-status-YYYY-Q.md` (see `tasks-status-2026-Q2.md` for Sessions 1–11).

## Pending

- [ ] Dogfood `/acw-instance audit` against cs-copilot using v0.7.0+ plan-based behavior (substrate-shaped, below organic threshold; should adopt cleanly with one-shot migration plan).
- [ ] Dogfood `/acw-instance upgrade` against gsg-copilot using v0.7.0+ plan-based behavior (older registered instance; should fetch canonical and walk through any drift gaps; the v0.5.0 `_inbox/` → `_buffer/` migration step should fold into the plan; v0.9.0 auto-load discipline check fires).
- [ ] Decide: formal retirement of adopt-mode hard-stop (D-ACW-022) — structurally redundant after v0.7.0 plan-approval gate. Schema retained for backward compat; needs a decision-log entry to formally retire.
- [ ] Decide: add `--save-plan <path>` flag to `/acw-instance audit` for plan persistence between audit and upgrade runs. Earned when substrate-race incidents make deterministic regen unsafe.
- [ ] Decide: add checksum/content-hash verification to `/acw-instance upgrade`'s "verify before delete" step (currently documented but not mechanically enforced). Earned when a content-loss incident occurs.
- [ ] Sync `~/synapse/Rules/Procedures/` copies with ACW canonical (mitigation for D-01). Particularly `skill-format.md` since ACW canonical now has the corrected version.
- [ ] Decide: should `tools/scaffold-instance.py` optionally create user-level skill junctions at scaffold time? (OQ-ACW-006 from Session 5.)
- [ ] Decide: extract the host entry file generation logic from `tools/scaffold-instance.py` into `tools/templates/` for single source of truth.
- [ ] Decide: defer C-04 synthesis-cycle to `DEFERRED.md` or ship now.
- [ ] Add cross-instance write trigger to `DEFERRED.md` for capability broker — three documented cross-instance write incidents earn the broker its ship at lattice scale.
- [ ] Add lint gate (in `release_gates`) for command-routed skills: every command in the table has a matching `references/<command>.md`; reference files don't redeclare the spine. Earned when first violation surfaces.
- [ ] Promote `v0.9.0` to `v1.0.0` after a soak window once lattice-level dogfooding has accumulated evidence. Per operator directive 2026-05-04: nothing new ships before 1.0.0 — v0.9.0 is the last pre-promotion substantive ship.

## Done

### 2026-05-04 — v0.9.0: auto-load discipline + tasks-status archive (Session 14)

- D-ACW-038 records the bundle. Auto-load bloat incident logged: `auto_load_at_session_start` carrying 8 entries (~83k context) at session start, with 4 entries failing the earn-by-incident gate.
- **`rules/auto-load-discipline.md`** (new template_layer rule): codifies earn-by-incident applied to auto-load. Each entry MUST declare a structured claim (or be `legacy-pending-review` transitional). Canonical recommendations list the four files ACW recommends with stated claims; declared demotion candidates name what fails the gate and why.
- **`tools/manifest.py`** extended: `STRUCTURED_LISTS = {"auto_load_at_session_start"}`. Parser handles dict-shaped entries (`- path: ... / claim: ... / earned_by: ...`); `load()` returns paths only (legacy backward compat); `load_structured()` returns full dict per entry; `validate()` enforces no duplicate paths in structured form. 8 new unit tests; all 54 tests pass.
- **`acw-state.yaml::auto_load_at_session_start`** migrated to structured form with 4 demotions: `rules/manifest-discipline.md`, `rules/instance-current-manifest.md`, `rules/multi-instance-topology.md`, `incidents.jsonl` removed (each consumer-skill loads them directly). 4 entries kept with structured claims: decision log, hard rules, tasks-status, glossary.
- **`tools/templates/acw-state.yaml.tmpl`** updated: scaffolded instances inherit the lean 4-entry default in structured form.
- **`CLAUDE.md`** updated: `@`-imports synced to the lean 4 entries; "Other substrate is read on demand" section names the demoted files and their consumer-skills.
- **`/acw-instance audit`** reference gained "Auto-load discipline" section: walks `auto_load_at_session_start`, classifies entries (KEEP / DEMOTE / REVIEW / MIGRATE-TO-STRUCTURED), proposes plan rows.
- **`/acw-instance upgrade`** reference gained auto-load demotion execution under existing single approval gate; v0.9.0 migration prompt for instances inheriting bloated lists.
- **`rules/instance-current-manifest.md`** updated: existing `auto_load_at_session_start` entry rewritten to reference the structured form and the discipline rule; new earned-in-0.9.0 entry for `rules/auto-load-discipline.md`.
- **`tasks-status.md`** Done section trimmed: Sessions 1–11 archived to `tasks-status-2026-Q2.md` (meta_layer). Sessions 12–14 stay inline. `rules/task-tracking.md` updated with rolling-window discipline (sessions ≥ N-2 inline; older quarters archived).
- **Auto-load context savings:** ~30k off session-load (manifest-discipline 5.2k + instance-current-manifest 11.5k + multi-instance-topology 5.2k + incidents.jsonl ~3k + tasks-status Done section ~7k), without losing anything load-bearing. Doctrine propagates to instances via `/acw-instance upgrade`; demotions propagate via the audit verb's per-instance walk.
- Bumped ACW version `0.8.0` → `0.9.0`. Bumped `last_reconciled_version` to `0.9.0`. Updated template baseline `last_reconciled_version` to `0.9.0`.
- Per operator directive: v0.9.0 is the final pre-1.0.0 substantive ship. v1.0.0 is the soak/promotion.

### 2026-05-04 — v0.8.0: bookend efficiency cluster — Haiku default, quick/full modes, /acw-session update, sessions/ at root, retire 4 superseded skills (Session 13)

- D-ACW-037 records the bundle. Cost-friction incident `a8e771f0-7686-484d-b89e-cc25e96f8c93` logged: operator hit halfway through Max-plan weekly budget after 2 days, with `/acw-session end` taking 7-10 minutes per invocation on Opus 4.7 1M context.
- **Bookend efficiency:**
  - `skills/acw-session/SKILL.md` declares `model: claude-haiku-4-5` in frontmatter. Phase steps requiring judgment (Phase 3 operator-confirm proposals, Phase 5 research-prompt construction, meta-layer trigger edits) escalate to Sonnet inline.
  - `references/end.md` adds Mode dispatch + Quick mode + Full mode sections; each phase tagged with mode behavior.
  - `/acw-session end` defaults to **quick mode** (Phase 1 capture + Phase 2 append-only subset + Phase 3 auto-update sweep). `/acw-session end full` runs all five phases. `--synapse` and `--research` flags surface those phases inside quick mode.
- **New verb `/acw-session update`:**
  - `references/update.md` ships as new file. Reads `<sessions_dir>/.current-session`; appends timestamped note under `## Updates` in active capture file. Self-bootstraps if no tracker exists. Haiku-grade end-to-end.
- **`.current-session` tracker:**
  - Single-line file at `<sessions_dir>/.current-session`. Written by `start`, read by `update`, cleared by `end`. SKILL.md documents the convention.
- **Sessions move to root:**
  - `paths.session_captures_dir` migrated `research/sessions` → `sessions`. `empty_dirs` swap. Existing 8 capture files moved via `git mv`. `rules/manifest-discipline.md` canonical-default-paths table updated.
- **Superseded skill cleanup:**
  - Deleted `skills/capture-session/`, `skills/capture-and-metabolize/`, `skills/resume-session/`, `skills/upgrade-instance/` from disk. Removed the four entries from `acw-state.yaml::meta_layer`. Closes the v0.4.0 Pending item that the careful guardrail blocked from automated removal.
- **Manifest registry:**
  - Three new earned-in-0.8.0 entries in `rules/instance-current-manifest.md`: `sessions/` at root, `.current-session` tracker, `model:` frontmatter for bookend skills.
- Bumped ACW version `0.7.0` → `0.8.0`. Bumped `last_reconciled_version` to `0.8.0`. Updated template baseline `last_reconciled_version` to `0.8.0`.
- Release gates green: vocab lint exit 0, drift check clean, 46/46 unit tests pass.
- `research/11-session-continuity-prior-art.md` (deep-research note from Session 12) recorded as meta_layer; cited in D-ACW-037 source.

### 2026-05-03 — v0.7.0: /acw-instance adopt-and-migrate rewrite + integrations scope refinement + _Command full migration dogfood (Session 12)

- Dogfooded `/acw-instance audit` against `_Command` (4/6 substrate signals, unregistered, organic substrate). Operator pushed back on v0.4.0/v0.5.0 interactive Mode B walk asking for one coherent migration plan instead of nine routing prompts. Earn-by-incident evidence for D-ACW-036.
- **Workstream B**: rewrote `skills/acw-instance/SKILL.md` + `references/audit.md` + `references/upgrade.md` to embody adopt-and-migrate mental model. Audit produces a per-file migration plan (source → canonical destination → action); upgrade executes under one approval gate. Substrate boundary made explicit: migration applies to recognized canonical paths plus substrate-shaped patterns; project code, data, configs, tests stay untouched. For coding projects: scaffolds substrate alongside untouched code. Action enum formalized: `move`, `reshape`, `merge`, `write-canonical`, `delete`, `leave-untouched`, `instance-specific`, `absorption-candidate`, `[?]`.
- **`integrations/<system>/` scope refined** to cover BOTH documentation AND integration-specific operational scripts that are tightly coupled to one external system (bulk-push tools, sync utilities, data extractors, auth helpers). Boundary with `tools/`: tools/ for general-purpose utilities; integrations/<system>/ for tooling that exists only because the integration exists. Earned by `_Command/integrations/zoho-desk/push_direct.py` finding. Updated `tools/templates/integrations-README.md.tmpl` and `rules/instance-current-manifest.md` § integrations entry.
- Bumped ACW version `0.6.1` → `0.7.0`. Bumped `last_reconciled_version`. No new manifest registry entries earned in v0.7.0; downstream instances at `last_reconciled_version` 0.6.1 stay drift-clean.
- D-ACW-036 records full rationale + 4 open follow-ups (plan persistence, hard-stop retirement, verify-before-delete enforcement, capability broker).
- Validated end-to-end against `_Command`: full migration via 8 parallel research subagents proposing routings + 1 reshape subagent. 18 file moves, 11 reshapes, 11 new canonical files, 9 source deletions. Pre-migration git commit at cb39d32 (operator's `_Command` was untracked; skill offered `git init` + initial commit before destructive operations). gitleaks pre-commit hook caught a SHA256 false-positive in `build-log.md:144` (binary verification hash, not API key) — mitigated via `.gitleaksignore` fingerprint.

*(Sessions 1–11 archived to `tasks-status-2026-Q2.md`.)*

## Parked

- C-04 synthesis-cycle: single cycle of evidence is too thin. Defer to DEFERRED.md or wait.
- C-05 runbooks layer: operator-preference-flavored. Document as recommended, not normative.
- C-07 vault-boundary as hard rule: include as suggested starting rule in instance-hard-rules template, not normative globally.
- C-08 backlog triple-tag: recommended convention only, not normative.
