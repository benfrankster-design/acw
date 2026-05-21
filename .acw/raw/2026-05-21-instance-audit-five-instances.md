---
class: raw
authority: instance
stability: in-progress
date: 2026-05-21
type: instance-audit-report
operator: Ben Frank
covers:
  - cs-ops-spec
  - cs-atlas
  - _command
  - cs-copilot
  - frank-context
---

# Instance audit — five-instance state report (2026-05-21)

Pre-upgrade audit for the five downstream instances queued for `/acw-instance upgrade` to canonical v0.10.0. Audit is read-only; the per-instance upgrade plan emerges from this report.

## Summary table

| Instance | Current state | Migration path to v0.10.0 | Notes |
|---|---|---|---|
| **cs-ops-spec** | Manual v0.10.0 migration committed (commit `f89ec44`); no remote | No-op or skip — already at v0.10.0 shape | Re-audit confirms shape; declare profile=spec-project explicitly via update_acw_state if not declared |
| **cs-atlas** | Pre-ACW (no acw-state.yaml); v0.10.0 substrate migration done manually (committed in initial commit) | `pre-acw-to-0.10.0.yaml` bootstrap, OR mark as already-migrated | Pushed locally only; Robert's Bitbucket invite pending |
| **_command** | ACW v0.9.7, single-file decisions, substrate at root, tasks-status-2026-Q2.md grandfathered | Chain: 0.9.7 → 0.9.9 (manifest TBD) → 0.10.0 | Tasks-status grandfathered shape needs v0.9.5 folder migration too; v0.9.7 → v0.9.9 manifests don't exist yet |
| **cs-copilot** | Pre-ACW (no acw-state.yaml); single-file decisions/decision-log.md; substantial code | `pre-acw-to-0.10.0.yaml` bootstrap with profile=coding-project | Has backend/, widget/, pipeline/, tests/ — code stays at root |
| **frank-context** | ACW v0.1.0 instance / last_reconciled v0.9.9; wiki shape; substrate at root | `0.9.9-to-0.10.0.yaml` direct | Cleanest of the five — already wiki shape, just needs .acw/ relocation |

## Per-instance detail

### cs-ops-spec

- **Status:** done. Manual v0.10.0 migration committed as `f89ec44` (109 file changes including substrate relocation to .acw/, _buffer → raw rename, OQ resolutions, D-COPS-035 + C-COPS-001 + OQ-COPS-019 entries).
- **Remaining work:** verify `.acw/acw-state.yaml::profile` is set to `spec-project` and `modules:` block is present. If missing, add via `/acw-session start` followed by a manual edit. Should be small no-op patch.
- **Remote:** none. Operator decision pending whether to push to GitHub/Bitbucket.

### cs-atlas

- **Status:** v0.10.0 substrate migration done manually (initial commit `099e57a` on master).
- **Remaining work:** add `.acw/acw-state.yaml` from scratch with operator-supplied profile=coding-project and the canonical paths block. The cs-atlas pre-ACW state had no acw-state.yaml; the bootstrap step is needed.
- **Migration manifest applicable:** `pre-acw-to-0.10.0.yaml` (skip steps 3, 4, 5 since substrate already relocated).
- **Remote:** none added yet — waiting on Robert's Bitbucket grant for `gsg-cs-atlas`.

### _command

- **Status:** ACW-registered at v0.9.7. Substrate at workspace root (decisions/, glossary/, sessions/, _buffer/, etc.). Has tasks-status-2026-Q2.md at root (pre-v0.9.5 grandfathered shape).
- **Migration chain:**
  1. **v0.9.7 → v0.9.8** — wiki migration if not already done. Audit suggests single-file decision-log present; needs `migrate_to_wiki.py`.
  2. **v0.9.8 → v0.9.9** — drift short-circuit + buffer sweep + synced_to frontmatter. No manifest authored yet — config-only changes, may not need a manifest.
  3. **v0.9.5+ archive folder migration** — move `tasks-status-2026-Q2.md` from workspace root to `archives/tasks-status/2026-Q2.md` per the canonical archive folder shape.
  4. **v0.9.9 → v0.10.0** — apply `0.9.9-to-0.10.0.yaml` (already authored).
