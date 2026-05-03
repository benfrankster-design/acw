---
date: 2026-05-03
participants: [operator, agent]
topic: v0.5.1 front-door cleanup and v0.6.0 operator-centric cluster
decisions_made:
  - D-ACW-030
  - D-ACW-031
  - D-ACW-032
  - D-ACW-033
  - D-ACW-034
conceptual_shifts: yes
linked_files:
  - README.md
  - CHANGELOG.md
  - acw-state.yaml
  - tools/templates/acw-state.yaml.tmpl
  - tools/templates/context-goals.md.tmpl
  - tools/templates/context-objectives.md.tmpl
  - tools/templates/context-how-i-work.md.tmpl
  - tools/templates/context-key-people.md.tmpl
  - tools/manifest.py
  - rules/manifest-discipline.md
  - rules/instance-current-manifest.md
  - rules/task-tracking.md
  - skills/acw-instance/references/audit.md
  - skills/acw-instance/references/upgrade.md
  - skills/acw-session/references/end.md
  - context/goals.md
  - context/objectives.md
  - context/how-i-work.md
  - context/key-people.md
  - inbox/.gitkeep
  - CLAUDE.md
  - decisions/decision-log.md
  - tasks-status.md
  - build-log.md
duration_minutes: 90
---

# v0.5.1 front-door cleanup and v0.6.0 operator-centric cluster

## 1. Topic & Goal

Continuation arc immediately after v0.5.0 closed. Operator's question — *"when's the last time you read the README.md?"* — surfaced v0.1.0-era staleness at the front door. That triggered v0.5.1 (cleanup) and exposed a structural gap: substrate had Phase 2 distribution since v0.4.0; meta-layer had nothing, which is exactly why README went stale across four versions before someone noticed. v0.6.0 closes the gap with the meta-layer maintenance harness, plus ships the operator-centric substrate cluster (`context/`, `inbox/`, tasks-status framing) that had been queued.

Two coherent ships back-to-back. v0.5.1 is the immediate cleanup; v0.6.0 is the structural fix that should prevent recurrence.

## 2. What was decided

- **D-ACW-030** — Front-door cleanup. Retired `bootstrap/`, `migration/`, `LAYERS.md` in v0.5.1. Each had its function absorbed by current tooling: `bootstrap/` → `tools/scaffold-instance.py` + templated `research/01-problem-framing.md`; `migration/` → `/acw-instance audit` + `/acw-instance upgrade` adopt-mode; `LAYERS.md` content folded into `README.md` as "How ACW is layered" section. README rewritten end-to-end with prominent 60-second scaffold quickstart up front; current operator commands; current directory map (runbooks/, integrations/, briefings/, _buffer/); current load-bearing files. CHANGELOG backfilled for v0.3.0, v0.4.0, v0.5.0, v0.5.1.

- **D-ACW-031** — `context/` canonical for operator/project context layer. Four templated files: `goals.md` (long-arc), `objectives.md` (near-term focus), `how-i-work.md` (operator preferences), `key-people.md` (who matters). Read on demand, not auto-loaded. Distinct from decisions/rules/skills/glossary — fills the lightweight context gap. Especially load-bearing for cockpit-shaped instances; useful in any workspace type.

- **D-ACW-032** — `tasks-status.md` is workspace-purpose tracker, adapted per workspace type (cockpit = config + chief-of-staff ops; project = deliverables; full = org coordination). Operator-personal life tasks, calendar, and email explicitly stay external — accessed via MCP at query time, never mirrored to workspace substrate. The general rule: don't duplicate operator-accessible-on-phone surfaces; lean on briefings/ for snapshots when aggregation is wanted.

- **D-ACW-033** — `inbox/` canonical (no underscore) as operator capture surface. Distinct from `_buffer/` (system surface for cross-instance handoffs) and `briefings/` (agent-generated dated snapshots). Items get processed and removed: routed to `tasks-status::Pending`, parked, sent to external task app, or deleted. Three different surfaces, three different lifecycles.

