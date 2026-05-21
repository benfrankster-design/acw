---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
section_conventions:
  pending: "Pending"
---

# Tasks Status — ACW

Pending-only (v0.9.3+ canonical shape). See `rules/task-tracking.md` for format. Completed work archives on completion to `archives/tasks-status/YYYY-MM.md` (v0.9.5+ shape; pre-v0.9.5 archive grandfathered at `archives/tasks-status/2026-Q2.md`). Deferred-but-keep ideas route to `inbox/ideas/` (wiki-shaped) or earn a decision-log entry.

## Pending

> **Architectural reframe (2026-05-21).** Skill is a thin portable executor; canonical repo is the source of truth. Migration knowledge lives in canonical as declarative data files, not in skill prose. New version → new migration manifest in `migrations/`; skill picks it up without redistribution. See D-ACW-050 § "Deferred to v0.10.1+" and the reframed entries below.

- [ ] **v0.10.1 — Migration-manifest schema in canonical.** Author `rules/migration-manifest.md` defining the YAML schema for `migrations/*.yaml` files: `from_version`, `to_version`, `breaking`, `steps[]` (each step has `kind` + parameters). Document the step-kind enum: `create_dir`, `git_mv` (with moves list), `update_acw_state` (path prefix, rename keys, add fields), `rebuild_index`, `run_hook`, etc.
- [ ] **v0.10.1 — `migrations/0.9.9-to-0.10.0.yaml` in canonical.** Author the v0.10.0 migration as a declarative manifest. Steps: create `.acw/`, `git mv` all substrate dirs and files into `.acw/`, rename `.acw/_buffer → .acw/raw`, update `.acw/acw-state.yaml` (prefix all substrate paths with `.acw/`, rename `buffer_dir` → `raw_dir`, add `profile:` and `modules:` fields), rebuild `.acw/decisions/INDEX.md` and `.acw/glossary/INDEX.md`, bump `version` 0.9.9 → 0.10.0. This data file IS the migration; skill executes it generically.
- [ ] **v0.10.1 — `/acw-instance upgrade` executor verification.** Read the skill's current `references/upgrade.md` and verify the executor handles every step kind the v0.10.0 manifest uses. Patch any gaps. The skill remains a generic executor; it does not know v0.10.0 specifically. Goal: zero skill changes per future version bump — only new manifest files in canonical.
- [ ] **v0.10.1 — `/codemap` skill** wrapping Graphify CLI. Verbs: `rebuild`, `rebuild --ast-only`, `rebuild --semantic`, `status`, `audit`. Output routes to `.acw/codemap/GRAPH_REPORT.md` + sidecar JSON. Pre-commit hook integration for AST stage.
- [ ] **v0.10.1 — `/substrate-map` skill** rendering the implicit cross-reference graph as an on-demand markdown view. Walks frontmatter cross-refs across decisions, glossary, incidents, codemap; emits `.acw/substrate-map.md`. Optional confidence-tag coloring.
- [ ] **v0.10.1 — Skill audit pass.** Walk every existing skill (`/acw-session start | update | end`, `/acw-instance audit | upgrade`, `/metabolize` if shipped, scaffolder, validators) and verify substrate paths read from `acw-state.yaml::paths` rather than hardcoded `decisions/`, `sessions/`, etc. Patch any hardcodes. Same portability principle: skills read from canonical state, never embed it.
- [ ] **v0.10.x — `rules/` migration question** (OQ-COPS-019). Decide: keep `rules/` at root (recommendation, load-bearing for skill discovery) or move to `.acw/rules/` (consistency with the dotfolder convention). If the latter wins, it becomes its own migration manifest (`0.10.x-to-0.11.0.yaml`), not a skill code change.
- [ ] **v0.10.x — `tools/scaffold-instance.py`** updated to generate `.acw/` shape from scratch, ask operator for `profile:` during scaffold, write profile + modules into the new `.acw/acw-state.yaml`. Scaffolder is a separate concern from upgrade — generates fresh instances at current canonical shape, not a migrator.
- [ ] Dogfood `/acw-instance upgrade` against cs-copilot / gsg-copilot / _Command for v0.9.9 reconciliation (D-ACW-049). Upgrade should write `synced_to: "0.9.9"` to each instance's `rules/instance-current-manifest.md` frontmatter as part of the canonical-cache refresh step. Verify next `/acw-session start` after upgrade short-circuits cleanly (no full manifest read). Bundles with the v0.9.8 wiki-mode dogfood already pending below.
- [ ] Dogfood `/acw-instance upgrade` against cs-copilot / gsg-copilot / _Command for v0.9.8 wiki-mode canonical-only migration (D-ACW-048). All three are still single-file; the upgrade should detect legacy shape and emit mandatory `reshape` plan rows that run `tools/migrate_to_wiki.py` against the live log + every quarterly archive, then update `acw-state.yaml` to wiki-shape blocks. Verify the SessionStart hook reads the new `auto_load_at_session_start` correctly after migration.
- [ ] Resolve cs-copilot citation drift from v0.9.1 synapse trim — five files reference `~/.claude/rules/Procedures/{skill-format, capability-broker, decision-tracking}.md` paths that no longer exist post-trim. Doc-only citations, not load-bearing. Fix when cs-copilot is touched next.
- [ ] Dogfood `/acw-instance upgrade` against cs-copilot/gsg-copilot/_Command for v0.9.3 doctrine propagation: weekly rolling window for decision-log (single-file mode), tasks-status Pending-only migration, wiki-mode opt-in support, bookend mode-portability. Audit verb should walk decision-log and propose archive splits when the weekly or threshold cutoff fires; should detect three-section tasks-status and propose Pending-only migration as a plan row.
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
- [ ] Decide: MADR 4.0.0 frontmatter alignment vs ACW-flavored extension for wiki-mode decisions (D-ACW-043 follow-up). Earn when a multi-author instance hits friction.
- [ ] Decide: skill-side INDEX rendering as canonical tooling (replacing `tools/migrate_to_wiki.py` external invocation). Earn when second instance adopts wiki and operator hits regen friction.
- [ ] Decide: ship `.claude/agents/session-end-judgment.md` as ACW canonical alongside skills/ (host-portability). Earn when a non-Claude-Code host needs the same dispatch pattern.
- [ ] Promote `v0.9.x` to `v1.0.0` after a soak window once lattice-level dogfooding has accumulated evidence. Per operator directive 2026-05-04: nothing new ships before 1.0.0.
