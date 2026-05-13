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
