---
class: reference
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Multi-Instance Topology

Canonical statement of how an organization (or any multi-domain operator) structures multiple coordinated ACW instances into a lattice. This rule exists so that any instance scaffolded from ACW already has the framing to reason about "where does this knowledge go" when scale demands more than one instance.

This rule is normative for the lattice shape and the knowledge-placement discriminator. It is informative for the coordination primitives, which earn their build through the deferred library and the promotion ritual.

For provenance and the longer-form derivation, see `research/10-multi-instance-topology.md` in ACW canonical.

---

## When this rule applies

A single operator running a single domain from a single instance does not need this rule. The lattice pattern earns its relevance when:

- The operator's work crosses two or more functional domains that have meaningfully different vocabulary, governance, or authority
- Multiple operators (or multiple agents acting on behalf of multiple humans) need to coordinate
- Knowledge in one domain references canonical answers owned by another domain
- An organization is articulating its operating knowledge into agent-actionable form across departments

Below that threshold, run a single instance. Above it, the lattice shape is the right architecture.

---

## The lattice shape

A business running from ACW is a federation of instances, not one giant instance. Two structural roles:

**Org-brain instance** — the canonical-truth instance. Holds knowledge that every department references and that needs **one** answer across the business. Vocabulary, org structure, mission, cross-cutting policies, security baselines, taxonomies that span departments. Source authority for everything departmental instances import.

**Departmental instances** — one per functional domain. Hold knowledge that is load-bearing for that department but irrelevant or misleading for others. Reference org-brain canon for shared terms; extend with department-specific vocabulary.

A departmental instance is itself a full ACW instance. It has its own substrate, its own bookend skills, its own operator (or operators), its own agents. The lattice is fractal — each node is a complete ACW.

---

## Knowledge placement discriminator

The single hardest question this architecture has to answer: **what goes where?**

The discriminator is two-part:

1. **Who queries it?** If multiple departments query the same fact, it's a candidate for org-brain. If one department queries it, it stays departmental.
2. **Does the answer need to be the same across departments?** If yes, org-brain. If different departments legitimately have different answers, departmental.

### Goes in org-brain

| Category | Examples |
|---|---|
| Vocabulary canon | Authoritative terms. Departmental glossaries extend; they don't override. |
| Organizational structure | Reporting lines, departments, current quarter rocks |
| Mission, vision, values | The "why we exist" layer informing every department's decisions |
| Cross-cutting policies | Security baselines, compliance requirements, brand voice, legal constraints |
| Shared taxonomies | Customer segments, product lines, geographic regions used by more than one department |
| External entities | Vendors, partners, regulators — the canonical record of who they are |

### Goes in departmental instance

The pattern is consistent across departments: each holds the knowledge load-bearing for its own domain that other departments don't query (or query through reference).

- **Product** — roadmap, feature decisions, customer feedback patterns, product taxonomy, release calendar
- **Finance** — payout rules, reconciliation, financial vendor relationships, compliance hold patterns, audit conventions
- **Leadership** — EOS state (rocks, scorecards, issues), board material, strategy, leadership-only context
- **CS** — triage taxonomy, response templates, escalation rules, ticket categorization, CS-specific vocabulary
- **Engineering** — architecture decisions, runbooks, on-call rotations
- **Marketing** — campaign histories, channel performance, messaging frameworks

Same shape, different content per domain.

---

## Reference, not duplicate

Departmental instances **reference** org-brain canon. They do not copy it.

The canonical glossary lives in org-brain. Departmental glossaries say "for shared vocabulary, see org-brain canon" and only add department-specific extensions. The canonical payout rule lives in the finance instance. CS references it ("source: finance instance D-NNN") and adds CS-facing operational notes; it does not re-state the rule.

Reference resolution happens at agent-read time, not at file-write time. An agent working in the CS instance loads CS substrate plus org-brain canon. The CS substrate stays small. Org-brain stays the single source of truth.

This is the same pattern as ACW's `template_layer` / `instance_layer` / `meta_layer` model from `rules/manifest-discipline.md`, but applied across instances rather than within one. Org-brain is the lattice's template_layer. Each departmental instance is an instance_layer of the org.

---

## Authority across the lattice

Each instance declares its `authority_set` per `rules/instance-hard-rules.md`. The lattice extends this:

- **Org-brain authority set** is the union of all department-recognized authorities at the canonical layer (e.g., `operator`, `department-lead`, `executive`, `board`).
- **Departmental authority sets** are subsets, scoped to that domain.

A cross-instance request carries the **requesting authority** in its payload. The receiving instance verifies the requesting authority against its admission rules. Without an authority model, the lattice is a polite suggestion.

---

## Coordination primitives (status)

Three primitives are needed for the lattice to function as more than parallel instances. Build status of each:

| Primitive | Status | Activation trigger |
|---|---|---|
| **Cross-instance handoff protocol** | Seed (`_inbox/` directory; one-way notification drops) | Three documented cases of lost, mis-routed, or hand-reconciled handoffs |
| **Capability broker** | Designed (`rules/capability-broker.md`); deferred | Triggers in `DEFERRED.md` plus three documented cross-instance write incidents |
| **Admission controller** | Unbuilt | Three documented cases of cross-instance writes that should have been blocked but weren't |

Earn-by-incident applies. None of these ship until evidence justifies it. The lattice can run with hand-coordination through these gaps; the coordination primitives sharpen the federation as the operator accumulates evidence.

---

## Bootstrapping the lattice

When an organization stands up its first ACW instance, which instance comes first? A pilot **departmental** instance, not org-brain.

- Stand up the most pressing department first as a single instance
- Let it accumulate substrate — decisions, glossary, incidents
- When a second department wants to start, pull shared terms into a new org-brain instance and refactor the pilot to reference it
- Subsequent departments scaffold against the existing org-brain

Build org-brain bottom-up from real departmental usage rather than top-down from a hypothetical canon. Org-brain populated before any department exists is theoretical canon, prone to drift and over-specification. Org-brain populated by extracting shared terms from real departmental substrate is grounded.

---

## What this rule does not yet specify

The following are declared open questions. See `research/10-multi-instance-topology.md` for the full list.

- Whether org-brain ships as a formal new instance type beyond Full / Cockpit / Project / Read-Only
- How the lattice handles forked or proposed-but-not-approved canonical entries (canon-governance state machine handles this in principle; lattice-level mechanics not yet specified)
- Whether multi-operator within a single instance needs formal support beyond "lead is the operator; agents are tools"
- Whether the lattice can recursively nest (e.g., a consultancy whose own instance is the meta-lattice for client engagements)

These earn their formalization through incidents, not anticipation.