- **D-ACW-034** — Meta-layer maintenance harness gated on `acw-state.yaml::meta_layer` block presence. `/acw-session end` Phase 2 walks per-file triggers (README on substrate-shape change, CHANGELOG on version bump, LINEAGE on new primitive, ORCHESTRATION on new methodology, SKEPTIC on med+ incident); `/acw-instance audit` flags stale meta-files; `/acw-instance upgrade` walks operator-confirmation per file. Consumer instances without the block pay no cost.

## 3. What changed in the conception

- **Symmetry between substrate and meta-layer is load-bearing.** Earlier framing assumed substrate maintenance via Phase 2 was sufficient; meta-layer was treated as static reference. The README staleness incident exposed the asymmetric-build gap. Now both have maintenance harnesses; the discipline is consistent.
- **"Don't duplicate operator-accessible-on-phone surfaces" is now an explicit rule, not an instinct.** Calendar, tasks, email all stay external. The chief-of-staff affordance lives in MCP-querying agents and briefing aggregations, not in cached substrate files. This generalizes — applies to any external system the operator already accesses elsewhere.
- **`context/`, `inbox/`, `briefings/`, `_buffer/`, `tasks-status.md` are five distinct surfaces.** Each has its own generator, lifecycle, and audience. The temptation to merge them (operator inbox = system inbox = briefings = tasks) was rejected explicitly. Mental model: surfaces differ by who writes (operator/agent/system), what lifecycle they have (untriaged/processed/snapshot/append-only), and who reads (operator/agent).
- **Earn-by-incident applies recursively.** v0.5.1 wasn't earned by a deferred primitive; it was earned by an *operator question* that exposed staleness. v0.6.0's harness is earned by the v0.5.1 incident. The discipline scales beyond the original "deferred library promotion" use case.

## 4. What was built / changed

**v0.5.1 (commit 8436a17):**
- Retired `bootstrap/README.md`, `migration/README.md`, `LAYERS.md`.
- `README.md` full refresh: 60-second scaffold quickstart, four-operator-commands table, current directory map, "How ACW is layered" section (LAYERS content absorbed), current load-bearing files.
- `CHANGELOG.md` backfilled for v0.3.0, v0.4.0, v0.5.0, v0.5.1.
- `acw-state.yaml::template_layer` removed `bootstrap/` and `migration/`; `meta_layer` removed `LAYERS.md`. Version bumped 0.5.0 → 0.5.1.

**v0.6.0 (commits cf68dba, fac5e72, 9c5a80b, 9d3c72f):**

*Operator-centric substrate cluster:*
- New `context/` directory with four templated files: `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`. Templates in `tools/templates/context-*.md.tmpl`. ACW's own `context/*.md` populated with current operating reality.
- New `inbox/` empty_dir for operator capture surface (`.gitkeep` marker).
- `acw-state.yaml::paths` keys for `context_dir` and `inbox_dir`. Mirrored in `rules/manifest-discipline.md` and `tools/manifest.py`.
- `rules/instance-current-manifest.md` two new registry entries (`context/`, `inbox/`).
- `rules/task-tracking.md` framing update — workspace-purpose vs operator-personal distinction; per-workspace-type table; explicit don't-duplicate-external-surfaces rule; relation to inbox/ (triage flow).

*Meta-layer maintenance harness:*
- `skills/acw-session/references/end.md` Phase 2 gained "Meta-layer maintenance" step with per-file trigger table.
- `skills/acw-instance/references/audit.md` Mode A extended with "Meta-layer staleness" check; report format extended.
- `skills/acw-instance/references/upgrade.md` gained "Resolve meta-layer staleness" step with operator-per-file confirmation prompts.
- All three gated on `acw-state.yaml::meta_layer` block presence.

*Housekeeping:*
- Version bumped 0.5.1 → 0.6.0. Template baseline `last_reconciled_version` to 0.6.0.
- Decision log entries D-ACW-030 through D-ACW-034 (five total across v0.5.1 + v0.6.0).
- `CHANGELOG.md` v0.6.0 entry per Keep a Changelog format.
- `CLAUDE.md` "Where things live" extended with `context/` and `inbox/` entries.
- `tasks-status.md` Pending cleared for the moment; carry-over deferred items moved to build-log metabolize report rather than cluttering Pending.

