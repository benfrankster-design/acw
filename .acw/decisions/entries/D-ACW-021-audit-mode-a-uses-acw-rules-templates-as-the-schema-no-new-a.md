---
id: D-ACW-021
title: "Audit Mode A uses ACW rules + templates as the schema; no new artifact"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-021 — Audit Mode A uses ACW rules + templates as the schema; no new artifact

**Date:** 2026-05-02
**Decision:** The audit verb's Mode A (canonical-conventions comparison) fetches ACW canonical rule files (`rules/decision-tracking.md`, `rules/task-tracking.md`, etc.) and template files (`tools/templates/*.tmpl`) directly from GitHub canonical. Compares the workspace's substrate file against the rule and template inline. No structured "canonical-conventions schema" artifact is built; ACW rules + templates ARE the schema in prose form.
**Rationale:** Operator pushed back on the "needs a schema" framing. Right call. The agent doing the audit can compare rule-vs-file the same way an operator would do it manually. Building a structured schema would duplicate what the rules already encode and risk drift between the rule and its serialized form.
**Source:** Operator correction during the v0.4.0 ship plan turn.
