---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
section_conventions:
  open_questions: "Open Questions"
  decisions: "Decisions and Rationale"
  constraints: "Constraints and Gotchas"
  resolved: "Resolved Questions"
---

# Decision Log

This file tracks all decisions, open questions, constraints, and resolved questions for this ACW instance. See `rules/decision-tracking.md` for entry format. When this file grows too large to navigate, split into four files via the promotion ritual in `rules/promotion-ritual.md`.

## Open Questions

### Q-001 — Defer or ship C-04 synthesis-cycle?

**Date raised:** 2026-04-30
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-04
**Question:** Promote `research/queries/` + `research/queries/_consumed/` single-file synthesis lifecycle into ACW canonical, or wait for second-instance evidence?
**Status:** v0.2.0-rc1 added the directories implicitly (capture-and-metabolize and resume-session reference them) but did NOT add a normative `rules/synthesis-cycle.md`. Effectively partial-shipped pending more evidence.

---

## Decisions and Rationale

### D-ACW-034 — Meta-layer maintenance harness gated on `meta_layer` block presence

**Date:** 2026-05-02
**Decision:** `/acw-session end` Phase 2 gains a "Meta-layer maintenance" step; `/acw-instance audit` Mode A gains a staleness check; `/acw-instance upgrade` gains a "Resolve meta-layer staleness" step. All three are gated on `acw-state.yaml::meta_layer` block presence — most consumer instances don't have meta-layer narrative files and pay no cost. Trigger table is hardcoded sensible defaults (README on substrate-shape change, CHANGELOG on version bump, LINEAGE on new primitive, ORCHESTRATION on new methodology pattern, SKEPTIC on med+ incident).
**Rationale:** v0.5.1's front-door cleanup exposed a structural gap — substrate had Phase 2 distribution; meta-layer had nothing. README went stale across four versions before someone noticed. The harness closes the gap. Gating on `meta_layer` block presence (not `is_canonical_source`) generalizes correctly: any workspace with declared meta-layer narrative files inherits the discipline; workspaces without it pay nothing.
**Source:** Operator question on README staleness during the v0.5.1 turn; meta-layer audit revealed five staleness candidates; harness designed in same conversation.

### D-ACW-033 — `inbox/` canonical as operator capture surface

**Date:** 2026-05-02
**Decision:** `inbox/` (no underscore) ships as canonical empty_dir for the operator's untriaged-items surface. Folder of dated markdown files plus loose entries. Items get processed and removed: routed to `tasks-status::Pending`, `tasks-status::Parked`, the operator's external task app, or deleted. Distinct from `_buffer/` (system surface for cross-instance handoffs) and `briefings/` (agent-generated dated snapshots) — three different surfaces, three different lifecycles.
**Rationale:** Operator needs a workspace-side capture surface for raw inbound items needing triage. Without it, mid-session captures and triage-skill outputs have nowhere to land that's distinct from committed work. The `_inbox/` → `_buffer/` rename in v0.5.0 cleared semantic space for this; v0.6.0 fills it. The triage-flow model (inbox → tasks/parked/external/deleted) is operator-driven; substrate shape is light (folder of dated files, no enforced structure).
**Source:** Operator design conversation during v0.5.0/v0.6.0 scoping; reaffirmed during v0.6.0 ship.

### D-ACW-032 — `tasks-status.md` is workspace-purpose tracker; personal tasks stay external

**Date:** 2026-05-02
**Decision:** `rules/task-tracking.md` updated to clarify that `tasks-status.md` tracks the workspace's purpose, adapted per workspace type (cockpit = config + chief-of-staff ops; project = deliverables; full = org coordination). Operator-personal life tasks (pick up kids, doctor's appointment, call mom) explicitly do NOT live in workspace substrate — they live in the operator's external task app, accessed via MCP at query time. Same logic applies to calendar (stays in Google/iCloud/Nextcloud) and email (Gmail/Outlook).
**Rationale:** The general rule: don't duplicate operator-accessible-on-phone surfaces in workspace substrate. Mirroring creates sync rot. Lean on MCP integrations for live data; lean on briefings/ for moment-in-time aggregations when a snapshot is wanted. Earlier conversation considered `my-tasks.yaml` as a separate operator-personal surface; rejected for the same reason calendar mirror was rejected. Same logic applied consistently.
**Source:** Operator decision during v0.5.0/v0.6.0 scoping; codified in rules/task-tracking.md framing update.

