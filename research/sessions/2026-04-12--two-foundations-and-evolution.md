---
date: 2026-04-12
type: session-transcript
topic: Two-foundation insight, research evolution infrastructure, capture-session design
scope: Post-ship discoveries (after v0.1.0 tag through research evolution commit)
form: cleaned
---

# Session Transcript — 2026-04-12 (Part 2)

Continuation of the ACW session. Part 1 (build completion through GitHub push) is at `Cortex/Resources/2026-04-12--acw-session-thread.md`. This transcript covers the post-ship discoveries: the cockpit pattern, canon deferral, nine problems, two foundations, deep research completeness audit, Gary HVAC scenario, naming discipline, research evolution infrastructure, and capture-session design.

---

## Turn 1 — Operator catches canon over-shipping

**Operator:** You know what, that makes me think. Depending on the size of the setup or the folder or the workspace, the rules canon.yaml might be one of those that shouldn't get implemented until it is triggered by something that recognizes that there's a need for terminology here, and there's some conflict and some overlap and some confusion happening. I bet on smaller setups canon might not even show up in the incident log. Am I right or am I wrong? I mean that literally.

**Agent:** You're right. Literally right. Canon-governance, canon-schema, and canon.yaml are shipped as operational but haven't earned their ship at single-operator scale. Same failure mode as DIP, one layer shallower. Small setups may never produce vocabulary drift. The glossary alone carries all the vocabulary work a single-operator workspace needs.

> **[SHIFT]** Canon governance identified as shipped-pre-earned, same pattern as DIP. Should be scaffold or deferred, not operational.

---

## Turn 2 — Operator identifies the cockpit pattern

**Operator:** Yeah, but what's interesting is this workspace is set up to be a very clean desk, and we've barely written anything to it. It's meant to be really clean. It's got pointers to other projects where the documentation exists or other folders like Nextcloud, and it's got MCPs, and so it literally doesn't store any explicit ongoing context. I think it is really only good for use within a session.

**Agent:** Named it: _Command isn't a workspace. It's a cockpit. A workspace accumulates state. _Command doesn't, it has pointers, controls, skills that read/write external systems, and a logbook. All knowledge goes to gsg-brain, all logs go to synapse, all articles go to Cortex. The cockpit is the chair you sit in while working on everything else.

> **[SHIFT]** "Cockpit pattern" identified as a workspace type ACW doesn't account for. Session-scoped operator consoles that don't accumulate state need lighter ACW hygiene than state-accumulating workspaces.

---

## Turn 3 — Operator insists on universal hygiene

**Operator:** Where you said the hard rules and the moderates felt like they were pushing _Command to become something it isn't, I mean I see what you're saying, but I would still prefer, even for a cockpit like this, to metabolize everything to the ACW framework. That way everything follows the same guidelines. I think that the ACW model probably should treat more files like glossary.md and canon.yaml the same way, like threat model or others that aren't supposed to kick in until they are needed.

