---
id: D-ACW-025
title: "`briefings/` as universal pattern, not cockpit-specific"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-025 — `briefings/` as universal pattern, not cockpit-specific

**Date:** 2026-05-02
**Decision:** Reversed earlier framing that flagged briefings/ as cockpit-specific. The pattern (agent-generated dated snapshot of aggregated state) is universal across workspace types. Cockpit, Project, and Full instances all benefit from it; only the aggregation content varies.
**Rationale:** Initial audit conservatism mis-classified. Operator's cockpit framing made it sound role-specific (leadership, CS, etc.) but cockpit is itself a workspace TYPE, not a role — anyone with a personal command center qualifies. And briefings work in project workspaces too (PR/build/issue snapshots). Universal pattern.
**Source:** Operator clarification on cockpit-vs-leadership framing during v0.5.0 scoping.
