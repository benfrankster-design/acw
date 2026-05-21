---
id: D-ACW-029
title: "`briefings/`, `runbooks/`, `integrations/` shipped as universal canonical substrate"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-029 — `briefings/`, `runbooks/`, `integrations/` shipped as universal canonical substrate

**Date:** 2026-05-02
**Decision:** Three new substrate directories earned by `_Command` audit dogfood. All three are universal patterns; content varies by workspace type but the shape is the same. `runbooks/` (operator how-tos), `integrations/` (external-system docs with templated README), `briefings/` (agent-generated dated snapshots). All earned in v0.5.0 via `rules/instance-current-manifest.md` registry entries.
**Rationale:** Initial `_Command` audit verdict flagged all three as "Likely [s] instance-specific." Operator pushed back: briefings is universal (cockpit aggregates calendar+tasks; project aggregates PR+build+issues; same shape, different content); runbooks is universal (operator how-tos that don't fit in any skill); integrations is universal (every workspace touching external systems via MCP/API/webhook accumulates docs about them). Verdict reversed. Three absorption candidates ship as canonical.
**Source:** `_Command` audit report + operator reframing.
