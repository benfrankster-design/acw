---
id: D-ACW-015
title: "Canonical-edit detection in capture-and-metabolize Phase 2 gates on `is_canonical_source`"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-015 — Canonical-edit detection in capture-and-metabolize Phase 2 gates on `is_canonical_source`

**Date:** 2026-05-02
**Decision:** Phase 2 of `capture-and-metabolize` adds a canonical-edit detection step. It computes the intersection of `auto_load_at_session_start` and `template_layer` (= the canonical files), checks whether any were edited this session, and branches on `acw-state.yaml::is_canonical_source`. Publishing instances (`true`) get a version-bump-and-push prompt; downstream consumers (`false` or absent, the default) get a warning that local edits to canonical files won't propagate and may be overwritten by `/upgrade-instance`.
**Rationale:** Without the gating flag, the propagation behavior would ship to every child instance. Child instances editing local snapshots of canonical files would start trying to push to ACW's GitHub on every edit. The flag separates "I publish canonical content downstream" from "I consume canonical content from upstream" cleanly. Operator-flagged the bug in real time during the design conversation; the fix earned its build before the skill shipped.
**Source:** Operator reasoning during the multi-instance topology discussion, turn 81 of the v0.3.0 absorption arc.
