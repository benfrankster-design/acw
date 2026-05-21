---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# aaif-submission

## What it is

A governance and publication path for contributing ACW primitives upstream — either to a hypothetical Agentic AI Interoperability Forum (AAIF) or to whichever standards body emerges to govern agentic workspace interoperability. The primitive is the process documentation for how a workspace would submit a new primitive for external adoption.

## What problem it addresses

The gap between "this primitive works in my workspace" and "this primitive is a standard others can adopt." Bridging that gap requires governance, documented behavior, test suites, and at least two independent implementations. The submission primitive defines the process.

## Prior art

IETF RFC process, W3C recommendation track, CNCF sandbox-to-incubation-to-graduation pipeline, schema.org community process. See `research/02-literature-survey.md`.

## Activation trigger

Two independent ACW workspaces exist, AND at least one external contributor has submitted a change to either workspace. Both conditions are required. A single-operator template with no external contributors has no primitives to submit.

## Shippable form factor

A markdown document at `governance/submission-process.md` (not shipped) describing the submission checklist, the required artifacts, the review process, and the acceptance criteria. Pairs with a hypothetical external governance body.

## What it is NOT

- Not a standards body — ACW has no authority to standardize anything
- Not a submission to any specific existing body — AAIF is hypothetical
- Not a roadmap commitment — this is the last primitive to earn its ship
- Not designed to bypass existing standards processes where they apply (e.g., if SKOS already covers the use case, submit to W3C instead)
