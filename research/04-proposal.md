---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# 04 — Proposal

After the synthesis phase named the missing foundation, the proposal phase had to decide what to actually ship. This file documents the minimum-primitive-plus-deferred-library proposal and the five-lens review pattern that produced it.

## The proposal in one sentence

Ship the governance-layer precursors to the typed contract registry (canon, roles, lint, promotion ritual, decision tracking) as the minimum viable primitive set, and preserve the full typed-layer design in a deferred library with explicit activation triggers.

## The minimum viable primitive set

**Shipped in v0.1.0:**

1. **Vocabulary canon** — typed concept registry with state machine governance
2. **Vocabulary lint** — commit-time enforcement of forbidden synonyms
3. **Pipeline roles enum** — four normative groups, sixteen-role appendix
4. **Incident ledger** — append-only JSON-lines file recording failures
5. **Promotion ritual** — the mechanical process by which deferred primitives earn their ship
6. **Decision tracking** — open questions, decisions, constraints, resolved questions
7. **Instance hard rules** — per-instance non-negotiable rules with decision-log provenance
8. **Capability broker design** — the doc ships, the tool is deferred

Eight primitives. The smallest set that addresses the governance layer without leaving load-bearing design work on the cutting-room floor.

## The deferred library

Eleven primitives preserved as design documents, each with a named activation trigger. The full table lives in `DEFERRED.md`. The rationale for deferral rather than exclusion is that every primitive here has earned research time — discarding them would lose the design work, while shipping them now would violate earn-by-incident. The library is the middle path.

## The five-lens review pattern

The proposal was reviewed through five lenses in parallel. Each lens had a distinct discipline and a distinct failure mode it was tuned to catch. Together they covered the space that no single reviewer could.

**Lens 1 — standards architect.** Asks: is this faithful to the prior art? Would a SKOS practitioner recognize the canon as a legitimate port? Would a Kubernetes practitioner recognize the admission controller design as a legitimate two-phase split? The standards architect's job is to catch shortcuts that save effort at the cost of interoperability.

**Lens 2 — professional implementer.** Asks: can this actually ship in reasonable effort? Are the Python scripts stdlib-only and platform-portable? Does the CLI surface make sense to someone who did not write it? The implementer's job is to catch design elegance that collapses under real execution constraints.

**Lens 3 — personal workspace implementer.** Asks: is this the right scope for a single operator? Does every primitive earn its place at single-operator scale, or are some of them designed for a larger organization? The personal implementer's job is to catch premature generalization.

**Lens 4 — productizer.** Asks: could this become a product someone would buy, or a consultancy engagement someone would hire for? Is the README understandable to a prospect? Is the activation story compelling? The productizer's job is to catch research that is technically correct but commercially illegible.

**Lens 5 — skeptic.** Asks: should any of this ship at all? What is the smallest slice that delivers real value? What would be lost if the skeptic's minimum set shipped and everything else stayed in the deferred library? The skeptic's job is to catch enthusiasm.

## What each lens changed

The five lenses converged on a proposal substantially tighter than any individual lens would have produced. The standards architect defended the full 11-primitive deferred library against the skeptic's attempts to cut it. The personal workspace implementer defended the four-group pipeline roles against the standards architect's preference for the full sixteen. The productizer defended the README disclaimer against the implementer's preference for terseness. Every decision that survived five-lens review survived because at least two lenses agreed it was load-bearing.

## The two-round stress test

After the proposal was drafted, it went through two rounds of adversarial review before any file shipped.

**Round 1: five parallel audit agents.** Five independent reviewers looked at the full plan from five angles (research fidelity, canon integration, portability, skeptic redux, first principles). Convergent diagnosis: the plan was substantively right but over-engineered by roughly 2x. The skeptic said 24 files; the first-principles reviewer said the same. The research-fidelity and canon-integration reviewers said the substance was load-bearing but sixteen surgical fixes were needed.

**Round 2: external reviews.** The plan was handed to two external reviewers (a long-context reasoning model at one frontier lab, a different model at another frontier lab). The sharper of the two caught four issues no internal reviewer had flagged:
- Class/authority status headers should ship on every non-code markdown file to prevent trust drift
- Earn-by-incident discipline was being applied asymmetrically (strict for code, exempted for prose)
- The dual-view design (canonical table + derived folder tree) had no canonical source declared
- The two-bucket approval model was under-generalized and carried forward an employer-specific noun

Each of those four issues was accepted and baked into the final plan.

## The operator reframing

Mid-proposal, the operator clarified the product question: ACW is not a product waiting for external adopters. ACW is the operator's training ground and toolset. The validation question is not "will someone clone this template from a public repo" but "will someone hire the operator to set up their system." This reframing mattered because it resolved the tension between the skeptic's "ship nothing that doesn't earn its ship" and the standards architect's "the shape is the teaching." Under the training-ground framing, the shape earns its ship via the operator's own learning apparatus, not via external adoption. Prose primitives can ship as `stability: experimental` labels without pretending to be validated.

The reframing is the reason the deferred library ships in full (11 subfolder READMEs + canonical table) rather than being cut to the bare minimum the skeptic would have preferred.
