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
| **Cross-instance handoff protocol** | Seed (`_buffer/` directory; one-way notification drops) | Three documented cases of lost, mis-routed, or hand-reconciled handoffs |
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

## Adopt, absorb, and divergence resolution

When a workspace's substrate doesn't match ACW canonical, three flows route per-file. There are only two terminal states (canonical-shaped, either via the workspace adopting ACW or ACW absorbing the workspace's pattern); divergence is always temporary, pending review.

### The three flows

| Flow | When it fires | What happens |
|---|---|---|
| **Adopt** | Workspace's file is canonical-shaped or close to it; ACW canonical is the right shape | Skill writes the canonical shape (enrichment of existing file, or migration with `<file>.pre-acw-backup` created) |
| **Absorb** | Workspace's file is *better* than ACW canonical, or addresses something ACW canonical doesn't | Skill writes an absorption candidate to ACW's `_buffer/`; workspace's `acw-state.yaml::divergent_pending_review` records the pending file; ACW operator reviews in a future ACW session |
| **Instance-specific** | The pattern is uniquely the workspace's and won't generalize upstream | Skill writes the file path to `acw-state.yaml::instance_specific_substrate`; future `/acw-instance` runs respect the marker and never propose canonical for it |

### Absorption candidate format (`_buffer/` payload)

When a workspace flags a file for absorption, the audit verb writes a structured note to ACW's `_buffer/`:

**Filename:** `_buffer/YYYY-MM-DD-<workspace>-<topic-slug>-absorption-candidate.md`

**Frontmatter:**
```yaml
---
type: absorption-candidate
from_workspace: <workspace name>
from_workspace_path: <absolute path of the workspace>
date: YYYY-MM-DD
topic: <short topic phrase>
divergent_files:
  - path: <path within workspace>
    canonical_counterpart: <path within ACW canonical, or "none" if net-new>
status: pending-review
read: false
---
```

**Body structure:**

1. **Summary (2–3 sentences).** What the workspace does, why it works, what ACW canonical would gain.
2. **Pattern.** The shape of the divergent substrate. Frontmatter, sections, conventions.
3. **Compared to canonical.** What ACW currently has (or doesn't have) for this concern.
4. **Why this is a candidate.** The specific advantage the workspace's shape offers — better governance, missing capability, more accurate model of the work.
5. **Files to study.** Pointers to the actual divergent files in the workspace (paths only; no content embedded).
6. **Recommendation.** Operator's read on whether ACW canonical should absorb, in what form. Not binding; ACW operator decides.

The note is **read-only after creation**. ACW operator reads, decides, and either:
- Promotes the pattern via the absorption arc (writes a `research/NN-*` note like `research/09`, then ships in next ACW version)
- Rejects it (writes a decision-log entry explaining why; the workspace's file is then re-routed to adopt flow)

### Buffer lifecycle (read flag + `_read/` archive)

After the operator processes an absorption candidate, two metadata edits to the file are allowed (the read-only-after-creation rule above governs the body, not the frontmatter):

1. Flip `read: false` → `read: true`.
2. Add `absorbed_in: <decision-id-or-pointer>` naming where the absorption landed (a decision-log id like `D-ACW-039`, a research note path like `research/13-build-then-rip-pattern-watch.md`, or a free-text pointer like `informational (no canonical promotion)` for FYI-only notes).

Then move the file to `_buffer/_read/`:

```
git mv _buffer/<filename>.md _buffer/_read/
```

`/acw-session start` reads the top level of `_buffer/` only; it does not descend into `_read/`. Moving processed files into the archive subdirectory keeps the top level legible and prevents already-handled notifications from re-surfacing as drift on every session-start. History is preserved via git; no file is ever deleted.

The discipline applies retroactively — operator may flip and move historical notifications that pre-date this convention.

### Divergence markers

Two structured blocks in `acw-state.yaml` track non-canonical substrate:

**`divergent_pending_review`** — temporary; awaiting ACW resolution.

```yaml
divergent_pending_review:
  - path: <substrate file path>
    absorption_candidate: <path to the _buffer/ note in ACW>
    sent_date: YYYY-MM-DD
    status: pending   # pending | absorbed | rejected
```

`/acw-instance upgrade` respects `pending` entries — does not propose canonical changes to those files. When ACW ships a new version that absorbs the pattern, the workspace's next `/acw-instance upgrade` detects the canonical now matches the workspace's shape, marks the entry `absorbed`, and clears it. If ACW rejects the pattern, the entry's `status` updates to `rejected` (manually or via an inbox notification back to the workspace), and the next upgrade run proposes canonical adoption.

**`instance_specific_substrate`** — permanent; intentionally divergent.

```yaml
instance_specific_substrate:
  - path: <substrate file or directory path>
    rationale: <one-line reason>
    decision_ref: <decision-log entry id>
```

`/acw-instance` never proposes canonical changes to files in this list. Adding an entry requires a decision-log entry recording why this substrate is uniquely the instance's (not for upstream absorption).

### Re-adoption flow

Concrete walkthrough of how a divergent pattern resolves:

1. Workspace runs `/acw-instance audit`. Finds a divergent file judged better than canonical.
2. Operator routes to absorb. Audit writes the absorption candidate to ACW `_buffer/`. Workspace's `divergent_pending_review` records the file with `status: pending`.
3. ACW operator opens an ACW session days/weeks later. `/acw-session start` surfaces "1 new notification in `_buffer/`."
4. ACW operator reads the candidate. Decides:
   - **Absorb:** writes a `research/NN-*` note proposing the pattern, runs the absorption arc (study, propose, ship), bumps ACW version with the new pattern in `template_layer` or whatever scope fits.
   - **Reject:** writes a decision-log entry explaining the rejection. Either drops a notification into the workspace's `_buffer/` (cross-repo-writes-permitting), or expects the workspace to discover the rejection on its next upgrade run.
5. Workspace's next `/acw-instance upgrade` fetches the latest canonical from GitHub. For each `divergent_pending_review` entry:
   - Compares the entry's file shape against the new canonical.
   - If canonical now matches the workspace's shape → mark `absorbed`, clear the entry; no further action.
   - If canonical hasn't changed and rejection-notification is present → mark `rejected`, route to adopt flow (replace the divergent file with canonical, with `.pre-acw-backup`).
   - If neither → keep `pending`, surface a one-line status reminder.

The workspace gradient: every divergent file resolves toward canonical-shaped within one or two upgrade cycles. Permanent divergence is only possible via `instance_specific_substrate`, which requires a decision-log entry.

## Cross-repo write governance

Workspaces writing absorption candidates to ACW's `_buffer/` perform a cross-repo write. The discipline:

1. The workspace's `acw-state.yaml::cross_repo_writes` MUST list the absolute path of ACW's `_buffer/` directory before any write fires.
2. The audit verb refuses the absorption write if the path is not declared. Surfaces to the operator: "absorption requires write to `<path>`; declare in `cross_repo_writes` to proceed."
3. The write itself is single-file, append-only (each absorption candidate is one new file; never edit existing notifications).
4. When the capability broker ships (deferred per `rules/capability-broker.md`), the broker becomes the enforcement layer and `cross_repo_writes` becomes the workspace-side declaration of scope. Until then, the declared list is the discipline.

The same governance applies to any future cross-instance write surface (e.g., a workspace dropping a notification into another workspace's `_buffer/`, not just ACW's).

## Runtime code in shipping instances

Some instances are pure-substrate workspaces (governance, decisions, captures only). Others ship real runtime code — a Next.js app, a server, an agent, a script suite. ACW canonical scaffolds every instance as if it were pure-substrate; instances shipping code make a structural choice canonical does not currently dictate.

**Rule (normative, AGENTS.md directive 8):** instances shipping runtime code locate it under a named subdirectory at instance root — `web/`, `server/`, `agents/`, `app/`, or whatever name fits — not at instance root itself. Substrate (`decisions/`, `rules/`, `sessions/`, `acw-state.yaml`, `CLAUDE.md`, `AGENTS.md`) stays at root. Agents writing runtime code mid-session apply this without asking the operator.

**Why:** substrate and runtime move on different clocks. Substrate is governance — slow-moving, decision-driven, audit-checked. Runtime is operational — fast-moving, build-driven, dependency-managed. Mixing them at one path level conflates the two clocks: build artifacts collide with substrate files in `git status`, package managers see substrate as project-root noise, deployment configs (Vercel, Docker) point at a path that also carries decisions/. Subdir separation gives each clock its own surface.

**Status:** normative directive (AGENTS.md #8). No schema field in `acw-state.yaml::paths` yet — the directive is sufficient for agent behavior. A schema field earns its build only when a skill or audit needs to read the runtime path programmatically (e.g., a build-runner skill that needs to know where to `cd` before `npm run build`).

**Migration:** if an existing instance already has runtime code at root and migrating is expensive, log an incident and propose a path forward — do not silently accept the conflation. The directive is forward-looking; it does not retroactively break existing layouts that pre-date it.

**Source:** absorption candidate `_buffer/2026-05-04-cx-dashboard-saas-app-code-location-friction.md` from `cx-dashboard-saas` Phase 0 scaffold; promoted from convention to normative directive same session per D-ACW-040 (operator override on earn-by-incident framing — the activating incident is every code-shipping session, not "operator hits friction").

## What this rule does not yet specify

The following are declared open questions. See `research/10-multi-instance-topology.md` for the full list.

- Whether org-brain ships as a formal new instance type beyond Full / Cockpit / Project / Read-Only
- How the lattice handles forked or proposed-but-not-approved canonical entries (canon-governance state machine handles this in principle; lattice-level mechanics not yet specified)
- Whether multi-operator within a single instance needs formal support beyond "lead is the operator; agents are tools"
- Whether the lattice can recursively nest (e.g., a consultancy whose own instance is the meta-lattice for client engagements)

These earn their formalization through incidents, not anticipation.