### D-ACW-031 — `context/` canonical for operator/project context layer

**Date:** 2026-05-02
**Decision:** `context/` ships as canonical instance_layer with four templated files: `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`. Lightweight pointers to operating reality. Read on demand by agents that need the context, not auto-loaded into every chat. Templates render at scaffold time; operator fills with workspace-specific content. Updates happen as operating reality shifts, not on a schedule.
**Rationale:** Substrate categories so far covered decisions (specific choices), rules (governance), skills (operations), glossary (vocabulary). Missing: lightweight context that helps agents calibrate ("what is this workspace for? who matters? how does the operator work?"). `context/` fills the gap. Especially load-bearing for cockpit-shaped instances where personal + business context blends; useful in any workspace type. The four canonical files match `_Command/context/` shape (which surfaced the absorption candidate).
**Source:** Operator design conversation during v0.5.0/v0.6.0 scoping; absorbed from `_Command`'s organic substrate.

### D-ACW-030 — Front-door cleanup: retire `bootstrap/`, `migration/`, `LAYERS.md`; refresh README

**Date:** 2026-05-02
**Decision:** Three meta/template files retired in v0.5.1; README rewritten to reflect current architecture. `bootstrap/README.md` (seven-question greenfield interview) — content absorbed by `tools/scaffold-instance.py` plus templated `research/01-problem-framing.md`. `migration/README.md` (brownfield audit guide) — absorbed by `/acw-instance audit` Mode A+B and `/acw-instance upgrade` adopt-mode. `LAYERS.md` (ACW-specific three-layer narrative) — folded into README.md as "How ACW is layered" section; the generic pattern continues to live in `rules/manifest-discipline.md`. README gained a 60-second scaffold quickstart up front; current operator commands; current directory map (runbooks/, integrations/, briefings/, _buffer/); current load-bearing files.
**Rationale:** Operator question "when's the last time you read the README.md?" exposed v0.1.0-era staleness. Audit of meta-layer found three retirement candidates (functions absorbed by current tooling) and revealed the harness gap — substrate has Phase 2 distribution; meta-layer has none. Front-door fix happens now (v0.5.1); harness ships in v0.6.0 alongside the operator-centric cluster. Three retirements are clean: each file's content is either preserved elsewhere (LAYERS in README, problem-framing template) or now embodied as tooling (scaffolder, audit verb).
**Source:** Operator question on README staleness; meta-layer audit during the v0.5.1 scoping turn.

### D-ACW-029 — `briefings/`, `runbooks/`, `integrations/` shipped as universal canonical substrate

