---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# 06 — Completeness Audit

A post-ship gap analysis conducted against ACW v0.1.0's five frontier problems. The question: are the five comprehensive, or are there structural problems in persistent agentic workspaces that the five miss? Does the "one missing foundation" (typed contract registry) claim hold up?

## Methodology

22 sources surveyed across academic papers, industry frameworks, standards bodies, and practitioner writing. Freshness window: February–April 2026. Sources span AAMAS 2026 proceedings, Anthropic engineering blog, NIST, CSA, RSA 2026 conference, and practitioner platforms.

## Finding 1 — The five problems are ~70% of the picture

ACW's five frontier problems (MECE enforcement, vocabulary drift, drift detection, credential management, semantic validation) capture the core governance concerns: what agents are allowed to do, what vocabulary means, how drift is caught, how credentials are managed, how tool calls are validated.

What they miss is systematic: everything on the *verification* side. The incompleteness is not random — it is consistent with the selection bias named in `SKEPTIC.md` Warning #1. The operator who designed ACW was building governance. The gaps are all on the detection, measurement, and recovery side.

## Finding 2 — Four missing problem categories

### State management and rollback

ACW's drift detection (problem #3) catches *stale* state but not *corrupted* state. The committer role writes; there is no undo. Production frameworks are shipping rollback as infrastructure:

- IBM's STRATUS framework uses transactional-no-regression with undo operators for every action
- LangGraph saves state after every tool call for checkpoint/resume
- Neon provides database-level branching with copy-on-write snapshots for agent state
- Replit's snapshot engine uses git-based checkpointing where each action creates a commit

The irreversibility boundary — actions outside the workspace (sent messages, API calls, financial transactions) that cannot be undone — is a named concern in multiple sources but unsolved in every framework. ACW's threat model should acknowledge it.

