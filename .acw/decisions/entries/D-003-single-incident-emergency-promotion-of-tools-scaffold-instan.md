---
id: D-003
title: "Single-incident emergency promotion of `tools/scaffold-instance.py`"
date: 2026-04-30
status: accepted
kind: decision
updated: 2026-05-13
---

# D-003 — Single-incident emergency promotion of `tools/scaffold-instance.py`

**Date:** 2026-04-30
**Decision:** Ship `tools/scaffold-instance.py` based on Incident D-02 (uuid `616d435b-ec6d-470a-9cdf-2935b739e4a1`) alone, rather than waiting for two more bootstrap-related incidents.
**Rationale:** The promotion ritual's emergency clause is reserved for severity-`high` incidents. D-02 is `med`, but is structurally severe in a different way: every future ACW instance that does not bootstrap from this tool generates more drift incidents downstream. The tool is the *prevention layer* for an incident class, not a primitive earned by lived friction. Form factor is small (~200 lines, stdlib-only), and the prevented incident class is structural. Discipline prefers cheap prevention over earn-by-incident accumulation when both apply.
**Source:** `research/09-gsg-copilot-instance-extensions.md` (final section)
