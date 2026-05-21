---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# skill-manifest

## What it is

An extension of the SKILL.md pattern that adds typed declaration of inputs, outputs, and role against the workspace input schema. Every skill declares exactly what it consumes, what it produces, and what role it plays in the pipeline.

## What problem it addresses

Frontier problem #1 (MECE) and #5 (semantic validation). Without a typed skill manifest, the workspace cannot mechanically check that a skill's declared inputs match any real payload shape, or that its outputs conform to what downstream skills expect.

## Prior art

Kubernetes CRDs, gRPC service definitions, OpenAPI operation definitions, SKILL.md conventions from the author's personal workspace. See `research/02-literature-survey.md`.

## Activation trigger

Activation of `deferred/workspace-input-schema/`. The skill manifest is meaningless without the schema it references, so it cannot ship alone.

## Shippable form factor

Extended YAML frontmatter in every SKILL.md file declaring `inputs`, `outputs`, and `role` against the workspace schema. A validator script (`tools/lint-skills.py`, not shipped) that walks the skills directory and checks every SKILL.md against the schema.

## What it is NOT

- Not a runtime type checker — it validates at commit time only
- Not a replacement for the role enum in `rules/pipeline-roles.md` — it extends it
- Not designed to support skill composition or pipelining (those are separate primitives)
