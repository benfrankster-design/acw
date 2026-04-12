---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Pipeline Roles — Skill Role Contract

**Version:** 0.1.0
**Status:** Normative. Every skill declares exactly one role from the four-group enum below. The sixteen-role finer taxonomy in the appendix is informative, not normative, and earns promotion only through the incident ritual.

---

## The Rule

Every skill MUST declare exactly one `role:` field in its `SKILL.md` frontmatter. The value MUST match one of the four role IDs in the enum below. A skill that cannot be assigned exactly one role is not a skill; it is a pipeline masquerading as a skill and must be split before it ships.

**No new skill is created until its role is chosen from this enum.** Role ambiguity is the upstream cause of domain collisions, undeclarable capability scopes, and validation failures. A skill that plays two roles at once cannot have its capability scope declared narrowly, which means downstream governance cannot protect it, and the workspace inherits a permission surface larger than any single operation requires.

---

## The Enum (Four Groups, Normative)

MECE dimension: **data flow**. A role is defined by where it sits in the flow from input to committed output, not by vocabulary or domain.

### 1. `orchestrator`

Coordinates other skills in sequence. Does no leaf work. Knows the order, handles handoffs, passes context between stages.

- **Allowed:** invoke other skills, pass payloads between stages, collect results, return a summary
- **Forbidden:** read external sources directly, transform payloads, write to the store, invoke external tools without delegation
- **Capability posture:** none directly; delegates every scope to the downstream skill it invokes

**Generic example:** a session-logging skill that invokes a committer to persist the log, then an extractor to update a glossary, then a composer to produce a briefing. The orchestrator owns the sequence but does none of the three jobs.

### 2. `pipeline-worker`

A skill that sits in the data flow and performs exactly one job: collecting, extracting, classifying, routing, enriching, transforming, composing, revising, or committing. The four-group enum collapses the finer taxonomy into one label because at the scale this template assumes (a single-operator or small-team instance without formal capability scoping), the finer distinctions are pedagogically interesting but operationally redundant.

