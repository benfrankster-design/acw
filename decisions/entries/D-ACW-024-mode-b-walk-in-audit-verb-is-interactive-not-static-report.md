---
id: D-ACW-024
title: "Mode B walk in audit verb is interactive, not static-report"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-024 — Mode B walk in audit verb is interactive, not static-report

**Date:** 2026-05-02
**Decision:** Audit verb's Mode B (organic substrate discovery) prompts the operator interactively per finding with the four-option route (`[a]/[b]/[s]/[n]`). Writes happen during the walk on `[b]` routing, not after the report finalizes. Default is "ask, don't guess" with explicit comparison to canonical surfaced in the prompt.
**Rationale:** v0.4.0 spec said "surface to the operator" which an agent could plausibly interpret as "include in the report." `_Command` audit produced static report; nothing landed in `_buffer/`. Spec tightened to make the interactive walk unambiguous. Also: default routing of `[s]` was too conservative — Mode B's whole point is the operator-as-judgment-call; auto-classifying defeats the purpose.
**Source:** `_Command` audit dogfood incident.
