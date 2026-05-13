---
id: D-ACW-013
title: "`is_canonical_source` flag added to `acw-state.yaml` schema"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-013 — `is_canonical_source` flag added to `acw-state.yaml` schema

**Date:** 2026-05-02
**Decision:** Added `is_canonical_source: <bool>` to `acw-state.yaml`. ACW itself sets it to `true`. The template (`tools/templates/acw-state.yaml.tmpl`) defaults it to `false` for every scaffolded instance. Added as a recommended block in `rules/instance-current-manifest.md` earned in v0.3.0.
**Rationale:** Needed a clean signal for "this instance publishes canonical content downstream" vs "this instance consumes canonical content from upstream." Used by `capture-and-metabolize` Phase 2 (canonical-edit detection branch) and potentially by future skills that need to distinguish publisher vs consumer behavior. Generalizes beyond ACW — any future canonical-publishing meta-instance (e.g., a consultancy serving as canonical for client engagements) sets the flag true.
**Source:** Required by D-ACW-015 (Phase 2 canonical-edit branching).