- **Required new manifests:** `0.9.7-to-0.9.8.yaml` (wiki migration). The skill currently has the v0.9.8 wiki migration logic embedded — this manifest authoring is the architectural correction (move it to data).
- **Profile:** `org-brain` (operator cockpit; entire personal-AI workspace).

### cs-copilot

- **Status:** pre-ACW. No `acw-state.yaml`. Has substrate-shaped patterns (decisions/decision-log.md single-file, glossary.md, incidents.jsonl, tasks-status.md, threat-model.md, _buffer/). Has substantial Python code (backend/, widget/, pipeline/, eval/, tests/) and data (catalogs/).
- **Migration manifest applicable:** `pre-acw-to-0.10.0.yaml` (full bootstrap).
- **Operator prompts at upgrade time:**
  - project_code: `CCP` or `COPILOT`
  - project_name: `cs-copilot`
  - domain: "CS agent copilot for GSG Zoho Desk"
  - profile: `coding-project`
  - has_single_file_decisions: `true` (decisions/decision-log.md exists)
- **Code dirs to leave untouched:** backend/, widget/, pipeline/, eval/, tests/, catalogs/, examples/, requirements.txt, Dockerfile, README.md.
- **Wiki migration:** required for decisions/decision-log.md (run `tools/migrate_to_wiki.py` before relocation per the manifest's step 2).

### frank-context

- **Status:** ACW v0.1.0 instance / last_reconciled v0.9.9. Already in wiki shape (decisions/entries/, decisions/INDEX.md, decisions/constraints/, decisions/open-questions/, glossary/). Substrate at workspace root (not yet .acw/).
- **Migration manifest applicable:** `0.9.9-to-0.10.0.yaml` directly.
- **Profile:** `spec-project` (consultancy substrate work).
- **Cleanest of the five** — no special cases. Substrate is already wiki, just needs relocation to .acw/.

## Recommended execution order

Sequencing minimizes risk by going easy-to-hard:

1. **frank-context** — clean 0.9.9 → 0.10.0. Dogfoods the `0.9.9-to-0.10.0.yaml` manifest. If issues surface, they're caught on the simplest target.
2. **cs-ops-spec** — verify shape, add profile/modules to acw-state.yaml if missing. Mostly confirmatory.
3. **cs-atlas** — add acw-state.yaml via bootstrap manifest (skipping already-done relocation steps). Or hand-author the acw-state.yaml directly; substrate is already in place.
4. **_command** — most complex; runs wiki migration + v0.9.5 archive folder + v0.10.0 dotfolder. Longest plan. Save for last so the executor work in items 1–3 catches gaps before _command runs.
5. **cs-copilot** — full pre-acw bootstrap. Most steps; defer until executor verified through items 1–4.

## Blockers and gaps

- **`/acw-instance upgrade` executor verification deferred to next session.** The skill's `upgrade.md` was patched today with the manifest-execution section, but the actual code paths for manifest-driven steps (`update_acw_state` parameters, `remove_gitignore_rule`, `only_if` conditional, `optional: true` on git_mv moves) need dry-run testing before any real instance upgrade fires.
- **Hooks referenced by manifests not yet authored:** `tools/migration-hooks/v0.9.3-archive-done-section.py`, `v0.9.3-handle-parked-section.py`, `v0.9.3-rewrite-pending-only.py`, `bootstrap-empty-dirs.py`. Each is 50-100 lines of straightforward Python. Earned when their manifest first runs against a real instance.
- **`0.9.7-to-0.9.8.yaml` manifest not yet authored.** Required for _command's wiki migration step in the chain. Lift the existing skill prose (lines 176-191 of `references/upgrade.md`) into a declarative manifest.

## Audit verdict

Three of five instances (cs-ops-spec, cs-atlas, frank-context) are ready for `/acw-instance upgrade` execution after the executor verification dry-run. Two (_command, cs-copilot) need intermediate manifest authoring (_command) or substantial bootstrap (cs-copilot) plus the same executor verification.

Net assessment: the multi-instance upgrade is not safe to one-shot. Sequential execution with operator-at-keyboard per instance is the correct posture. The approval gates built into `/acw-instance upgrade` exist for exactly this reason.
