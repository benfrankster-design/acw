---
id: D-ACW-022
title: "Hard-stop threshold for adopt-mode set at 5"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-022 — Hard-stop threshold for adopt-mode set at 5

**Date:** 2026-05-02
**Decision:** `/acw-instance upgrade` adopt-mode bails (with pointer to `/acw-instance audit`) when the count of non-canonical markdown files in `decisions/` or `rules/` is at-or-above 5. Threshold lives in `acw-state.yaml::adopt_mode_organic_threshold` with canonical default 5.
**Rationale:** Below-5 catches cs-copilot-shape workspaces (canonical-shaped, just unregistered; ~1-2 files). At-or-above-5 catches `_Command`-shape workspaces with substantial organic substrate. Tunable per-instance only when the default produces wrong-direction failures in practice.
**Source:** Operator-confirmed during the v0.4.0 ship plan synthesis turn.
