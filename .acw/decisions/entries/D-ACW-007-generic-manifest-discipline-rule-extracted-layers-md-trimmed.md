---
id: D-ACW-007
title: "Generic manifest-discipline rule extracted; LAYERS.md trimmed to ACW-specific narrative"
date: 2026-04-30
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-007 — Generic manifest-discipline rule extracted; LAYERS.md trimmed to ACW-specific narrative

**Date:** 2026-04-30
**Decision:** The generic three-layer pattern ships as `rules/manifest-discipline.md` in `template_layer`. ACW's own `LAYERS.md` stays in `meta_layer` with ACW-specific content only.
**Rationale:** Operator question surfaced that LAYERS.md as written carried both the generic pattern (would be useful in every derived workspace) and ACW-specific narrative (only useful in ACW). Splitting on that axis makes the pattern reusable; recursive instances (Frank Context, hypothetically) get the same machinery and write their own narrative on top.
**Source:** Operator question on three-layer model shipping behavior; turn 35–37.
