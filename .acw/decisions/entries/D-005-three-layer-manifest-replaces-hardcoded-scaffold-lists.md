---
id: D-005
title: "Three-layer manifest replaces hardcoded scaffold lists"
date: 2026-04-30
status: accepted
kind: decision
updated: 2026-05-13
---

# D-005 — Three-layer manifest replaces hardcoded scaffold lists

**Date:** 2026-04-30
**Decision:** `acw-state.yaml` now carries three blocks — `template_layer`, `instance_layer`, `meta_layer` — that classify every file in ACW. The scaffold tool reads from this manifest instead of carrying hardcoded `VERBATIM_FILES` / `VERBATIM_RULES` / `TEMPLATED_FILES` lists. Default for new files is `instance_layer`; promotion to `template_layer` or `meta_layer` requires an explicit decision-log entry.
**Rationale:** ACW is both a template and its own first instance. Without explicit classification, the template-vs-instance split lived inside scaffold-instance.py as five hardcoded lists — adding a new propagatable file required a paired script edit, and a forgotten edit silently broke instances scaffolded thereafter. The asymmetry of mistakes (instance content shipping as template > template missing from instance) drives the default-to-instance discipline. This is the third application of the manifest-discipline pattern in ACW (after `auto_load_at_session_start` and the canon governance state machine), making the pattern itself worth naming.
**Source:** Operator-flagged during v0.2.0-rc1 absorption work; classified as the actionable form of D-01/D-02 follow-up.
**See also:** `LAYERS.md` (the meta_layer explainer).
