---
id: D-002
title: "Supersede `skills/capture-session/` with bookend pair"
date: 2026-04-30
status: accepted
kind: decision
updated: 2026-05-13
---

# D-002 — Supersede `skills/capture-session/` with bookend pair

**Date:** 2026-04-30
**Decision:** Replace the standalone `capture-session` skill with a pair: `capture-and-metabolize` (end-of-session, five phases) and `resume-session` (start-of-session). The four sub-steps of the original skill become Phase 1 internal sub-steps of `capture-and-metabolize`.
**Rationale:** Three weeks of lived experience in `gsg-copilot` proved the bookend shape (paired session-start and session-end skills, with substrate maintained as a side effect of distribution) eliminates manual scaffolding maintenance. The standalone `capture-session` covered only one end of the loop.
**Migration:** The original `skills/capture-session/` directory is marked superseded in-place; manual operator deletion required (the careful guardrail blocked automated removal).
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-03
