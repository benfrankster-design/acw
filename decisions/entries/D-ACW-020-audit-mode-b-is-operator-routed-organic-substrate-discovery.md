---
id: D-ACW-020
title: "Audit Mode B is operator-routed organic substrate discovery; ships in v0.4.0"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-020 — Audit Mode B is operator-routed organic substrate discovery; ships in v0.4.0

**Date:** 2026-05-02
**Decision:** Mode B walks the workspace looking for substrate-like patterns (markdown files with frontmatter, dated-prefix filenames, structured directories) not covered by canonical types. For each finding, the verb surfaces a four-option route to the operator: adopt-as-canonical, absorption candidate, instance-specific, or not-substrate. Operator routing is the authoritative classification — the skill never auto-routes Mode B findings.
**Rationale:** Operator pushed back on deferring Mode B. Right call. Mode B doesn't need sophisticated heuristics; it needs the operator in the loop. The decision to absorb upstream vs. declare instance-specific is a judgment call about whether the pattern would generalize, and only the operator has the context to make it.
**Source:** Operator correction during the v0.4.0 ship plan turn.
