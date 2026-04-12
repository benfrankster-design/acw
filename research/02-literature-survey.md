---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# 02 — Literature Survey

This file surveys prior art relevant to the five frontier problems. Twenty-eight sources were reviewed during the research project. The annotated bibliography with citation tiers lives in `sources.md`; this file focuses on what was ported into ACW and what was deliberately omitted.

## The big four lineages

ACW draws substantively from four lineages. Each contributed a shape or a discipline without being copied wholesale.

### SKOS (Simple Knowledge Organization System, W3C)

SKOS is the W3C standard for representing controlled vocabularies — thesauri, classification schemes, subject heading lists. It defines concepts, preferred labels, alternative labels, hidden labels, definitions, scope notes, and hierarchical relations (broader / narrower / related). The shape of `rules/canon-schema.yaml` is a minimal port of SKOS.

**Ported:** concept_id, pref_label, alt_labels, hidden_labels, definition, scope_note, broader, narrower, related, state machine for approval workflow.

**Not ported:** URIs (ACW does not use namespace identifiers), SKOS-XL (extended labels with lexical relations), multi-lingual labels (one language per instance), full hierarchy semantics beyond parent/child links, collection/ordered collection (too much machinery for the problem ACW solves at v0.1.0).

**Honest port note:** SKOS is designed for static thesauri maintained by librarians. ACW adapts it for a dynamic vocabulary maintained by an operator. The adaptation is load-bearing; the operator is responsible for understanding what was left out.

### Kubernetes admission control

Kubernetes enforces cluster invariants via a two-phase admission control pipeline: mutators run first and can rewrite incoming requests, validators run second and can only accept or reject. The two-phase split is critical — mutators cannot reject, validators cannot mutate. ACW's `deferred/admission-controller/` design applies the same split to tool calls against the workspace.

**Ported:** the two-phase discipline (mutator before validator, hard separation), the reject-only semantics of validators, the idea that the admission layer is separate from the tool itself.

**Not ported:** the webhook mechanism (ACW is local), the Kubernetes CRD ecosystem, the operator pattern. ACW's admission controller is a stdlib Python script in the deferred library, not a running service.

### Object capabilities (Miller canon, SPIFFE/SPIRE, Vault response wrapping)

The object-capability discipline says: authority flows by reference-passing, not by naming. A subject that holds a reference to a capability can use it; a subject that does not hold the reference cannot obtain it. There is no ambient authority. Vault's response wrapping extends this with single-use tokens; SPIFFE/SPIRE extend it with workload identity.

**Ported:** the broker pattern in `rules/capability-broker.md`. Skills declare capabilities they need; the broker issues narrow leases; credentials are never read directly by skills.

**Not ported:** the actual broker implementation (deferred in v0.1.0), the SPIFFE workload attestation machinery, the full Vault lease model. ACW's broker design is a minimum viable capability broker, not a production implementation.

### Truth Maintenance Systems and AGM belief revision

Doyle's JTMS (1979) and de Kleer's ATMS (1986) describe how an inference engine can track contradictions across a justification graph and revise beliefs when new evidence invalidates old conclusions. AGM belief revision (Alchourrón-Gärdenfors-Makinson 1985) formalized the postulates that any revision operation must satisfy to be coherent.

**Ported:** the shape of the drift-detection problem in `deferred/drift-detector/`. The intuition that drift is a contradiction between an old claim and a new one, and that resolving it requires either retracting the old claim or rejecting the new one.

**Not ported:** the actual ATMS machinery, the AGM postulates as executable code, any inference engine. ACW's drift detector design is a design document that names the shape of the problem and points at the literature; it does not ship an implementation.

## The SKOS port table

| SKOS element | ACW treatment | Notes |
|---|---|---|
| `skos:Concept` | `concept_id` | stable identifier, never reused |
| `skos:prefLabel` | `pref_label` | one per concept |
| `skos:altLabel` | `alt_labels` | list |
| `skos:hiddenLabel` | `hidden_labels` | list, enforced by lint |
| `skos:definition` | `definition` | one sentence |
| `skos:scopeNote` | `scope_note` | boundary conditions |
| `skos:broader` | `broader` | optional parent link |
| `skos:narrower` | `narrower` | optional child link |
| `skos:related` | `related` | optional peer link |
| `skos:inScheme` | (omitted) | single-scheme assumption per instance |
| `skos:Collection` | (omitted) | not needed for v0.1.0 |
| `skos:OrderedCollection` | (omitted) | not needed for v0.1.0 |
| URI namespace | (omitted) | string identifiers only |
| SKOS-XL | (omitted) | no lexical relations |
| Multi-lingual labels | (omitted) | single language per instance |

The port is conservative. A future version could extend to full SKOS if cross-instance export becomes load-bearing — that's what `deferred/jsonld-export/` is for.

## Other sources

The full annotated bibliography is in `sources.md`. Highlights:

- **Domain-Driven Design** (Evans, Fowler) — bounded contexts and ubiquitous language. The idea that vocabulary is bounded by domain and contexts talk to each other through explicit translation layers. ACW's domain field in the canon is a minimalist version of bounded context.
- **CloudEvents** — typed event envelopes for cross-system events. Shape inspiration for `deferred/workspace-input-schema/`.
- **OpenTelemetry semantic conventions** — an industry example of a large, maintained, cross-vendor vocabulary with mechanical consistency enforcement. Inspiration for the governance discipline.
- **PDDL** (Planning Domain Definition Language) — preconditions and effects as typed contracts. Inspiration for `deferred/self-correcting-contract/` (typed version).
- **Multiparty session types** (Honda-Yoshida-Carbone, POPL 2008) — typed protocols between multiple parties. Referenced in the deferred self-correcting-contract design.
- **Rust pattern-match exhaustiveness and GHC exhaustiveness checking** — examples of mechanical MECE enforcement in type systems. Inspiration for the intuition that MECE can be checked by a tool rather than a human.
- **OntoClean, OOPS!, Skosify** — ontology quality checkers. Prior art for the idea of lint-gated vocabulary.
- **Eiffel design-by-contract** (Meyer) — preconditions, postconditions, invariants as first-class language features. Inspiration for the contract metaphor.

## What was deliberately not ported

- Anything requiring a running service (Kubernetes CRDs, SPIFFE agents, Vault servers)
- Anything requiring ontology-language machinery (OWL reasoners, Protégé, description logics)
- Anything requiring a typed functional programming language as the host
- Anything requiring an inference engine

ACW is plain-text infrastructure by design. Every primitive that requires more than stdlib Python or a markdown file is deferred.
