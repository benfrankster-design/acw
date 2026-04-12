---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# 03 — Synthesis

This file is the turning point of the research project. Phase 1 surveyed the problem space, phase 2 surveyed prior art, and this phase diagnosed what the survey revealed: the five frontier problems are not five problems at all. They are five symptoms of one missing foundation.

## The diagnosis

Every failure mode documented in phase 1 traces back to the same structural absence: the workspace has no machine-readable contract layer that every skill, asset, and tool call is validated against.

| Symptom | Trace to missing foundation |
|---|---|
| Skills collide on overlapping input shapes | No typed input schema the router can consult |
| Vocabulary drifts across agents and sessions | No canonical term registry the lint can enforce |
| Assets go stale without detection | No typed claim structure the drift detector can measure against |
| Credentials accumulate beyond need | No declaration surface for skill scope that the broker can narrow |
| Tool calls pass syntax but violate semantics | No typed precondition the admission layer can check |

Once you see the pattern, the shape of the solution follows directly: build the typed layer the tools need, and each tool becomes tractable.

## The missing foundation: a typed contract registry

The research calls this primitive "the typed contract registry." It is deferred in v0.1.0 (see `deferred/contract-registry/`), but v0.1.0 ships its governance-layer precursor: the canon, the pipeline roles enum, and the vocabulary lint. These three primitives together form the minimum viable version of the registry's contract-declaration surface.

**Canon** = the typed vocabulary layer. Every concept has a stable id, a preferred label, a definition, a domain, and an approval state. Every lookup in the workspace that would historically be a keyword match is now a canonical-id match.

**Pipeline roles enum** = the typed role layer. Every skill declares exactly one role from a closed enum. Every role has a declared set of allowed operations. Role ambiguity becomes a lint-detectable condition instead of a subtle bug.

**Vocabulary lint** = the enforcement edge. At commit time, content that contains forbidden synonyms is rejected. The canon is not documentation; it is the thing the lint consults to decide what passes.

These three together give v0.1.0 roughly half the benefit of the full registry at roughly one-tenth the complexity. The remaining half waits for a second workspace.

## Why governance ships before typing

The research considered three alternative synthesis paths:

**Path A — ship the full typed registry in v0.1.0.** Rejected. Requires a second workspace for validation. Requires the broker, the admission controller, and the drift detector to all work together. Rejected as premature.

**Path B — ship nothing until the full registry is ready.** Rejected. The canon and the pipeline roles enum provide real value at single-workspace scale, and their absence forces every workspace to solve the same problems from scratch. Rejected as unnecessarily austere.

**Path C — ship the governance-layer precursors and hold the typed registry in deferred library.** Selected. The governance layer is valuable on its own. The typed registry activation trigger is "second workspace exists." The deferred library preserves the design work so the typed layer ships fast when the activation fires.

Path C is the ACW v0.1.0 decision. Every primitive that made it into `rules/` is a governance-layer precursor. Every primitive that landed in `deferred/` is a typed-layer primitive waiting for its activation trigger.

## The cross-cut with Willison's "lethal trifecta"

Willison's threat model names three properties that combine to make an LLM agent dangerous: (1) access to sensitive data, (2) access to a way to exfiltrate data, (3) exposure to untrusted content. All three together are the lethal trifecta; any two are acceptable.

ACW's role separation and broker pattern address the trifecta directly: skills that hold credentials do not read untrusted content, skills that read untrusted content do not hold credentials, and skills that exfiltrate (the committer role) cannot classify (the classifier role). The role enum enforces the split at declaration time; the broker enforces it at runtime (when it ships).

This is not a replacement for Willison's discipline — it is an architectural realization of it. The fact that ACW's role enum and the lethal trifecta point at the same shape is evidence that both are tracking a real structure.

## What the synthesis did not resolve

The synthesis phase produced the diagnosis but did not produce a complete solution. Several questions were explicitly left open for the proposal phase and beyond:

- How should the canon handle polysemes where domain is genuinely ambiguous?
- How should the broker revoke leases that are no longer needed but have not been explicitly released?
- How should drift detection distinguish contradiction from update?
- How should MECE enforcement handle the case where two skills legitimately overlap by design?

Each of these open questions maps to a deferred primitive with its own activation trigger. The synthesis's contribution is the diagnosis, not the full answer.
