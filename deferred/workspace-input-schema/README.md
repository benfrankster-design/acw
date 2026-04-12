---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# workspace-input-schema

## What it is

A closed enum of verbs, domains, asset types, and surfaces that every skill in a workspace can consume as its typed input shape. The schema is the machine-readable declaration of "what kinds of things can enter this workspace and how are they classified."

## What problem it addresses

Frontier problem #1: mechanical MECE enforcement. Without a closed enum, two skills can claim to handle the same input and the router has no way to decide between them. With the enum, the router consults the schema and dispatches deterministically.

## Prior art

CloudEvents typed event envelopes, Kubernetes custom resource definitions, JSON Schema, OpenAPI. See `research/02-literature-survey.md` for the full survey.

## Activation trigger

Three incidents above `med` severity documenting skill routing collisions where a payload could not be unambiguously classified. One collision is an accident; two is coincidence; three is a pattern that earns the schema.

## Shippable form factor

A single YAML file `workspace.schema.yaml` at the instance root, declaring verbs, domains, asset types, and surfaces as closed enums. Validation is a stdlib Python script that loads the schema and checks incoming payloads against it.

## What it is NOT

- Not a full type system with generics or parametric polymorphism
- Not a protocol specification — it describes shapes, not conversations
- Not a replacement for the canon — the canon governs vocabulary, the schema governs shapes
- Not designed for cross-workspace export (that's `deferred/jsonld-export/`)
