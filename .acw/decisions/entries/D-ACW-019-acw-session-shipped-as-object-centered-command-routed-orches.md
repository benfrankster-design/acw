---
id: D-ACW-019
title: "`/acw-session` shipped as object-centered command-routed orchestrator (verbs: start, end)"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-019 — `/acw-session` shipped as object-centered command-routed orchestrator (verbs: start, end)

**Date:** 2026-05-02
**Decision:** Renamed `/resume-session` → `/acw-session start` and `/capture-and-metabolize` → `/acw-session end` as a single object-centered command-routed orchestrator. Object: this ACW instance's session lifecycle. Verbs: boundary operations on it. Shared spine: load `acw-state.yaml`, resolve `paths`, check `_inbox/`, identify recent captures. Specialist work after the spine diverges per verb (Impeccable pattern).
**Rationale:** Initial pushback (the four-test rule reading "same invariant workflow") was based on the strict voice in the old skill-format. Operator pointed at Impeccable as the precedent: 23+ commands across genuinely different specialist workflows, unified by shared setup and shared object. Re-reading the skill-format with that lens, `/acw-session start|end` fits cleanly. Skill-format also tightened in same release to remove the strict-voice/permissive-voice contradiction.
**Source:** Operator's invocation of Impeccable as precedent; subsequent skill-format correction.
