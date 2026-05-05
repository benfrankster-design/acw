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

### D-ACW-037 — v0.8.0: bookend efficiency cluster (Haiku, subagent isolation, quick/full modes, /acw-session update verb, .current-session tracker, sessions/ at root, retire 4 superseded skills)

**Date:** 2026-05-04

**Decision:** Six changes ship together as v0.8.0:

1. `skills/acw-session/SKILL.md` declares `model: claude-haiku-4-5` in frontmatter. Phase steps that need real reasoning (Phase 3 operator-confirm proposals, Phase 5 research-prompt construction, meta-layer trigger proposed-edit text) escalate to Sonnet inline.
2. Bookend invokes a fresh subagent context to avoid inheriting the parent session's Opus 4.7 1M pricing.
3. `/acw-session end` defaults to **quick mode** (Phase 1 capture + minimal Phase 2 append-only writes + Phase 3 auto-update sweep). `full` argument runs all phases as previously documented. Phase 4 conditional on `--synapse` flag (quick) or `synapse_log_path` set (full); Phase 5 conditional on `--research` flag (quick) or operator confirmation (full).
4. New `/acw-session update` verb for mid-session checkpoints. Reads `.current-session`, appends timestamped note. Self-bootstraps if no tracker exists.
5. `paths.session_captures_dir` migrates from `research/sessions` to `sessions/` at root. Sessions are operational logs, not research artifacts. Existing capture files moved via `git mv`. `empty_dirs` swap.
6. The four superseded skills marked in `meta_layer` since v0.4.0 (`capture-session/`, `capture-and-metabolize/`, `resume-session/`, `upgrade-instance/`) are deleted from disk; their entries removed from `meta_layer`.
7. New `plans/` directory at workspace root for plan artifacts. Operational outputs from planning agents (or operator hand-written plans) save here as dated markdown (`plans/YYYY-MM-DD--<slug>.md`). Empty `.gitkeep` at scaffold time. New canonical default path `plans_dir: plans` in `acw-state.yaml::paths`. Convention only in v0.8.0 — no automatic writer skill; operator drops plans here manually. Earn-by-content reasoning: cheap to pre-create the directory; the writer skill earns its build only when convention demands automation.

**Rationale:** Operator session 2026-05-04 surfaced acute cost pressure — `/acw-session end` running 7-10 minutes per invocation on Opus 4.7 1M context, burning ~5-8M tokens per session, halfway through Max-plan weekly budget after 2 days. Cost-friction incident logged in `incidents.jsonl` this session. The bookend's work is overwhelmingly mechanical (read transcript, append to file, classify against manifest) — Haiku-grade in 80%+ of phases. Running mechanical bookend work at the most expensive Claude variant is structurally wrong. Quick mode collapses session-end to its append-only essentials, deferring expensive operator-interactive work to explicit `full` invocations at logical boundaries. The `update` verb closes a long-standing gap (binary bookend vs Ian Nuttall's session-update precedent) without paying full session-end cost. Sessions move to root because they are operational logs — `research/` is for design notes and queries. Superseded skill deletion closes a Pending item from v0.4.0 that the careful guardrail blocked from automated removal.

**Source:** Operator session 2026-05-04; deep-research note `research/11-session-continuity-prior-art.md` (Ian Nuttall claude-sessions precedent for `update` verb and `.current-session` tracker pattern; Anthropic Memory Stores filesystem-as-memory validation; ETH Zurich finding on hand-curated substrate); cost-friction incident logged this session.

**Open follow-ups:**

- **v0.9.0 — substrate earn-by-content refactor.** Scaffolder ships discipline floor only; bookend scaffolds substrate files on-demand when content earns them. Threshold table per content type to be argued through in `research/12-substrate-earn-by-content.md` (not yet written).
- **Future — `CLAUDE.md` becomes a thin pointer** ("see `AGENTS.md`"); `AGENTS.md` carries the substantive content currently in `CLAUDE.md` as the instance version of the file. Separate ship; not in v0.8.0 or v0.9.0.
- **Risk: `model:` frontmatter honored?** Field may not be honored by all Claude Code versions. If not honored, the skill still works at whatever model the harness picks; cost-cut is just smaller. No breakage.
- **Risk: quick mode defers operator-interactive work.** Manifest classification, host-entry-file maintenance, canonical-edit detection, meta-layer triggers, cross-repo writes, cross-project notifications accumulate until the next `/acw-session end full` runs them. Long stretches of quick-only mode could let substrate drift. Mitigation: audit verb catches structural gaps; operator instinct picks the heavy session.
- **Risk: self-bootstrap from `update` creates "untitled" capture files.** Mitigation: `end` always renames to topic-from-Phase-1; if operator never runs end, the file stays as-is, harmless.

