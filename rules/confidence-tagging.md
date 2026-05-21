---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Confidence tagging

Discipline borrowed from Graphify (https://graphify.net) for distinguishing facts from inferences across ACW substrate. Every cross-reference, dependency, or relationship between substrate entries carries a confidence tag.

## The three tags

| Tag | Meaning | Confidence | Example |
|---|---|---|---|
| `EXTRACTED` | Pulled directly from source. The document explicitly says so. | 1.0 (always) | `D-COPS-035 supersedes: D-COPS-019` declared in frontmatter. |
| `INFERRED` | Derived from prose, similarity, or LLM reasoning. Variable confidence. | 0.0–1.0 (explicit number required) | "This decision appears to address the concern in OQ-COPS-008" noticed by `/metabolize` over prose. |
| `AMBIGUOUS` | Conflicting signals detected. Confidence withheld. Human review required. | (not assigned) | Two decisions appear to contradict, or a cross-reference is unresolvable. |

### The `confidence_score` numeric field

Every tagged link MAY also carry a numeric `confidence_score: 0.0–1.0` companion field alongside the tag. Convention:

- **EXTRACTED** → `confidence_score: 1.0` always.
- **INFERRED** → `confidence_score: <explicit float>` required. The number is the discipline; tagging INFERRED without a score is hand-waving.
- **AMBIGUOUS** → `confidence_score` not assigned (omit the field entirely).

This mirrors Graphify's native edge schema (the `/codemap` skill's underlying engine emits both fields per edge). Wiki-shaped substrate uses `score:` in frontmatter; structured logs use `"confidence_score":` in JSON. Either name maps to the same semantic field.

## What gets tagged

Any link between substrate entries:

- Decision → decision (`supersedes`, `depends_on`, `related_to`, `conflicts_with`)
- Decision → open-question (`resolves`, `partially_resolves`)
- Decision → constraint (`authority_for`)
- Constraint → decision (`derives_from`)
- Open-question → decision (`gated_by`, `unblocks`)
- Glossary term → glossary term (`synonym`, `parent_term`, `deprecated_by`)
- Incident → decision (`violated`)
- Task → decision (`implements`, `blocks_until`)
- Session → any (`touched`, `decided_in`, `discovered_in`)
- Codemap edge (function → function, file → file, function → decision)

## Where the tag lives

**Wiki-shaped substrate** (decisions, glossary, open-questions, constraints, sessions, plans, research artifacts): frontmatter.

```yaml
---
id: D-COPS-035
title: "..."
supersedes:
  - id: D-COPS-019
    confidence: EXTRACTED
related_to:
  - id: D-CATL-001
    confidence: INFERRED
    score: 0.85
    rationale: "Sibling decision applying same convention in cs-atlas."
---
```

**Structured logs** (`incidents.jsonl`): per-record field.

```json
{"id": "I-COPS-007", "violated": [{"id": "D-COPS-008", "confidence": "EXTRACTED"}]}
```

**Flat narrative** (`build-log.md`): inline annotation or sidecar `.confidence.jsonl` file. Convention to be set per-instance based on operator preference.

## When tags are assigned

- **At write time** when the operator or skill knows the source. A frontmatter `supersedes:` that the operator types is EXTRACTED. A cross-reference a skill discovered during synthesis is INFERRED with a score.
- **At audit time** when `/acw-instance audit` walks the substrate and discovers implicit links not yet tagged. New discoveries default to INFERRED until reviewed.
- **At metabolize time** when `/metabolize` distills raw inputs into enriched substrate. Discovered relationships are INFERRED.

## How tags surface

`/acw-instance audit` reports:

```
Confidence audit:
  EXTRACTED links:  142
  INFERRED links:    23  (avg confidence 0.78)
  AMBIGUOUS links:    4  (review needed — see report)
```

AMBIGUOUS links block clean-audit status. Operators must resolve them (promote to EXTRACTED, demote to INFERRED with a score, or delete) before audit passes.

`/substrate-map` (when shipped) uses tags to color or stratify the rendered link view: EXTRACTED solid, INFERRED dashed, AMBIGUOUS flagged.

## What is NOT tagged

Internal content of a substrate entry — body prose, schema fields, frontmatter values that aren't cross-references — is not tagged. Confidence tagging is for the *graph* of substrate, not for the *content* of any single entry.

If an entry's content itself is uncertain (e.g., a decision was accepted under partial information), that uncertainty belongs in the entry's body, not in the confidence-tagging convention.

## Anti-patterns

- **All-EXTRACTED.** Mass-tagging every cross-reference as EXTRACTED to make audits pass. Defeats the discipline. The reviewer must actually distinguish facts from inferences.
- **INFERRED without a score.** Variable confidence without a number is hand-waving. Always provide 0.0–1.0.
- **AMBIGUOUS as the dustbin.** Using AMBIGUOUS to defer hard calls. AMBIGUOUS is for genuine conflicts, not for "I don't want to decide right now."
- **Mixing tag levels in a single field.** A frontmatter `related_to:` list either uses tags on every entry or none. Don't half-apply.

## Migration path for existing substrate

Existing instances (pre-0.10.0) have un-tagged cross-references. Migration is gradual:

1. New entries get tags from creation forward (enforced by skill or pre-commit hook).
2. Existing entries get tags during the next `/acw-instance audit` pass — skill discovers links and defaults them to INFERRED with operator review.
3. Frontmatter-declared cross-refs (`supersedes:`, `depends_on:` etc.) auto-promote to EXTRACTED on first audit since the file explicitly states them.
4. AMBIGUOUS surfaces during audit and gates clean status.

No instance is forced to tag everything at upgrade time. The discipline grows with use.
