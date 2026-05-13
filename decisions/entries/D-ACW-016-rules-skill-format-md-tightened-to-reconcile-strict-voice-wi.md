---
id: D-ACW-016
title: "`rules/skill-format.md` tightened to reconcile strict-voice with object-centered carve-out"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-016 — `rules/skill-format.md` tightened to reconcile strict-voice with object-centered carve-out

**Date:** 2026-05-02
**Decision:** Three targeted edits to `rules/skill-format.md`:
1. Reframe test 1 ("same invariant workflow") as "same shared spine" — names the spine as setup gates + shared-context loading; specialist work after the spine may diverge in object-centered orchestrators.
2. Split the strongest-version rule by orientation: operation-centered (parameterization of same operation) vs. object-centered (sibling specialist operations on same object).
3. Scope test 4 (deltas-are-configuration) to the spine only; specialist-work divergence is allowed in object-centered.
Also ported the full command-routed orchestrator material from synapse global into ACW canonical (it had only existed in the operator's personal global rules).
**Rationale:** The strict-voice contradicted the permissive-voice (command-count ladder explicitly carving out object-centered workbenches at 10+ commands). This contradiction false-flagged Impeccable-shape patterns including `/acw-session start|end`. Closing the contradiction lets the rule self-validate.
**Source:** Operator's pushback on my false-flag of `/acw-session start|end`; Impeccable as precedent.
