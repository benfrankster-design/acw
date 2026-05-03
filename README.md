---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# ACW — Agentic Contract Workspace

A standalone, portable, model-agnostic starter kit for persistent agentic AI workspaces. Plain-text, stdlib-only, Windows/macOS/Linux portable.

## The thesis

Persistent agentic workspaces drift. ACW is the minimum governance layer that stops drift from becoming damage, plus the lattice topology that lets an organization run from a federation of coordinated instances. Built earn-by-incident: nothing ships without a documented incident or activation trigger justifying it.

## Disclaimer

**ACW is a teaching template and methodology archive, not production infrastructure. The deferred primitives are design documents, not validated implementations.**

Read `SKEPTIC.md` before proposing any extension. Read the research archive before editing any rule.

## Scaffold a new instance (60 seconds)

```bash
git clone https://github.com/benfrankster-design/acw.git
cd acw
python tools/scaffold-instance.py \
  --code MYINST \
  --domain "your domain" \
  --host claude-code \
  /path/to/your-new-instance
```

That's it. `tools/scaffold-instance.py` reads `acw-state.yaml`'s manifest, copies the generic doctrine (`template_layer`), renders templated files (`instance_layer`) with token substitution, creates empty directories with `.gitkeep`, and writes the host-specific entry file (e.g., `CLAUDE.md` for Claude Code).

After scaffolding:

1. Edit `<your-instance>/research/01-problem-framing.md` to record what the workspace is for.
2. Add domain-specific hard rules to `<your-instance>/rules/instance-hard-rules.md`.
3. Run `cd <your-instance> && python tools/lint-vocab.py glossary.md --content-dir .` to baseline the vocab lint.
4. Run `cd <your-instance> && python -m unittest discover tests` to verify the manifest tooling.
5. Open the workspace in your agent host and run `/acw-session start` to enter the first session.

## The four operator commands

ACW's bookend pair plus its instance-management orchestrator. Both are object-centered command-routed orchestrators (per `rules/skill-format.md`):

| Command | What it does |
|---|---|
| `/acw-session start` | Loads variable context for a new session — recent captures, queued research prompts, unread `_buffer/` notifications, drift alert against current ACW canonical. Read-only. |
| `/acw-session end` | Five-phase session-end pass — capture transcript, distribute findings into substrate, metabolize stale entries, optional synapse log, optional next-session research prompt. |
| `/acw-instance audit` | Read-only walk of the workspace's substrate. Mode A compares each canonical file against `rules/skill-format.md` and the rule files governing it. Mode B surfaces organic substrate and routes interactively per finding (adopt-as-canonical / absorb upstream / instance-specific / not substrate). Writes absorption candidates to ACW's `_buffer/` on operator routing. |
| `/acw-instance upgrade` | Reconciles the workspace with current ACW canonical fetched from GitHub. Walks gaps in `acw-state.yaml`, runs adopt-mode for unregistered substrate-shaped workspaces (with hard-stop above the organic threshold), respects divergence markers, refreshes the local manifest cache, bumps versions, logs the run. |

## Tools

```bash
python tools/scaffold-instance.py        # greenfield instantiation
python tools/manifest.py                 # manifest read/write/validate (library; consumed by skills)
python tools/lint-vocab.py glossary.md   # vocab discipline against rules/canon.yaml
python tools/log-incident.py log <primitive> <severity> <symptom>
python tools/log-incident.py count --primitive <name>
python tools/log-incident.py check-drift
python -m unittest discover tests        # verify manifest tooling end-to-end
```

## Directory map

