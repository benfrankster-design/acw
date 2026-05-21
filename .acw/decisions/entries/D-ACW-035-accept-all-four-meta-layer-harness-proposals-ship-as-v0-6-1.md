---
id: D-ACW-035
title: "Accept all four meta-layer harness proposals; ship as v0.6.1"
date: 2026-05-03
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-035 — Accept all four meta-layer harness proposals; ship as v0.6.1

**Date:** 2026-05-03
**Decision:** Accept all four proposals from the meta-layer harness's first run (post-v0.6.0 `/acw-session end`): extend README directory map with `context/` and `inbox/`; backfill LINEAGE with v0.2.0+ primitive-trace entries; add ORCHESTRATION "v0.2.0+ evolution methodology" section documenting the dogfood-driven loop; add SKEPTIC Warning 4 ("Substrate is not static") earned by incident `e167b922`. Ship as v0.6.1 patch.
**Rationale:** Operator approved with single word ("ship") immediately after the harness surfaced the proposals. The harness earned its build by finding real staleness on its first run; declining the proposals would surface them again on next audit anyway. Better to absorb now while context is warm than to defer and re-discover. The four files together represent the meta-layer's full backfill from the v0.2.0+ cluster — LINEAGE alone has nine primitive-trace gaps closed, ORCHESTRATION gains a major new section, SKEPTIC gains a fifth warning grounded in a documented incident. Validates the harness's first-test correctness (OQ-ACW-010 earn-by-incident path appears clean).
**Source:** Operator approval after Phase 2 meta-layer trigger walk in 2026-05-03 session-end; see build-log entry that documented the proposals.

*(Entries D-ACW-034 down through D-004, dated 2026-04-30 to 2026-05-02, archived to `decisions/decision-log-2026-Q2.md` per the bi-weekly rolling-window discipline in `rules/decision-tracking.md`.)*
