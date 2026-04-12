---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# ORCHESTRATION — How ACW v0.1.0 Was Built

This file documents the methodology that produced ACW v0.1.0. It is not the template; it is the process that produced the template. The methodology is the more reusable artifact — the template is a single instantiation of the process applied to one problem space.

Read this if you want to know what "running the ACW methodology" looks like when a contractor shows up at a client's company and builds a system. The template is what you ship. This is what you do.

## The seven-phase arc

Every primitive in v0.1.0 traces back through the same seven phases. Each phase has an output the next phase consumes.

1. **Problem framing.** Name the problems you think exist. Write them down. Do not solve them yet. Output: a numbered list of problems you cannot dismiss on inspection.

2. **Deep research.** For each named problem, find the prior art. Walk citation graphs. Verify sources independently — do not take an LLM's bibliography on trust. Output: an annotated bibliography with verification notes and a forbidden-source list.

3. **Operator context pack.** Write down what is true about your own situation that shaped the problem framing. This phase exists to catch operator-specific nouns and scale assumptions before they harden into the design. Output: a context brief that downstream phases can sanitize against.

4. **Research synthesis.** Diagnose. Collapse the problem list to its smallest foundation. The synthesis phase is where most research projects fail — they catalog findings without diagnosing what the findings mean together. Output: a one-sentence diagnosis and the evidence trail that supports it.

5. **Five-lens adversarial review.** Dispatch five parallel reviewers with distinct disciplines: standards architect (faithfulness to prior art), professional implementer (can it actually ship), personal workspace implementer (is scope right for the smallest real user), productizer (is it legible to outside eyes), skeptic (should any of this ship). Each lens catches failure modes the others miss. Output: a scope decision shaped by adversarial pressure.

6. **Final proposal.** Take the five-lens pushback and produce a concrete proposal. Name what ships, what defers, and the activation triggers for everything deferred. Output: a plan file with ship order, directory tree, and explicit operator decisions.

7. **Reading report.** Hand the plan to two external reasoning models (different labs, different cultures). Accept the sharpest critiques even when they cost scope. Output: surgical fixes baked into the plan before execution begins.

## Stress-test before execution

The plan from phase 6 is not the plan that ships. Before any file is written, the plan goes through two rounds of adversarial review:

**Round 1 — parallel internal agents.** Five audit agents dispatched simultaneously, each with a distinct attack vector: research fidelity, prior-art integration, portability, skeptic redux, first principles. Convergent diagnosis across agents is the strongest signal; divergence tells you where the reviewers have different priors and the operator has to decide.

**Round 2 — external reasoning models.** Plan handed to two external models at frontier labs. Their feedback is weighted higher than internal agents because they have different training distributions and catch blind spots internal reviewers share. When their feedback conflicts with internal reviewers, default to believing them unless you can name a specific reason their advice doesn't transfer.

Do not execute the plan until both rounds land. Scope decisions locked in during stress testing are not re-litigated during execution.

## Tier-by-tier execution

After stress testing, execution proceeds in explicit tiers. Each tier completes before the next begins. A tier is a set of files that depend on each other and can be written against each other's contracts.

The tiers exist because mid-execution scope changes are the most expensive kind of change. Forcing tier completion before moving on creates natural checkpoints where the operator can decide whether to continue, revise, or stop — without losing a half-written file to a scope revision.

## Class/authority status headers

Every non-code file declares its own class (operational, reference, deferred, archive), authority (canonical, derived), stability (stable, experimental), and whether an agent should load it (`loaded_by_agent: yes/no`). This is the cheapest, highest-leverage discipline the external reviewers flagged. It prevents trust drift — the failure mode where explanatory files and operational files blend together over time until nobody can tell which file is governing behavior.

Without the headers, any template with more than ten files will drift within six months. With the headers, a reader can always tell what they are looking at.

## Earn-by-incident

No infrastructure primitive ships until a named, dated, documented incident justifies it. Three incidents above low severity on the same primitive earn promotion review. This discipline exists because the operator's known failure mode is builder-mode tunnel vision, and it is the mechanical restraint against that pattern.

The discipline ships asymmetric in v0.1.0: strict for code primitives (they carry real implementation risk), honest-labeling for prose primitives (they ship as `stability: experimental` because the operator is internalizing the patterns by using them). The asymmetry is defensible under the training-ground framing and is named explicitly in `SKEPTIC.md`.

## Reading report narrative form

Every major research artifact in `research/` is written as a reading report — summary + interpretation + what it changed in the design — rather than a chronological transcript. The reading-report form forces the author to have a position, not just a list of sources. A bibliography without a diagnosis is research theater; a reading report is the unit of thought.

## What makes this methodology the IP

Three things distinguish this methodology from generic research-then-build:

1. **Adversarial review is structural, not optional.** Five internal lenses, then two external models, before any code is written. The cost is high and the payoff is catching scope and faithfulness problems before they enter the file system.

2. **Earn-by-incident is mechanical.** The restraint is a rule with a counter, not a principle a reviewer invokes by memory. The counter lives in a file. The rule is checked by a tool.

3. **Trust drift is prevented at the file level.** Every file declares its own status. A reader does not have to infer authority from filename or folder; the authority is in the frontmatter.

The template is the artifact. The methodology is the skill. When this methodology is applied to a client's workspace rather than to ACW's own template, the outputs will be different — different domains, different primitives, different activation triggers — but the process will be the same.

## Not a cookbook

This file is not a step-by-step tutorial. It is a methodology summary. Running the methodology on a new problem space requires judgment about which tools apply, which reviewers to dispatch, which external models to trust, and when to stop stress-testing and ship. The judgment is the part that cannot be automated.
