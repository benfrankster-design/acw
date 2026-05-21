---
id: D-ACW-010
title: "`/upgrade-instance` skill closes the drift loop"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-010 — `/upgrade-instance` skill closes the drift loop

**Date:** 2026-05-02
**Decision:** New skill `skills/upgrade-instance/` walks the operator through reconciling instance state with the current ACW recommended-blocks registry. Drift detection lives in `/resume-session` Step 5; reconciliation lives here. Together they form the upgrade loop: detect → reconcile → bump `last_reconciled_version` → quiet alert.
**Rationale:** Drift visibility without a path-to-fix is half a feature. Operators shouldn't have to hand-edit `acw-state.yaml` and look up canonical defaults manually. The skill walks each gap with the registry's "How to add" content surfaced inline. Pure additive — no demotions, no removals, no shape repair.
**Source:** Operator instruction, turn 73 of the v0.2.0 absorption arc; subagent stress test informed final shape.
