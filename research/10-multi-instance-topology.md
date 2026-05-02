---
class: research
authority: derived
stability: experimental
loaded_by_agent: no
date: 2026-05-02
proposes: architectural target for the deferred capability broker; multi-instance lattice as endpoint of "business automated from ACW"
relates_to:
  - research/07-instance-types.md
  - rules/capability-broker.md
  - DEFERRED.md
  - rules/instance-current-manifest.md
---

# 10 — Multi-Instance Topology

How an organization runs from a lattice of coordinated ACW instances. This note formalizes the architectural endpoint of the substrate-as-articulation insight: the substrate of a single instance articulates one operator's domain; a lattice of coordinated instances articulates a whole business. The deferred capability broker, the not-yet-built admission controller, and the not-yet-formalized cross-instance handoff protocol all aim at this target.

This is a sketch, not a specification. Promotion of any primitive named here still runs through `rules/promotion-ritual.md` and requires incident evidence per primitive.

---

## The articulation gap, restated

A business knows how to do its work. It cannot tell an AI system that work clearly enough for the AI to act reliably, because the knowledge lives in three places that don't talk to each other:

- **Tacit** — in operators' heads, transferred by apprenticeship and never written down
- **Drifted** — in documents that were once true and are now stale, with no signal of which is which
- **Ephemeral** — in Slack threads, email, hallway conversations that decay into noise within a week

AI systems can only act on what's been articulated. Tacit, drifted, and ephemeral knowledge is invisible to them. The articulation gap is the distance between what the business knows and what the AI can see.

ACW's substrate pattern closes this gap **as a side effect of doing the work**, not as a separate documentation activity. The metabolize loop forces tacit knowledge into the substrate at session-end. Decisions land in the decision log with rationale attached. Incidents land categorized so patterns emerge. The glossary forces vocabulary discipline. Evolution tracks what changed.

The substrate that results is not a documentation pile. It is **the business's operating knowledge in machine-readable, agent-actionable form**.

A single ACW instance closes the gap for one operator's domain. A lattice of instances closes it for the whole business.

---

## The instance lattice

A business running from ACW is not one giant instance. It is a federation of instances, each with its own substrate, coordinating through declared protocols.

```
                    ┌────────────────────┐
                    │   org-brain        │
                    │  (canon authority) │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
       ┌──────▼─────┐  ┌──────▼─────┐  ┌─────▼──────┐
       │ leadership │  │   product  │  │     CS     │
       │  instance  │  │  instance  │  │  instance  │
       └────────────┘  └────────────┘  └────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                       ┌──────▼──────┐
                       │   finance   │
                       │   instance  │
                       └─────────────┘
```

Two structural roles:

**Org-brain instance** — the canonical-truth instance. Holds knowledge that every department references and that needs **one** answer across the business. Vocabulary, org structure, mission, cross-cutting policies, security baselines, taxonomies that span departments. Source authority for everything departmental instances import.

**Departmental instances** — one per functional domain. Hold knowledge that is load-bearing for that department but irrelevant or misleading for others. Reference org-brain canon for shared terms; extend with department-specific vocabulary.

A departmental instance is itself a full ACW instance. It has its own substrate (decisions, incidents, evolution, research, glossary, threat model), its own bookend skills, its own operator (or operators), its own agents. The lattice is fractal — each node is a complete ACW.

---

## Knowledge placement rules

The single hardest question this architecture has to answer: **what goes where?**

The discriminator is two-part:

1. **Who queries it?** If multiple departments query the same fact, it's a candidate for org-brain. If one department queries it, it stays departmental.
2. **Does the answer need to be the same across departments?** If yes, org-brain. If different departments legitimately have different answers, departmental.

### Goes in org-brain

| Category | Examples |
|---|---|
| **Vocabulary canon** | "Customer" vs "user" vs "organizer" — the authoritative term. Departmental glossaries extend this; they don't override it. |
| **Organizational structure** | Who reports to whom, what the departments are, what the rocks are this quarter |
| **Mission, vision, values** | The "why we exist" layer that informs every department's decisions |
| **Cross-cutting policies** | Security baselines, compliance requirements, brand voice, legal constraints |
| **Shared taxonomies** | Customer segments, product lines, geographic regions — when more than one department uses them |
| **External entities** | Vendors, partners, regulators — the canonical record of who they are |

### Goes in the departmental instance

**Product team instance** — roadmap, feature decisions, customer feedback patterns, product taxonomy, release calendar, product-specific incident patterns, product-specific vocabulary (feature codenames, internal product slang)

