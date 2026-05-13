---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Instance Current Manifest

Declarative registry of recommended blocks an ACW instance should carry to be current with this version of ACW. The session-start bookend (`/acw-session start`) reads this file, compares against the instance's `acw-state.yaml`, and surfaces a one-line drift alert when gaps are detected. The `/acw-instance upgrade` verb walks the operator through reconciliation.

Each entry below documents one recommended block: what it is, why it helps, whether it's required, how to add it, and the ACW version in which it earned its build. The drift check uses the **earned in** field to suppress alerts for blocks that landed before the instance's `last_reconciled` date.

The current ACW version is declared in `acw-state.yaml::version`. An instance is "current" when every recommended block whose `earned in` is at-or-before the ACW version is present in its state file.

---

## `project` block

- **What:** A `project:` block in `acw-state.yaml` with `name`, `code`, `domain` fields.
- **Why it helps:** Enables `D-{CODE}-NNN` and `HR-{CODE}-NNN` id prefixing in the decision log and hard-rules file. Names the project in narrative output. Without it, ids ship unprefixed and narrative falls back to the repo's directory name.
- **Required:** No. The bookend skill ships unprefixed ids (`D-NNN`, `HR-NNN`) when the block is absent.
- **How to add:** Edit `acw-state.yaml`. Add a top-level block:
  ```yaml
  project:
    name: "<human-readable name>"
    code: "<short identifier, e.g. 'ACW' or 'CP'>"
    domain: "<primary domain>"
  ```
- **Earned in:** `0.2.0-rc3`.

## `paths` block

- **What:** A `paths:` block in `acw-state.yaml` listing every substrate file path.
- **Why it helps:** Decouples the bookend skills from hardcoded paths. The skills read paths from this block at runtime. Future template evolution that moves a substrate file requires only one edit per instance instead of grepping skills.
- **Required:** No (canonical defaults apply when absent — see `rules/manifest-discipline.md`). Effectively load-bearing in practice; absent instances run on defaults silently, but operators are encouraged to add the block for clarity even if no overrides are needed.
- **How to add:** Edit `acw-state.yaml`. Add a top-level block matching the canonical defaults:
  ```yaml
  paths:
    decisions_log: decisions/decision-log.md
    tasks_status: tasks-status.md
    build_log: build-log.md
    glossary: glossary.md
    threat_model: threat-model.md
    incidents: incidents.jsonl
    evolution: research/evolution.md
    sources: research/sources.md
    research_state: research/research-state.yaml
    problem_framing: research/01-problem-framing.md
    session_captures_dir: research/sessions
    research_queries_dir: research/queries
    research_queries_consumed_dir: research/queries/_consumed
    buffer_dir: _buffer
  ```
  Override any key the instance places elsewhere; omit keys that match the default.
- **Earned in:** `0.2.0-rc4`.

## `auto_load_at_session_start`

- **What:** A list block in `acw-state.yaml` naming files agent hosts auto-load at session start. From v0.9.0, entries are structured (`path` / `claim` / `earned_by`); bare-path entries remain valid as a backward-compat form (treated as `legacy-pending-review` by the audit verb).
- **Why it helps:** The cross-vendor contract per `AGENTS.md` directive 7. Each host implements via its native mechanism (Claude Code: `@`-imports in `CLAUDE.md`). The structured form earns each entry's slot per `rules/auto-load-discipline.md`.
- **Required:** No. When absent, the host has no canonical auto-load list and either reads nothing automatically or relies on host-specific files only.
- **How to add:** Edit `acw-state.yaml`. Canonical default (matches the v0.9.0 default for new instances) — four entries that earned their slot per `rules/auto-load-discipline.md`:
  ```yaml
  auto_load_at_session_start:
    - path: decisions/decision-log.md
      claim: "Recently decided history must be visible to agents at session start; without it agents re-litigate settled choices."
      earned_by: structural
    - path: rules/instance-hard-rules.md
      claim: "Stop-work rules must be visible to every agent at session start; loading them on demand is too late."
      earned_by: structural
    - path: tasks-status.md
      claim: "Pending work surface must be visible at session start; without it agents propose duplicate work and lose continuity."
      earned_by: structural
    - path: glossary.md
      claim: "Vocabulary canon prevents drift to colloquial English in agent output."
      earned_by: structural
  ```
  Each new entry MUST declare a structured `claim` and `earned_by`. Adding to or removing from the list is governed by `rules/auto-load-discipline.md`. The audit verb walks the list and proposes demotion for entries that fail the gate.
