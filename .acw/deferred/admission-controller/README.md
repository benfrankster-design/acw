---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# admission-controller

## What it is

A two-phase mutator + validator that gates every tool call against the workspace's declared contracts. The mutator rewrites incoming calls to normalize them; the validator accepts or rejects based on the contract registry. The two phases are hard-separated — mutators cannot reject, validators cannot mutate.

## What problem it addresses

Frontier problem #5: pre-tool-call semantic validation. Tool calls can be syntactically valid, permitted by authority, and still damage assets because they violate semantic invariants that the tool's signature does not capture. The admission controller catches these at the last moment before the call executes.

## Prior art

Kubernetes admission controllers (the direct ancestor), Eiffel design-by-contract preconditions, SQL constraint checking, HTTP middleware patterns. See `research/02-literature-survey.md`.

## Activation trigger

One cross-domain tool call that damaged an asset. Severity `high` counts as a single triggering incident.

## Shippable form factor

A stdlib Python script (`tools/admission-controller.py`, not shipped) that wraps tool calls and consults the contract registry. Invoked by orchestrator skills before any tool call to a mutating surface. Two-phase internal architecture with strict separation between mutator and validator.

## What it is NOT

- Not a replacement for the broker — the broker gates credentials, this gates semantic validity
- Not a runtime type system for the full workspace — it checks individual tool calls
- Not designed to run as a service — it's a Python script called inline
- Must not ship before the broker — without broker-gated credentials, the admission controller has authority it cannot narrow, which defeats the two-phase discipline
