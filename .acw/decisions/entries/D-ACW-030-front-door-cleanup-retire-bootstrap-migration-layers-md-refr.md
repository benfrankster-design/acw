---
id: D-ACW-030
title: "Front-door cleanup: retire `bootstrap/`, `migration/`, `LAYERS.md`; refresh README"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-030 — Front-door cleanup: retire `bootstrap/`, `migration/`, `LAYERS.md`; refresh README

**Date:** 2026-05-02
**Decision:** Three meta/template files retired in v0.5.1; README rewritten to reflect current architecture. `bootstrap/README.md` (seven-question greenfield interview) — content absorbed by `tools/scaffold-instance.py` plus templated `research/01-problem-framing.md`. `migration/README.md` (brownfield audit guide) — absorbed by `/acw-instance audit` Mode A+B and `/acw-instance upgrade` adopt-mode. `LAYERS.md` (ACW-specific three-layer narrative) — folded into README.md as "How ACW is layered" section; the generic pattern continues to live in `rules/manifest-discipline.md`. README gained a 60-second scaffold quickstart up front; current operator commands; current directory map (runbooks/, integrations/, briefings/, _buffer/); current load-bearing files.
**Rationale:** Operator question "when's the last time you read the README.md?" exposed v0.1.0-era staleness. Audit of meta-layer found three retirement candidates (functions absorbed by current tooling) and revealed the harness gap — substrate has Phase 2 distribution; meta-layer has none. Front-door fix happens now (v0.5.1); harness ships in v0.6.0 alongside the operator-centric cluster. Three retirements are clean: each file's content is either preserved elsewhere (LAYERS in README, problem-framing template) or now embodied as tooling (scaffolder, audit verb).
**Source:** Operator question on README staleness; meta-layer audit during the v0.5.1 scoping turn.