### D-ACW-035 — Accept all four meta-layer harness proposals; ship as v0.6.1

**Date:** 2026-05-03
**Decision:** Accept all four proposals from the meta-layer harness's first run (post-v0.6.0 `/acw-session end`): extend README directory map with `context/` and `inbox/`; backfill LINEAGE with v0.2.0+ primitive-trace entries; add ORCHESTRATION "v0.2.0+ evolution methodology" section documenting the dogfood-driven loop; add SKEPTIC Warning 4 ("Substrate is not static") earned by incident `e167b922`. Ship as v0.6.1 patch.
**Rationale:** Operator approved with single word ("ship") immediately after the harness surfaced the proposals. The harness earned its build by finding real staleness on its first run; declining the proposals would surface them again on next audit anyway. Better to absorb now while context is warm than to defer and re-discover. The four files together represent the meta-layer's full backfill from the v0.2.0+ cluster — LINEAGE alone has nine primitive-trace gaps closed, ORCHESTRATION gains a major new section, SKEPTIC gains a fifth warning grounded in a documented incident. Validates the harness's first-test correctness (OQ-ACW-010 earn-by-incident path appears clean).
**Source:** Operator approval after Phase 2 meta-layer trigger walk in 2026-05-03 session-end; see build-log entry that documented the proposals.

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

### D-ACW-041 — Buffer lifecycle: `read:` flag + `_buffer/_read/` archive subdirectory

**Date:** 2026-05-05

**Decision:** After an absorption candidate is processed, the operator flips `read: false` → `read: true` in the file's frontmatter, adds an `absorbed_in:` pointer naming where it landed, and moves the file from `_buffer/` to `_buffer/_read/`. The session-start spine already excludes `_read/` from its walk (per spine convention), so processed notifications stop surfacing as drift. History preserved via git. Documented in `rules/multi-instance-topology.md` § "Buffer lifecycle." Applied retroactively — five existing files moved this session (3 backfilled with `read: true` + `absorbed_in:` pointers; 2 already flipped earlier today).

**Rationale:** Convention gap surfaced when operator asked "what happens to files in the buffer once they've been consumed?" The honest answer was: nothing, today. Three older absorbed-but-never-flipped files (D-001 source, cs-copilot rename FYI, Kashef YT note) would still surface as unread notifications on every `/acw-session start` if the spine took the read flag seriously — noise that defeats the buffer's purpose. The session-start spine already documents "do not descend into a `_read/` subdirectory," implying the convention was envisioned but never operationalized. This decision operationalizes it. Cheap form factor (one paragraph in the topology rule + one mkdir + git mv); structural prevention (every absorbed candidate stops surfacing as drift, every session, forever).

