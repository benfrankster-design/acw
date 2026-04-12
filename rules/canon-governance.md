---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Canon Governance

How vocabulary enters, advances, and retires in an ACW instance. This file is the governance-layer implementation of "self-correcting contract." It is NOT the typed-remediation version in `deferred/self-correcting-contract/`. Read that folder's README for the distinction.

## Why a canon

Vocabulary drift is the single biggest multi-domain pitfall in persistent agentic workspaces. When two skills use "ticket" to mean two different things, or "approved" moves through a state machine that isn't written down, the workspace silently accumulates contradictions until an agent acts on one and damages an asset. A canon is the minimum viable defense: one file that names every concept, one process that decides what enters, one lint that blocks drift at commit time.

## SKOS lineage

The schema in `rules/canon-schema.yaml` is a minimal port of SKOS (Simple Knowledge Organization System, W3C). Full literature survey and port decisions live in `research/02-literature-survey.md`. What was ported: `pref_label`, `alt_labels`, `hidden_labels`, `definition`, `scope_note`, `broader`, `narrower`, `related`. What was deliberately omitted: hierarchy semantics beyond parent/child, URIs, SKOS-XL, multi-lingual labels. See the research file for the full port table.

## Schema fields (mirrors `rules/canon-schema.yaml`)

- **concept_id** — stable machine identifier, never reused after retirement
- **pref_label** — the one canonical human-readable name
- **alt_labels** — acceptable synonyms that resolve to the same concept
- **hidden_labels** — forbidden synonyms; lint blocks commits that contain them
- **definition** — one sentence, plain language
- **scope_note** — boundary conditions, what the term does and doesn't cover
- **domain** — which MECE domain this concept belongs to
- **disambiguator** — short phrase that resolves polysemes (see polyseme example below)
- **state** — draft / proposed / approved / deprecated / retired
- **approval_authority** — free-form string naming who advanced this term to approved
- **broader / narrower / related** — optional concept links

## N-authority approval model

`approval_authority` is a free-form string. The single-operator default is `operator`. Any instance may declare its own authority set in `rules/instance-hard-rules.md`. Three worked examples:

**Single-authority (default).** `approval_authority: operator`. One person advances every term. Fastest. Appropriate for a solo contractor, a personal workspace, or the earliest phase of any new instance.

**Two-tier (one valid configuration, not the default).** `approval_authority: operator` for operational concepts, `approval_authority: leadership` for cross-functional concepts. Appropriate when a single operator owns one domain but shares vocabulary with a broader group. This is one valid configuration among many, not the recommended shape.

**Four-tier.** `approval_authority: operator`, `department-lead`, `director`, `sponsor`. Each authority has a declared scope in `instance-hard-rules.md`. Advancement requires approval from the authority whose scope covers the concept's domain. Appropriate for larger instances with genuine separation of concerns.

**Novelty callout.** The N-authority approval pattern generalizes the two-bucket term-owner concept found in Better Rules NZ and the DataHub term governance model. It is not a SKOS standard and it is not a KCS standard. This generalization is shipped as `stability: experimental` and earns promotion via documented use, not by citation.

## State machine

| State | Allowed transitions | Who advances | Evidence required |
|---|---|---|---|
| draft | → proposed, → retired | author | none |
| proposed | → approved, → draft, → retired | declared approval_authority | one decision-log entry |
| approved | → deprecated | declared approval_authority | one decision-log entry + migration note |
| deprecated | → retired | declared approval_authority | no usages in committed content |
| retired | (terminal) | — | — |

Retired `concept_id` values are never reused.

## Ingest-time canonicalization gate

When `tools/lint-vocab.py` detects a `hidden_label` in committed content, the lint exits non-zero and emits a repair hint naming the canonical `pref_label`. Commit is blocked until the content is updated or the hidden_label is removed from the canon entry. This is the enforcement edge of the whole system; without it, the canon is documentation, not governance.

## Intra-workspace propagation scope

Canonicalization propagates within one ACW instance only. External systems (ticketing, docs, chat) are out of scope for v0.1. A future deferred primitive (`deferred/jsonld-export/`) addresses cross-system export; see that folder's README.

## Worked polyseme example

"QA" is a real collision. In one domain it means Quality Assurance (the team, the process, the tests). In another it means Question Answering (the retrieval task, the benchmark, the model capability). Both are legitimate. Both ship in the same canon via two entries:

```
- concept_id: qa-quality-assurance
  pref_label: QA
  disambiguator: "quality assurance team and process"
  domain: operations
- concept_id: qa-question-answering
  pref_label: QA
  disambiguator: "question answering retrieval task"
  domain: ml-research
```

Lint treats `domain` + `disambiguator` as the tiebreaker. Content that uses "QA" without domain context is flagged for clarification.

## Relationship to deferred self-correcting contract

This file ships the governance-escalation version of self-correcting contract: drift is detected at lint time, escalated to the declared approval_authority, and resolved via a decision-log entry. The typed-remediation version — where contract postconditions automatically repair asset state via MPST/PDDL-style machinery — is deferred. See `deferred/self-correcting-contract/README.md` for why the typed version is not shipping in v0.1.