- **Earned in:** `0.2.0-rc1`. Set expanded in `0.2.0-rc4` to seven entries to include manifest-discipline and instance-current-manifest. **Restructured in `0.9.0`** to structured form with discipline gate; canonical recommendations narrowed to four entries (the four declared `earned_by: structural` above). Demoted from canonical: `rules/manifest-discipline.md`, `rules/instance-current-manifest.md`, `rules/multi-instance-topology.md`, `incidents.jsonl` — each consumer-skill loads them directly.

## `template_layer`, `instance_layer`, `meta_layer`

- **What:** Three list blocks classifying every file in the workspace per `rules/manifest-discipline.md`.
- **Why it helps:** Workspaces that serve as both an instance and a template (i.e., spawn child workspaces) need explicit classification so the scaffold tool knows what to propagate and what to keep local. One-off instances that don't spawn children can leave these blocks empty and absorb no overhead.
- **Required:** No. Blocks may be present-but-empty or absent. The bookend skill's manifest-classification step silently skips when blocks are empty.
- **How to add:** Edit `acw-state.yaml`. See `rules/manifest-discipline.md` for the schema and the default-to-instance discipline.
- **Earned in:** `0.2.0-rc2`.

## `empty_dirs`

- **What:** A list block naming directories the scaffold tool creates with `.gitkeep` markers when scaffolding a child instance.
- **Why it helps:** Ensures the canonical directory layout is present in scaffolded children from session zero, even when the directories start empty.
- **Required:** No. Workspaces that don't spawn children can leave the block empty or absent.
- **How to add:** Edit `acw-state.yaml`. Typical defaults:
  ```yaml
  empty_dirs:
    - research/sessions
    - research/queries
    - research/queries/_consumed
    - skills
    - deferred
  ```
- **Earned in:** `0.2.0-rc2`.

## `cross_repo_writes`

- **What:** A list block enumerating absolute paths outside the project repo that the bookend skill is allowed to write to.
- **Why it helps:** Vault-boundary discipline. By default the skill refuses to write outside the project repo. Instances that legitimately need cross-repo writes (e.g., publishing to a docs site, dropping notifications into a shared inbox) declare those targets explicitly here.
- **Required:** No. Empty list or absent block means no external writes allowed.
- **How to add:** Edit `acw-state.yaml`. List paths the skill may write to.
- **Earned in:** `0.2.0-rc1`.

## `synapse_log_path`

- **What:** A scalar string declaring an operator-personal cross-project day-index directory. The bookend skill's Phase 4 appends a session block there.
- **Why it helps:** Provides a per-day cross-project index for operators who work across many projects. Optional convenience.
- **Required:** No. `null` or absent disables Phase 4 entirely; the skill skips silently.
- **How to add:** Edit `acw-state.yaml`. Set `synapse_log_path: <absolute path>` for the operator's personal day-index directory.
- **Earned in:** `0.2.0-rc1`.

## `voice`

- **What:** A list block declaring voice-reference files applied during transcript cleanup in Phase 1.
- **Why it helps:** Lets the skill enforce the operator's voice conventions (brand voice, customer voice, etc.) when cleaning the transcript before persistence.
- **Required:** No. Empty list or absent means no voice opinion.
- **How to add:** Edit `acw-state.yaml`. List paths to voice-reference files.
- **Earned in:** `0.2.0-rc1`.

## `is_canonical_source`

- **What:** A scalar boolean flag in `acw-state.yaml` declaring whether this instance publishes canonical content downstream to other instances.
- **Why it helps:** Gates the propagation behavior in `capture-and-metabolize` Phase 2. Instances with `is_canonical_source: true` (e.g., ACW itself) get a "canonical file edited — confirm version bump and push to GitHub" prompt when an auto-loaded template_layer file is touched. Instances with the flag absent or false (every child instance, the default) get a different warning when they hand-edit a template_layer file: "this is a canonical file from upstream; local edits won't propagate and may be overwritten on next /acw-instance upgrade." The flag separates "I am the source of truth for downstream" from "I consume canonical truth from upstream."
- **Required:** No. Default is `false` (treat as a downstream consumer). Set explicitly only on instances that publish canonical content (ACW itself; future canonical-publishing meta-instances).
- **How to add:** Edit `acw-state.yaml`. Add a top-level scalar:
  ```yaml
  # Set to true ONLY on instances that publish canonical content downstream.
  # ACW itself sets this to true. Every child instance defaults to false.
  is_canonical_source: false
  ```
- **Earned in:** `0.3.0`.

## `rules/multi-instance-topology.md`

