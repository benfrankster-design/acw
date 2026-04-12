---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

```yaml
name: Example Collector
description: Reads new items from a declared source and returns them as a structured list.
role: pipeline-worker
capabilities:
  - source.read
```

# Example Skill — Reference Implementation

This is a worked reference showing how a skill declares itself against the ACW contracts. It does not do anything real. Copy this shape when authoring a new skill.

## What this skill would do

Given a declared source (a folder of markdown files, an inbox, a feed), read items that have appeared since the last run and return them as a structured list. One shape in, one shape out. No transformation, no routing, no writes.

## Why `role: pipeline-worker`

Every SKILL.md must declare exactly one role from `rules/pipeline-roles.md`. The four normative groups are `orchestrator`, `pipeline-worker`, `guardian`, and `broker-sideband`. This skill declares `pipeline-worker` because it sits in the data flow and performs a single leaf operation on one surface.

The finer sixteen-role taxonomy in the `rules/pipeline-roles.md` appendix would label this more specifically as a `collector` — a pipeline-worker that pulls raw data from exactly one source on demand, returns the raw shape, and does not interpret or route. The appendix is informative, not normative. A skill that declares `pipeline-worker` is conformant; a skill that also annotates `collector` in its description is helpful but not required.

## Capabilities

The `capabilities` list in frontmatter declares the scopes this skill needs from the broker (when the broker ships). For now, `source.read` is a placeholder naming the smallest useful scope: read access to one source. A real implementation would narrow this further — e.g., `inbox.md.read` or `feed.rss.read`.

## What this skill would NOT do

- Classify the items (that is a `classifier` role — separate skill)
- Route them to a destination (that is a `router` role — separate skill)
- Transform their shape (that is a `transformer` role — separate skill)
- Persist them to disk (that is a `committer` role — separate skill)

If you find yourself wanting one skill to do more than one of these, stop and split. Role ambiguity is the upstream cause of most workspace pathologies documented in `SKEPTIC.md`.