## 5. Open questions left — structured

#### OQ-ACW-010 — When does the meta-layer harness's first real test fire?

**Question:** The meta-layer maintenance harness shipped in v0.6.0 specifies trigger detection and operator-confirmation flow, but it hasn't actually run end-to-end yet (this session-end is the first invocation post-shipping). The harness's correctness depends on agents reading the spec and walking it correctly. v0.4.0's audit verb had a similar dependency and produced five bugs on first dogfood (D-ACW-026). Will the meta-layer harness produce similar bugs on its first real test?

**Candidates considered:**
- **Run and watch.** Trust the spec, fire the harness on next substantive session, document any bugs as a v0.6.1 patch following the same earn-by-incident pattern as v0.4.0 → v0.5.0.
- **Pre-emptive subagent stress test.** Spawn a subagent to read `skills/acw-session/references/end.md` Phase 2 meta-layer step and `skills/acw-instance/references/audit.md` Mode A meta-layer staleness step; have it produce a worked example walking through the spec; surface any ambiguities before the first real run.
- **Wait for organic dogfood.** Let v0.6.0 simmer; run audit against `_Command` after the meta_layer block is populated (currently `_Command` doesn't have one); document the harness's behavior empirically.

**Why unresolved:** Hasn't fired yet. v0.4.0's audit verb specs read fine on inspection but produced five bugs on first dogfood. The meta-layer harness might too. The right answer depends on whether the operator wants pre-emptive verification or earn-by-incident.

**Who needs to weigh in:** Operator decision before next substantive session, or accept earn-by-incident.

#### OQ-ACW-011 — Should the meta-layer harness's trigger table be data-driven or hardcoded?

**Question:** v0.6.0 ships the trigger table as hardcoded sensible defaults (README on substrate-shape change, CHANGELOG on version bump, etc.) embedded in the skill reference files. Per-instance trigger overrides are explicitly deferred to earn-by-incident. But if a workspace has meta-layer files with substantively different update conditions (e.g., a `BRAND.md` that should update on every customer-facing copy change), the operator has to either fork the skill or wait for the trigger registry to earn promotion.

**Candidates considered:**
- **Keep hardcoded** until 3+ documented cases of per-instance trigger needs surface. Earn-by-incident.
- **Add a `meta_layer_triggers:` block** to `acw-state.yaml` now that lets operators declare per-file triggers. Spec the format alongside the harness ship.
- **Move triggers into the meta-layer file frontmatter** itself (each meta-file declares its own trigger conditions). More distributed but more discoverable.

**Why unresolved:** No second case yet. v0.6.0 ships hardcoded; per-instance overrides deferred until evidence accumulates.

**Who needs to weigh in:** Operator after first non-ACW workspace populates a `meta_layer` block.

## 6. Operator directives (verbatim)

> "When's the last time you read the README.md?" (turn after v0.5.0 push)
> — The single question that exposed v0.1.0-era staleness at the front door. Set the v0.5.1 cleanup arc in motion.

> "Just as long as someone landing on repo doesn't have to hunt for a lifetime to figure out how to scaffold an instance." (turn ~3, v0.5.1 ship plan approval)
> — The constraint that drove the new README's "Scaffold a new instance (60 seconds)" quickstart up front.

> "I'm cool with all that, but I would just kind of push back at the layers.md because that's just more of a document for my own conceptualization. It's for the human reader, but if that belongs in the README.md instead of layers.md, I'm fine with that too." (turn ~5)
> — Reframed LAYERS.md as human-reader narrative; folding into README was the right consolidation.

> "Calendar, tasks, email all stay external. Don't duplicate." (paraphrased across v0.5.0 and v0.6.0 turns)
> — Codified consistently in v0.6.0. Same logic applied to all three operator-accessible-on-phone surfaces.

> "ship" (single word, turn directly after v0.5.1 ship report)
> — Approval for v0.6.0 scope queued at v0.5.1 close. Concise.

## 7. Cleaned transcript excerpt

Skipped — substantive content captured in §2-§6. The session was design-conversation followed by execution; the operator's directives in §6 carry the wording that mattered.