**Proposed:** Consider "state corruption and rollback" as a sixth frontier problem, or expand drift detection (#3) to cover corruption and irreversibility explicitly. A rollback primitive could enter the deferred library.

### Observability and debugging

ACW has no observability story. The earn-by-incident discipline depends on *noticing* incidents, but the workspace has no mechanism for detecting them other than human observation.

- OpenTelemetry GenAI conventions now cover agent spans, tool calls, and guardrail triggers as a vendor-neutral standard
- LangSmith renders full execution trees showing tool selections, parameters, and retrieved documents
- Laminar ($3M seed, March 2026) provides step-by-step agent replay with synchronized browser session recordings
- The industry consensus is that teams over-measure prompt quality while under-measuring workflow reliability — tool success rates, handoff completion, guardrail triggers, and retry patterns are the real failure indicators

Long-running workspaces generate thousands of interactions. ACW's monthly `check-drift` is the only automated detection, and it only checks DEFERRED.md consistency.

**Proposed:** Observability may be the missing "observation layer" that makes the contract layer work. Without observation, the contract layer is declaration without verification.

### Cost and resource governance

Not a structural problem in the same sense as the five, but it becomes structural at scale:

- The AAMAS 2026 paper formalizes "moral hazard" — agents consuming more resources than predicted because LLM output costs are non-deterministic
- Runaway agent loops ("Mirror Mirror" effect) where agents with conflicting instructions loop endlessly are documented in production
- EU AI Act requires rapid revocation capability (seconds, not minutes) — ACW's guardian role blocks pre-action but has no mechanism to halt a running agent mid-execution

**Proposed:** May not deserve a named frontier problem. Could be an instance-hard-rule per workspace plus a guardian enhancement. The AAMAS paper's resource constraints formalization is worth citing.

### Human-AI handoff

ACW's human-in-the-loop gate (new file creation requires review) is a primitive version of what the field is converging on:

- Four autonomy levels (Graph Digital): execute autonomously, execute and flag, recommend and wait, escalate immediately. ACW has binary: approve or skip.
- Time-boxed decision lanes (Strata): 15 seconds for low-risk, 2 minutes for PII, 15 minutes for financial. ACW has no time dimension on approvals.
- Automation complacency (human factors research): oversight quality degrades as agent reliability increases. ACW's SKEPTIC warns about reflexive injection but not about human trust erosion.

**Proposed:** May not be structural at single-operator scale (the operator is the handoff). Becomes structural when a team member is the approval gate. The 6C governance tier is the right seed — it signals how much oversight a skill needs but not what kind.

## Finding 3 — The "one foundation" claim should become "two foundations"

The evidence suggests two foundational primitives, not one:

| Layer | What it does | ACW status |
|---|---|---|
| **Contract layer** (declaration) | Declares roles, capabilities, domains, vocabulary, hard rules. Says what agents are *supposed* to do. | This is ACW v0.1.0. Pipeline roles, canon governance, skill format, instance hard rules. |
| **Observation layer** (verification) | Detects that agents *actually did* what contracts declared. Taint tracking, permission drift, resource consumption, state corruption, outcome measurement. | ACW has incidents.jsonl (manual) and check-drift (DEFERRED.md only). No automated observation. |

The contract layer without the observation layer is policy without enforcement. The observation layer without the contract layer is monitoring without a baseline.

ACW's deferred library partially covers the observation layer (drift-detector, conformance-test, manifest). But these are deferred individually. The evidence suggests the observation layer is a **peer foundation** to the contract layer, not a collection of optional add-ons.

**Recommendation:** Do not restructure v0.1.0. Acknowledge the two-layer architecture in the research and SKEPTIC.md. When the first observation incident fires — a problem the contract layer declared against but did not detect — that is the evidence that the observation layer is a second foundation, not just a deferred primitive.

## Finding 4 — Closest academic analog

An AAMAS 2026 paper ("Agent Contracts: Reliability for LLM Agents," arxiv 2601.08815) formalizes agent contracts as a seven-tuple: `C = (I, O, S, R, T, Φ, Ψ)` covering Input/Output specs, Skill Set, Resource Constraints, Temporal Constraints, Success Criteria, and Termination Conditions.

Key differences from ACW:
- Their contracts are **runtime execution contracts** (budget, time, halt conditions). ACW's contracts are **structural capability contracts** (role, domain, vocabulary).
- They identify **moral hazard** and **incomplete contracts** as named problems. ACW has not named either.
- They distinguish **soft enforcement** (budget-aware prompts the agent may ignore) from **hard enforcement** (external harness that halts execution). ACW's guardian role is hard enforcement; ACW lacks the soft/hard distinction as a named concept.
- **No role taxonomy.** Their framework is role-agnostic. ACW's pipeline-roles enum is a dimension they do not address.

The two formalizations are complementary, not competing. ACW governs *what agents are allowed to do*. The AAMAS paper governs *how much agents are allowed to consume*. Both are needed for a complete contract.

## Finding 5 — Named problems from sources not covered by the five

| Problem | Source | Relation to ACW |
|---|---|---|
| Hallucinated consensus | Cogent Playbook 2026 | Multiple agents converging on fabricated data. Not a MECE problem — a correctness problem unique to LLM agents. |
| Memory poisoning across sessions | Willison 2025-2026 | Malicious data written to persistent memory influences future unrelated sessions. Directly relevant to any persistent workspace. ACW has no defense. |
| Permission drift over time | RSA 2026 | Permissions expand silently (3x in one month). ACW can audit current state but not detect gradual scope creep. |
| Ghost agent inventory | RSA 2026 | Only 21% of organizations maintain real-time agent inventory. Deprecated skills persist without cleanup. |
| Instruction budget as hard constraint | HumanLayer 2026 | ~150-200 effective instructions per frontier model. Over-governance degrades output. ACW loads all rules/ files without measuring attention cost. |
| Schema evolution breakage | Cogent Playbook 2026 | Modifying one agent's I/O schema requires synchronized updates across connected agents. |
| Workspace semantic versioning | Decagon 2026 | Treating the governance layer as a single versioned unit with outcome measurement between versions. ACW versions per-file (git) not per-governance-unit. |

## Finding 6 — Alternative framings from the field

### The AAMAS seven-tuple
`C = (I, O, S, R, T, Φ, Ψ)` — richer than ACW's frontmatter by adding resource, temporal, and termination dimensions.

### Adaline Labs' four control primitives
**Permissions, Handoffs, Visibility, Recovery.** ACW covers Permissions and partially Handoffs. Visibility (observability) and Recovery (rollback) are the gaps.

### RSA 2026's three-layer identity model
**Identity (WHO) → Verification (HOW) → Governance (WHY).** ACW does Governance. Partially does Identity. Does not do Verification.

### Willison's information-flow axis
**Private data × untrusted content × external communication.** ACW's role separation addresses the trifecta architecturally but doesn't implement taint tracking or trust zones.

## Practitioners building similar things

| Who | What | Relevance |
|---|---|---|
| Decagon | Agent versioning with workspace isolation + outcome measurement | Closest production analog for workspace governance |
| LangGraph | Graph-based state with typed schemas + checkpointing | State management more mature than ACW |
| Anthropic Agent SDK | Orchestrator-worker with subagent isolation | Role separation similar to pipeline roles |
| CrewAI | Role-based agent teams | Simpler role model, same philosophy |
| Laminar | Agent observability with step-by-step replay | The observation layer ACW lacks |
| IBM STRATUS | Transactional agent operations with undo | Rollback primitive ACW hasn't shipped |
| NIST | AI Agent Standards Initiative (Feb 2026) | Interoperability profile + SP 800-53 agent overlays by Q4 2026 |

## Updated source count

This audit adds 22 sources to the 28 in `sources.md`, bringing the total research base to 50 verified sources. The new sources are listed in the operator's private research archive and can be sanitized into `sources.md` in a future update.

## What this changes for ACW

Nothing in v0.1.0. The five problems and the contract layer ship as designed. This audit earns its place in the research archive as the first post-ship gap analysis. The two-foundation insight (contract + observation) should be acknowledged in `SKEPTIC.md` and `03-synthesis.md` as a known limitation of the v0.1.0 framing.

When the first observation-layer incident fires, it will be evidence for restructuring the deferred library around two foundations rather than one. Until then, the current deferred-primitive-by-primitive approach is the honest path.
