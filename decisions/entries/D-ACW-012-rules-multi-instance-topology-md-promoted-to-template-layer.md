---
id: D-ACW-012
title: "`rules/multi-instance-topology.md` promoted to template_layer canonical"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-012 — `rules/multi-instance-topology.md` promoted to template_layer canonical

**Date:** 2026-05-02
**Decision:** Promoted the lattice model + knowledge-placement discriminator + reference-not-duplicate principle from `research/10-multi-instance-topology.md` (meta_layer) to `rules/multi-instance-topology.md` (template_layer). Added to `auto_load_at_session_start` and `template_layer` blocks in `acw-state.yaml`. Added as recommended block in `rules/instance-current-manifest.md` earned in v0.3.0. Research note retained in meta_layer as provenance.
**Rationale:** The lattice framing is load-bearing for any operator scaling beyond a single instance. Baking it into template_layer means every scaffolded instance (and every existing instance via /upgrade-instance) inherits the framing without operator effort. Stable but flagged experimental until lattice-level incidents earn promotion to normative.
**Source:** Operator decision in the multi-instance topology conversation, turn 79.
