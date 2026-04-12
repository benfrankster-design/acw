---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# 05 — Ship Decision

This is the shortest research file. It records the final ship decision and the rationale for every primitive that made the cut versus every primitive that was deferred.

## What shipped in v0.1.0

Thirty-nine files total:

- **Eight already-shipped in the governance precursors** — pipeline-roles, canon-schema, vocabulary-lint, capability-broker (design doc), decision-tracking, promotion-ritual, glossary, CHANGELOG
- **Five tier 2 files** — canon-governance, canon.yaml (empty), instance-hard-rules, DEFERRED.md, decision-log scaffold
- **Two tier 3 tools** — lint-vocab.py, log-incident.py (log + count + check-drift)
- **Five tier 4 tests and fixtures** — two test files, three fixture files
- **One tier 5 example skill**
- **Three tier 6 operator-facing files** — bootstrap, migration, threat-model
- **Seven tier 7 research files** — this archive
- **Five tier 8 root indexes** — README, AGENTS, SKEPTIC, AUTHOR, LINEAGE
- **Twelve deferred library files** — DEFERRED.md overview + 11 subfolder READMEs
- **Six supporting files** — LICENSE-CONTENT, LICENSE-CODE, .gitignore, .editorconfig, incidents.jsonl, CHANGELOG header

## What was deferred

Eleven primitives in the deferred library, each with an activation trigger. The full table is in `DEFERRED.md`. Summary by class:

- **Three schemas** — workspace-input-schema, skill-manifest, asset-frontmatter
- **Four tools** — admission-controller, drift-detector, conformance-test, jsonld-export
- **Two infrastructure layers** — contract-registry, self-correcting-contract (typed version)
- **One governance process** — aaif-submission
- **One append-only log** — manifest

## The decision matrix

Every primitive was evaluated against three questions:

1. **Does it earn its ship at single-operator scale?** If no, defer.
2. **Does the ship require infrastructure ACW does not have?** If yes, defer.
3. **Is the design load-bearing such that losing it would collapse the rest?** If yes, ship as design document even if the tool is deferred.

| Primitive | Q1 | Q2 | Q3 | Decision |
|---|---|---|---|---|
| canon-governance | yes | no | yes | ship |
| pipeline-roles | yes | no | yes | ship |
| vocabulary-lint | yes | no | yes | ship tool |
| log-incident | yes | no | yes | ship tool |
| capability-broker | partial | yes | yes | ship doc, defer tool |
| workspace-input-schema | no | no | partial | defer |
| skill-manifest | no | yes | partial | defer |
| asset-frontmatter | partial | no | partial | defer |
| contract-registry | no | yes | yes | defer |
| admission-controller | no | yes | yes | defer |
| drift-detector | no | yes | yes | defer |
| conformance-test | no | yes | partial | defer |
| jsonld-export | no | no | partial | defer |
| aaif-submission | no | yes | partial | defer |
| self-correcting-contract (typed) | no | yes | yes | defer |
| manifest (append-only log) | partial | no | partial | defer |

## Why this is the right ship

Path C (39 files) is the answer to the question "how much shape is load-bearing for teaching without being theater, under the training-ground framing?" The skeptic's 24-file minimum removes too much of the design lineage. The architect's 48-file maximum includes primitives that have not earned a ship. The 39-file middle includes every primitive that either earns its ship at single-operator scale or preserves design work that would be expensive to reconstruct later.

## What v0.1.0 is explicitly not

- Not a validated production system
- Not a standard (no external adopters, no governance body)
- Not a complete solution to the five frontier problems
- Not a drop-in replacement for anyone's existing workspace
- Not the final form of any primitive except the licenses and the .editorconfig

The disclaimer in `README.md` says this in one sentence. This file says it in several. Both are the same claim.