**Agent:** Named the three-tier model: Active (always enforcing), Scaffold (file exists but dormant until needed), Deferred (design doc only, file doesn't exist until promotion).

> **[SHIFT]** "Scaffold" tier identified as missing from ACW's vocabulary. Middle ground between active and deferred. Files that ship empty so the shape is learnable, activate when incidents earn it.

---

## Turn 4 — Skill format with 6C classification

**Operator:** Why not have the gotchas and the 6C in what the ACW ships?

**Agent:** No reason not to. gotchas.md is universal good practice. 6C (Creation, Curation, Clarification, Cognition, Communication, Coordination) is a clean capability classification orthogonal to role.

**Operator:** Yeah, the 6C classification is actually part of ITIL 5. It's new and might be really helpful for the ACW. We should build it in.

> **[SHIFT]** 6C classification (ITIL 5) identified as universal, not operator-specific. Ships in ACW as required classification table alongside role and domain.

---

## Turn 5 — DIP Domain replaced by ACW Domain

**Operator:** Explain domain to me again, because in my own setup I am currently using DIP's domains, which we're going to have to get rid of too.

**Agent:** DIP's Domain = functional boundary (Exfiltration, Routing, etc.). ACW's Role already covers the functional boundary. ACW's Domain = subject area (operations, engineering, finance). Three orthogonal axes: Role (data flow position), Domain (subject area), 6C (capability type).

> **[SHIFT]** DIP's functional-area Domain replaced by ACW's subject-area Domain. Role covers the functional question. Domain covers the subject question. No redundancy.

---

## Turn 6 — Naming discipline ("format" not "standard")

**Operator:** Should we call it skill format or skill standard?

**Agent:** skill-format.md is safer. SKEPTIC do-not-do #5: "Do not call anything a standard without adopters."

**Operator:** So the SKEPTIC is against governance?

**Agent:** No, the SKEPTIC is against claiming governance you don't have. The entire template is governance. The SKEPTIC is against naming things above their current authority level.

**Operator:** Ohhhh okay got it that's actually really safe.

> **[SHIFT]** Naming discipline crystallized: every word earns its weight or gets the lighter label. "Format" not "standard." "Template" not "framework." "Restraint device" not "roadmap." The upgrade path is built in, the word upgrades when evidence arrives.

---

## Turn 7 — Deep research completeness audit

**Operator:** Do deep research to see if we're missing problems or perspective on this.

**Agent:** Ran /deep-research with three parallel agents (22 sources). Found four missing problem categories on the observation side: state corruption/rollback, observability/debugging, cost/resource governance, human-AI handoff. Found the "one foundation" claim should become "two foundations": contract layer (declaration) + observation layer (verification).

> **[SHIFT]** Five problems expanded to nine. One foundation expanded to two. The contract layer (what ACW ships) is the declaration side. The observation layer (what ACW defers individually) is the verification side. Neither works alone.

---

## Turn 8 — Operator reframes the scope

**Operator:** What are they the problems of? Like what is the end state or aim that surfaces these problems?

**Agent:** Persistent agentic AI systems that stay coherent over time without human rescue.

**Operator:** Is "workspaces" the correct term to be all encompassing?

**Agent:** No. "Workspace" implies a folder on disk. The problems apply to any configuration where an AI agent operates against declared rules, tools, and knowledge across multiple sessions with increasing autonomy. Persistent agentic AI systems.

> **[SHIFT]** Scope broadened from "workspaces" to "persistent agentic AI systems." The workspace is one implementation pattern. The problems are bigger than the pattern.

---

## Turn 9 — Operator envisions Canon Works engagement

**Operator:** Let's use my buddy's HVAC business to take a look at Canon Works and get the context for his business. Run me a scenario of what I would build for him.

**Agent:** Designed three-instance architecture: cockpit (gary-command/), business (expert-air/), optional personal brain (gary-brain/). One ACW per concern. The cockpit is the sticky product people feel first. The business vault is the valuable deliverable. Mapped the P3-P8 engagement pipeline against the ACW template.

> **[SHIFT]** Canon Works engagement model crystallized: every client gets one ACW per concern (cockpit + business minimum). The cockpit is where the operator feels the automation. The business vault is where the knowledge lives.

---

## Turn 10 — Research evolution infrastructure

**Operator:** I'm almost having the idea that we need a research state document in the ACW research folder that works like the acw-state.yaml. I would also like a file for the paper with just front matter placeholding it.

**Agent:** Designed research-state.yaml as conception SSOT, evolution.md as dated shift log, paper.md as placeholder, sessions/ for cleaned transcripts.

**Operator:** What updates the research-state.yaml automatically?

**Agent:** capture-session does it. The chain: deep-research saves findings, operator engages and discusses, capture-session cleans the transcript, tags shifts, diffs against research-state.yaml, proposes updates, operator approves.

> **[SHIFT]** Research evolution infrastructure designed: research-state.yaml (current truth) + evolution.md (how you got there) + sessions/ (raw provenance). Updated by capture-session, not by research tools. The conception shifts when the operator reacts to research, not when research is saved.

---

## Turn 11 — Origin tracking for template vs instance

**Operator:** Will the operators' specific research just fold into the same research-state.yaml, or will they need another one?

**Agent:** Same file. Operator edits it in place. An `origin:` field distinguishes template knowledge from instance findings. Template entries: `origin: acw-template`. Operator entries: `origin: instance`. When a new ACW version ships, template entries can be merged in, instance entries stay untouched.

> **[SHIFT]** Origin tracking solves the template-vs-instance merge problem. One file, two origins. Template knowledge upgrades when ACW ships new research. Instance knowledge accumulates independently.

---

## Turn 12 — GSG vocabulary drift example

**Operator:** Give me an example of how this works at GSG.

**Agent:** GSG has two glossaries that don't talk to each other (cs-operational-glossary + platform-terminology). Today: human review catches "campaign" vs "fundraiser" drift. After metabolize: seed glossary + lint (no forbidden blocks). After first incident: one canon.yaml entry with hidden_labels. After three incidents: canon governance activated. After Robert/Tom contribute: N-authority approval. Each step earns the next.

> **[SHIFT]** GSG vocabulary drift example validates the earn-by-incident progression. The canon governance that felt premature for _Command (cockpit, no drift) is load-bearing at GSG (6-person team, 60+ articles, answer bot incoming, multiple contributors). Same template, different activation timelines per instance.

---

## Current state

Nine problems across two foundations. Template ships the contract layer. Observation layer identified but deferred. Research evolution infrastructure ships with every instance. Capture-session skill designed as orchestrator with four sub-steps. Origin tracking solves template-vs-instance research merge. Naming discipline: every word earns its weight.
