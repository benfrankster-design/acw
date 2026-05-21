---
id: D-ACW-028
title: "Calendar, tasks, email stay external; briefings is the snapshot mechanism"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-028 — Calendar, tasks, email stay external; briefings is the snapshot mechanism

**Date:** 2026-05-02
**Decision:** Don't duplicate calendar, task app, or email in workspace substrate. Lean on MCP integrations for live data. When the operator wants a snapshot of aggregated external state, briefing skills aggregate calendar + tasks + email + integrations into a dated artifact in `briefings/`. Documented as a doc note in `rules/instance-current-manifest.md` § briefings.
**Rationale:** Operator extended the calendar-stays-external logic to tasks and email. Same reasoning for all three: they're already operator-accessible on phone/desktop via native apps; mirroring locally creates sync rot. The chief-of-staff affordance ("what's on my plate?") lives in agents that call the appropriate MCP at query time, not in cached substrate.
**Source:** Operator decision during v0.5.0 / v0.6.0 scoping turn.