- **Allowed:** exactly one job on exactly one declared shape of input and output
- **Forbidden:** perform more than one job; write to a store outside the declared target; invoke other skills (that is the orchestrator's job)
- **Capability posture:** one narrow scope matching the one job

**Generic example:** a skill that reads unread messages from a single messaging surface and returns them as a structured list. It collects. It does not classify, route, or write. The next step in the pipeline is a different skill.

**When to split:** when a single `pipeline-worker` skill carries two sub-jobs internally (for example, "reads a ticket and also writes the classification"), split into two skills. The sixteen-role finer taxonomy in the appendix is the reference for how to name the split.

### 3. `guardian`

Blocks unsafe actions preventively. Implemented as a hook or lightweight check that fires before destructive or exposure-prone operations. Accept-or-reject only.

- **Allowed:** pattern-match against action, block, warn, allow, optionally rewrite with rationale
- **Forbidden:** fix, mutate store state, route, commit, invoke downstream skills
- **Capability posture:** read-only on action metadata; no tool access

**Generic example:** a pre-commit hook that blocks any command containing a credential literal, regardless of which skill emitted it.

### 4. `broker-sideband`

Not in the data flow. Sits beside it. Holds credentials or performs any other cross-cutting function that every pipeline skill may need to invoke but that is not itself a pipeline step.

- **Allowed:** issue references, verify declared scope against the requesting skill's manifest, swap references for real authority at egress, revoke on session end, append to an audit log
- **Forbidden:** participate in payload transformation; read payload content beyond what is needed for egress; be invoked inside the pipeline as a normal skill
- **Capability posture:** holds credentials the pipeline skills do not; issues narrow leases; logs every issuance

**Generic example:** a capability broker that holds external-service tokens. A pipeline-worker skill asks the broker for a lease scoped to one read operation; the broker verifies the skill's manifest declares that scope, issues a reference with a short TTL, and swaps the reference for the real token at the moment of outbound call. See `rules/capability-broker.md`; the tool implementation is deferred in v0.1.0.

---

## Declaration Format

Every `SKILL.md` file MUST include `role:` in its YAML frontmatter:

```yaml
---
name: Example Skill
description: Reads new items from a declared source and returns them as a list
role: pipeline-worker
capabilities:
  - source.read
---
```

The `role:` value MUST match one of the four IDs above (`orchestrator`, `pipeline-worker`, `guardian`, `broker-sideband`), lowercase, exactly.

---

## Forbidden Patterns

A skill that exhibits any of the following is not conformant and must be split or refactored:

1. **Multi-role.** Declares `role: pipeline-worker` but also invokes other skills. Split into a pipeline-worker plus a parent orchestrator.
2. **Role drift.** Declares `role: orchestrator` but performs leaf work. Split the leaf work into a pipeline-worker the orchestrator invokes.
3. **Guardian with state.** Declares `role: guardian` but writes to the store or mutates payload. Guardians are pure accept-or-reject. Any mutation should live in a pipeline-worker the guardian invokes after approval.
4. **Broker co-option.** A pipeline-worker skill reads a credential directly from a config file. All credential access must route through a broker-sideband, even in broker-absence fallback.

---

## Why four groups and not sixteen

An earlier draft of this file shipped sixteen roles as normative, with a four-group classification layer above them. The rationale was pedagogical: the sixteen-role finer taxonomy (collector, watcher, extractor, classifier, router, enricher, transformer, composer, worker, committer, auditor, sanitizer, researcher, plus orchestrator, guardian, and broker) makes capability scopes declarable narrowly and forces the operator or reader to think about what a skill actually does at a finer grain.

That draft was reviewed by multiple stress-test agents who independently argued that the sixteen-role enum is premature precision at single-operator scale. At scale where one operator is playing all sixteen roles in the same session, the fine grain creates a naming tax (every skill author must pick from sixteen options and understand the distinctions) without delivering the capability-scoping payoff that a real multi-agent permission model would require.

The current version ships four groups as normative and preserves the sixteen-role finer taxonomy in the appendix. Skills declare at the four-group level. Operators who have earned incident evidence that four groups are too coarse can promote the sixteen-role taxonomy via the promotion ritual in `rules/promotion-ritual.md`.

**One honest admission:** the sixteen-role taxonomy is still valuable as a teaching artifact even when it is not normative. An operator choosing between `pipeline-worker` as a label and `collector` or `router` or `composer` as a sharper label is doing real thinking about the skill's purpose. The sixteen labels exist to support that thinking. They do not exist to enforce interop.

The operator maintaining their own personal workspace may choose to make the sixteen-role taxonomy normative in their instance. That is a valid instance-level override and should be recorded in `decisions/decision-log.md`.

---

## Extension Protocol

Promoting the sixteen-role finer taxonomy from appendix to normative, or adding an entirely new role, requires:

1. **Evidence in `incidents.jsonl`.** At least three documented cases where the current four-group enum produced role ambiguity or forced a bad split.
2. **MECE check.** Any new or promoted role must be mutually exclusive with all existing roles. If it overlaps, the existing role gets sharpened first.
3. **Decision entry** in `decisions/decision-log.md` recording the promotion.
4. **Version bump.** Additions go to v0.2. Replacements or renames go to v1.0 (breaking change).

See `rules/promotion-ritual.md` for the mechanical procedure.

---

## Appendix: The Sixteen-Role Finer Taxonomy (Informative, Not Normative)

This appendix documents the finer-grained role taxonomy available to operators whose incident evidence has earned the expansion. Skills in a v0.1.0 ACW instance declare at the four-group level; the sixteen roles below exist as teaching material and as a target for future promotion.

Each role is a specialization of one of the four normative groups.

**Sub-roles of `pipeline-worker`:**
- `collector` — pulls raw data from one source on demand
- `watcher` — a collector that fires on a trigger instead of on demand
- `extractor` — parses unstructured input into structured output
- `classifier` — labels input; does not dispatch
- `router` — dispatches classified items to downstream skills
- `enricher` — adds lookup fields to a payload
- `transformer` — rewrites payload shape without changing meaning
- `composer` — creates a new artifact from inputs and templates
- `worker` — revises an existing artifact in place
- `committer` — persists an artifact to its declared target
- `auditor` — compares state to declared rules; reports only
- `sanitizer` — fixes what the auditor reports

**Research role (composite):**
- `researcher` — gathers from tiered sources, verifies, synthesizes into `research/` only

**Guardian role:** same as the four-group `guardian`.

**Broker sideband role:** same as the four-group `broker-sideband`.

An operator whose incidents have earned the promotion can adopt the sixteen-role taxonomy as normative for their instance. Until then, the four groups are the contract.

---

## Changelog

- **v0.1.0 — 2026-04-11** — Initial release. Four role groups normative. Sixteen-role finer taxonomy in the appendix as informative. Extension protocol requires incident evidence.