```
acw/
├── AGENTS.md                    # six directives every agent honors
├── README.md                    # this file
├── DEFERRED.md                  # deferred-primitive table (canonical)
├── SKEPTIC.md                   # four warnings + do-not-do list
├── AUTHOR.md / LINEAGE.md       # attribution + research chain
├── CHANGELOG.md                 # version history
├── LICENSE-CODE / LICENSE-CONTENT
├── acw-state.yaml               # manifest: template_layer / instance_layer / meta_layer
├── glossary.md / threat-model.md
├── tasks-status.md / build-log.md / incidents.jsonl
│
├── rules/                       # governance layer
│   ├── skill-format.md          # skill contract + command-routed orchestrator pattern
│   ├── pipeline-roles.md        # four-group role enum (orchestrator/pipeline-worker/guardian/broker-sideband)
│   ├── canon-governance.md      # vocabulary state machine
│   ├── canon-schema.yaml        # SKOS-inspired controlled-vocab schema
│   ├── canon.yaml               # the canonical vocabulary itself
│   ├── manifest-discipline.md   # three-layer pattern + manifest tooling spec
│   ├── instance-current-manifest.md  # recommended-blocks registry
│   ├── multi-instance-topology.md     # lattice + absorption mechanics
│   ├── instance-hard-rules.md   # per-instance authority/domain/hard rules (instance-specific)
│   ├── decision-tracking.md / task-tracking.md / incident-tracking.md
│   ├── promotion-ritual.md      # how primitives earn the deferred → shipped move
│   ├── capability-broker.md     # broker design (deferred)
│   └── vocabulary-lint.md       # lint contract
│
├── skills/
│   ├── acw-session/             # bookend orchestrator: verbs `start` and `end`
│   ├── acw-instance/            # instance-management orchestrator: verbs `audit` and `upgrade`
│   └── example-skill/           # reference implementation of the skill format
│
├── tools/                       # stdlib-only Python
│   ├── scaffold-instance.py     # greenfield instantiation
│   ├── manifest.py              # manifest tooling reference impl + canonical defaults
│   ├── lint-vocab.py            # vocab lint
│   ├── log-incident.py          # incident ledger
│   └── templates/               # rendered forms of instance_layer files
│
├── decisions/decision-log.md    # single file with four sections (open / decisions / constraints / resolved)
├── tests/                       # unittest + fixtures (verifies manifest tooling)
│
├── runbooks/                    # operator-facing how-to docs (free-form)
├── integrations/                # external-system docs (APIs, MCPs, adapters); README explains convention
├── briefings/                   # agent-generated dated snapshots (daily/weekly/on-demand aggregations)
├── context/                     # lightweight pointers to operating reality
│   ├── goals.md                 # long-arc goals
│   ├── objectives.md            # current near-term focus
│   ├── how-i-work.md            # operator preferences, schedule, communication
│   └── key-people.md            # who matters in this workspace's domain
├── inbox/                       # operator's untriaged items (folder of dated files)
├── _buffer/                     # system surface for cross-instance handoffs (absorption candidates etc.)
│
├── research/                    # research archive (origin chain) + sessions/ + queries/
├── deferred/                    # per-primitive design notes for the deferred library
└── (LICENSE files, ORCHESTRATION.md as meta narrative)
```

For the live, machine-checked classification of every file into `template_layer`, `instance_layer`, or `meta_layer`, see `acw-state.yaml`. The scaffolder reads from there; the YAML is the source of truth.

## How ACW is layered

ACW is two things at once: a template that scaffolds new agentic-contract workspaces, and its own first instance with substantial lived history. Three layers formalize both roles:

| Layer | What goes here | Propagates to scaffolded instances? |
|---|---|---|
| `template_layer` | Generic doctrine — rules, tools, the bookend skills, tests, the integrations README template | Yes, verbatim |
| `instance_layer` | This workspace's own populated content; children get a templated initial form | Yes, rendered from a template (e.g., a fresh empty `decisions/decision-log.md` for new instances) |
| `meta_layer` | About ACW itself only — lineage, attribution, changelog, this README, the deferred library, retired-skill placeholders | No |

The generic pattern (any workspace classifying its files into three buckets, scaffold tool reads from the manifest, skill maintains it additively, lint catches drift, default-to-instance discipline) is in `rules/manifest-discipline.md`. Every derived workspace gets that rule. What's ACW-specific — which exact files live in which layer — lives in `acw-state.yaml`.

## Load-bearing files

If you only read a few files in this template, read these:

1. **`AGENTS.md`** — six directives that govern how any agent should open this workspace.
2. **`rules/skill-format.md`** — the contract every skill must satisfy, plus the command-routed orchestrator pattern.
3. **`rules/multi-instance-topology.md`** — how organizations run from a lattice of coordinated instances; absorption mechanics.
4. **`rules/instance-current-manifest.md`** — declarative registry of what "current ACW" expects; drives the drift alert and `/acw-instance upgrade`.
5. **`skills/acw-session/SKILL.md`** and **`skills/acw-instance/SKILL.md`** — the orchestrators an operator interacts with most.

Everything else scaffolds these.

## Forbidden until earned

The canonical list lives in `DEFERRED.md`. Nothing ships without a named, dated, documented incident or activation trigger justifying it. If a primitive isn't in the deferred library or doesn't have its activation trigger met, it doesn't get built. Read `DEFERRED.md` before proposing anything that looks like infrastructure for a hypothetical need.

## License

Content is CC BY 4.0 (see `LICENSE-CONTENT`). Code is MIT (see `LICENSE-CODE`). This split is deliberate so the methodology can be cited and the tools can be adapted with minimal friction.

## Pointers

- `AGENTS.md` — how an agent should open this workspace
- `SKEPTIC.md` — four warnings and a do-not-do list
- `AUTHOR.md` — attribution
- `LINEAGE.md` — research chain and prior art
- `ORCHESTRATION.md` — methodology that produced ACW v0.1.0
- `CHANGELOG.md` — version history
- `DEFERRED.md` — deferred-primitive table
