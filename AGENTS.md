---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# AGENTS — Directives and Operational Commands

This file is the entry point for any agent opening this workspace. It is deliberately named `AGENTS.md` rather than a vendor-specific file (`CLAUDE.md`, `GEMINI.md`, `GPT.md`) so the workspace is portable across frontier models. Any agent that honors this file can operate inside ACW; any agent that does not honor it cannot.

## Eight directives

1. **Read `rules/pipeline-roles.md` before declaring a role.** Every skill in this workspace declares exactly one role from the four-group normative enum. A skill that cannot cleanly declare a single role is not a skill and must be split. The sixteen-role appendix is informative, not normative.

2. **Read `rules/canon-governance.md` before adding vocabulary.** New terms enter the canon through a state machine (`draft` → `proposed` → `approved`). The approval authority is declared in `rules/instance-hard-rules.md`. Adding a term without running the governance process is a drift incident.

3. **Read `rules/instance-hard-rules.md` for instance constraints.** Every hard rule in that file is stop-work if violated. Read it before your first write.

4. **Run `tools/lint-vocab.py` before committing.** The lint enforces the canon at commit time. Exit code 1 blocks the commit. The fix is to either update the content or (with authority) update the canon.

5. **Consult `SKEPTIC.md` before proposing a new primitive.** The skeptic exists specifically to push back on well-intentioned premature ships. Every primitive in `deferred/` has an activation trigger and every proposal to promote one requires evidence in `incidents.jsonl`.

6. **If you disagree with a rule, read `research/` before editing it.** Every rule in this template traces to a documented research finding. Edit without reading the research and you are likely to re-introduce a problem the research already solved.

7. **Auto-load every file listed in `acw-state.yaml::auto_load_at_session_start` at the start of any session in this workspace.** Each agent host implements via its native mechanism. Claude Code uses the SessionStart hook at `.claude/hooks/load-context.py`, registered in `.claude/settings.json`; the hook reads `acw-state.yaml` at runtime and injects file contents as `additionalContext`. `CLAUDE.md` is a thin pointer (`See AGENTS.md.`) and carries no `@`-imports. Other hosts (Codex, Gemini, etc.) implement equivalent SessionStart behavior pointing at the same yaml; agents that read `acw-state.yaml` directly need no host-specific hook. The list is maintained additively by `/acw-session end`; removal requires an explicit decision-log entry. Auto-load entries themselves earn their slot per `rules/auto-load-discipline.md` — every entry declares a structured claim. See the **Auto-load (Resource / When / Why)** and **What NOT to Load** sections below.

8. **When writing runtime code (a Next.js app, server, CLI tool, agent, etc.) inside an instance, locate it under a named subdirectory at instance root** — `web/`, `server/`, `agents/`, `app/`, `tools/<scoped-name>/`, or whatever name fits. ACW operator-metadata substrate lives under `.acw/` (v0.10.0+); `rules/`, `AGENTS.md`, `CLAUDE.md`, project artifacts (`research/`, `threat-model.md`) stay at root. Substrate is governance and moves on a slow, decision-driven clock; runtime is operational and moves on a fast, build-driven clock. Co-locating the two conflates the clocks: build artifacts collide with substrate in `git status`, package managers see substrate as project-root noise, deployment configs (Vercel, Docker) point at a path that also carries substrate. If the workspace already has runtime code at root and migrating is expensive, log an incident and propose a path forward — do not silently accept the conflation. See `rules/multi-instance-topology.md` § "Runtime code in shipping instances" and `rules/instance-types.md` for instance-type profiles.

## Auto-load (Resource / When / Why)

Canonical recommendations from `rules/auto-load-discipline.md`. Instances override (drop a canonical entry, add an instance-specific entry) per the discipline gate; each override carries its own structured claim in `.acw/acw-state.yaml::auto_load_at_session_start`.

> **v0.10.0:** Substrate paths prefix `.acw/`. Pre-0.10.0 instances upgrade via `/acw-instance upgrade`. See `rules/instance-types.md` for the profile + modules declaration.

| Resource | When | Why |
|---|---|---|
| `.acw/decisions/INDEX.md` (wiki mode is canonical from v0.9.8) | session-start | Recently decided history must be visible at session start; without it agents re-litigate settled choices. |
| `rules/instance-hard-rules.md` | session-start | Stop-work rules must be visible at every session start; loading them on-demand is too late. |
| `.acw/tasks-status.md` | session-start | Pending work surface must be visible at session start; without it agents propose duplicate work. |
| `.acw/glossary/INDEX.md` (wiki mode) | session-start | Vocabulary canon prevents drift to colloquial English in agent output. |
| `.acw/codemap/GRAPH_REPORT.md` (coding-project / library only) | session-start | Code structure summary so the agent navigates pre-computed graph instead of re-reading source. |

## What NOT to Load

Files that look load-bearing but aren't. Auto-loading them costs context without shaping session behavior; consumers load them on demand. `/acw-instance audit` flags these as DEMOTE if it finds them in an instance's auto-load list.

| Resource | Why not |
|---|---|
| `rules/manifest-discipline.md` | Consumed only by skills doing manifest classification; they load it themselves. |
| `rules/instance-current-manifest.md` | Consumed only by `/acw-session start` drift check and `/acw-instance audit\|upgrade`. |
| `rules/multi-instance-topology.md` | Applies only to multi-domain workspaces; single-instance loads waste context. |
| `incidents.jsonl` | Forensic record. Consumed by audit + promotion-ritual. On-demand only. |
| Empty or near-empty research scaffolds (`evolution.md`, `sources.md`, `research-state.yaml` before they carry content) | Nothing earned — no incident, no consumer, no shaped behavior. |
| `research/01-problem-framing.md` | One-time orientation read; not session-recurring. Read on demand when entering the workspace fresh. |

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
