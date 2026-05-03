---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# LINEAGE — Research Chain and Prior Art

This file traces every primitive in ACW back to the research or evidence that produced it. It is the accountability record for what was adapted from prior art versus what was invented vs what earned its build through documented incidents in the operator's own use. If a primitive cannot be traced here, it should not be in the template.

The v0.1.0 cluster traces to formal research projects (threads 1–2 below, surveying 50+ sources). The v0.2.0+ cluster traces predominantly to **earn-by-incident in the operator's own dogfood across multiple instances**, with selected absorptions from prior art surfaced when the incident pointed at an existing pattern.

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

## v0.2.0+ primitives (earned-by-incident; selected prior-art absorption)

The v0.2.0+ cluster shipped on a different cadence: substantive new primitives earned from operator dogfood across multiple instances (`gsg-copilot` / `cs-copilot`, `_Command`, ACW itself), with absorption candidates promoted via the formal arc when patterns generalized. Each entry traces to its triggering evidence, not to a research project.

### Substrate categories

- **`tasks-status.md` and `build-log.md`** — ported from `cs-copilot`'s lived experience (3 weeks of single-operator use). See `research/09-gsg-copilot-instance-extensions.md` C-01, C-02. Earned in v0.2.0-rc1.
- **`runbooks/`, `integrations/`, `briefings/`** — absorbed from `_Command`'s organic substrate during the first `/acw-instance audit` dogfood (2026-05-02). Original audit verdict mis-classified these as instance-specific; operator pushback identified them as universal patterns. See decision-log D-ACW-029. Earned in v0.5.0.
- **`context/` (with `goals.md` / `objectives.md` / `how-i-work.md` / `key-people.md`)** — absorbed from `_Command`'s organic substrate. Lightweight pointer layer that decisions/rules/skills/glossary didn't address. See decision-log D-ACW-031. Earned in v0.6.0.
- **`inbox/` (operator capture surface, no underscore)** — designed alongside `context/`; distinct from `_buffer/` (system surface) and `briefings/` (agent-generated snapshots). Three-surface model surfaced from operator design conversation, not from prior art. See decision-log D-ACW-033. Earned in v0.6.0.

### Architectural primitives

- **Three-layer manifest (`template_layer` / `instance_layer` / `meta_layer`)** — earned by D-005 / D-ACW-007 incidents. Originally the scaffold tool carried five hardcoded Python lists; adding a propagatable file required paired script edits, and forgotten edits silently broke instances scaffolded thereafter. Operator surfaced the gap. Generic pattern extracted into `rules/manifest-discipline.md` v0.2.0-rc3. No formal prior-art ancestor; pattern is recurrent across infrastructure-as-code (Terraform modules vs root, Helm chart templates) but not a direct port.
- **Multi-instance topology (org-brain + departmental lattice)** — earned from operator question on whether ACW could run a full business. See `research/10-multi-instance-topology.md` for the derivation. Promoted to canonical rule in v0.3.0 (D-ACW-012). Conceptual ancestors: SOA service boundaries, microservices' Conway's-law shape, federated knowledge graphs. None ported directly; framing is operator-derived.
- **Command-routed orchestrator pattern (object-centered + operation-centered)** — direct port from `pbakaus/impeccable` design system skill (`https://impeccable.style/docs/impeccable/`). The format spec for command-routed skills was authored in the operator's synapse global rules with Impeccable as the cited precedent; v0.4.0 ported the material into ACW canonical with three corrections to reconcile strict-voice with object-centered carve-out (D-ACW-016). The five-test for object-centered orchestrators is operator-original.
- **GitHub-first canonical fetch** — earned by D-ACW-014 (cs-copilot session showed local manifest snapshots go stale silently). No prior-art ancestor; the discipline (canonical lives in one remote repo, instances cache via fetch-on-demand) is a single-source-of-truth shape common in package managers and config-as-code systems.
- **`is_canonical_source` flag and absorption mechanics** — earned from D-ACW-015 (operator caught the would-be-bug where Phase 2 push prompt would propagate to child instances). Absorption mechanics formalize the cross-instance handoff seed already present in `_buffer/` (originally `_inbox/`). Direct conceptual ancestor: monorepo-with-publish-subscribe patterns; no specific port.

### Skills

- **`/acw-session start|end` (object-centered command-routed; replaces `/resume-session` and `/capture-and-metabolize`)** — restructure earned in v0.4.0. The two skills had been operating as a sequential pair since v0.2.0; collapsing into one orchestrator with two verbs improved muscle-memory and namespace coherence per D-ACW-019. Spec template ancestor: Impeccable.
- **`/acw-instance audit|upgrade` (object-centered command-routed; replaces `/upgrade-instance`)** — earned in v0.4.0 (D-ACW-018). Audit verb's Mode A (canonical comparison via fetched rule files + templates) and Mode B (operator-routed organic substrate discovery) earned in v0.5.0 from the first `_Command` audit dogfood (D-ACW-026 retrospective on v0.4.0 audit verb's five bugs). Hard-stop scope widened in v0.5.0 (D-ACW-023) when `_Command` evidence showed the v0.4.0 scope (only `decisions/` and `rules/`) missed root-level organic substrate.

### Tooling

- **`tools/scaffold-instance.py`** — earned by D-02 incident. Single-incident emergency promotion: `gsg-copilot` had not bootstrapped from the (then-empty) `bootstrap/` directory and grew its substrate parallel-evolution-style, generating downstream drift incidents. Tool prevents the incident class structurally. See `research/09-gsg-copilot-instance-extensions.md` (final section).
- **`tools/manifest.py`** — earned in v0.2.0-rc4 (D-ACW-008). Stdlib-only reference implementation of the four-operation manifest tooling spec (load / append / contains / validate). 33-test TDD; subagent-verified spec/impl alignment.

### Discipline primitives

- **`rules/instance-current-manifest.md` (recommended-blocks registry) + drift detection in `/acw-session start`** — earned in v0.2.0-rc4 (D-ACW-009, D-ACW-010). Closes the loop between "ACW evolves" and "downstream instance learns it's behind." No prior-art ancestor; pattern is operator-derived and resembles dependency-version freshness checks in package managers.
- **Meta-layer maintenance harness (`/acw-session end` Phase 2 + `/acw-instance audit|upgrade` meta-layer staleness check)** — earned in v0.6.0 (D-ACW-034) from `e167b922` incident: README went stale across four versions before someone noticed because substrate had Phase 2 distribution but meta-layer had nothing. Closes the asymmetric-build gap. No prior-art ancestor; the pattern is a generalization of the substrate Phase 2 discipline applied to a different file class.
- **Earn-by-incident applied recursively (to spec evolution, not just primitive promotion)** — earned through the v0.2.0–v0.6.0 cluster as a recurring pattern. Original earn-by-incident was about deferred-library promotion (`rules/promotion-ritual.md`); the recurring pattern extends it to: spec ambiguities revealed by dogfood earn next-version tightening (D-ACW-016), missing maintenance harnesses revealed by staleness earn the harness (D-ACW-034), conservative classification revealed by operator pushback earn re-classification (D-ACW-029, D-ACW-025). Documented as methodology in `ORCHESTRATION.md` § "v0.2.0+ evolution methodology."
