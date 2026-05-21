---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# asset-frontmatter

## What it is

Required frontmatter on every asset in the workspace declaring the asset's justification (why it exists), its valid-time (when the claim is true in the world), and its system-time (when the claim was written to the workspace). The frontmatter is the minimum surface that drift detection needs.

## What problem it addresses

Frontier problem #3: self-correcting drift detection. Assets go stale because nothing in the workspace knows when a claim stopped being true. Valid-time / system-time separation (bitemporal) gives the workspace a way to measure staleness.

## Prior art

Bitemporal data modeling (Snodgrass, Date), event sourcing patterns, git commit metadata, SQL temporal extensions (SQL:2011). See `research/02-literature-survey.md`.

## Activation trigger

One stale-claim incident where an asset was trusted past its valid window and the damage propagated to another asset. Severity `high` counts as a single triggering incident, not three.

## Shippable form factor

A required frontmatter block on every markdown asset with fields `justification`, `valid_time`, and `system_time`. The lint is extended to check that these fields are present and that `system_time` is never in the future. A separate drift-detection primitive consumes these fields at runtime.

## What it is NOT

- Not a full bitemporal database — it's a minimum surface
- Not a replacement for git history — it's orthogonal
- Not designed to handle transactions across multiple assets
- Not sufficient on its own — must pair with a drift detector