- **What:** A template_layer rule file declaring the lattice model, knowledge-placement discriminator (org-brain vs departmental), and reference-not-duplicate principle for organizations running multiple coordinated ACW instances. Also documents the three-flow resolution model (adopt / absorb / instance-specific), absorption candidate format, divergence markers, re-adoption flow, and cross-repo write governance.
- **Why it helps:** Bakes the lattice framing into every scaffolded instance from day one. When an operator's work scales beyond a single domain (multiple departments, multiple operators, cross-domain knowledge references), the rule already has the framing for "where does this knowledge go." Closes the articulation gap at organizational scale by giving agents a normative reference for the lattice shape and the absorption mechanics.
- **Required:** No. Single-instance operators may ignore the rule. Earned-experimental, not normative until lattice-level incidents earn promotion.
- **How to add:** Run `/acw-instance upgrade`, which fetches the canonical content from GitHub and walks the operator through adoption. Or manually: copy `rules/multi-instance-topology.md` from ACW canonical into the instance's `rules/` directory. Add the path to `template_layer` in `acw-state.yaml` (recommended) and to `auto_load_at_session_start` (recommended).
- **Earned in:** `0.3.0`.

## `_buffer` directory

- **What:** A `_buffer/` directory at the workspace root. Every instance has one. Read by `/acw-session start` at session-start to surface unread cross-project notifications. Receives absorption candidates and other cross-instance handoffs. (Renamed from `_inbox/` in v0.5.0 per DIP vocabulary canon — "buffer" is the canonical term for a holding area awaiting processing; the rename also clears semantic space for the operator-facing `inbox/` surface arriving in v0.6.0.)
- **Why it helps:** The seed cross-instance handoff mechanism. Without a `_buffer/`, the lattice handoff design has no destination — workspaces can't notify each other, and absorption candidates have nowhere to land. Listed in `empty_dirs` so the scaffold tool creates it with `.gitkeep` for fresh instances.
- **Required:** Recommended (the lattice handoff design assumes its presence). Empty list / absent in `empty_dirs` means scaffold won't create one.
- **How to add:** Edit `acw-state.yaml::empty_dirs` to include `_buffer`. For existing instances missing the directory, also create `_buffer/.gitkeep` manually or via `mkdir`. Existing instances on v0.4.0 with `_inbox/` directories should rename their directory to `_buffer/` and update `paths.buffer_dir` accordingly; `/acw-instance upgrade` v0.5.0+ proposes this migration when it detects the old name.
- **Earned in:** `0.4.0` (originally as `_inbox`); renamed `_buffer` in `0.5.0`.

## `divergent_pending_review`

- **What:** A list block in `acw-state.yaml` recording substrate files that diverge from ACW canonical and have an absorption candidate sent to ACW awaiting upstream review. Each entry: `path`, `absorption_candidate` (path to the `_buffer/` note in ACW), `sent_date`, `status` (`pending` | `absorbed` | `rejected`).
- **Why it helps:** Lets `/acw-instance upgrade` respect pending entries — does not propose canonical changes to those files until ACW resolves the absorption review. Schema and resolution mechanics in `rules/multi-instance-topology.md` § "Re-adoption flow."
- **Required:** No. Empty list or absent means the workspace has no pending absorption candidates. Most workspaces will have an empty block until the audit verb fires for the first time.
- **How to add:** Edit `acw-state.yaml`. Add the block as an empty list to opt in:
  ```yaml
  divergent_pending_review: []
  ```
  Subsequent `/acw-instance audit` runs append entries when the operator routes a divergence to absorption.
- **Earned in:** `0.4.0`.

## `instance_specific_substrate`

- **What:** A list block in `acw-state.yaml` recording substrate files or directories that intentionally diverge from ACW canonical and will not be promoted upstream. Each entry: `path`, `rationale` (one-line reason), `decision_ref` (decision-log entry id).
- **Why it helps:** Lets `/acw-instance upgrade` recognize substrate that is uniquely the workspace's. Without this marker, every audit run would re-flag the same divergences. Schema in `rules/multi-instance-topology.md` § "Divergence markers."
- **Required:** No. Empty list or absent means no instance-specific substrate. Workspaces that genuinely have unique substrate (e.g., department-specific operational journals not generalizable upstream) declare entries here, each with a decision-log reference explaining the rationale.
- **How to add:** Edit `acw-state.yaml`. Add the block as an empty list to opt in. Adding entries requires a decision-log entry first; the entry id goes in `decision_ref`.
- **Earned in:** `0.4.0`.

## `runbooks/` directory

