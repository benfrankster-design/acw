---
id: D-ACW-023
title: "Hard-stop scan widened to root-level organic substrate"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-023 — Hard-stop scan widened to root-level organic substrate

**Date:** 2026-05-02
**Decision:** `/acw-instance upgrade` adopt-mode hard-stop now counts (a) markdown files in `decisions/` and `rules/` (existing v0.4.0 logic) PLUS (b) root-level directories not in canonical PLUS (c) root-level non-canonical markdown files. The threshold (default 5) applies to the total. v0.4.0 counted only (a) and missed exactly the case it was designed to catch — workspaces like `_Command` accumulate organic substrate at root, not inside `decisions/` or `rules/`.
**Rationale:** `_Command` audit revealed ~1 file each in `decisions/` and `rules/` (well under threshold) despite having `briefings/`, `runbooks/`, `integrations/`, `notes/`, `context/` directories at root. v0.4.0 hard-stop wouldn't have fired; would have steamrolled into adoption. v0.5.0 fixes scope.
**Source:** `_Command` audit dogfood incident.