**Finance instance** — payout rules, reconciliation procedures, vendor relationships at the financial-operations level, compliance hold patterns, payment processor specifics, fraud patterns, financial calendar, audit trail conventions

**Leadership instance** — EOS state (rocks, scorecards, issues lists, meeting cadences), board-facing material, strategy docs, leadership decisions that haven't been broadcast to departments yet, leadership-only context (sensitive personnel matters, M&A discussions, etc.)

**CS instance** — triage taxonomy, response templates, escalation rules, ticket categorization, agent training materials, CS-specific vocabulary, the things-that-bite-CS that are invisible to other departments

**Other departments** — same shape, different content. Engineering would have architecture decisions, runbooks, on-call rotations. Marketing would have campaign histories, channel performance, messaging frameworks.

### The reference, not duplicate, rule

Departmental instances **reference** org-brain canon. They don't copy it. The canonical glossary lives in org-brain; departmental glossaries say "these are our department-specific terms; for shared vocabulary, see org-brain canon."

Reference resolution happens at agent-read time, not at file-write time. An agent working in the CS instance loads CS substrate plus org-brain canon. The CS substrate stays small. Org-brain stays the single source of truth.

This is the same pattern as ACW's `template_layer` / `instance_layer` / `meta_layer` model from `rules/manifest-discipline.md`, but applied across instances rather than within one. Org-brain is the lattice's template_layer; each departmental instance is an instance_layer of the org.

### The boundary fight will happen

Every business has knowledge that wants to live in two places. CS knows the payout rules at the operational level (because customers ask about them); finance owns the payout rules at the canonical level. Both are right. The resolution is **declared authority + reference**: finance owns the canonical rule in finance instance; CS references it in CS instance and adds CS-facing operational notes ("when a customer asks X, the answer is Y, source: finance instance D-NNN").

This is the canon-governance pattern (`rules/canon-governance.md`) extended across instances. The authority who owns a term in the canon is the same authority who owns the corresponding fact in the lattice.

---

## Cross-instance coordination

Three primitives are needed. None are fully built; one is in seed form.

### 1. Cross-instance handoff protocol

When CS needs finance to act, the handoff has to travel with structure. Today, the operator hand-coordinates. The pattern needed:

- A structured payload (what is being handed off)
- Provenance (which instance is handing it, which session, which operator/agent)
- Target instance (where it's going)
- Requesting authority (under what authority the request is made)
- Payload schema (what shape the receiving instance expects)
- Acknowledgment loop (so the sender knows it landed)

ACW has the `_inbox/` directory as a seed. Today it's a one-way notification drop. The full protocol would be a typed message bus — RFC-style requests with declared schemas, like the Ralphinho RFC pipeline pattern but applied across instances rather than across agents.

**Earn-by-incident trigger:** three documented cases where a cross-instance handoff was lost, mis-routed, or required manual reconciliation between operators.

### 2. Capability broker (the deferred primitive aimed at this)

Cross-instance coordination requires agents to act on behalf of one instance against another. CS instance's agent sending a request into finance's `_inbox/` needs write authority to a path outside its own repo. Today this is governed by `cross_repo_writes` in `acw-state.yaml` — declarative but unenforced.

The broker is the enforcement layer. Designed in `rules/capability-broker.md`, deferred in v0.1.0. The multi-instance lattice is the architectural target that justifies the broker's ship: when one instance's agents act on another instance's substrate, **bounded credentials with declared scope** stop being optional.

The current activation triggers in `DEFERRED.md` are framed as single-machine credential incidents. **This research note proposes adding a new trigger:** three documented cases of cross-instance writes where scope ambiguity caused damage or required manual reconciliation. That earns the broker its ship at the lattice scale.

### 3. Admission controller

When an agent in CS instance issues a write to finance instance, who decides whether it's allowed? Today: nobody, because the case doesn't formally exist yet. The admission controller sits above the broker. The broker says "this credential is valid for this scope"; the admission controller says "this scope is allowed for this requesting authority on this target."

Admission rules live in the target instance, not the requesting instance. Finance declares "CS may write to `_inbox/cs-to-finance/` with payload schema X, but may not write anywhere else." The admission controller enforces.

This is fully unbuilt. **Earn-by-incident trigger:** three documented cases where a cross-instance write should have been blocked at the target but wasn't.

---

## Authority model across the lattice

Each instance declares its `authority_set` per `rules/instance-hard-rules.md`. The lattice extends this:

- **Org-brain authority set** is the union of all department-recognized authorities at the canonical layer. Examples: `operator`, `department-lead`, `executive`, `board`. Promoting a term in org-brain canon may require executive authority.
- **Departmental authority sets** are subsets, scoped to that domain. CS instance's authority set might be `operator, cs-lead`; finance's might be `operator, finance-lead, cfo`.

A cross-instance request carries the **requesting authority** in its payload. The receiving instance verifies the requesting authority against its admission rules. CS instance's `cs-lead` may have authority to ping finance's `_inbox/`; CS instance's `operator` may not.

The authority model is the governance foundation. Without it, the lattice is just a polite suggestion.

---

## Evidence loops across the lattice

A business running from ACW needs to know its agents are doing what they should. Three nested loops:

1. **Per-instance loop** — already in seed form. Each instance's `incidents.jsonl`, evolution, capture-and-metabolize cycle catches single-instance drift.
2. **Cross-instance loop** — does not exist yet. Surfaces friction at boundaries: handoffs lost, admission rules wrong, canon references stale, vocabulary drift between org-brain and a departmental glossary.
3. **Lattice-level loop** — does not exist yet. Aggregates across all instances to surface patterns: "every department had a session-start drift incident in the same week, suggesting an org-brain canon update broke something."

The lattice-level loop is the most distant. It earns its build only after the per-instance and cross-instance loops are stable.

---

## Implementation phases

Earn-by-incident applies. No primitive ships until evidence justifies it.

**Phase 0 — already done.** Single-instance ACW substrate pattern. Bookend skills. Manifest discipline. Decision log, incidents, evolution, glossary, research, threat model. Cross-vendor portability via AGENTS.md.

**Phase 1 — current frontier.** Adopt-mode for `/upgrade-instance` so substrate-shaped pre-ACW workspaces (cs-copilot today; future analogs) can be brought into formal management. This is the immediate spinoff from this research note. Detailed in the next section.

**Phase 2 — earn-by-incident.** First cross-instance handoff protocol. Activation: when the operator hand-coordinates between two instances three times and feels the friction. The first protocol may be as simple as a typed schema for `_inbox/` payloads.

**Phase 3 — earn-by-incident.** Capability broker ships. Activation: trigger from `DEFERRED.md` plus the new trigger proposed in this note. The broker's first job is gating cross-instance writes.

**Phase 4 — earn-by-incident.** Admission controller. Activation: three documented cases of cross-instance writes that should have been blocked.

**Phase 5 — speculative.** Lattice-level evidence aggregation. May or may not earn its build; depends on whether the per-instance and cross-instance loops surface lattice-level patterns that aren't visible at lower levels.

---

## Phase 1 spinoff: adopt-mode for `/upgrade-instance`

The cs-copilot session that prompted this research note exposed a real bug in the current `/upgrade-instance` skill: it runs a **registration check**, not a **substance check**, and refuses to act when the registration files are missing.

The substance definition is the correct one. cs-copilot has every load-bearing piece of an ACW instance — decisions, rules, glossary, evolution, research, incidents, bookend skills, substrate. What it's missing is the registration metadata (`acw-state.yaml` + `rules/instance-current-manifest.md`) that lets the upgrade tooling know it's a managed instance. That's a formality, not the essence.

### Proposed fix

Restructure `/upgrade-instance` to a three-step flow:

1. **Registration check.** Look for `acw-state.yaml` and `rules/instance-current-manifest.md`. If present, proceed to existing reconciliation flow.

2. **If missing: substance scan.** Look for substrate signals:
   - `decisions/` directory with `decision-log.md`
   - `rules/` directory
   - `incidents.jsonl`
   - `glossary.md` or equivalent
   - `research/` directory
   - bookend skills under `skills/`
   - any combination above a threshold (e.g., three of six)

3. **If substance present without registration: offer adoption.** Surface what was found, propose writing the missing registration files using canonical defaults, get operator confirmation, write `acw-state.yaml` (with `last_reconciled_version` set to a value that suppresses the noisiest backfill alerts) and `rules/instance-current-manifest.md` (copied from canonical).

The adoption offer is **opt-in, not automatic**. The skill surfaces "this looks like an ACW instance that pre-dates registration. Adopt as a formal instance? [yes/no]". Operator confirmation gates the write.

If substance is absent (a workspace with none of the signals), the skill still bails — but with a clearer message: "this workspace doesn't appear to be an ACW instance. To start one, run `tools/scaffold-instance.py`."

### What this fix earns

- cs-copilot can be adopted as a formal instance without manual scaffold work
- Future pre-ACW workspaces with substrate get a graceful adoption path
- The registration definition stops being a wedge between substance and tooling
- The substance definition becomes the operative one; registration becomes the metadata that makes substance machine-tractable

### Open question on this fix

What `last_reconciled_version` does the adoption write? Three options:

- **`"0.0.0"`** — produces noisy first run; every recommended block earned-in v0.2.0+ shows as drift. Operator runs `/upgrade-instance` again immediately to reconcile.
- **Match the substance** — scan what's present, set `last_reconciled_version` to the highest ACW version whose recommended blocks are all already present. Quietest first run; most accurate.
- **Current ACW version** — silent first run; assumes the substrate is already compliant. Risky; may suppress real drift.

The middle option is correct in principle but expensive to implement (requires inverse-mapping recommended blocks back to ACW versions). The first option is cheapest and safest. **Recommendation: ship with option 1; let the noisy first reconciliation be the price of adoption.**

---

## Open questions

### OQ-10-1 — Does org-brain ship as a formal ACW instance type?

`research/07-instance-types.md` defines four types: Full, Cockpit, Project, Read-Only. None of them quite name "org-brain as canonical-truth instance." Should this be a fifth type, or is it just a Full instance with a special role in the lattice?

**Recommendation:** Full instance for now. The lattice role is governance, not structure. If lattice-specific primitives ship later (admission rules surfaces, cross-instance reference resolution), revisit.

### OQ-10-2 — How does the lattice handle org-brain forks?

What happens when leadership wants to update a canonical term but legal hasn't approved? Does org-brain support proposed-but-not-approved canon entries that departmental instances can opt into?

**Recommendation:** the canon-governance state machine (`rules/canon-governance.md`) already handles this — `proposed` state is distinct from `approved`. Departmental instances reference `approved` only by default; departments that need to track `proposed` explicitly opt in.

### OQ-10-3 — Multi-operator within a single instance

Currently every ACW instance assumes a single operator. A real CS instance has 4-6 agents plus a CS lead. Does the instance need formal multi-operator support, or is "the CS lead is the operator; agents are tools" sufficient?

**Recommendation:** Start with the latter. Promote when incidents earn it.

### OQ-10-4 — Lattice bootstrapping

When a business stands up its first ACW instance, which instance comes first? Org-brain (canonical foundation, but empty without departmental knowledge to canonize)? A departmental instance (concrete, but references nothing yet)?

**Recommendation:** A pilot departmental instance first. Let it accumulate substrate. When a second department wants to start, pull shared terms into a new org-brain instance and refactor the pilot to reference it. Build org-brain bottom-up from real departmental usage rather than top-down from a hypothetical canon.

### OQ-10-5 — Can the lattice cross organizations?

A consultancy serving multiple clients has a meta-level: each client engagement is its own lattice. The consultancy's own ACW instance (frank-context style) is the meta-lattice. Does ACW's design support nesting lattices, or does it stop at one level?

**Recommendation:** out of scope for this note. Revisit when the consultancy use case generates its own incidents.

---

## Decision needed

This research note proposes:

1. **Phase 1 immediate ship:** fix `/upgrade-instance` to support adopt-mode per the spec above. Earn-by-incident is satisfied (cs-copilot session is the documented incident).
2. **Add a new activation trigger to `DEFERRED.md`** for the capability broker: three documented cross-instance write incidents earn the broker its ship at lattice scale.
3. **Defer everything else in this note** until incidents earn the next phase. The lattice is the architectural target; it is not the ship.

Open question for the operator: ship Phase 1 in the next session? The fix to `/upgrade-instance` is well-scoped and concrete.

---

## Provenance

This note emerged from a 2026-05-02 conversation in the ACW instance with the operator. The triggering moment was a session in cs-copilot where `/upgrade-instance` correctly identified missing registration files and bailed. The operator pushed back on the "not an ACW instance" verdict, asking what an ACW instance fundamentally **is**. The conversation surfaced the substance-vs-registration distinction, then escalated to the broader question: can a full business run from ACW, and if so, what's the architecture?

The lattice model and knowledge-placement rules were derived during that conversation. The Phase 1 fix to `/upgrade-instance` is the immediately actionable spinoff. The deferred phases catalog the architecture without committing to build.
