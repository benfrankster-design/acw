---
id: D-ACW-039
title: "Runtime-code-location convention (subdir, not root) absorbed from cx-dashboard-saas"
date: 2026-05-04
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-039 — Runtime-code-location convention (subdir, not root) absorbed from cx-dashboard-saas

**Date:** 2026-05-04

**Decision:** Add a "Runtime code in shipping instances" section to `rules/multi-instance-topology.md` documenting the observed convention: instances shipping runtime code locate it under a named subdirectory at instance root (`web/`, `server/`, `agents/`, `app/`), not at instance root itself. Substrate stays at root. Convention only — no schema field in `acw-state.yaml`, no separate rule file, no audit enforcement. Source absorption note marked read.

**Rationale:** Absorption candidate from `cx-dashboard-saas` Phase 0 scaffold (`_buffer/2026-05-04-cx-dashboard-saas-app-code-location-friction.md`) flagged a real gap — ACW canonical scaffolds every instance as pure-substrate, but several active instances (cs-copilot, cx-dashboard-saas, future project workspaces) ship runtime code and have to make an unguided structural decision. The candidate proposed three options: (1) `runtime_code_location` schema field, (2) dedicated `rules/runtime-code-location.md`, (3) light-touch convention note. Option 3 is correct under earn-by-incident discipline: this is incident #1 of this class. Schema fields and dedicated rule files earn their build by being load-bearing for skills or audits; nothing in current ACW canonical reads or enforces the runtime path. The convention paragraph in the topology rule is enough until a second instance trips on the same gap.

**Why subdir over root:** substrate and runtime move on different clocks. Substrate is governance (slow-moving, decision-driven, audit-checked); runtime is operational (fast-moving, build-driven, dependency-managed). Co-locating at one path level conflates the two clocks — build artifacts collide with substrate in `git status`, package managers see substrate as project-root noise, deployment configs (Vercel, Docker) point at a path that also carries decisions/.

**Source:** Absorption candidate from cx-dashboard-saas, 2026-05-04. Operator approved option 3 (convention note) in same session.

**Open follow-ups:**
- If a second consumer instance hits the same friction independently (a different operator scaffolding a project workspace and asking the same "where does code go?" question), the convention has accumulated enough incident evidence to earn promotion. Candidates: structured field in `acw-state.yaml`, a dedicated `rules/runtime-code-location.md`, or a scaffolder flag (`tools/scaffold-instance.py --runtime-code-dir web`).
- Eventual: if/when a skill needs to read the runtime path programmatically (e.g., a build-runner skill that needs to know where to `cd` before `npm run build`), the schema field earns its build at that moment.
- Not v1.0.0 — soak only. v1.1.0+ candidate.
