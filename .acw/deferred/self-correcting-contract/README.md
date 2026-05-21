---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# self-correcting-contract (typed-remediation version)

## Critical note: two distinct mechanisms share this name

There are two distinct mechanisms in ACW that are both called "self-correcting contract." They solve related problems but via completely different machinery and it is essential not to conflate them.

**The governance-escalation version is already shipping** inside `rules/canon-governance.md`. When the lint detects drift at commit time, the drift is escalated to the declared approval authority, a decision-log entry is opened, and the resolution propagates back into the canon. This mechanism works, ships in v0.1.0, and does not require anything in this folder.

**The typed-remediation version is what this folder documents**, and it is deferred. This version uses MPST-style (multiparty session types) or PDDL-style (planning domain definition language) machinery to define contract postconditions as typed predicates, automatically detect when postconditions have failed, and mechanically repair asset state via a constraint solver or inference engine.

These two mechanisms solve the same shape of problem at two completely different layers. The governance version catches drift with a lint and a human-in-the-loop; the typed version catches drift with a type system and an automated remediation step. The typed version is strictly more powerful and strictly more expensive.

## What it is

Typed contract postconditions attached to every asset and every tool call. When a postcondition fails, a constraint solver or planner produces a repair operation that returns the workspace to a valid state. The machinery is the same shape as MPST typed protocols with automatic session repair.

## What problem it addresses

Frontier problem #3 (drift detection) and problem #5 (semantic validation) at mechanical rather than governance scale. The governance version catches drift and asks a human to fix it; the typed version detects drift and produces the fix as a derived artifact.

## Prior art

Multiparty session types (Honda, Yoshida, Carbone, POPL 2008), PDDL preconditions and effects, Eiffel design-by-contract, Hoare logic, constraint solvers (Z3, cvc5), automated planners. See `research/02-literature-survey.md`.

## Activation trigger

Two conditions, both required:

1. A named incident where the governance-escalation version of self-correcting contract (in `rules/canon-governance.md`) is insufficient to resolve a drift, AND
2. A cited external publication (peer-reviewed or widely-adopted implementation) confirming that MPST- or PDDL-style typed remediation is production-mature for agentic workspaces at single-operator scale.

Both conditions must be documented before this primitive earns promotion review. Neither alone is sufficient.

## Shippable form factor

A constraint solver or planner invocation wrapped in a Python script, consuming typed contract annotations on assets, producing repair operations. Implementation strategy depends on which prior art is cited at activation time.

## What it is NOT

- Not the governance-escalation version — that is already shipped in `rules/canon-governance.md`
- Not a drop-in for any existing typed-remediation framework — it would require adaptation
- Not designed to run at commit time without external infrastructure (solver, planner)
- Not viable without asset frontmatter and the contract registry as prerequisites

Do not conflate this with the governance version. Read the critical note at the top of this file twice.
