---
id: D-ACW-006
title: "ACW becomes instance of itself; gains `project:` block"
date: 2026-04-30
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-006 — ACW becomes instance of itself; gains `project:` block

**Date:** 2026-04-30
**Decision:** `acw-state.yaml` carries `project:` block (`name: "ACW"`, `code: "ACW"`, `domain: "meta-template"`). Existing legacy ids `D-001` through `D-005` stay unprefixed; new entries use `D-ACW-NNN`.
**Rationale:** Operator pressed on the framing that "ACW is the template, not an instance" — the accumulated substrate gave the lie to that framing. ACW had been operating as its own instance from session zero. The reframe formalizes ACW = instance + template, both at once. The `project.code` derivation in capture-and-metabolize now works on ACW; the missing-block fallback (skill ships unprefixed ids) remains for downstream one-off instances.
**Source:** Operator-surfaced framing question, turn 37.
