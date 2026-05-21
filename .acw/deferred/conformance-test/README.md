---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# conformance-test

## What it is

A twelve-check runner that validates a workspace against the full ACW primitive set: schema conformance, contract registry coherence, canon approval state validity, role declaration integrity, hard-rule enforcement, lint cleanliness, incident log format, header consistency, drift-detector clean run, deferred-library drift, decision-log coherence, and credential broker scope narrowness.

## What problem it addresses

Meta-level validation. Individual primitives each check their own thing; the conformance test checks that all of them together constitute a coherent ACW instance. Without it, a workspace can pass every individual check while being globally incoherent.

## Prior art

Kubernetes conformance tests, RFC compliance suites, language specification test suites (Python's test suite, Rust's compiler test suite). See `research/02-literature-survey.md`.

## Activation trigger

Activation of `deferred/contract-registry/`. The conformance test cannot run without the registry to validate against.

## Shippable form factor

A Python script (`tools/conformance-test.py`, not shipped) that invokes each individual check and reports a structured pass/fail matrix. Stdlib-only, offline-capable, runnable as `python tools/conformance-test.py`.

## What it is NOT

- Not a replacement for individual primitive tests — it composes them
- Not a certification — passing the conformance test is a self-check, not an external validation
- Not designed to catch novel primitive failures — it only checks what it knows to check
