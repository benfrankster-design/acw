---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# DEFERRED — The Deferred Library

This file is the canonical list of infrastructure primitives that ACW has designed but deliberately not shipped. It is not a roadmap. It is not a "coming soon" page. It is a restraint device.

## What the deferred library is

The seven-phase research project that produced ACW identified more primitives than any single operator should ship at once. Shipping everything would collapse the earn-by-incident discipline into builder-mode tunnel vision — the exact failure mode the discipline exists to prevent. The deferred library is the mechanical restraint that says: these primitives are designed, the design notes are preserved, and each one has a named activation trigger that earns its ship.

Every entry in this table has a companion subfolder under `deferred/` with a README describing the design, the prior art, the activation trigger, and the explicit scope cut. The subfolder READMEs are `authority: derived` — this table is canonical. If they drift, `tools/log-incident.py check-drift` catches it.

## The activation trigger rule

A primitive earns promotion review when three incidents at severity `med` or higher, on that primitive, are logged in `incidents.jsonl`. Review means opening a decision-log entry, not automatic ship. Promotion still runs through `rules/promotion-ritual.md`.

Some primitives have stricter triggers — a single named high-severity incident of a specific shape, or an external condition (e.g., a standard reaching production maturity). The table below is authoritative; subfolder READMEs elaborate.

## The 11 primitives

| # | Name | Class | One-line summary | Activation trigger | Pointer |
|---|---|---|---|---|---|
| 1 | workspace-input-schema | schema | Closed enum of verbs, domains, types, surfaces that any skill can consume | 3+ skill routing collisions where a payload could not be unambiguously classified | `deferred/workspace-input-schema/` |
| 2 | skill-manifest | schema | SKILL.md pattern extension declaring inputs, outputs, and role against the input schema | Activation of workspace-input-schema | `deferred/skill-manifest/` |
| 3 | asset-frontmatter | schema | Required frontmatter on every asset: justification, valid-time, system-time | One stale-claim incident where an asset was trusted past its valid window | `deferred/asset-frontmatter/` |
| 4 | contract-registry | infra | Aggregated typed view across all skills and assets in a workspace | Second workspace exists (cross-workspace consistency becomes the problem) | `deferred/contract-registry/` |
| 5 | admission-controller | tool | Two-phase mutator + validator that gates every tool call against declared contracts | One cross-domain tool call that damaged an asset | `deferred/admission-controller/` |
| 6 | drift-detector | tool | Merkle-hashed assets + NLI + ATMS-style contradiction tracking | One contradiction the operator could not date | `deferred/drift-detector/` |
| 7 | conformance-test | tool | 12-check runner validating schema, contract, and asset health | Activation of contract-registry | `deferred/conformance-test/` |
| 8 | jsonld-export | tool | JSON-LD @context file for handing vocabulary to external systems | Handing controlled vocabulary to an external client or partner | `deferred/jsonld-export/` |
| 9 | aaif-submission | governance | Submission and publication path for contributing primitives upstream | Two independent workspaces + one external contributor | `deferred/aaif-submission/` |
| 10 | self-correcting-contract | infra | MPST/PDDL-style typed remediation via contract postconditions | (a) named incident where governance escalation fails AND (b) cited external publication confirming MPST/PDDL production maturity | `deferred/self-correcting-contract/` |
| 11 | manifest | tool | Append-only receipt log outside agent edit surface | First registry-gated action outside cap-broker surface | `deferred/manifest/` |

## Explicit non-goals

The deferred library is not a roadmap. There is no calendar commitment to ship any of these. There is no implied ordering beyond the activation triggers themselves. A primitive can sit in `deferred/` indefinitely and that is the intended behavior — the library only shrinks when lived experience justifies a ship.

## Self-correcting-contract honesty note

Primitive #10 is specifically the typed-remediation version of self-correcting contract — MPST (multiparty session types) or PDDL-style machinery that automatically repairs asset state when postconditions fail. The governance-escalation version of self-correcting contract is already shipping inside `rules/canon-governance.md` (lint detects drift, escalates to approval authority, resolved via decision-log). These are two distinct mechanisms that share a name. Do not conflate them. The deferred version is a much harder problem and requires external research maturity before it can ship.

## Pointer

Before proposing a promotion from this library, read `SKEPTIC.md`. The skeptic exists precisely to push back on well-intentioned premature ships.
