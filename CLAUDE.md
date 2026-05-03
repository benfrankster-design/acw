# acw — project instructions

ACW is its own first instance and also the template that scaffolds derived instances. Working in this repo is "instance of itself" work: every change is both an instance edit (ACW evolves) and a template edit (children inherit). For the layered model, see `LAYERS.md`. For the recurring manifest pattern, see `rules/manifest-discipline.md`.

This file describes how to navigate ACW; it does not duplicate substrate. Specifics that can drift live in the files this file points at.

## Project substrate (auto-loaded every session)

The canonical list lives in `acw-state.yaml::auto_load_at_session_start`. Treat that array as the source of truth; the imports below mirror it. If they disagree, `acw-state.yaml` wins and this file gets reconciled.

@decisions/decision-log.md
@rules/instance-hard-rules.md
@rules/manifest-discipline.md
@rules/instance-current-manifest.md
@rules/multi-instance-topology.md
@tasks-status.md
@glossary.md
@incidents.jsonl

Other substrate is read on demand:
- Append-only narrative (`build-log.md`) and meta-layer documents grow unboundedly; read when you need historical context for a specific phase or design decision.
- Session captures and queued research prompts under `research/sessions/` and `research/queries/` are loaded by `/acw-session start`, not by auto-load.
- Other research artifacts under `research/` are read on demand for design work; promotion into auto-load goes through a decision-log entry.

To boot a new session into full context, run `/acw-session start` first thing.

## Hard rules

The canonical list lives in `rules/instance-hard-rules.md`. The principles below explain the *shape* of what belongs there; specific rules are in that file.

- **Earn-by-incident before tooling.** No deferred primitive promotes without the evidence threshold defined in `rules/promotion-ritual.md`. Single-incident emergency promotion is reserved for prevented incident classes that are structural and cheap to ship.
- **Manifest discipline.** Every new file at a tracked path is classified into one of the manifest layers in `acw-state.yaml`. Default-to-instance. Demotion or removal goes through the decision log.
- **Append-only history.** Files declared append-only in their frontmatter never get past entries edited. Corrections append a new entry that supersedes the old.
- **No vendor coupling in template_layer.** Files that propagate to children must work across hosts. Vendor-specific implementations of `AGENTS.md` directive 7 are instance_layer or scaffolder-generated.
- **The state file wins disagreements with prose.** When `acw-state.yaml` and a prose file conflict, the state file is authoritative and the prose gets a decision-log entry.
- **No `--no-verify`, no force-push to the main branch.** Hooks fail loudly for a reason; investigate the root cause.

## Stack

- Python 3.11+, stdlib only for shipped tools (no external dependencies in the template layer)
- Markdown plus YAML for substrate; UTF-8; LF line endings
- Git for version control
- `unittest` for tests
- Host-agnostic agent contract via `AGENTS.md`; this file is the host-specific implementation for one such host

Model and runtime details are not pinned here. They belong in skill metadata or in a project-specific stack note when the choice is load-bearing for a specific instance.

## Voice

Canon documents (rules, schemas, the entry-point and contract files): formal-spec voice — direct, normative, no hedging. Narrative documents (the meta-layer story files, build-log entries, evolution entries): reflective; honest about tradeoffs and earn-by-incident reasoning. Session captures: structured per the bookend skill's reference files. No customer-voice; no emojis. Em dashes are fine.

## Where things live

Conceptual map; for current contents see the files themselves and the manifest in `acw-state.yaml`.

- **Doctrine** lives in `rules/`. Almost all of it is template_layer; the per-instance carve-out is `rules/instance-hard-rules.md`.
- **Tools** live in `tools/`. Stdlib Python. The `tools/templates/` subdirectory holds the rendered forms of instance_layer files.
- **Skills** live in `skills/`. The bookend pair (`/acw-session start` and `/acw-session end`) is the load-bearing pattern; instance management lives in `/acw-instance audit` and `/acw-instance upgrade`. Other skills follow the role taxonomy in `rules/pipeline-roles.md`.
- **Decisions, tasks, incidents, build narrative, glossary, threat model, state file** live at root as instance_layer.
- **Research** lives in `research/`: problem-framing, evolution, sources, research-state, plus session captures and queued research prompts in subdirectories.
- **Meta-layer narrative** (story files, license, changelog, this file) lives at root and is not propagated to children.
- **Cross-project notifications and absorption candidates** land in `_buffer/`; `/acw-session start` reads it.
- **Operator-facing how-to docs** live in `runbooks/`. Not skill-specific; operator-facing, free-form markdown.
- **External system documentation** (APIs, MCPs, adapters, webhooks) lives in `integrations/`. One subdirectory or file per system. See `integrations/README.md` for convention.
- **Agent-generated dated snapshots** (briefings, weekly reviews, status reports) live in `briefings/`. Generated by triage/aggregation skills.
- **Operator/project context** (lightweight pointers to operating reality) lives in `context/`: `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`. Read on demand.
- **Operator's untriaged items** land in `inbox/` (no underscore — distinct from system `_buffer/`). Items get processed and removed: routed to `tasks-status::Pending`, parked, sent to external task app, or deleted.
- **Deferred primitives** are catalogued in `DEFERRED.md` (canonical) with per-primitive notes in `deferred/` (derived view).

## Forbidden until earned

The canonical list lives in `DEFERRED.md`. The principle: nothing ships without a named, dated, documented incident or activation trigger justifying it. If a primitive isn't in the deferred library or doesn't have its activation trigger met, it doesn't get built. Read `DEFERRED.md` before proposing anything that looks like infrastructure for a hypothetical need.

---

## Maintenance

The session-end bookend skill treats host-specific entry files (any file in this repo that implements `AGENTS.md` directive 7 for a particular host) as maintained surfaces. When a session shifts what a new contributor needs to know to work on the project — a new substrate file enters auto-load, the manifest layer for a class of files changes, a hard-rule principle gets added or retired, the bookend pair changes name — Phase 2 surfaces a proposed edit to whichever host entry files exist. Specific lists and ids should not appear in this file; if they do, the next session-end run should propose moving them into the file that owns them and replacing them here with a pointer.
