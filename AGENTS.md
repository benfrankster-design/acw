---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# AGENTS — Directives and Operational Commands

This file is the entry point for any agent opening this workspace. It is deliberately named `AGENTS.md` rather than a vendor-specific file (`CLAUDE.md`, `GEMINI.md`, `GPT.md`) so the workspace is portable across frontier models. Any agent that honors this file can operate inside ACW; any agent that does not honor it cannot.

## Six directives

1. **Read `rules/pipeline-roles.md` before declaring a role.** Every skill in this workspace declares exactly one role from the four-group normative enum. A skill that cannot cleanly declare a single role is not a skill and must be split. The sixteen-role appendix is informative, not normative.

2. **Read `rules/canon-governance.md` before adding vocabulary.** New terms enter the canon through a state machine (`draft` → `proposed` → `approved`). The approval authority is declared in `rules/instance-hard-rules.md`. Adding a term without running the governance process is a drift incident.

3. **Read `rules/instance-hard-rules.md` for instance constraints.** Every hard rule in that file is stop-work if violated. Read it before your first write.

4. **Run `tools/lint-vocab.py` before committing.** The lint enforces the canon at commit time. Exit code 1 blocks the commit. The fix is to either update the content or (with authority) update the canon.

5. **Consult `SKEPTIC.md` before proposing a new primitive.** The skeptic exists specifically to push back on well-intentioned premature ships. Every primitive in `deferred/` has an activation trigger and every proposal to promote one requires evidence in `incidents.jsonl`.

6. **If you disagree with a rule, read `research/` before editing it.** Every rule in this template traces to a documented research finding. Edit without reading the research and you are likely to re-introduce a problem the research already solved.

## Operational commands

Same as `README.md` Quickstart — reproduced here so an agent that only loads `AGENTS.md` still has what it needs.

```
python tools/lint-vocab.py glossary.md --content-dir .
python tools/log-incident.py log <primitive> <severity> <symptom>
python tools/log-incident.py count --primitive <name>
python tools/log-incident.py check-drift
python -m unittest discover tests
```

## Why AGENTS.md and not CLAUDE.md

Vendor-specific entry files (CLAUDE.md, GPT.md, GEMINI.md) couple the workspace to a single frontier model. ACW is designed to outlive any single vendor's tooling — the research that produced it is model-agnostic, the primitives are model-agnostic, and the activation triggers are model-agnostic. `AGENTS.md` is the cross-vendor convention that honors the same shape without the coupling.

If a particular agent's host environment requires a vendor-specific file, that file should be a thin pointer that reads: "See AGENTS.md." Never duplicate directives across files.

## Not a content file

`AGENTS.md` is a directive file, not a content file. Content lives in `rules/`. A contributor who wants to change how ACW behaves should edit the relevant rule file, log an incident if warranted, and leave `AGENTS.md` alone except when adding or removing a top-level directive. The directive list is small on purpose.
