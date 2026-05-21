---
id: D-ACW-033
title: "`inbox/` canonical as operator capture surface"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-033 — `inbox/` canonical as operator capture surface

**Date:** 2026-05-02
**Decision:** `inbox/` (no underscore) ships as canonical empty_dir for the operator's untriaged-items surface. Folder of dated markdown files plus loose entries. Items get processed and removed: routed to `tasks-status::Pending`, `tasks-status::Parked`, the operator's external task app, or deleted. Distinct from `_buffer/` (system surface for cross-instance handoffs) and `briefings/` (agent-generated dated snapshots) — three different surfaces, three different lifecycles.
**Rationale:** Operator needs a workspace-side capture surface for raw inbound items needing triage. Without it, mid-session captures and triage-skill outputs have nowhere to land that's distinct from committed work. The `_inbox/` → `_buffer/` rename in v0.5.0 cleared semantic space for this; v0.6.0 fills it. The triage-flow model (inbox → tasks/parked/external/deleted) is operator-driven; substrate shape is light (folder of dated files, no enforced structure).
**Source:** Operator design conversation during v0.5.0/v0.6.0 scoping; reaffirmed during v0.6.0 ship.
