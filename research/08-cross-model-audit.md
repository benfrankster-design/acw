---
class: reference
authority: informative
stability: stable
loaded_by_agent: no
---

# Cross-Model Governance Audit — 2026-04-13

## Method

Two-model sequential review of ACW's governance architecture. Neither model saw the codebase directly. Both were given the design principles and asked to stress-test them.

- **Gemini 3 (thinking mode):** PMF-style analysis of governance primitives. Produced pruning frameworks.
- **ChatGPT (GPT-4o with search):** Literature grounding and steelman. Produced boundary conditions and a concrete design memo.

## Key Frameworks Produced

### 1. Governance PMF

Governance primitives are products. The operator is the market. A primitive that gets bypassed is a market rejection, not a user failure.

### 2. Governance Drift Metric (GD)

$$GD_{rule} = \frac{B}{U + B}$$

- B = bypasses (operator walked around the rule)
- U = usages (rule actually informed a decision)
- GD < 0.2 = healthy
- 0.2 < GD < 0.5 = friction alert
- GD > 0.5 = dead letter (prune or defer)

Requires minimum sample size (~10 events) to be meaningful. Below that, GD is anecdotal.

### 3. Ghost Count

$$\Gamma = \text{Count of primitives where } U = 0 \text{ over } t \text{ days}$$

At low scale, Ghost Count replaces GD as the primary signal. A high ghost count means the workspace is "haunting the present" with unused governance.

### 4. Ghost vs. Deferred Control Taxonomy

| Type | Definition | Treatment |
|------|-----------|-----------|
| Ghost primitive | No consumer, no trigger, no activation criteria | Archive to vision/ |
| Deferred control | No consumer yet, but addresses real non-local risk with explicit activation triggers | Keep design doc in deferred/, strip from runtime schema |

### 5. Artifact-Contract Convergence (Intrinsic Contracts)

**Prefer endogenous governance: make the contract live in the artifact when the rule is local, structural, and stable. Escalate to exogenous governance only when the rule is cross-cutting, dynamic, independently imposed, or system-relational.**

Synthesis of three known families:
- Convention over configuration
- Description-driven / self-describing systems
- Executable specification / living specification

Closest existing literature terms: "endogenous vs. exogenous governance" (EconStor), "infrastructure as code" (Fowler), OPA policy-as-code.

### 6. Six Cases Where Intrinsic Contracts Break

1. Cross-artifact constraints (rules about sets, not items)
2. Runtime and contextual policy (environment, identity, risk tier)
3. Separation of duties (producer should not define acceptability)
4. Legal/institutional compliance (must be effective even if artifact is hostile)
5. Portability and evolution (policy survives artifact format changes)
6. Exception handling (structure-as-contract becomes escape-hatch maze)

### 7. Clean Pruning Rule

- Archive anything unused and unjustified (ghost)
- Defer anything unused but with real non-local risk model and clear activation triggers (deferred control)
- Promote only what has a live consumer and actual enforcement

### 8. Enforcement Chain for Extrinsic Controls

Declaration -> Policy evaluation -> Credential materialization

Without materialization control, governance is theater. A deferred control should stay out of schema until enforcement has a consumer.

## Findings Applied to ACW

### Primitives confirmed as ghosts (archive to vision/)

- 16-role normative override in synapse (revert to four-group)
- Governance tiers (no enforcement, no consumer)
- Canon vocabulary state machine (zero entries in any instance)
- Promotion ritual (never fired, threshold never tested)
- DIP vocabulary standard (already archived)

### Primitives confirmed as deferred controls (keep design, strip from schema)

- Capability broker (legitimate extrinsic governance for verb/relationship rules)

### Primitives confirmed as survivors (keep in runtime)

- Skill folder convention (intrinsic — structure is the contract)
- Instance hard rules (low-friction, high-consequence)
- Four-group role model (lightweight, helps the "second persona")
- Decision log (institutional memory)
- Incident ledger (event recording, not governance)
- gotchas.md per skill (append-only, zero schema)

### New primitives to implement

- Bypass ledger (`bypasses.jsonl`) — parallel to incidents, captures market rejections
- Ghost comment in skill template — "If you are filling this field with a placeholder just to satisfy the schema, the schema has failed."

## Design Principles Extracted

1. **Prefer contracts structurally identical to the thing they govern.** Zero implementation delta means zero drift.
2. **A governance mechanism that never fires is decoration, not governance.**
3. **Infrastructure without a consumer is a hobby.**
4. **A deferred control should stay out of schema until enforcement has a consumer.**
5. **At single-operator scale, operator judgment is the real gate. Mechanical thresholds are aspirational until signal density supports them.**
6. **The stickiest features are where "following the rule" and "doing the work" are the same physical act.**
7. **Log bypasses, not just incidents. Bypasses are market rejections; incidents are system failures. Different signals, different treatment.**

## Cross-Model Audit as Primitive

This session is the first evidence that cross-model review produces insights neither model finds alone. Gemini found the PMF framing and pruning discipline. ChatGPT found the literature grounding, boundary conditions, and the ghost/deferred-control taxonomy.

A fresh session of the same model is a "second persona." A different model entirely is a "second perspective." Both are valuable; they catch different blind spots.

This is logged as Incident 01 for the cross-model auditor deferred primitive.
