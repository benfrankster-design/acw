---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Research Archive

This folder preserves the research lineage that produced ACW v0.1.0. Every primitive in `rules/`, every entry in `DEFERRED.md`, every design choice in the schema, and every role in `rules/pipeline-roles.md` traces back to one of the files here. If you disagree with a rule, read the research before editing it.

## What is in here

Research files covering the arc from problem framing through ship decision, plus a post-ship completeness audit and the living-state infrastructure for ongoing conception evolution. Each file is a synthesized summary — not a transcript of the research process, not a verbatim copy of source documents, not a blog post. Think of them as the methodology archive a teacher would hand a student after a semester: "here is why we did what we did, in the order it happened."

## What is NOT in here

- Operator-specific context from the original research project
- Employer-specific examples or scale references
- Research prompts verbatim
- LLM chat logs
- Citations that could not be independently verified

## Sanitization notes

The source material for these files lived in a private research project with operator-specific framing. Every reference to a specific person, organization, tool, ticketing system, chat surface, or geographic location has been removed or generalized. Where a source cited something the operator could not independently verify, the citation was dropped rather than preserved on trust. The seven files here are conservative summaries, not the whole truth of the research.

## Reading order

1. `01-problem-framing.md` — the five frontier problems, why they matter, what collapses them to one foundation
2. `02-literature-survey.md` — prior art, twenty-eight sources, what ports and what doesn't
3. `03-synthesis.md` — diagnosis, the typed contract registry as the missing foundation
4. `04-proposal.md` — the minimum primitive set, the deferred library, and the five-consultant team pattern
5. `05-ship-decision.md` — why v0.1.0 ships what it ships and defers what it defers
6. `sources.md` — annotated bibliography

7. `06-completeness-audit.md` — post-ship gap analysis: what the five problems miss, the two-foundation insight, 22 additional sources
8. `07-instance-types.md` — four instance types (full, cockpit, project, read-only) and what ACW primitives apply at each level

**Living-state files (populated by the operator over time):**
- `research-state.yaml` — machine-readable source of truth for the current conception. Ships with template knowledge (`origin: acw-template`); operator findings accumulate as `origin: instance`. Updated by `/capture-session`.
- `evolution.md` — dated log of conceptual shifts. How the operator got from the shipped understanding to their current one. Updated by `/capture-session`.
- `paper.md` — placeholder for a future formal write-up. Populate when the conception stabilizes.
- `sessions/` — cleaned session transcripts saved by `/capture-session`. The raw provenance trail.

A reader who only has time for one file should read `03-synthesis.md`. A reader who wants to argue with a specific primitive should read `02-literature-survey.md` first. A reader who wants to know what ACW got wrong should read `06-completeness-audit.md`. A reader who wants to see how the conception evolved over time should read `evolution.md`.