**Date:** 2026-05-02
**Decision:** Three new substrate directories earned by `_Command` audit dogfood. All three are universal patterns; content varies by workspace type but the shape is the same. `runbooks/` (operator how-tos), `integrations/` (external-system docs with templated README), `briefings/` (agent-generated dated snapshots). All earned in v0.5.0 via `rules/instance-current-manifest.md` registry entries.
**Rationale:** Initial `_Command` audit verdict flagged all three as "Likely [s] instance-specific." Operator pushed back: briefings is universal (cockpit aggregates calendar+tasks; project aggregates PR+build+issues; same shape, different content); runbooks is universal (operator how-tos that don't fit in any skill); integrations is universal (every workspace touching external systems via MCP/API/webhook accumulates docs about them). Verdict reversed. Three absorption candidates ship as canonical.
**Source:** `_Command` audit report + operator reframing.

### D-ACW-028 — Calendar, tasks, email stay external; briefings is the snapshot mechanism

**Date:** 2026-05-02
**Decision:** Don't duplicate calendar, task app, or email in workspace substrate. Lean on MCP integrations for live data. When the operator wants a snapshot of aggregated external state, briefing skills aggregate calendar + tasks + email + integrations into a dated artifact in `briefings/`. Documented as a doc note in `rules/instance-current-manifest.md` § briefings.
**Rationale:** Operator extended the calendar-stays-external logic to tasks and email. Same reasoning for all three: they're already operator-accessible on phone/desktop via native apps; mirroring locally creates sync rot. The chief-of-staff affordance ("what's on my plate?") lives in agents that call the appropriate MCP at query time, not in cached substrate.
**Source:** Operator decision during v0.5.0 / v0.6.0 scoping turn.

### D-ACW-027 — `_inbox/` renamed to `_buffer/` per DIP vocabulary canon

**Date:** 2026-05-02
**Decision:** System cross-instance handoff directory renamed from `_inbox/` to `_buffer/` in v0.5.0. All active substrate (skills, rules, state, tools, tests) updated. Append-only history (decisions/, build-log, CHANGELOG, research/) retains historical `_inbox` references. `/acw-instance upgrade` v0.5.0+ adds a migration step proposing the rename to legacy workspaces.
**Rationale:** Two reasons pulling the same direction: (a) operator's DIP vocabulary canon already declares "buffer" as the canonical term replacing inbox/queue/staging — the rename brings ACW canonical inline with existing vocabulary. (b) v0.6.0 will introduce an operator-facing `inbox/` surface; the system surface keeping `_inbox/` would collide. Renaming now (one downstream instance, `_Command`) is cheap; renaming later (after lattice scale) would be expensive.
**Source:** Operator decision during v0.5.0 / v0.6.0 scoping turn; DIP vocabulary in `~/synapse/Rules/Procedures/dip-vocabulary.md`.

### D-ACW-026 — `_Command` audit dogfood incident retrospective

**Date:** 2026-05-02
**Decision:** First `/acw-instance audit` against `_Command` produced clean Mode A output but exposed five bugs in v0.4.0: (1) hard-stop scan counted only `decisions/` and `rules/` files; missed root-level organic substrate. (2) Mode B walk produced static report with proposed routings instead of interactive prompts; nothing landed in `_buffer/`. (3) Default routing was `[s] instance-specific`; should be `ask, don't guess`. (4) Skills audit not part of verb spine. (5) Absorption flow gated on workspace registration. Five bugs all earned by this single dogfood.
**Rationale:** Earn-by-incident in action. v0.4.0 design was sound at the rule level but the verb implementation had ambiguities and gaps that only surfaced under real-workspace use. v0.5.0 fixes all five, plus reverses the conservative routing on three substrate categories that turned out to be universal patterns.
**Source:** Operator pasted `_Command` audit report; agent reading produced the bug list; operator confirmed fixes.

### D-ACW-025 — `briefings/` as universal pattern, not cockpit-specific

**Date:** 2026-05-02
**Decision:** Reversed earlier framing that flagged briefings/ as cockpit-specific. The pattern (agent-generated dated snapshot of aggregated state) is universal across workspace types. Cockpit, Project, and Full instances all benefit from it; only the aggregation content varies.
**Rationale:** Initial audit conservatism mis-classified. Operator's cockpit framing made it sound role-specific (leadership, CS, etc.) but cockpit is itself a workspace TYPE, not a role — anyone with a personal command center qualifies. And briefings work in project workspaces too (PR/build/issue snapshots). Universal pattern.
**Source:** Operator clarification on cockpit-vs-leadership framing during v0.5.0 scoping.

### D-ACW-024 — Mode B walk in audit verb is interactive, not static-report

**Date:** 2026-05-02
**Decision:** Audit verb's Mode B (organic substrate discovery) prompts the operator interactively per finding with the four-option route (`[a]/[b]/[s]/[n]`). Writes happen during the walk on `[b]` routing, not after the report finalizes. Default is "ask, don't guess" with explicit comparison to canonical surfaced in the prompt.
**Rationale:** v0.4.0 spec said "surface to the operator" which an agent could plausibly interpret as "include in the report." `_Command` audit produced static report; nothing landed in `_buffer/`. Spec tightened to make the interactive walk unambiguous. Also: default routing of `[s]` was too conservative — Mode B's whole point is the operator-as-judgment-call; auto-classifying defeats the purpose.
**Source:** `_Command` audit dogfood incident.

### D-ACW-023 — Hard-stop scan widened to root-level organic substrate

**Date:** 2026-05-02
**Decision:** `/acw-instance upgrade` adopt-mode hard-stop now counts (a) markdown files in `decisions/` and `rules/` (existing v0.4.0 logic) PLUS (b) root-level directories not in canonical PLUS (c) root-level non-canonical markdown files. The threshold (default 5) applies to the total. v0.4.0 counted only (a) and missed exactly the case it was designed to catch — workspaces like `_Command` accumulate organic substrate at root, not inside `decisions/` or `rules/`.
**Rationale:** `_Command` audit revealed ~1 file each in `decisions/` and `rules/` (well under threshold) despite having `briefings/`, `runbooks/`, `integrations/`, `notes/`, `context/` directories at root. v0.4.0 hard-stop wouldn't have fired; would have steamrolled into adoption. v0.5.0 fixes scope.
**Source:** `_Command` audit dogfood incident.

### D-ACW-022 — Hard-stop threshold for adopt-mode set at 5

**Date:** 2026-05-02
**Decision:** `/acw-instance upgrade` adopt-mode bails (with pointer to `/acw-instance audit`) when the count of non-canonical markdown files in `decisions/` or `rules/` is at-or-above 5. Threshold lives in `acw-state.yaml::adopt_mode_organic_threshold` with canonical default 5.
**Rationale:** Below-5 catches cs-copilot-shape workspaces (canonical-shaped, just unregistered; ~1-2 files). At-or-above-5 catches `_Command`-shape workspaces with substantial organic substrate. Tunable per-instance only when the default produces wrong-direction failures in practice.
**Source:** Operator-confirmed during the v0.4.0 ship plan synthesis turn.

### D-ACW-021 — Audit Mode A uses ACW rules + templates as the schema; no new artifact

**Date:** 2026-05-02
**Decision:** The audit verb's Mode A (canonical-conventions comparison) fetches ACW canonical rule files (`rules/decision-tracking.md`, `rules/task-tracking.md`, etc.) and template files (`tools/templates/*.tmpl`) directly from GitHub canonical. Compares the workspace's substrate file against the rule and template inline. No structured "canonical-conventions schema" artifact is built; ACW rules + templates ARE the schema in prose form.
**Rationale:** Operator pushed back on the "needs a schema" framing. Right call. The agent doing the audit can compare rule-vs-file the same way an operator would do it manually. Building a structured schema would duplicate what the rules already encode and risk drift between the rule and its serialized form.
**Source:** Operator correction during the v0.4.0 ship plan turn.

### D-ACW-020 — Audit Mode B is operator-routed organic substrate discovery; ships in v0.4.0

**Date:** 2026-05-02
**Decision:** Mode B walks the workspace looking for substrate-like patterns (markdown files with frontmatter, dated-prefix filenames, structured directories) not covered by canonical types. For each finding, the verb surfaces a four-option route to the operator: adopt-as-canonical, absorption candidate, instance-specific, or not-substrate. Operator routing is the authoritative classification — the skill never auto-routes Mode B findings.
**Rationale:** Operator pushed back on deferring Mode B. Right call. Mode B doesn't need sophisticated heuristics; it needs the operator in the loop. The decision to absorb upstream vs. declare instance-specific is a judgment call about whether the pattern would generalize, and only the operator has the context to make it.
**Source:** Operator correction during the v0.4.0 ship plan turn.

### D-ACW-019 — `/acw-session` shipped as object-centered command-routed orchestrator (verbs: start, end)

**Date:** 2026-05-02
**Decision:** Renamed `/resume-session` → `/acw-session start` and `/capture-and-metabolize` → `/acw-session end` as a single object-centered command-routed orchestrator. Object: this ACW instance's session lifecycle. Verbs: boundary operations on it. Shared spine: load `acw-state.yaml`, resolve `paths`, check `_inbox/`, identify recent captures. Specialist work after the spine diverges per verb (Impeccable pattern).
**Rationale:** Initial pushback (the four-test rule reading "same invariant workflow") was based on the strict voice in the old skill-format. Operator pointed at Impeccable as the precedent: 23+ commands across genuinely different specialist workflows, unified by shared setup and shared object. Re-reading the skill-format with that lens, `/acw-session start|end` fits cleanly. Skill-format also tightened in same release to remove the strict-voice/permissive-voice contradiction.
**Source:** Operator's invocation of Impeccable as precedent; subsequent skill-format correction.

### D-ACW-018 — `/acw-instance` shipped as object-centered command-routed orchestrator (verbs: audit, upgrade)

**Date:** 2026-05-02
**Decision:** Renamed `/upgrade-instance` → `/acw-instance` as a command-routed orchestrator with two verbs. Audit is read-only (Mode A canonical comparison + Mode B organic discovery + per-file routing report). Upgrade is interactive (gap-walk with adopt-mode hard-stop, divergence-marker respect, decision-log entry). Shared spine: registration check, GitHub canonical fetch, substrate scan, routing-table generation.
**Rationale:** The cs-copilot session that triggered v0.3.0 work also exposed a deeper need: when a workspace has organic substrate (`_Command`-shape), adopt-mode shouldn't run blindly. Audit verb is the safety layer — operator surveys before reconciling. Upgrade verb hard-stops above the organic threshold and points at audit. Both verbs share the same canonical-fetch and substrate-scan logic, which is the spine.
**Source:** Conversation arc 2026-05-02 turn 79 onward; operator confirmed v0.4.0 scope.

### D-ACW-017 — Multi-instance topology rule expanded with absorption mechanics

**Date:** 2026-05-02
**Decision:** `rules/multi-instance-topology.md` expanded with four sections: three-flow resolution model (adopt / absorb / instance-specific), absorption candidate format (`_inbox/` payload schema), divergence markers (`divergent_pending_review` for temporary, `instance_specific_substrate` for permanent with decision-log ref), and re-adoption flow. Plus cross-repo write governance for workspaces writing absorption candidates to ACW's `_inbox/`.
**Rationale:** The v0.3.0 ship named the lattice topology but didn't specify how absorption actually flows mechanically. The operator's question "how does ACW know about an absorption candidate?" exposed the gap. The mechanics now use the existing `_inbox/` cross-instance handoff seed. ACW's `/acw-session start` reads `_inbox/`; absorption candidates surface naturally in next session-start.
**Source:** Operator's question on absorption mechanics during the multi-instance lattice conversation.

### D-ACW-016 — `rules/skill-format.md` tightened to reconcile strict-voice with object-centered carve-out

**Date:** 2026-05-02
**Decision:** Three targeted edits to `rules/skill-format.md`:
1. Reframe test 1 ("same invariant workflow") as "same shared spine" — names the spine as setup gates + shared-context loading; specialist work after the spine may diverge in object-centered orchestrators.
2. Split the strongest-version rule by orientation: operation-centered (parameterization of same operation) vs. object-centered (sibling specialist operations on same object).
3. Scope test 4 (deltas-are-configuration) to the spine only; specialist-work divergence is allowed in object-centered.
Also ported the full command-routed orchestrator material from synapse global into ACW canonical (it had only existed in the operator's personal global rules).
**Rationale:** The strict-voice contradicted the permissive-voice (command-count ladder explicitly carving out object-centered workbenches at 10+ commands). This contradiction false-flagged Impeccable-shape patterns including `/acw-session start|end`. Closing the contradiction lets the rule self-validate.
**Source:** Operator's pushback on my false-flag of `/acw-session start|end`; Impeccable as precedent.

### D-ACW-015 — Canonical-edit detection in capture-and-metabolize Phase 2 gates on `is_canonical_source`

**Date:** 2026-05-02
**Decision:** Phase 2 of `capture-and-metabolize` adds a canonical-edit detection step. It computes the intersection of `auto_load_at_session_start` and `template_layer` (= the canonical files), checks whether any were edited this session, and branches on `acw-state.yaml::is_canonical_source`. Publishing instances (`true`) get a version-bump-and-push prompt; downstream consumers (`false` or absent, the default) get a warning that local edits to canonical files won't propagate and may be overwritten by `/upgrade-instance`.
**Rationale:** Without the gating flag, the propagation behavior would ship to every child instance. Child instances editing local snapshots of canonical files would start trying to push to ACW's GitHub on every edit. The flag separates "I publish canonical content downstream" from "I consume canonical content from upstream" cleanly. Operator-flagged the bug in real time during the design conversation; the fix earned its build before the skill shipped.
**Source:** Operator reasoning during the multi-instance topology discussion, turn 81 of the v0.3.0 absorption arc.

### D-ACW-014 — `/upgrade-instance` fetches canonical from GitHub as single source of truth; supports adopt mode

**Date:** 2026-05-02
**Decision:** `/upgrade-instance` fetches `rules/instance-current-manifest.md` from the ACW GitHub repo (`benfrankster-design/acw`, private) on every run via `gh` CLI or `urllib.request` with `GITHUB_TOKEN`. The instance's local copy is a write-once cache of "the last canonical I reconciled to," never used as comparison yardstick. Skill fails closed if GitHub is unreachable. Also adds an adopt mode: when `acw-state.yaml` and/or `rules/instance-current-manifest.md` are missing but ≥3 substrate signals are present, the skill offers to write the missing registration files using the GitHub canonical and proceed to reconciliation.
**Rationale:** Operator rejected a local-ACW fallback as introducing race conditions between local and remote canonical. Single source of truth via GitHub means one pointer; if the repo ever moves, only one place needs updating. The cs-copilot session that prompted this work surfaced a pre-existing substrate-shaped workspace that the original `/upgrade-instance` refused to act on; adopt mode closes that gap. Substance signals threshold (3 of 6) prevents false positives in random workspaces.
**Source:** Operator rejection of local-ACW fallback in the multi-instance topology conversation; cs-copilot adopt-mode requirement surfaced earlier in same arc.

### D-ACW-013 — `is_canonical_source` flag added to `acw-state.yaml` schema

**Date:** 2026-05-02
**Decision:** Added `is_canonical_source: <bool>` to `acw-state.yaml`. ACW itself sets it to `true`. The template (`tools/templates/acw-state.yaml.tmpl`) defaults it to `false` for every scaffolded instance. Added as a recommended block in `rules/instance-current-manifest.md` earned in v0.3.0.
**Rationale:** Needed a clean signal for "this instance publishes canonical content downstream" vs "this instance consumes canonical content from upstream." Used by `capture-and-metabolize` Phase 2 (canonical-edit detection branch) and potentially by future skills that need to distinguish publisher vs consumer behavior. Generalizes beyond ACW — any future canonical-publishing meta-instance (e.g., a consultancy serving as canonical for client engagements) sets the flag true.
**Source:** Required by D-ACW-015 (Phase 2 canonical-edit branching).

### D-ACW-012 — `rules/multi-instance-topology.md` promoted to template_layer canonical

**Date:** 2026-05-02
**Decision:** Promoted the lattice model + knowledge-placement discriminator + reference-not-duplicate principle from `research/10-multi-instance-topology.md` (meta_layer) to `rules/multi-instance-topology.md` (template_layer). Added to `auto_load_at_session_start` and `template_layer` blocks in `acw-state.yaml`. Added as recommended block in `rules/instance-current-manifest.md` earned in v0.3.0. Research note retained in meta_layer as provenance.
**Rationale:** The lattice framing is load-bearing for any operator scaling beyond a single instance. Baking it into template_layer means every scaffolded instance (and every existing instance via /upgrade-instance) inherits the framing without operator effort. Stable but flagged experimental until lattice-level incidents earn promotion to normative.
**Source:** Operator decision in the multi-instance topology conversation, turn 79.

### D-001 — Absorb gsg-copilot extensions into v0.2.0-rc1

**Date:** 2026-04-30
**Decision:** Ship C-01 (tasks-status), C-02 (build-log), C-03 (bookend skills), C-06 (auto-load convention), C-09 (incident category enum) into ACW canonical. Defer C-04, C-05, C-07-as-hard-rule, C-08 as recommendations only.
**Rationale:** The shipped set is the minimal cohesive substrate for any new ACW instance to pick up gsg-copilot's three weeks of lived experience. Deferred items are operator-preference-flavored or lack second-instance evidence.
**Source:** `research/09-gsg-copilot-instance-extensions.md`

### D-002 — Supersede `skills/capture-session/` with bookend pair

**Date:** 2026-04-30
**Decision:** Replace the standalone `capture-session` skill with a pair: `capture-and-metabolize` (end-of-session, five phases) and `resume-session` (start-of-session). The four sub-steps of the original skill become Phase 1 internal sub-steps of `capture-and-metabolize`.
**Rationale:** Three weeks of lived experience in `gsg-copilot` proved the bookend shape (paired session-start and session-end skills, with substrate maintained as a side effect of distribution) eliminates manual scaffolding maintenance. The standalone `capture-session` covered only one end of the loop.
**Migration:** The original `skills/capture-session/` directory is marked superseded in-place; manual operator deletion required (the careful guardrail blocked automated removal).
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-03

### D-003 — Single-incident emergency promotion of `tools/scaffold-instance.py`

**Date:** 2026-04-30
**Decision:** Ship `tools/scaffold-instance.py` based on Incident D-02 (uuid `616d435b-ec6d-470a-9cdf-2935b739e4a1`) alone, rather than waiting for two more bootstrap-related incidents.
**Rationale:** The promotion ritual's emergency clause is reserved for severity-`high` incidents. D-02 is `med`, but is structurally severe in a different way: every future ACW instance that does not bootstrap from this tool generates more drift incidents downstream. The tool is the *prevention layer* for an incident class, not a primitive earned by lived friction. Form factor is small (~200 lines, stdlib-only), and the prevented incident class is structural. Discipline prefers cheap prevention over earn-by-incident accumulation when both apply.
**Source:** `research/09-gsg-copilot-instance-extensions.md` (final section)

### D-ACW-011 — ACW skills register globally via user-level directory junctions

**Date:** 2026-05-02
**Decision:** ACW's three bookend-arc skills (`capture-and-metabolize`, `resume-session`, `upgrade-instance`) register on the operator's machine via directory junctions at `~/.claude/skills/<name>/` pointing at `c:\Users\benja\projects\acw\skills\<name>/`. ACW's `skills/` directory is the canonical runtime source. Child instances scaffolded via `tools/scaffold-instance.py` ship with their own copies of the skills as part of template_layer propagation; those copies are passive (self-contained distribution surface) and not the registered runtime copy.
**Rationale:** Operator works across multiple ACW-derived workspaces (ACW itself, cs-copilot, gsg-copilot, future Frank Context). The framework-agnostic skill design from rc4 already supports one canonical source serving every workspace, since paths resolve from each workspace's own `acw-state.yaml` at runtime. User-level registration with a single canonical source means edits to a skill propagate to every workspace immediately — no per-instance update step. Project-level overrides remain available on demand (Claude Code resolves project-level skills before user-level), so a workspace that needs a customized skill can still add its own `.claude/skills/<name>/` junction.
**Source:** Operator turn requesting the wisest approach; reasoning surfaced the multi-instance pollution concern and the canonical-source preference.

### D-ACW-010 — `/upgrade-instance` skill closes the drift loop

**Date:** 2026-05-02
**Decision:** New skill `skills/upgrade-instance/` walks the operator through reconciling instance state with the current ACW recommended-blocks registry. Drift detection lives in `/resume-session` Step 5; reconciliation lives here. Together they form the upgrade loop: detect → reconcile → bump `last_reconciled_version` → quiet alert.
**Rationale:** Drift visibility without a path-to-fix is half a feature. Operators shouldn't have to hand-edit `acw-state.yaml` and look up canonical defaults manually. The skill walks each gap with the registry's "How to add" content surfaced inline. Pure additive — no demotions, no removals, no shape repair.
**Source:** Operator instruction, turn 73 of the v0.2.0 absorption arc; subagent stress test informed final shape.

### D-ACW-009 — Drift detection via instance-current-manifest

**Date:** 2026-05-02
**Decision:** New file `rules/instance-current-manifest.md` (template_layer) declares the recommended-blocks registry. Each entry documents what / why / required / how-to-add / earned-in. `/resume-session` Step 5 reads the registry, compares earned-in versions against `acw-state.yaml::last_reconciled_version`, and surfaces a one-line drift alert when gaps exist.
**Rationale:** ACW evolves; existing instances need a way to learn they're behind without manual audit. The registry is the source of truth for "what current ACW expects"; the alert is the prompt; `/upgrade-instance` (D-ACW-010) is the action. Backwards-compatible — instances with no `last_reconciled_version` field default to `"0.0.0"` and get a noisy first run that quiets after one reconciliation.
**Source:** Operator instruction during the "framework-agnostic skills" scoping conversation, turns 67–73.
**Implementation note:** Required adding `last_reconciled_version` (semantic version) alongside the existing `last_reconciled` (date) field in `acw-state.yaml`. Subagent caught the version-vs-date conflation during Phase 4 verification; fixed before commit.

### D-ACW-008 — Paths block + manifest-tooling spec

**Date:** 2026-05-02
**Decision:** `acw-state.yaml::paths` declares every substrate file path. The bookend skills read paths from this block at runtime; canonical defaults documented in `rules/manifest-discipline.md`. The manifest-tooling spec (four operations: load, append, contains, validate) ships in `rules/manifest-discipline.md` with a stdlib-only Python reference implementation in `tools/manifest.py`.
**Rationale:** Decouples bookend skills from hardcoded paths. Future template evolution (moving a substrate file) requires editing one yaml block per instance instead of grepping skills. Manifest-tooling spec is the fourth application of the manifest-discipline pattern (after auto_load_at_session_start, three-layer manifest, vocabulary canon) — the operator chose to ship the shared tooling now rather than wait for a fifth case. Section heading conventions also moved to per-file frontmatter (`section_conventions` key).
**Source:** Operator scoping conversation, turns 67–73. Reference implementation is 33-test TDD; subagent verified spec/impl alignment before commit.

### D-ACW-007 — Generic manifest-discipline rule extracted; LAYERS.md trimmed to ACW-specific narrative

**Date:** 2026-04-30
**Decision:** The generic three-layer pattern ships as `rules/manifest-discipline.md` in `template_layer`. ACW's own `LAYERS.md` stays in `meta_layer` with ACW-specific content only.
**Rationale:** Operator question surfaced that LAYERS.md as written carried both the generic pattern (would be useful in every derived workspace) and ACW-specific narrative (only useful in ACW). Splitting on that axis makes the pattern reusable; recursive instances (Frank Context, hypothetically) get the same machinery and write their own narrative on top.
**Source:** Operator question on three-layer model shipping behavior; turn 35–37.

### D-ACW-006 — ACW becomes instance of itself; gains `project:` block

**Date:** 2026-04-30
**Decision:** `acw-state.yaml` carries `project:` block (`name: "ACW"`, `code: "ACW"`, `domain: "meta-template"`). Existing legacy ids `D-001` through `D-005` stay unprefixed; new entries use `D-ACW-NNN`.
**Rationale:** Operator pressed on the framing that "ACW is the template, not an instance" — the accumulated substrate gave the lie to that framing. ACW had been operating as its own instance from session zero. The reframe formalizes ACW = instance + template, both at once. The `project.code` derivation in capture-and-metabolize now works on ACW; the missing-block fallback (skill ships unprefixed ids) remains for downstream one-off instances.
**Source:** Operator-surfaced framing question, turn 37.

### D-005 — Three-layer manifest replaces hardcoded scaffold lists

**Date:** 2026-04-30
**Decision:** `acw-state.yaml` now carries three blocks — `template_layer`, `instance_layer`, `meta_layer` — that classify every file in ACW. The scaffold tool reads from this manifest instead of carrying hardcoded `VERBATIM_FILES` / `VERBATIM_RULES` / `TEMPLATED_FILES` lists. Default for new files is `instance_layer`; promotion to `template_layer` or `meta_layer` requires an explicit decision-log entry.
**Rationale:** ACW is both a template and its own first instance. Without explicit classification, the template-vs-instance split lived inside scaffold-instance.py as five hardcoded lists — adding a new propagatable file required a paired script edit, and a forgotten edit silently broke instances scaffolded thereafter. The asymmetry of mistakes (instance content shipping as template > template missing from instance) drives the default-to-instance discipline. This is the third application of the manifest-discipline pattern in ACW (after `auto_load_at_session_start` and the canon governance state machine), making the pattern itself worth naming.
**Source:** Operator-flagged during v0.2.0-rc1 absorption work; classified as the actionable form of D-01/D-02 follow-up.
**See also:** `LAYERS.md` (the meta_layer explainer).

### D-004 — Auto-load convention is vendor-agnostic

**Date:** 2026-04-30
**Decision:** AGENTS.md directive 7 declares the auto-load convention as the cross-vendor contract. The canonical file list lives in `acw-state.yaml::auto_load_at_session_start`. Each agent host implements via its native mechanism (Claude Code: `@`-imports in `CLAUDE.md`; agents reading `acw-state.yaml` directly need no host-specific file).
**Rationale:** ACW is designed to outlive any single vendor. Coupling the convention to `@`-imports would couple ACW to Claude Code. Splitting the convention across three layers (prose contract, machine-readable list, host-specific implementation) preserves portability.
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-06

---

## Constraints and Gotchas

### C-001 — `skills/capture-session/` directory still exists on disk

`skills/capture-session/` is marked superseded in its SKILL.md frontmatter (`status: superseded`, `superseded_by: skills/capture-and-metabolize/`) but the directory itself was not removed. The careful guardrail blocked automated `rm -rf`. Operator must delete manually before the v0.2.0 tag.

### C-002 — Synapse copies still stale

Per Incident D-01, `~/synapse/Rules/Procedures/` copies are still stale relative to `/Projects/acw/rules/`. Mitigation deferred to a separate session.

---

## Resolved Questions

*(No entries yet.)*
