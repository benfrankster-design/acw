---
id: C-001
title: "`skills/capture-session/` directory still exists on disk"
date: 2026-05-13
status: active
kind: constraint
updated: 2026-05-13
---

# C-001 — `skills/capture-session/` directory still exists on disk

`skills/capture-session/` is marked superseded in its SKILL.md frontmatter (`status: superseded`, `superseded_by: skills/capture-and-metabolize/`) but the directory itself was not removed. The careful guardrail blocked automated `rm -rf`. Operator must delete manually before the v0.2.0 tag.
