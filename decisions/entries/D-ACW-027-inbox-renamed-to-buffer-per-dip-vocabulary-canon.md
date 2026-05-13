---
id: D-ACW-027
title: "`_inbox/` renamed to `_buffer/` per DIP vocabulary canon"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-027 — `_inbox/` renamed to `_buffer/` per DIP vocabulary canon

**Date:** 2026-05-02
**Decision:** System cross-instance handoff directory renamed from `_inbox/` to `_buffer/` in v0.5.0. All active substrate (skills, rules, state, tools, tests) updated. Append-only history (decisions/, build-log, CHANGELOG, research/) retains historical `_inbox` references. `/acw-instance upgrade` v0.5.0+ adds a migration step proposing the rename to legacy workspaces.
**Rationale:** Two reasons pulling the same direction: (a) operator's DIP vocabulary canon already declares "buffer" as the canonical term replacing inbox/queue/staging — the rename brings ACW canonical inline with existing vocabulary. (b) v0.6.0 will introduce an operator-facing `inbox/` surface; the system surface keeping `_inbox/` would collide. Renaming now (one downstream instance, `_Command`) is cheap; renaming later (after lattice scale) would be expensive.
**Source:** Operator decision during v0.5.0 / v0.6.0 scoping turn; DIP vocabulary in `~/synapse/Rules/Procedures/dip-vocabulary.md`.
