---
id: D-ACW-011
title: "ACW skills register globally via user-level directory junctions"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-011 — ACW skills register globally via user-level directory junctions

**Date:** 2026-05-02
**Decision:** ACW's three bookend-arc skills (`capture-and-metabolize`, `resume-session`, `upgrade-instance`) register on the operator's machine via directory junctions at `~/.claude/skills/<name>/` pointing at `c:\Users\benja\projects\acw\skills\<name>/`. ACW's `skills/` directory is the canonical runtime source. Child instances scaffolded via `tools/scaffold-instance.py` ship with their own copies of the skills as part of template_layer propagation; those copies are passive (self-contained distribution surface) and not the registered runtime copy.
**Rationale:** Operator works across multiple ACW-derived workspaces (ACW itself, cs-copilot, gsg-copilot, future Frank Context). The framework-agnostic skill design from rc4 already supports one canonical source serving every workspace, since paths resolve from each workspace's own `acw-state.yaml` at runtime. User-level registration with a single canonical source means edits to a skill propagate to every workspace immediately — no per-instance update step. Project-level overrides remain available on demand (Claude Code resolves project-level skills before user-level), so a workspace that needs a customized skill can still add its own `.claude/skills/<name>/` junction.
**Source:** Operator turn requesting the wisest approach; reasoning surfaced the multi-instance pollution concern and the canonical-source preference.