- **What:** A `runbooks/` directory at the workspace root. Holds operator-facing how-to docs that aren't part of any skill — *"how I onboard a new vendor,"* *"how I run the weekly metrics review,"* *"how to deploy this codebase."* Markdown files; no enforced subdirectory structure.
- **Why it helps:** Workspaces accumulate operational how-to content that doesn't fit anywhere else in canonical substrate. Without `runbooks/`, this content scatters into skill `references/` (where it doesn't belong unless the runbook is skill-specific) or into ad-hoc files. A canonical `runbooks/` directory gives operator runbooks a clean home.
- **Required:** No. Workspaces with no operator runbooks can leave the directory empty or absent. Recommended for any workspace with recurring operations the operator runs by hand.
- **How to add:** Edit `acw-state.yaml::empty_dirs` to include `runbooks`. Drop runbook markdown files in directly. Operator decides naming convention per workspace.
- **Earned in:** `0.5.0`.

## `integrations/` directory

- **What:** An `integrations/` directory at the workspace root. Holds documentation about external systems this workspace talks to (APIs, MCP servers, adapters, webhooks, anything cross-system) AND integration-specific operational scripts that are tightly coupled to one external system (bulk-push tools, sync utilities, data extractors, auth helpers). Ships with a `README.md` template that explains the docs+scripts convention and the boundary between `integrations/<system>/` (system-coupled) and `tools/` (general-purpose).
- **Why it helps:** Most instances that touch external systems accumulate both "how this integration works" docs AND integration-specific operational scripts. Without canonical naming, workspaces invent their own (`adapters/`, `mcp/`, scattered notes in skill `references/`, scripts dumped into general `tools/`). Naming this surface canonically standardizes the pattern and keeps integration-coupled tooling co-located with its docs rather than scattered.
- **Required:** No. Workspaces with no external integrations can leave the directory empty or absent. Recommended for any workspace with at least one external system integration.
- **How to add:** Add `integrations/README.md` to `acw-state.yaml::instance_layer` with `template: tools/templates/integrations-README.md.tmpl`. The scaffolder renders the README at scaffold time. Per-integration subdirectories (e.g., `integrations/zoho-desk/`, `integrations/slack-mcp/`) are operator-organized; no canonical structure beyond the README.
- **Earned in:** `0.5.0`.

## `briefings/` directory

- **What:** A `briefings/` directory at the workspace root. Holds dated agent-generated aggregated snapshots — daily briefings, weekly reviews, status reports, on-demand snapshots. Markdown files with `YYYY-MM-DD-<topic>.md` naming convention. Pattern is universal: *"agent-generated snapshot of state at a moment in time."* Content varies by workspace type:
  - **Cockpit** — calendar + tasks + email + integrations aggregated.
  - **Project** — PR status + build results + recent issues + deploy logs aggregated.
  - **Full / org-brain** — cross-domain rollups, state-of-the-org snapshots.
- **Why it helps:** Many workspace types benefit from a "this is what the system produced for me at moment X" surface. Generated by triage/aggregation skills. Distinct from `_buffer/` (system handoffs) and `inbox/` (operator captures, arriving v0.6.0). Each surface has its own lifecycle: buffer items get processed, briefings accumulate dated and archived rarely.
- **Required:** No. Workspaces without briefing skills can leave the directory empty or absent.
- **How to add:** Edit `acw-state.yaml::empty_dirs` to include `briefings`. Briefing skills write dated files into the directory; the operator (or `/acw-session start`) reads the latest at session-start.
- **Earned in:** `0.5.0`.

## `context/` directory

