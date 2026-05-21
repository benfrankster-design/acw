---
id: D-ACW-026
title: "`_Command` audit dogfood incident retrospective"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-026 — `_Command` audit dogfood incident retrospective

**Date:** 2026-05-02
**Decision:** First `/acw-instance audit` against `_Command` produced clean Mode A output but exposed five bugs in v0.4.0: (1) hard-stop scan counted only `decisions/` and `rules/` files; missed root-level organic substrate. (2) Mode B walk produced static report with proposed routings instead of interactive prompts; nothing landed in `_buffer/`. (3) Default routing was `[s] instance-specific`; should be `ask, don't guess`. (4) Skills audit not part of verb spine. (5) Absorption flow gated on workspace registration. Five bugs all earned by this single dogfood.
**Rationale:** Earn-by-incident in action. v0.4.0 design was sound at the rule level but the verb implementation had ambiguities and gaps that only surfaced under real-workspace use. v0.5.0 fixes all five, plus reverses the conservative routing on three substrate categories that turned out to be universal patterns.
**Source:** Operator pasted `_Command` audit report; agent reading produced the bug list; operator confirmed fixes.
