---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# contract-registry

## What it is

The aggregated typed view across every skill, every asset, and every tool call in a workspace. The registry is the primitive that all five frontier problems collapse to — the typed contract layer the research synthesis named as the missing foundation.

## What problem it addresses

All five frontier problems at once. The registry is the surface that MECE enforcement, vocabulary lookup, drift detection, credential scoping, and semantic validation all consult. Without a registry, each of those problems has to solve its typing problem independently.

## Prior art

The full typed registry draws from everything ACW ports from in `research/02-literature-survey.md`: SKOS for vocabulary, CloudEvents for event typing, Kubernetes CRDs for declared shapes, object capabilities for scope, PDDL for preconditions, multiparty session types for protocol typing. No single prior art is the ancestor; the registry is the synthesis.

## Activation trigger

A second workspace exists in the same hands. The registry is a cross-workspace consistency layer; testing it requires two instances to maintain consistency across. With only one instance, the registry would be shipping a solution to a problem that does not yet exist.

## Shippable form factor

A generated aggregate file that walks the workspace, reads every skill manifest, every canon entry, every hard rule, every asset frontmatter block, and produces a typed view usable by validators. Generation is a Python script (`tools/build-registry.py`, not shipped). The registry itself is read-only derived output — the sources of truth remain in `rules/` and `skills/`.

## What it is NOT

- Not a runtime database — it's a build artifact
- Not a replacement for the sources of truth — it's a derived view
- Not a standard — it's a minimum viable aggregation
- Not designed to support multi-tenant or multi-operator workspaces without extension
