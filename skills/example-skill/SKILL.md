---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

```yaml
name: example-collector
description: >
  Reads new items from a declared source and returns them as a structured
  list. Fires when an orchestrator requests fresh items from a single
  surface. Not for classification, routing, or persistence — those are
  separate skills.
role: pipeline-worker
capabilities:
  - source.read
```

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (declare in instance-hard-rules.md) | Curation | Medium |

# Example Collector

Reads new items from a declared source (a folder of markdown files, an inbox, a feed) and returns them as a structured list. One shape in, one shape out. This is a worked reference — copy this shape when authoring a new skill. See `rules/skill-format.md` for the full contract.

## Why these values

**`role: pipeline-worker`** — this skill sits in the data flow and performs a single leaf operation on one surface. The finer sixteen-role taxonomy in the `rules/pipeline-roles.md` appendix would label this more specifically as a `collector` — a pipeline-worker that pulls raw data from exactly one source on demand, returns the raw shape, and does not interpret or route. The appendix is informative, not normative.

**`6C: Curation`** — this skill selects and organizes (reads items, returns a list). It does not generate new content (Creation) or reason about meaning (Cognition).

**`Governance: Medium`** — derived from Curation per the ITIL 5 classification table in `rules/skill-format.md`.

**`Domain: (blank)`** — domains are declared per-instance. In a fresh ACW clone, this field is a placeholder. Once the operator declares domains in `rules/instance-hard-rules.md`, every skill's Domain column should resolve to one of those values.

**`capabilities: [source.read]`** — the scope this skill needs from the broker (when the broker ships). A real implementation would narrow this further: `inbox.md.read` or `feed.rss.read`.

## What this skill would NOT do

- Classify the items (that is a `classifier` role — separate skill)
- Route them to a destination (that is a `router` role — separate skill)
- Transform their shape (that is a `transformer` role — separate skill)
- Persist them to disk (that is a `committer` role — separate skill)

If you find yourself wanting one skill to do more than one of these, stop and split. Role ambiguity is the upstream cause of most workspace pathologies documented in `SKEPTIC.md`.