**Why subdirectory and not deletion:** the absorbed candidate is mirrored into the consuming surface (decision-log entry, research note, etc.), so the buffer file IS technically redundant after absorption. But: the buffer file carries source attribution (the `from_session_capture` pointer back to the originating instance's session) that the consuming surface may not preserve. Keeping the buffer file in `_read/` preserves the chain of evidence at zero cost.

**Why not just trust git history:** operator legibility. `git log _buffer/` requires intent; `ls _buffer/_read/` is the natural read. Archive subdirectory is the cheaper UX for "what's been processed?"

**Source:** Operator session 2026-05-05, immediately after the buffer-state inspection that revealed three older files still showing `read: false`. Operator approved option 2 (archive subdirectory) over option 1 (accept accumulation) and option 3 (delete on flip).

**Open follow-ups:**
- `/acw-session end` could optionally surface a "any unprocessed buffer notifications?" prompt during the bookend, prompting the operator to flip-and-move at session-end. Earn-by-incident: surfaces only if buffer accumulates faster than the operator processes manually.
- Cross-instance: downstream instances (cs-copilot, _Command, etc.) inherit the convention via the topology rule (template_layer propagation). Their own `_buffer/` directories follow the same lifecycle.
- `_read/` archive is not pruned. If it grows large enough to bother `git status` or directory listings, an annual archive (e.g., `_buffer/_read/2026/`) would earn its build. Not now.

---

### D-ACW-040 — Promote runtime-code-location from convention to AGENTS.md directive 8 (single-incident emergency promotion)

**Date:** 2026-05-04

**Decision:** Promote the runtime-code-location convention shipped in D-ACW-039 from a "convention only" paragraph in `rules/multi-instance-topology.md` to a normative directive (AGENTS.md #8). AGENTS.md goes from "Seven directives" to "Eight directives." Topology rule paragraph rewritten to drop the "convention only" hedge and point at the directive as the normative source.

**Rationale:** Operator overrode the earn-by-incident framing in D-ACW-039 with a sharper read on what counts as the activating incident. D-ACW-039 framed the absorption note from cx-dashboard-saas as "incident #1, wait for #2 before promoting." Operator's correction: the absorption note is itself meta-evidence; the *real* incident #1 is "agent starts writing runtime code in an instance and has to guess where it goes." That incident fires every time a code-shipping instance spins up. A convention buried in a rule file the agent doesn't read at session start fails to prevent it; the agent guesses, the operator corrects, the friction recurs. The fix has to live in a surface the agent reads at session start.

AGENTS.md is the canonical entry point for any agent opening any ACW workspace, declared `loaded_by_agent: yes`, propagated verbatim to every scaffolded instance via template_layer. Adding a single directive line is the smallest possible form factor for the prevention. This is the structural-prevention single-incident emergency promotion path documented in `rules/promotion-ritual.md` and exercised once before in D-003 (scaffold-instance.py).

**Why this is a structural-prevention class:**
- Form factor: one directive line in AGENTS.md, one paragraph rewrite in topology rule.
- Prevented incident class: agents writing runtime code in an instance without canonical guidance, every session. Recurs by structure, not by accident.
- Cost of waiting for "incident #2": every code-shipping session before #2 fires accumulates the same friction.
- The discipline of earn-by-incident is preserved by the *evidence* requirement (cx-dashboard-saas absorption note is the named, dated, documented incident); operator override applied to the *threshold count*, which is reserved for structural-prevention cases.

**Source:** Operator session 2026-05-04, immediately after D-ACW-039 ship. Operator quote: "the first incident should be writing code runtime code. at acw session start claude should read somewhere about this and if code happens in session it knows what to do."

**Open follow-ups:**
- Schema field `acw-state.yaml::paths::runtime_code_dir` (or similar) — still earn-by-incident. Earns when a skill or audit needs to read the runtime path programmatically.
- Existing instances with runtime code already at root: not retroactively breaking. Migration earns its own decision-log entry per instance if the operator chooses to migrate.
- Other AGENTS.md directive expansions: don't expand on speculation. The eight-directive list is small on purpose. Future directives need the same single-incident emergency promotion or earn-by-incident threshold.

---

### D-ACW-039 — Runtime-code-location convention (subdir, not root) absorbed from cx-dashboard-saas

**Date:** 2026-05-04

**Decision:** Add a "Runtime code in shipping instances" section to `rules/multi-instance-topology.md` documenting the observed convention: instances shipping runtime code locate it under a named subdirectory at instance root (`web/`, `server/`, `agents/`, `app/`), not at instance root itself. Substrate stays at root. Convention only — no schema field in `acw-state.yaml`, no separate rule file, no audit enforcement. Source absorption note marked read.

**Rationale:** Absorption candidate from `cx-dashboard-saas` Phase 0 scaffold (`_buffer/2026-05-04-cx-dashboard-saas-app-code-location-friction.md`) flagged a real gap — ACW canonical scaffolds every instance as pure-substrate, but several active instances (cs-copilot, cx-dashboard-saas, future project workspaces) ship runtime code and have to make an unguided structural decision. The candidate proposed three options: (1) `runtime_code_location` schema field, (2) dedicated `rules/runtime-code-location.md`, (3) light-touch convention note. Option 3 is correct under earn-by-incident discipline: this is incident #1 of this class. Schema fields and dedicated rule files earn their build by being load-bearing for skills or audits; nothing in current ACW canonical reads or enforces the runtime path. The convention paragraph in the topology rule is enough until a second instance trips on the same gap.

**Why subdir over root:** substrate and runtime move on different clocks. Substrate is governance (slow-moving, decision-driven, audit-checked); runtime is operational (fast-moving, build-driven, dependency-managed). Co-locating at one path level conflates the two clocks — build artifacts collide with substrate in `git status`, package managers see substrate as project-root noise, deployment configs (Vercel, Docker) point at a path that also carries decisions/.

**Source:** Absorption candidate from cx-dashboard-saas, 2026-05-04. Operator approved option 3 (convention note) in same session.

**Open follow-ups:**
- If a second consumer instance hits the same friction independently (a different operator scaffolding a project workspace and asking the same "where does code go?" question), the convention has accumulated enough incident evidence to earn promotion. Candidates: structured field in `acw-state.yaml`, a dedicated `rules/runtime-code-location.md`, or a scaffolder flag (`tools/scaffold-instance.py --runtime-code-dir web`).
- Eventual: if/when a skill needs to read the runtime path programmatically (e.g., a build-runner skill that needs to know where to `cd` before `npm run build`), the schema field earns its build at that moment.
- Not v1.0.0 — soak only. v1.1.0+ candidate.

---

### D-ACW-038 — v0.9.0: auto-load discipline (earn-by-incident applied to auto-load) + tasks-status rolling-window archive; final pre-1.0.0 substantive ship

**Date:** 2026-05-04

**Decision:** Eight changes ship together as v0.9.0. Per operator directive ("there should be nothing for 1.0.0"), v0.9.0 is the final pre-promotion substantive ship; v1.0.0 is the soak/promotion.

1. **`rules/auto-load-discipline.md`** ships as new template_layer rule. Codifies earn-by-incident applied to `auto_load_at_session_start`: every entry MUST declare a structured claim ("what fails if not loaded every session?") and an `earned_by` field. The rule names canonical recommendations (the four files ACW recommends with stated claims) and declared demotion candidates (paths that fail the gate, with reasons).

2. **`tools/manifest.py`** extended: new `STRUCTURED_LISTS = {"auto_load_at_session_start"}` set; parser handles dict-shaped entries (`- path: ... / claim: ... / earned_by: ...`); `load()` returns paths only (legacy backward compat — existing consumers and the drift check work unchanged); `load_structured()` returns full dict per entry; `validate()` enforces no duplicate paths and required `path` field on dict entries. 8 new unit tests; all 54 tests pass.

3. **`acw-state.yaml::auto_load_at_session_start`** migrated to structured form with 4 demotions: `rules/manifest-discipline.md`, `rules/instance-current-manifest.md`, `rules/multi-instance-topology.md`, `incidents.jsonl` removed (each consumer-skill loads them directly when needed; no agent-context value justifies auto-load). 4 entries kept with structured claims: decision-log, instance-hard-rules, tasks-status, glossary.

4. **`tools/templates/acw-state.yaml.tmpl`** updated: new instances scaffolded by `tools/scaffold-instance.py` inherit the lean 4-entry structured-form default. Bumped baseline `last_reconciled_version` to `0.9.0`.

5. **`CLAUDE.md`** synced: `@`-imports reduced to the 4 canonical entries; "Other substrate is read on demand" section names the demoted files and their consumer-skills.

6. **`/acw-instance audit`** reference (`skills/acw-instance/references/audit.md`) gained "Auto-load discipline" section: walks `auto_load_at_session_start`, classifies entries (KEEP / KEEP-migrate-to-structured / KEEP-instance-specific / DEMOTE / REVIEW), proposes consolidated `reshape` plan row with verdicts applied per entry. Also proposes `write-canonical` for the discipline rule itself when missing.

7. **`/acw-instance upgrade`** reference (`skills/acw-instance/references/upgrade.md`) gained "v0.9.0 migration: auto-load discipline" section: applies the audit's verdicts under the existing single approval gate; converts bare entries to structured form using canonical claims; removes demotion entries; resolves REVIEW entries interactively; updates host entry files to mirror.

8. **`tasks-status.md` rolling-window archive**: Sessions 1–11 archived to `tasks-status-2026-Q2.md` (meta_layer); Sessions 12–14 stay inline. `rules/task-tracking.md` updated with rolling-window discipline declaring inline ≤ 2–3 sessions and quarterly archive convention. New earned-in-0.9.0 entry in `rules/instance-current-manifest.md` documents the archive shape.

**Rationale:** The cost-friction incident `a8e771f0-7686-484d-b89e-cc25e96f8c93` (logged 2026-05-04 against v0.8.0) attacked the bookend's per-invocation cost (Haiku default, quick mode). v0.9.0 attacks the structural per-session-load cost. Operator opened this session by surfacing context-budget bloat: 113.2k at session start, with `Memory files` consuming 83.1k (mostly from the 8-entry auto-load list). Audit of each auto-load file against an earn-by-incident gate ("what fails if this isn't loaded every session?") revealed that 4 of 8 entries failed the gate — their consumer-skills load them directly, single-operator workspaces don't need the multi-instance lattice rule, and the incidents log is consumed only by audit and promotion-ritual review.

The doctrine extension ("earn-by-incident applied to auto-load") generalizes ACW's existing earn-by-incident discipline (governing the deferred library and the recommended-blocks registry) to the most expensive substrate surface in the workspace. Bringing this surface under the same gate closes a structural blind spot.

The discipline propagates to downstream instances via `/acw-instance upgrade`: the new rule lands in template_layer and instance-current-manifest; the demotions DO NOT auto-propagate (each instance owns its own auto-load list); the audit verb's per-instance walk proposes demotions when an instance's bloated list contains canonical-demotion candidates. This separation is correct — doctrine flows downstream automatically; list curation stays operator-driven per workspace.

**Source:** Operator session 2026-05-04 immediately following v0.8.0 ship. Operator surfaced context-budget bloat via screenshot, then directed: "I'd like somehow for the 'Project substrate (auto-loaded every session)' to earn its ship." Then: "instances doing acw instance audit should be audited for demotions." Then: "Get it all done. there should be nothing for 1.0.0."

**Auto-load context savings:** ~30k off session-load when fully applied:
- `rules/manifest-discipline.md` (5.2k)
- `rules/instance-current-manifest.md` (11.5k)
- `rules/multi-instance-topology.md` (5.2k)
- `incidents.jsonl` (~3k current; grows unboundedly)
- `tasks-status.md` Done section (~7k via archive split)

**Open follow-ups:**

- **Backward-compat soak.** Bare-path entries remain valid in v0.9.0 (parser accepts both shapes; audit flags as `legacy-pending-review`). If parser ambiguities surface in the wild, fix forward; do not roll back.
- **`rules/auto-load-discipline.md` canonical recommendations may need expansion.** Today's recommendation list is four entries. If a future incident demonstrates a path that materially earns auto-load (skill X failed because file Y was not in context, consistently, across N sessions), expand canonical recommendations and document the incident as the activation evidence.
- **Auto-load enforcement at session-start time.** Currently the discipline gate fires only at audit time. A v0.10.0+ harness could surface a "auto-load discipline drift" warning at session start when the workspace carries entries declared as demotion candidates. Earn-by-incident: surface only after operator runs into the same demotion three times across three audits.
- **Instance-specific override claims may drift.** When an operator declares an instance-specific entry with a claim, the claim doesn't auto-validate over time — the file's content may evolve such that the claim no longer holds. No detection mechanism in v0.9.0; would earn its build if drift surfaces.

**Risks:**

- **Risk: parser accepts both shapes; misformed structured entries may fail silently.** Mitigation: `validate()` raises `ManifestError` on missing `path` field or duplicate paths; release gate runs validate; future audit verb invocation surfaces malformed entries as `[?]` REVIEW rows.
- **Risk: consumer-skill must load demoted files itself.** Already true in current implementation (skills read paths directly from `acw-state.yaml::paths`; the demoted files are read via skill action, not via auto-load context). No change needed.
- **Risk: downstream instances at `last_reconciled_version` < 0.9.0 will see a v0.9.0 drift alert mentioning `rules/auto-load-discipline.md` AND a separate audit-driven proposal to demote their own auto-load entries.** The two are sequential: first run `/acw-instance upgrade` to land the rule + bump last_reconciled_version; second run `/acw-instance audit` to propose demotions. Documented in upgrade reference.

### D-ACW-036 — `/acw-instance audit|upgrade` rewritten to adopt-and-migrate model; `integrations/` scope refined; ship as v0.7.0

**Date:** 2026-05-03
**Decision:** Three changes ship together as v0.7.0:

1. `skills/acw-instance/` rewritten to embody the adopt-and-migrate mental model. Audit produces a migration plan (per-file table: source → canonical destination → action) instead of an interactive Mode A/B walk. Upgrade executes the plan under a single approval gate, performing renames, format reshapes, content merges, and source deletions in one bulk operation. Substrate boundary made explicit: migration applies to recognized canonical paths (decisions/, rules/, research/, briefings/, runbooks/, integrations/, context/, inbox/, _buffer/, skills/, tools/, glossary.md, tasks-status.md, build-log.md, incidents.jsonl, CLAUDE.md, AGENTS.md, acw-state.yaml) plus substrate-shaped patterns (frontmatter class/authority/stability, dated capture files, jsonl); everything else (project code, data, configs, tests) stays untouched. For coding projects: substrate scaffolds alongside untouched code. Pre-migration safety commit recommended (offered when workspace is git-untracked); plan approval gate is the load-bearing safety surface. Interactive prompts reserved only for ambiguous routings flagged `[?]`; default behavior makes the routing call from canonical knowledge.

2. `integrations/` scope refined: `integrations/<system>/` covers BOTH documentation AND integration-specific operational scripts that are tightly coupled to one external system (bulk-push tools, sync utilities, data extractors, auth helpers). Boundary with `tools/`: tools/ holds general-purpose utilities; integrations/<system>/ holds tooling that exists only because the integration exists ("if you removed the integration, the script would be deleted with it"). Updated in `tools/templates/integrations-README.md.tmpl` and `rules/instance-current-manifest.md` § integrations entry.

3. ACW version bumped 0.6.1 → 0.7.0 reflecting the substantive `/acw-instance` behavior change. No new manifest registry entries earned; existing recommended-blocks list is unchanged. Downstream instances at `last_reconciled_version` 0.6.1 stay drift-clean (no new earned-in entries to flag).

**Rationale:** Today's `_Command` migration dogfood produced the earned-by-incident evidence for both refinements. The v0.4.0/v0.5.0 interactive Mode B walk forced the operator into nine routing prompts when six of the nine had clear canonical destinations after v0.6.0 absorbed the cockpit cluster. Operator's directive verbatim: *"that's what I want the skill to do. I want the skill to really perfectly ACW can absorb everything we have here, and it's going to do it. We've been doing better when I lose any context. It's going to actually keep it all but make it all better."* The `_Command/integrations/zoho-desk/push_direct.py` finding (an operational direct-HTTP pusher co-located with Zoho integration docs) revealed that `integrations/<system>/` wants both docs and integration-coupled scripts; current canonical README implied scripts did not belong. Migration model proves out under load: 18 file moves, 11 reshapes, 11 new canonical files, 9 deletes, one-shot via subagent-parallelized authoring + sequential write+delete, with pre-migration commit at cb39d32 as rollback path.

**Source:** Operator session 2026-05-03; `_Command` migration commits at cb39d32 (pre-migration), 7ea96e7 (migration), e179bbf (missing template_layer rules backfill). Workstream B subagent rewrite of `skills/acw-instance/SKILL.md`, `references/audit.md`, `references/upgrade.md`. Companion D-CMD-001 in `_Command/decisions/decision-log.md`.

**Open follow-ups (per Workstream B subagent):**
- Plan persistence: not persisted to disk between audit and upgrade (deterministic regeneration). May earn a `--save-plan` flag if substrate races become an incident.
- Adopt-mode hard-stop (D-ACW-022) is now structurally redundant with the plan-approval gate. Schema retained for backward compat; formal retirement deferred to a future decision-log entry.
- "Verify content at destination before deleting source" is documented but not mechanically enforced; may earn a checksum step from a future incident.
- Cross-repo writes still rely on `cross_repo_writes` declaration; capability broker (deferred per `rules/capability-broker.md`) remains the eventual replacement.

---

## Constraints and Gotchas

### C-001 — `skills/capture-session/` directory still exists on disk

`skills/capture-session/` is marked superseded in its SKILL.md frontmatter (`status: superseded`, `superseded_by: skills/capture-and-metabolize/`) but the directory itself was not removed. The careful guardrail blocked automated `rm -rf`. Operator must delete manually before the v0.2.0 tag.

### C-002 — Synapse copies still stale

Per Incident D-01, `~/synapse/Rules/Procedures/` copies are still stale relative to `/Projects/acw/rules/`. Mitigation deferred to a separate session.

---

## Resolved Questions

*(No entries yet.)*
