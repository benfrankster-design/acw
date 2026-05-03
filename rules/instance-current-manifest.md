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

- **What:** A list block in `acw-state.yaml` naming files agent hosts auto-load at session start.
- **Why it helps:** The cross-vendor contract per `AGENTS.md` directive 7. Each host implements via its native mechanism (Claude Code: `@`-imports in `CLAUDE.md`).
- **Required:** No. When absent, the host has no canonical auto-load list and either reads nothing automatically or relies on host-specific files only.
- **How to add:** Edit `acw-state.yaml`. Recommended canonical set (matches the rc4 default for new instances):
  ```yaml
  auto_load_at_session_start:
    - decisions/decision-log.md
    - rules/instance-hard-rules.md
    - rules/manifest-discipline.md
    - rules/instance-current-manifest.md
    - tasks-status.md
    - glossary.md
    - incidents.jsonl
  ```
  Add or remove entries as substrate enters/leaves the auto-load discipline.
- **Earned in:** `0.2.0-rc1`. Set expanded to seven entries in `0.2.0-rc4` to include the manifest-discipline and instance-current-manifest rules.

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

- **What:** An `integrations/` directory at the workspace root. Holds documentation about external systems this workspace talks to — APIs, MCP servers, adapters, webhooks, anything cross-system. Ships with a `README.md` template that explains *"this is where API, MCP, adapter, and external-system documentation lives; organize subdirectories per-integration however the workspace prefers."*
- **Why it helps:** Most instances that touch external systems accumulate "how this integration works" docs. Without canonical naming, workspaces invent their own (`adapters/`, `mcp/`, scattered notes in skill `references/`). Naming this surface canonically standardizes the pattern.
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
