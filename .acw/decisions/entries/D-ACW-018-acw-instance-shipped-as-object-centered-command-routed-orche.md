---
id: D-ACW-018
title: "`/acw-instance` shipped as object-centered command-routed orchestrator (verbs: audit, upgrade)"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-018 — `/acw-instance` shipped as object-centered command-routed orchestrator (verbs: audit, upgrade)

**Date:** 2026-05-02
**Decision:** Renamed `/upgrade-instance` → `/acw-instance` as a command-routed orchestrator with two verbs. Audit is read-only (Mode A canonical comparison + Mode B organic discovery + per-file routing report). Upgrade is interactive (gap-walk with adopt-mode hard-stop, divergence-marker respect, decision-log entry). Shared spine: registration check, GitHub canonical fetch, substrate scan, routing-table generation.
**Rationale:** The cs-copilot session that triggered v0.3.0 work also exposed a deeper need: when a workspace has organic substrate (`_Command`-shape), adopt-mode shouldn't run blindly. Audit verb is the safety layer — operator surveys before reconciling. Upgrade verb hard-stops above the organic threshold and points at audit. Both verbs share the same canonical-fetch and substrate-scan logic, which is the spine.
**Source:** Conversation arc 2026-05-02 turn 79 onward; operator confirmed v0.4.0 scope.
