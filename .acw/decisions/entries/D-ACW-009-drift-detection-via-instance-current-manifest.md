---
id: D-ACW-009
title: "Drift detection via instance-current-manifest"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-009 — Drift detection via instance-current-manifest

**Date:** 2026-05-02
**Decision:** New file `rules/instance-current-manifest.md` (template_layer) declares the recommended-blocks registry. Each entry documents what / why / required / how-to-add / earned-in. `/resume-session` Step 5 reads the registry, compares earned-in versions against `acw-state.yaml::last_reconciled_version`, and surfaces a one-line drift alert when gaps exist.
**Rationale:** ACW evolves; existing instances need a way to learn they're behind without manual audit. The registry is the source of truth for "what current ACW expects"; the alert is the prompt; `/upgrade-instance` (D-ACW-010) is the action. Backwards-compatible — instances with no `last_reconciled_version` field default to `"0.0.0"` and get a noisy first run that quiets after one reconciliation.
**Source:** Operator instruction during the "framework-agnostic skills" scoping conversation, turns 67–73.
**Implementation note:** Required adding `last_reconciled_version` (semantic version) alongside the existing `last_reconciled` (date) field in `acw-state.yaml`. Subagent caught the version-vs-date conflation during Phase 4 verification; fixed before commit.
