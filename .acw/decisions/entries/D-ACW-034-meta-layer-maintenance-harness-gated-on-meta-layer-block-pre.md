---
id: D-ACW-034
title: "Meta-layer maintenance harness gated on `meta_layer` block presence"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-034 — Meta-layer maintenance harness gated on `meta_layer` block presence

**Date:** 2026-05-02
**Decision:** `/acw-session end` Phase 2 gains a "Meta-layer maintenance" step; `/acw-instance audit` Mode A gains a staleness check; `/acw-instance upgrade` gains a "Resolve meta-layer staleness" step. All three are gated on `acw-state.yaml::meta_layer` block presence — most consumer instances don't have meta-layer narrative files and pay no cost. Trigger table is hardcoded sensible defaults (README on substrate-shape change, CHANGELOG on version bump, LINEAGE on new primitive, ORCHESTRATION on new methodology pattern, SKEPTIC on med+ incident).
**Rationale:** v0.5.1's front-door cleanup exposed a structural gap — substrate had Phase 2 distribution; meta-layer had nothing. README went stale across four versions before someone noticed. The harness closes the gap. Gating on `meta_layer` block presence (not `is_canonical_source`) generalizes correctly: any workspace with declared meta-layer narrative files inherits the discipline; workspaces without it pay nothing.
**Source:** Operator question on README staleness during the v0.5.1 turn; meta-layer audit revealed five staleness candidates; harness designed in same conversation.
