---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# LINEAGE — Research Chain and Prior Art

This file traces every primitive in ACW v0.1.0 back to the research that produced it. It is the accountability record for what was adapted from prior art versus what was invented. If a primitive cannot be traced here, it should not be in the template.

## Research threads

**Thread 1 — Seven-phase MECE and vocabulary research (April 2026).** A structured research project that ran through problem framing, deep research, operator context capture, research synthesis, consulting briefs, final proposal, and reading report. The final proposal identified the five frontier problems, diagnosed their collapse to the typed contract registry, and proposed the minimum viable primitive set plus deferred library.

**Thread 2 — Controlled vocabulary canon design.** A complementary research project that reviewed SKOS, KCS, Better Rules NZ, DataHub term governance, OntoClean, OOPS!, Skosify, and related prior art. Produced a SKOS-inspired canon schema backed by verified sources. The schema ports directly into `rules/canon-schema.yaml` and the governance state machine ports into `rules/canon-governance.md`.

Both threads are summarized (not reproduced) in `research/`.

## Prior art

The full annotated bibliography lives in `research/sources.md`. This file highlights only the load-bearing ancestors of each primitive.

- **Domain-Driven Design** (Evans, Fowler) — bounded contexts, ubiquitous language. Ancestor of the `domain` field in the canon.
- **SKOS** (W3C) — `skos:Concept`, `skos:prefLabel`, `skos:altLabel`, `skos:hiddenLabel`, `skos:scopeNote`, approval workflow. Direct ancestor of `rules/canon-schema.yaml`.
- **KCS v6** — term-owner model. Ancestor of the N-authority approval generalization (via Better Rules NZ).
- **Better Rules NZ** — government rules-as-code with term-owner model. Intermediate ancestor of N-authority approval.
- **OpenTelemetry semantic conventions** — industry example of maintained cross-vendor vocabulary. Ancestor of the governance discipline throughout ACW.
- **CloudEvents** — typed event envelopes. Ancestor of `deferred/workspace-input-schema/`.
- **Truth Maintenance Systems** (Doyle 1979, de Kleer 1986) — JTMS and ATMS. Ancestor of `deferred/drift-detector/`.
- **AGM belief revision** (Alchourrón, Gärdenfors, Makinson 1985) — postulates for coherent belief revision. Intellectual ancestor of drift-detector.
- **Kubernetes admission control** — two-phase mutator + validator. Direct ancestor of `deferred/admission-controller/`.
- **Object capabilities (Miller canon)** — authority flows by reference-passing. Ancestor of `rules/capability-broker.md`.
- **HashiCorp Vault response wrapping** — single-use tokens. Ancestor of the broker lease model.
- **SPIFFE / SPIRE** — workload identity. Ancestor of the broker's scope-bounded credentials.
- **PDDL preconditions** — typed preconditions in planning. Ancestor of `deferred/self-correcting-contract/` (typed version).
- **Eiffel design-by-contract** (Meyer) — preconditions, postconditions, invariants. Intellectual ancestor of the contract metaphor throughout.
- **Multiparty session types** (Honda, Yoshida, Carbone, POPL 2008) — typed protocols. Ancestor of the self-correcting-contract design.
- **Rust / GHC pattern-match exhaustiveness** — compiler-checked MECE. Intellectual ancestor of mechanical MECE enforcement.
- **OntoClean, OOPS!, Skosify** — ontology quality tooling. Ancestors of `tools/lint-vocab.py` (though ACW's implementation is much simpler).

## Five-lens consulting pattern

The proposal phase used a five-lens adversarial review: standards architect, professional implementer, personal workspace implementer, productizer, skeptic. Each lens caught problems no other lens would have caught. The pattern itself is a contribution of the research project and is documented in `research/04-proposal.md`.

## What was retained vs discarded

**Retained from research:**
- Eight governance-layer primitives in v0.1.0 (canon, governance, lint, broker design, decision tracking, promotion ritual, roles, instance hard rules)
- Eleven design documents in the deferred library with activation triggers
- The earn-by-incident discipline as the mechanical restraint on premature shipping
- Class/authority/stability/loaded_by_agent header convention
- Four-group pipeline roles enum as normative
- Sixteen-role taxonomy as informative appendix
- N-authority approval model as the generalization of term ownership

**Discarded from research:**
- Employer-specific scale references and examples
- Operator-specific decisions that did not generalize
- Quarterly-goal planning framing tied to a specific operating system
- Vendor-specific model references (Claude/GPT/Gemini)
- Full MECE enforcement — replaced with governance-layer approximation
- Admission controller as shipped tool — preserved as design only
- Typed self-correcting contract — preserved as design only

## Justification for pipeline-roles and canon-governance as metabolized prior research

Both `rules/pipeline-roles.md` and `rules/canon-governance.md` are substantial files (800w+ each) that may appear to be new v0.1 creations but are in fact condensed syntheses of prior work. The pipeline-roles enum compresses a larger sixteen-role taxonomy that the author has been iterating on in a separate personal workspace; the four-group normative layer is the v0.1 simplification. The canon-governance file compresses the canon research thread with its twenty-eight sources; the N-authority approval model is the generalization of the term-owner pattern from KCS and Better Rules NZ.

Neither file is a new invention in v0.1.0. Both are metabolized prior research shaped for the single-operator training-ground use case. This distinction matters for the earn-by-incident discipline: the files are shipped as `stability: experimental` because they have not been validated in a non-author environment, not because they are untested in the author's own use.
