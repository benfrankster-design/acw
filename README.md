---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# ACW — Agentic Contract Workspace

A standalone, portable, model-agnostic starter kit for persistent agentic AI workspaces. Plain-text, stdlib-only, Windows/macOS/Linux portable.

## The thesis

Persistent agentic workspaces drift. ACW is the minimum governance layer that stops drift from becoming damage, and the preserved design work for the typed contract registry that would eventually solve drift mechanically.

## Disclaimer

**ACW is a teaching template and methodology archive, not production infrastructure. The deferred primitives are design documents, not validated implementations.**

Read `SKEPTIC.md` before proposing any extension. Read the research archive before editing any rule.

## Quickstart

1. Read `AGENTS.md` for the six directives that govern how an agent should open this workspace.
2. Read `bootstrap/README.md` and answer the seven-question interview.
3. Fill in `rules/instance-hard-rules.md` with your authority set, domains, and first hard rules.
4. Seed `rules/canon.yaml` with five to ten concepts.

## Tools Quickstart

```
python tools/lint-vocab.py glossary.md --content-dir .
python tools/log-incident.py log <primitive> <severity> <symptom>
python tools/log-incident.py count --primitive <name>
python tools/log-incident.py check-drift
python -m unittest discover tests
```

## Directory map

```
acw/
├── rules/              governance-layer primitives (canon, roles, lint, broker design)
├── tools/              stdlib-only Python (lint + incident log + drift check)
├── decisions/          single decision-log.md with four sections
├── tests/              unittest + fixtures
├── skills/             reference example skill only
├── bootstrap/          greenfield instantiation guide
├── migration/          brownfield audit guide
├── deferred/           the deferred library (11 subfolder design docs)
├── research/           seven-file research archive
├── glossary.md         seed vocabulary
├── DEFERRED.md         canonical deferred-primitive table
├── threat-model.md     eight threats, defenses, known gaps
├── incidents.jsonl     append-only incident ledger (starts empty)
├── AGENTS.md           agent directives + operational commands
├── SKEPTIC.md          four warnings + do-not-do list
├── AUTHOR.md           attribution
├── LINEAGE.md          research chain and prior art
├── CHANGELOG.md        version history
├── LICENSE-CONTENT     CC BY 4.0
└── LICENSE-CODE        MIT
```

## The four load-bearing files

If you only read four files in this template, read these:

1. **`rules/pipeline-roles.md`** — the role contract every skill must declare
2. **`rules/canon-governance.md`** — the vocabulary governance state machine
3. **`tools/lint-vocab.py`** — the enforcement edge
4. **`tools/log-incident.py`** — the ledger the earn-by-incident discipline depends on

Everything else scaffolds these four.

## License

Content is CC BY 4.0 (see `LICENSE-CONTENT`). Code is MIT (see `LICENSE-CODE`). This split is deliberate so the methodology can be cited and the tools can be adapted with minimal friction.

## Pointers

- `AGENTS.md` — how an agent should open this workspace
- `AUTHOR.md` — attribution
- `LINEAGE.md` — research chain and prior art
- `SKEPTIC.md` — four warnings and a do-not-do list
