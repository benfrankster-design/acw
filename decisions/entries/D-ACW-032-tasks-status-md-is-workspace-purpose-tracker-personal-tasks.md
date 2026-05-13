---
id: D-ACW-032
title: "`tasks-status.md` is workspace-purpose tracker; personal tasks stay external"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-032 — `tasks-status.md` is workspace-purpose tracker; personal tasks stay external

**Date:** 2026-05-02
**Decision:** `rules/task-tracking.md` updated to clarify that `tasks-status.md` tracks the workspace's purpose, adapted per workspace type (cockpit = config + chief-of-staff ops; project = deliverables; full = org coordination). Operator-personal life tasks (pick up kids, doctor's appointment, call mom) explicitly do NOT live in workspace substrate — they live in the operator's external task app, accessed via MCP at query time. Same logic applies to calendar (stays in Google/iCloud/Nextcloud) and email (Gmail/Outlook).
**Rationale:** The general rule: don't duplicate operator-accessible-on-phone surfaces in workspace substrate. Mirroring creates sync rot. Lean on MCP integrations for live data; lean on briefings/ for moment-in-time aggregations when a snapshot is wanted. Earlier conversation considered `my-tasks.yaml` as a separate operator-personal surface; rejected for the same reason calendar mirror was rejected. Same logic applied consistently.
**Source:** Operator decision during v0.5.0/v0.6.0 scoping; codified in rules/task-tracking.md framing update.
