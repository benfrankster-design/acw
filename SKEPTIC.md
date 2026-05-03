---
class: reference
authority: canonical
stability: stable
loaded_by_agent: yes
---

# SKEPTIC — Five Warnings and a Do-Not-Do List

This file exists because the author knows their own failure mode. Builder-mode tunnel vision is a real hazard when working on infrastructure, and the earn-by-incident discipline is the mechanical restraint against it. The skeptic is the voice of that discipline in prose form.

Before proposing any extension to ACW — a new role in the enum, a new primitive in the deferred library, a new tool, a new governance layer — read this file and check your proposal against the five warnings.

## Warning 1 — Selection bias

The research that produced ACW surveyed a specific slice of prior art, filtered through the author's background and the specific problems observed in the author's own workspace. It is not a comprehensive survey. There are communities, literatures, and tools that are highly relevant to these problems and were not reviewed because the author did not know they existed or did not have time to verify them.

Before proposing that ACW adopt a new pattern, check whether the pattern already has a better-developed implementation in a community the author did not survey. See `research/01-problem-framing.md` for the scope of the original research.

## Warning 2 — Reinvention

Several primitives in ACW's deferred library are minimum viable versions of things that already exist in more mature form elsewhere: SKOS for controlled vocabularies, Kubernetes admission control for two-phase validation, object capabilities for credential management, truth maintenance systems for drift detection. Before shipping an ACW-specific primitive, check whether the existing mature tool can be adapted instead.

The reason ACW ships its own minimum-viable versions is specifically that the mature tools come with infrastructure (running services, type systems, inference engines) that ACW does not have. If you are in an environment where the mature infrastructure is available, use it. See `research/02-literature-survey.md` for the port decisions.

## Warning 3 — Transfer failure

A primitive that works in one workspace may fail in another for reasons that are not obvious in advance. Vocabulary that is well-partitioned for one operator's domains may collide for another's. Role declarations that are well-separated in one skill architecture may be ambiguous in another. The pipeline-roles enum is stable in the author's own usage; it is experimental in any other environment.

Before declaring that ACW's primitives "work" for your workspace, log at least one month of real incidents and review them against the primitive's intended behavior. If the primitive is silent, that is information — the silence might mean it's working or it might mean the failure mode hasn't surfaced yet.

## Warning 4 — Substrate is not static

(Earned 2026-05-03 via incident `e167b922`. README went stale across four versions before someone noticed because substrate had Phase 2 distribution since v0.4.0 and meta-layer had no equivalent harness. The asymmetric build assumed meta-layer was reference material that doesn't drift; it was wrong.)

Any file class that the operator or agents *read* drifts. Decisions drift. Tasks drift. Glossaries drift. So do narrative files — README, CHANGELOG, LINEAGE, ORCHESTRATION, SKEPTIC, top-level rules. Treating any class as "static reference" is a category error: if a reader will ever look at it after the moment of writing, it's substrate, and substrate without a maintenance harness will go stale silently.

The mitigation is symmetric maintenance discipline. v0.6.0 shipped the meta-layer maintenance harness gated on `acw-state.yaml::meta_layer` block presence. Before proposing that a new file class needs no maintenance harness, check whether the file is meant to be read more than once. If yes, it needs trigger detection in `/acw-session end` Phase 2 and staleness detection in `/acw-instance audit`.

The general anti-pattern: every "this won't drift, it's just reference" claim has been wrong on a long enough timeline. Default to assuming any file in the workspace will need maintenance unless you can name a specific reason it won't (license texts; binary assets; declarative manifest entries that are themselves the source of truth).

## Warning 5 — Reflexive injection

Several of ACW's primitives ask an agent to validate its own output against a rule the agent wrote. The lint is run by the agent; the canon is edited by the agent; the incident log is written by the agent. This is a reflexive loop and it has a known failure mode: the agent can silently collude with itself, passing validations that should fail because the agent has already rationalized the violation into compliance.

The mitigation is human review at key points. Specifically: the canon's approval state machine requires a named approval authority, not just "the agent said so." The decision-log exists so that decisions have a record outside the agent's conversation. The incident log exists so that failures are counted by a tool, not remembered by an agent. None of these fully defeat reflexive injection — they make it harder.

## Known v0.1 limitations

The research identified six unresolved issues that are not solved in v0.1.0 and will not be solved without real incidents to earn their solutions:

1. **Partial overlap semantics.** Two skills that legitimately overlap by design (e.g., two auditors checking overlapping properties) have no clean declaration surface. Forced into pure MECE they become awkward; left alone they collide.

2. **Reality drift.** The canon describes the workspace's ground truth at the moment each term was approved. There is no mechanism for detecting when the world has changed and the ground truth is now wrong.

3. **Repair-hint format.** When the lint catches a forbidden synonym, it emits a one-line repair hint. There is no schema for the hint, so downstream tools cannot parse it structurally.

4. **LLM validation cost.** Several deferred primitives (drift-detector, self-correcting-contract) would benefit from LLM-powered validation steps, but the cost of running those steps at commit time is not addressed in v0.1.0.

5. **Reflexive injection (Warning 5).** Documented but not mitigated beyond human review.

6. **Prompt cache and revoked lease interaction.** When the broker ships and leases become short-lived, there is an interaction with LLM prompt caching that has not been analyzed. A cached prompt may hold a reference to a lease that has already been revoked.

## Do not do

Five specific things the author has explicitly decided ACW should not do, each with a one-line rationale.

1. **Do not rebrand existing vocabularies.** If SKOS calls something a `prefLabel`, do not invent a new name. Ported fields keep their source names; new fields get new names.

2. **Do not pitch to leadership before incident evidence.** "We should adopt ACW across the organization" is a pitch that needs three documented incidents to back it up. Without incidents it is enthusiasm, not evidence.

3. **Do not build admission controllers before brokers.** The broker gates credentials; the admission controller gates tool calls. Building the admission controller first means the admission layer has authority it cannot narrow, which is the exact problem the broker exists to solve.

4. **Do not publish to standards bodies unvalidated.** ACW is a template. It is not a standard. Submitting it to a standards body without at least two independent workspaces and one external contributor is noise in the standards process.

5. **Do not call anything a "standard" without adopters.** "Standard" is a word with a specific meaning — a thing with external adopters and some form of governance. ACW is not a standard. It is a template.

## Closing rule

**No deferred primitive promotes without a dated, documented incident.** This is the single mechanical rule that defeats builder-mode. Break this rule and you have broken ACW's earn-by-incident discipline; everything else in the template is downstream of this rule working.
