---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# jsonld-export

## What it is

A JSON-LD `@context` file that maps ACW's canon and schema to public vocabularies (SKOS, schema.org, Dublin Core, CloudEvents), allowing the workspace to export its controlled vocabulary to external systems that speak JSON-LD.

## What problem it addresses

Cross-system vocabulary handoff. The canon is locally consistent within a workspace but uses plain string identifiers, not URIs. Export to an external system (a client, a partner, a public repository) requires the vocabulary to be linkable and dereferenceable.

## Prior art

JSON-LD 1.1 specification, SKOS URI conventions, schema.org, Dublin Core, Linked Open Data principles. See `research/02-literature-survey.md`.

## Activation trigger

Handing controlled vocabulary to an external client or partner who needs to integrate it with their own systems. Severity-neutral: the trigger is a real external request, not an internal incident.

## Shippable form factor

A single `canon.context.jsonld` file at the instance root, hand-authored or generated from `canon.yaml` by a script (`tools/build-jsonld.py`, not shipped). The file maps every canon concept to a URI under a declared namespace and binds every field (`pref_label`, `alt_labels`, etc.) to its SKOS equivalent.

## What it is NOT

- Not a full Linked Data deployment — just a `@context` file
- Not a replacement for the canon — it's a derived export
- Not designed to run as a service — it's a static build artifact
- Not sufficient for two-way synchronization with external systems — it's one-way export only
