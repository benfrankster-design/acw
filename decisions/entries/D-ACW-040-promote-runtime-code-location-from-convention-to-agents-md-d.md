---
id: D-ACW-040
title: "Promote runtime-code-location from convention to AGENTS.md directive 8 (single-incident emergency promotion)"
date: 2026-05-04
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-040 — Promote runtime-code-location from convention to AGENTS.md directive 8 (single-incident emergency promotion)

**Date:** 2026-05-04

**Decision:** Promote the runtime-code-location convention shipped in D-ACW-039 from a "convention only" paragraph in `rules/multi-instance-topology.md` to a normative directive (AGENTS.md #8). AGENTS.md goes from "Seven directives" to "Eight directives." Topology rule paragraph rewritten to drop the "convention only" hedge and point at the directive as the normative source.

**Rationale:** Operator overrode the earn-by-incident framing in D-ACW-039 with a sharper read on what counts as the activating incident. D-ACW-039 framed the absorption note from cx-dashboard-saas as "incident #1, wait for #2 before promoting." Operator's correction: the absorption note is itself meta-evidence; the *real* incident #1 is "agent starts writing runtime code in an instance and has to guess where it goes." That incident fires every time a code-shipping instance spins up. A convention buried in a rule file the agent doesn't read at session start fails to prevent it; the agent guesses, the operator corrects, the friction recurs. The fix has to live in a surface the agent reads at session start.

AGENTS.md is the canonical entry point for any agent opening any ACW workspace, declared `loaded_by_agent: yes`, propagated verbatim to every scaffolded instance via template_layer. Adding a single directive line is the smallest possible form factor for the prevention. This is the structural-prevention single-incident emergency promotion path documented in `rules/promotion-ritual.md` and exercised once before in D-003 (scaffold-instance.py).

**Why this is a structural-prevention class:**
- Form factor: one directive line in AGENTS.md, one paragraph rewrite in topology rule.
- Prevented incident class: agents writing runtime code in an instance without canonical guidance, every session. Recurs by structure, not by accident.
- Cost of waiting for "incident #2": every code-shipping session before #2 fires accumulates the same friction.
- The discipline of earn-by-incident is preserved by the *evidence* requirement (cx-dashboard-saas absorption note is the named, dated, documented incident); operator override applied to the *threshold count*, which is reserved for structural-prevention cases.

**Source:** Operator session 2026-05-04, immediately after D-ACW-039 ship. Operator quote: "the first incident should be writing code runtime code. at acw session start claude should read somewhere about this and if code happens in session it knows what to do."

**Open follow-ups:**
- Schema field `acw-state.yaml::paths::runtime_code_dir` (or similar) — still earn-by-incident. Earns when a skill or audit needs to read the runtime path programmatically.
- Existing instances with runtime code already at root: not retroactively breaking. Migration earns its own decision-log entry per instance if the operator chooses to migrate.
- Other AGENTS.md directive expansions: don't expand on speculation. The eight-directive list is small on purpose. Future directives need the same single-incident emergency promotion or earn-by-incident threshold.