- **What:** A `context/` directory at the workspace root holding lightweight pointers to operating reality. Four canonical files: `goals.md` (long-arc goals), `objectives.md` (current near-term focus), `how-i-work.md` (operator preferences, schedule, communication), `key-people.md` (who matters in this workspace's domain). Read on demand by agents that need the context, not auto-loaded into every chat.
- **Why it helps:** Distinct from decisions (specific choices), rules (governance), skills (operations), or glossary (vocabulary). Captures the "operating reality" that agents need to calibrate their work — what the workspace is for, who matters, how the operator works — without bloating every chat's context window. Especially load-bearing for cockpit-shaped instances where personal + business context blends; useful in any workspace type.
- **Required:** No. Workspaces with thin context can leave `context/` empty or absent. Recommended for any workspace where agents would benefit from operator-/project-context cues beyond what canonical substrate captures.
- **How to add:** Add four entries to `acw-state.yaml::instance_layer` mapping each canonical file to its template:
  ```yaml
  - path: context/goals.md
    template: tools/templates/context-goals.md.tmpl
  - path: context/objectives.md
    template: tools/templates/context-objectives.md.tmpl
  - path: context/how-i-work.md
    template: tools/templates/context-how-i-work.md.tmpl
  - path: context/key-people.md
    template: tools/templates/context-key-people.md.tmpl
  ```
  Scaffolder renders the four files at scaffold time. Operator fills them with workspace-specific content. Updates happen as operating reality shifts (new goal, person moves on, working preference changes), not on a schedule.
- **Earned in:** `0.6.0`.

## `inbox/` directory

- **What:** An `inbox/` directory at the workspace root holding the operator's untriaged items. Folder of dated markdown files (`YYYY-MM-DD-<topic>.md`) plus optional loose entries. Operator captures things mid-session ("remember this for later") or triage skills route external items in (calendar surfacing, email digest, etc.). Items get processed and removed: routed to `tasks-status.md::Pending` (committed work), parked, or deleted.
- **Why it helps:** Distinct from `_buffer/` (system surface for cross-instance handoffs) and from `briefings/` (agent-generated dated snapshots). Inbox is the operator's *write* surface for raw inbound items needing triage; buffer is the system's *write* surface for cross-instance messages; briefings are agent-generated *read* surfaces for aggregated snapshots. Three different surfaces, three different lifecycles.
- **Required:** No. Workspaces without operator-capture flow can leave `inbox/` empty or absent. Recommended for any workspace where the operator wants a triage queue distinct from the workspace task tracker.
- **How to add:** Edit `acw-state.yaml::empty_dirs` to include `inbox`. Scaffolder creates the directory with `.gitkeep`. Operator captures into it directly or via triage skills.
- **Earned in:** `0.6.0`.

## `sessions/` at root

- **What:** Session captures live in `sessions/` at the workspace root, not under `research/`. The default for `paths.session_captures_dir` is `sessions`. Existing instances on v0.7.0 or earlier with substrate at `research/sessions` either keep the override in their `acw-state.yaml::paths` block or migrate via `git mv research/sessions sessions`.
- **Why it helps:** Session captures are operational logs (what happened in this session, what was decided, what's pending), not research artifacts (problem framing, design notes, queued prompts). Naming them with their actual purpose at root improves the workspace's mental model and clears semantic space in `research/` for what `research/` actually holds.
- **Required:** No. Workspaces that override `paths.session_captures_dir` to a different location remain valid.
- **How to add:** Edit `acw-state.yaml::paths`. Set:
  ```yaml
  paths:
    session_captures_dir: sessions
  ```
  Edit `acw-state.yaml::empty_dirs`: replace `research/sessions` with `sessions`. Migrate any existing capture files: `git mv research/sessions sessions`.
- **Earned in:** `0.8.0`.

## `.current-session` tracker

- **What:** A single-line file at `<paths.session_captures_dir>/.current-session` containing the relative filename of the active capture. Created by `/acw-session start`; read (or self-bootstrapped) by `/acw-session update`; cleared by `/acw-session end`.
- **Why it helps:** Lets `/acw-session update` append timestamped notes to the active capture without taking a filename argument. Without the tracker, every `update` invocation would have to either prompt the operator for the filename or glob the directory and guess the latest. The tracker makes the active session a first-class state.
- **Required:** No. Workspaces that don't use the `update` verb can ignore the tracker; `start` will still create it but no consumer reads it. Cost: one tiny file.
- **How to add:** No state-file change required. The tracker is created and managed by the bookend skills automatically. The first `/acw-session start` after upgrade writes it.
- **Earned in:** `0.8.0`.

## `plans/` directory

- **What:** A `plans/` directory at the workspace root holding plan artifacts. Plans saved as dated markdown (`plans/YYYY-MM-DD--<slug>.md`) — operational outputs from planning agents (e.g., the Plan agent's structured plans, ExitPlanMode outputs) or operator hand-written plans. Distinct from `decisions/` (governance choices), `tasks-status.md` (live work tracker), and `research/` (design notes) — plans are *intent before execution*, written before substantive work begins, and either get executed (then archived) or get parked.
- **Why it helps:** Plans currently land in the global Claude Code state directory (`.claude/`) or in chat-only ephemeral form. Both lose the plan to the workspace's history. Routing plans into instance substrate makes them durable, git-tracked, and reviewable across sessions. Plans are operational artifacts; instance-substrate is where operational artifacts belong.
- **Required:** No. Workspaces with no plan-driven workflow can leave the directory empty or absent. Recommended for any workspace with substantive multi-session features, refactors, or investigations.
- **How to add:** Edit `acw-state.yaml::empty_dirs` to include `plans`. Add canonical default path to `acw-state.yaml::paths`:
  ```yaml
  paths:
    plans_dir: plans
  ```
  Scaffolder creates the directory with `.gitkeep`. Operator (or planning agents) write plans there directly. v0.8.0 ships convention only — no automatic writer skill; the writer earns its build when convention demands automation.
- **Earned in:** `0.8.0`.

## `model:` frontmatter for bookend skills

- **What:** `skills/acw-session/SKILL.md` declares `model: claude-haiku-4-5` in frontmatter. Phase steps that need real reasoning (Phase 3 operator-confirm proposals, Phase 5 research-prompt construction, meta-layer trigger proposed-edit text) escalate to Sonnet inline. Bookend invokes a fresh subagent context to avoid inheriting the parent session's larger-context pricing.
- **Why it helps:** The bookend's work is overwhelmingly mechanical — read transcript, append to file, classify against manifest. Running it at the most expensive Claude variant (Opus 4.7 1M context, the parent session's likely default) is structurally wrong. Haiku-grade is correct for 80%+ of phases. Earned by the cost-friction incident logged in v0.8.0 (operator hit halfway through Max-plan weekly budget after 2 days, with `/acw-session end` taking 7-10 minutes per invocation).
- **Required:** No. The field may not be honored by all Claude Code versions; if not honored, the skill still works at whatever model the harness picks. No breakage.
- **How to add:** Edit `skills/acw-session/SKILL.md` frontmatter:
  ```yaml
  ---
  name: acw-session
  ...
  model: claude-haiku-4-5
  ---
  ```
  Operators wanting to override per-instance can change the model field; not normative.
- **Earned in:** `0.8.0`.

## `rules/auto-load-discipline.md`

- **What:** A template_layer rule file declaring earn-by-incident applied to the auto-load list. Every entry in `auto_load_at_session_start` MUST declare a structured claim ("what fails if this isn't loaded every session?") and an `earned_by` field. The rule includes canonical recommendations (the four files ACW recommends) and declared demotion candidates (paths that fail the gate).
- **Why it helps:** The auto-load list is the most expensive substrate surface in the workspace. Every entry costs context every chat. Without an earn-by-incident gate, the list bloats accumulatively, costing real money across thousands of agent invocations per week. The discipline rule applies the same earn-by-incident discipline that governs the deferred library and the recommended-blocks registry, but for auto-load specifically.
- **Required:** No. Workspaces that don't run `/acw-instance audit` won't enforce the discipline; the rule's gate fires only at audit time. Recommended for any workspace where the operator wants to reduce session-load context cost.
- **How to add:** Run `/acw-instance upgrade`, which fetches the canonical content from GitHub and walks the operator through adoption. Or manually: copy `rules/auto-load-discipline.md` from ACW canonical into the instance's `rules/` directory. The rule is loaded by `/acw-instance audit` when it walks the workspace's `auto_load_at_session_start` block; not auto-loaded into chat context.
- **Earned in:** `0.9.0`.

## `rules/substrate-boundary.md`

- **What:** A template_layer rule file declaring the in-scope / out-of-scope partition that `/acw-instance audit|upgrade` reads when identifying the substrate boundary. Owns the project-content exclusion list (build/dependency directories, package manifests, source file extensions) plus the substrate-shaped pattern signals. Authoritative source: extends authoritative state-file blocks (`template_layer`, `instance_layer`, `paths`, `empty_dirs`, `meta_layer`) with the language-/build-tool-specific exclusions those blocks don't capture.
- **Why it helps:** Previously the project-content exclusion list lived inline in `skills/acw-instance/SKILL.md` prose. Adding a new ecosystem's build output or source extension required editing skill prose, which was easy to miss when canon evolved. Moving the list to its own rule makes the skill a pure consumer of canonical sources: when a new exclusion is added here, the skill picks it up on next canonical fetch.
- **Required:** No. Workspaces that don't run `/acw-instance audit` don't consult the rule. The skill loads it on demand at boundary-identification time; not auto-loaded into chat context.
- **How to add:** Run `/acw-instance upgrade`, which fetches the canonical content from GitHub and lands it under `rules/`. Or manually: copy `rules/substrate-boundary.md` from ACW canonical into the instance's `rules/` directory.
- **Earned in:** `0.9.4`. Earned-by-incident: the audit of `skills/acw-instance/` for canon-vs-rules redundancy found the exclusion list as one of 10 sites where the skill carried inline content that belonged in an authoritative source. See `decisions/entries/D-ACW-044` (skill-redundancy refactor).

## `tasks-status-YYYY-Q*.md` archive (weekly rolling-window discipline)

- **What:** Archive files for older `tasks-status.md::Done` session blocks. Format `tasks-status-YYYY-Q*.md` (e.g., `tasks-status-2026-Q2.md`). Live at workspace root. Classified `meta_layer` (about the instance's history; not propagated to children). Replace archived content in `tasks-status.md` with a one-line pointer.
- **Why it helps:** `tasks-status.md` is auto-loaded at session start. Inline Done entries cost context every chat. The weekly rolling-window discipline keeps the file lean while preserving full history in archive files. Build-log narrative covers the same period in fuller form; archive is the structured-task version.
- **Required:** No. Instances with thin Done logs can leave Done inline indefinitely. Earned when Done blocks age past 7 days OR the file's auto-load cost surfaces as friction (>~15k tokens).
- **How to add:** When the weekly cadence or threshold fires, operator (or `/acw-session end` proposal) creates `tasks-status-YYYY-Q*.md` with frontmatter (class: archive, authority: derived, stability: stable, loaded_by_agent: no), copies older Done blocks into it, and replaces the archived content in `tasks-status.md` with a pointer line. See `rules/task-tracking.md` § "Rolling-window discipline." Add the archive file to `acw-state.yaml::meta_layer`.
- **Earned in:** `0.9.0`. Cadence aligned to weekly in `0.9.1` (was session-count-based; see `decisions/decision-log.md::D-ACW-042`). Same shape applies symmetrically to `decision-log-YYYY-Q*.md` per the entry below.

## `decision-log-YYYY-Q*.md` archive (weekly rolling-window discipline)

- **What:** Archive files for older `decisions/decision-log.md::Decisions and Rationale` entries. Format `decisions/decision-log-YYYY-Q*.md` (e.g., `decision-log-2026-Q2.md`). Live alongside the live file in the workspace's `decisions/` directory. Classified `meta_layer` (about the instance's history; not propagated to children). Replace archived block in the live file with one italicized pointer line. Open Questions, Constraints and Gotchas, and Resolved Questions sections do not archive — they're active surfaces, not historical narrative.
- **Why it helps:** `decisions/decision-log.md` is auto-loaded at session start. Inline entries cost context every chat across every workspace where the file is loaded. The weekly rolling-window discipline keeps the file lean while preserving full historical reasoning in archive files. Mirrors the `tasks-status` archive shape under one unified rule pattern.
- **Required:** No. Instances with thin decision logs can leave entries inline indefinitely. Earned when entries age past 7 days OR the file's auto-load cost surfaces as friction (>~15k tokens, threshold from `rules/auto-load-discipline.md`).
- **How to add:** When the weekly cadence or threshold fires, operator (or `/acw-session end` proposal) creates `decisions/decision-log-YYYY-Q*.md` with frontmatter (class: archive, authority: derived, stability: stable, loaded_by_agent: no), copies older "Decisions and Rationale" entries into it, and replaces the archived block in the live file with a pointer line citing the entry id range and date range. See `rules/decision-tracking.md` § "Rolling-window discipline." Add the archive file to `acw-state.yaml::meta_layer`.
- **Earned in:** `0.9.1`. Doctrine-completion patch on `0.9.0` — the threshold for decision-log was named in v0.9.0's `rules/auto-load-discipline.md` caveat but the rolling-window mechanism for `decision-log` (analogous to v0.9.0's tasks-status pattern) was missing. v0.9.1 closes the gap and unifies cadence (weekly) across both surfaces. See `decisions/decision-log.md::D-ACW-042`.

## `adopt_mode_organic_threshold`

- **What:** A scalar integer in `acw-state.yaml` setting the threshold above which `/acw-instance upgrade` adopt-mode bails (with pointer to `/acw-instance audit`) instead of offering automatic adoption. Counts markdown files in `decisions/` and `rules/` excluding canonical files copied from ACW.
- **Why it helps:** Prevents adopt mode from steamrolling workspaces with substantial organic substrate (the `_Command` problem). Below threshold = canonical-shaped-but-unregistered, safe to adopt. At-or-above threshold = organic substrate, audit required first to route divergences before any writes fire.
- **Required:** No. Default value is `5` (canonical defaults applied when key absent). Tunable per-instance only when the default produces wrong-direction failures in practice.
- **How to add:** Edit `acw-state.yaml`. Add a top-level scalar:
  ```yaml
  adopt_mode_organic_threshold: 5
  ```
  Override only with a decision-log entry naming the reason for divergence.
- **Earned in:** `0.4.0`.

---

## How `/acw-session start` reads this file

At session start, the skill walks each entry above. For each entry, the skill compares the entry's **earned in** version against `acw-state.yaml::last_reconciled_version` (NOT against `last_reconciled`, which is a date). Version comparison uses semantic-version ordering with rc-suffixes treated as pre-release (e.g., `0.2.0-rc1 < 0.2.0-rc2 < 0.2.0`).

For each entry whose earned-in version is newer than `last_reconciled_version`, the skill checks whether the block is present in the instance's state file:

- **Block absent from file** → counts as missing; flag.
- **Block present-but-empty** (e.g., `template_layer: []`) → counts as DELIBERATELY OPTED OUT; do not flag. Present-but-empty is the operator's explicit choice.
- **Block present and populated** → not missing; do not flag.

For each entry whose earned-in version is at-or-before `last_reconciled_version`, do not flag regardless of presence. The instance has already been reconciled past that point.

If the gap list is non-empty, the skill emits one alert line:

```
[acw-drift] Your instance is reconciled to ACW <last_reconciled_version> as of <last_reconciled>. Current ACW (<version>) expects N additional blocks: <names>. Run /acw-instance upgrade to reconcile.
```

Otherwise the skill stays silent on drift.

If `last_reconciled_version` is absent from the state file, the skill treats it as `"0.0.0"` — every recommended block whose earned-in version is set will be flagged. This produces a noisy first run for very old instances; running `/acw-instance upgrade` once quiets the alert.

`last_reconciled` is the human-friendly date the reconciliation happened. `last_reconciled_version` is the semantic ACW version the reconciliation synced to. Both are bumped automatically by `/acw-instance upgrade` after a successful reconciliation pass.

## How `/acw-instance upgrade` reads this file

**Single source of truth: GitHub.** The upgrade skill fetches the canonical `rules/instance-current-manifest.md` from the ACW GitHub repo on every run. The instance's local copy of this file is a write-once cache representing "the last canonical I reconciled to" — never used as the comparison yardstick except in extreme offline-degraded mode (not currently shipped).

Fetch path (private repo): use the `gh` CLI, which is already authenticated on the operator's machine:

```
gh api -H "Accept: application/vnd.github.raw" \
   repos/benfrankster-design/acw/contents/rules/instance-current-manifest.md
```

Or equivalent via `urllib.request` with `Authorization: Bearer <PAT>` header pulled from a `GITHUB_TOKEN` env var. If neither path is available (no `gh` CLI, no token), the skill fails closed with a clear error: "cannot fetch canonical manifest from GitHub. Install `gh` and authenticate, or set `GITHUB_TOKEN`, then re-run."

**Adopt mode for unregistered substrate-shaped workspaces.** When the skill is invoked in a workspace where `acw-state.yaml` and/or `rules/instance-current-manifest.md` are missing, the skill scans for substrate signals (presence of `decisions/`, `rules/`, `incidents.jsonl`, `glossary.md`, `research/`, bookend skills under `skills/`). If three or more signals are present, the skill offers adoption: "this looks like an ACW instance that pre-dates registration. Adopt as a formal instance? [yes/no]." On confirmation, the skill writes `acw-state.yaml` (with `last_reconciled_version: "0.0.0"` to drive a noisy first reconciliation) and copies the GitHub-fetched canonical manifest into the instance's `rules/` directory. After adoption, normal gap-walking proceeds.

If substance signals are below threshold, the skill bails with: "this workspace doesn't appear to be an ACW instance. To start one, run `tools/scaffold-instance.py`."

**Walk and reconcile.** With the canonical manifest in hand (whether via GitHub fetch on a registered instance or via adoption write-then-read), the skill walks each entry, detects gaps per the comparison rules above, and surfaces the canonical default content alongside the operator's three options (add as proposed / modify / skip). On confirmation, the skill writes the chosen blocks via `tools/manifest.py::append`, writes the fetched canonical manifest to the instance's local `rules/instance-current-manifest.md` (overwrites the cache), bumps `last_reconciled` and `last_reconciled_version`, and logs a decision-log entry recording the reconciliation.

## Maintenance

When ACW ships a new recommended block in a future version, append a new entry to this file with the same fields (What / Why it helps / Required / How to add / Earned in). The earned-in version sets the floor for when existing instances start seeing the block as drift.

Adding an entry to this file is itself a substrate shift. The bookend skill's Phase 2 host-entry-file maintenance step may propose updates to `CLAUDE.md` (or other host entry files) when a new block enters the recommended registry.
