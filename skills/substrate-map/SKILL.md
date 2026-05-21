---
name: substrate-map
description: >
  Renders the implicit cross-reference graph across ACW substrate as an
  on-demand markdown view. Walks frontmatter cross-refs and prose mentions
  across decisions, glossary, incidents, codemap (when present), and tasks;
  emits `.acw/substrate-map.md` showing what depends on what, with optional
  confidence-tag coloring per `rules/confidence-tagging.md`. Read-only on
  source substrate. Operator-invoked when navigation help is needed.
role: pipeline-worker
capabilities:
  - substrate.read
  - substrate.write
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Clarification | Low |

# substrate-map

Renders the cross-reference graph that's already implicit in ACW substrate as a single navigable markdown view. The graph isn't stored — it's computed each time the skill runs and emitted as a rendered artifact. Same idea Graphify uses for code; applied to substrate.

## Why this exists

ACW substrate already carries cross-references in frontmatter (`supersedes:`, `depends_on:`, `resolves:`, `derives_from:`, `authority:`, `related_to:`) and in prose (mentions of D-NNN, OQ-NNN, C-NNN, I-NNN by ID). Today those references are scattered across many files. The operator and the agent both lack a single navigable view of "what depends on what." This skill renders that view on demand.

The view is the value. The data underneath is unchanged.

## When to fire

- Operator wants to see what depends on a specific decision before changing it: "What's downstream of D-COPS-008?"
- Onboarding a new agent (or human) into the instance: "Show me the substrate topology."
- After a substantial session-end, to verify cross-references are clean and AMBIGUOUS edges aren't accumulating.
- As a pre-commit sanity check that a new decision/constraint/OQ entry's frontmatter cross-refs resolve to real entries.

## When NOT to fire

- Mid-edit. Render after the change lands, not during.
- For codemap navigation specifically. That's `/codemap`'s job — `substrate-map` covers substrate cross-refs, `codemap` covers code structure. Both can run; they're complementary, not redundant.
- Just because. The rendered view is regenerable; running it on every session start would waste tokens.

## Instructions

### Phase 1 — Discover substrate

Read `acw-state.yaml::profile` and `acw-state.yaml::modules`. Resolve effective modules per `rules/instance-types.md`. Skip modules absent from the declaration.

For each adopted module, locate substrate files per `acw-state.yaml::paths`:

- `decisions_entries_dir` → `.acw/decisions/entries/*.md`
- `decisions_open_questions_dir` → `.acw/decisions/open-questions/*.md`
- `decisions_constraints_dir` → `.acw/decisions/constraints/*.md`
- `glossary_entries_dir` → `.acw/glossary/entries/*.md`
- `session_captures_dir` → `.acw/sessions/*.md`
- `incidents` → `.acw/incidents.jsonl`
- `tasks_status` → `.acw/tasks-status.md`

### Phase 2 — Extract edges

For each entry, parse frontmatter and collect declared cross-references. Schema per `rules/confidence-tagging.md`:

```yaml
supersedes:
  - id: D-COPS-019
    confidence: EXTRACTED        # always 1.0 for frontmatter-declared refs
related_to:
  - id: D-CATL-001
    confidence: INFERRED
    score: 0.85
```

Also scan prose for ID mentions matching the pattern `[A-Z]+-[A-Z]+-\d+` (e.g., `D-COPS-008`, `OQ-ACW-006`, `C-003`). Prose mentions without a frontmatter declaration tag as INFERRED with a default score of 0.6. The operator can promote to EXTRACTED later by adding a frontmatter entry.

For incidents.jsonl, parse each line as JSON and extract `violated:`, `triggered_by:`, `related:` fields.

For tasks-status.md, scan the Pending section for inline ID references.

### Phase 3 — Render

Emit `.acw/substrate-map.md` with the following structure:

```markdown
---
class: derived
authority: derived
stability: regenerable
loaded_by_agent: no
generated_by: substrate-map
generated_at: <ISO timestamp>
---

# Substrate Map — <project name>

Computed by `/substrate-map`. Regenerable; do not edit by hand.

## Summary

- Total nodes: N
- Total edges: N
  - EXTRACTED: N
  - INFERRED: N (avg confidence 0.NN)
  - AMBIGUOUS: N (review needed)

## Hubs (highest-connectivity nodes)

- `D-COPS-035` — degree 7
- `D-ACW-050` — degree 5
- ...

## AMBIGUOUS edges (review required)

- `D-COPS-008` ↔ `D-COPS-024` — conflicting authority claims
- ...

## Cross-references by source

### Decisions

#### D-ACW-050 — v0.10.0: .acw/ dotfolder...
- supersedes: (none) [EXTRACTED]
- resolves: OQ-COPS-019 [EXTRACTED]
- related_to: D-CATL-001 [INFERRED 0.85], D-COPS-035 [INFERRED 0.92]
- referenced_by: C-003 [EXTRACTED], C-004 [EXTRACTED], CHANGELOG.md prose [INFERRED 0.60]

...

### Open questions

...

### Constraints

...

### Incidents

...
```

### Phase 4 — Detect anomalies

Surface in the rendered output:

- **Dangling references.** An entry references `D-COPS-099` but no such file exists. Flag with `[DANGLING]` and a "did you mean?" suggestion based on Levenshtein distance.
- **Orphan entries.** A decision/OQ/constraint that nothing references and that references nothing. Not necessarily wrong (some entries are standalone) — flag for operator awareness.
- **Confidence drift.** Many INFERRED edges with low scores indicate substrate hygiene gap. Surface "N edges have confidence below 0.5 — consider promoting or removing."

### Phase 5 — Confirm

Single-line completion output:

```
substrate-map rendered to .acw/substrate-map.md (N edges across N entries; N AMBIGUOUS)
```

## Output

One file: `.acw/substrate-map.md`. Overwrites prior version (always regeneratable). Includes a `generated_at:` timestamp in frontmatter.

No other substrate writes. The skill is **read-only on source substrate**; the rendered view is the only thing written.

## What this skill is NOT

- **Not a graph database.** No persistent storage of nodes/edges. The rendered markdown is the only artifact.
- **Not a code navigator.** That's `/codemap`. This skill walks substrate, not source.
- **Not an editor.** It surfaces AMBIGUOUS edges and orphans for operator awareness but does not modify entries. The operator resolves drift by editing entries directly.
- **Not auto-loaded.** The rendered map is on-demand reference, not session-start context. Auto-loading it would defeat the point of having INDEX.md as the lightweight session-start surface.

## Operator invocation

```
/substrate-map              # render full map
/substrate-map --module=decisions    # render only decisions sub-graph
/substrate-map --node=D-ACW-050      # render only the neighborhood around one node
/substrate-map --ambiguous-only      # render only AMBIGUOUS edges for review
```

See `references/scope-filters.md` for the full flag set and rendering options.
