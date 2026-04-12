---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Sources — Annotated Bibliography

Every source cited in the research files, with a tier and a verification note. Tiers range from T1 (peer-reviewed or widely-adopted standards body) down to T4 (blog post or working note). Verification notes describe what the author independently confirmed versus what was taken on trust from secondary summaries.

Sources that could not be independently verified during the research project have been excluded from this bibliography rather than preserved on trust. The original research notes contained a larger list; this is the pruned version.

## Vocabulary and controlled terminology

**SKOS Reference (W3C Recommendation, 2009)** — T1, verified. The foundational standard for representing controlled vocabularies. Defines `skos:Concept`, `skos:prefLabel`, `skos:altLabel`, `skos:hiddenLabel`, `skos:broader`, `skos:narrower`, `skos:related`, and the approval workflow semantics. ACW's canon is a minimal port.

**KCS v6 (Knowledge-Centered Service)** — T2, verified. Industry methodology for knowledge management in support organizations. Contributed the intuition that vocabulary should be owned by the people who use it (the term-owner concept) and that drift is detected via usage rather than audit.

**Better Rules NZ** — T2, partial verification. Government-rules-as-code project with a term-owner model that contributed to ACW's N-authority generalization. Only the term-owner pattern was ported; the broader rules-as-code framework is out of scope.

**OntoClean** — T2, verified. Ontology quality methodology focused on catching subsumption errors. Contributed the intuition that ontology quality can be lint-checked.

**OOPS! (OntOlogy Pitfall Scanner)** — T2, verified. A lint-style tool for OWL ontologies. Direct prior art for the idea of vocabulary lint, though ACW's lint is much simpler.

**Skosify** — T2, verified. A Python library for cleaning and validating SKOS vocabularies. Direct prior art for `tools/lint-vocab.py`, though ACW's implementation is stdlib-only and regex-based rather than SKOS-aware.

## Software architecture and domain modeling

**Domain-Driven Design** (Evans, 2003) — T1, verified. The source of "ubiquitous language" and "bounded context." ACW's domain field and the overall discipline of vocabulary-per-domain trace here.

**Patterns of Enterprise Application Architecture** (Fowler, 2002) — T1, verified. Secondary inspiration for the separation of concerns in the pipeline roles enum.

**Eiffel: Design by Contract** (Meyer, 1992) — T1, verified. The origin of preconditions, postconditions, and invariants as first-class language features. Inspiration for the contract metaphor throughout ACW.

## Typed protocols and planning

**Multiparty Session Types** (Honda, Yoshida, Carbone, POPL 2008) — T1, verified. Typed protocols between multiple parties. Referenced in the deferred self-correcting-contract design as the shape of "typed remediation."

**PDDL (Planning Domain Definition Language)** — T1, verified. Preconditions and effects as typed contracts for planners. Referenced in the deferred self-correcting-contract design.

**AGM belief revision** (Alchourrón, Gärdenfors, Makinson, 1985) — T1, verified. The postulates that any belief revision operation must satisfy. Referenced in the drift-detector design.

**Truth Maintenance Systems** (Doyle, 1979) — T1, verified. The original JTMS paper. Referenced in the drift-detector design.

**ATMS** (de Kleer, 1986) — T1, verified. The assumption-based TMS. Referenced in the drift-detector design.

## Infrastructure and capability discipline

**Kubernetes admission controllers** — T2, verified via official documentation. Two-phase mutator + validator pattern. Direct shape inspiration for `deferred/admission-controller/`.

**Object capabilities (Miller canon)** — T1, verified. The discipline that authority flows by reference-passing. Foundational to the broker design.

**SPIFFE / SPIRE** — T2, verified via specification. Workload identity and attestation. Referenced in the broker design as prior art for scope-bounded credentials.

**HashiCorp Vault response wrapping** — T2, verified via official documentation. Single-use token pattern for credential handoff. Direct inspiration for the broker's lease semantics.

**CloudEvents specification** — T2, verified via specification. Typed event envelopes. Inspiration for `deferred/workspace-input-schema/`.

**OpenTelemetry semantic conventions** — T2, verified via the semantic conventions repository. Industry example of a maintained cross-vendor vocabulary. Inspiration for ACW's governance discipline.

## Type systems

**Rust pattern-match exhaustiveness** — T2, verified via the Rust Reference. Example of mechanical MECE enforcement by the compiler.

**GHC pattern-match exhaustiveness checking** — T2, verified via GHC documentation. Same pattern, different language.

## Threat modeling

**Willison's "lethal trifecta"** — T3, verified via author's public writing. The threat model that names access to sensitive data + exfiltration path + untrusted content as the dangerous combination. Referenced throughout `SKEPTIC.md` and the threat model.

## Explicit exclusions

The following sources appeared in earlier research notes and were excluded from this bibliography because they could not be independently verified during the research project. Their absence is intentional.

- Several blog posts on "agent memory architectures" whose technical claims could not be traced to primary sources
- An unreleased internal specification from one lab that was paraphrased in a conference talk but never published
- Several academic papers whose abstracts matched the research question but whose full text was not reviewed

Excluding an unverified source is the right call even when the source's claims sound correct. The research project adopted this discipline after an early draft was caught citing a paper whose abstract had been hallucinated by an LLM assistant during bibliography assembly.
