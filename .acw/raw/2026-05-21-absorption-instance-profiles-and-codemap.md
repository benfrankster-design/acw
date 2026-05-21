---
class: absorption-candidate
authority: instance
stability: proposed
date: 2026-05-21
origin_instances:
  - cs-atlas (anticipated codemap consumer post-Robert-clone)
  - gsg-cs-chatbot (future coding instance)
  - synapse (org-brain instance type)
  - cs-ops-spec (spec-project instance type)
operator: Ben Frank
proposes: convention extension
scope: substrate-shape + instance-type modularity (cross-cutting)
influences:
  - Graphify (https://graphify.net) — codebase-as-knowledge-graph
  - enrichment-vs-memory principle (synapse/Rules/Procedures/enrichment-vs-memory.md)
companion_to: 2026-05-21-absorption-acw-substrate-under-dotfolder.md
review_status: pending
---

# Absorption Candidate — Multi-Instance-Type Profiles + Codemap Substrate Module

## TL;DR

ACW canonical currently assumes one instance shape: substrate-heavy, decisions/sessions/glossary/build-log all expected. But ACW is evolving to host multiple instance types — org brains, spec projects, coding projects, libraries — each with different substrate needs. This proposal:

1. **Declares instance-type profiles** as a first-class concept in `acw-state.yaml`. Each profile names the substrate modules it adopts.
2. **Introduces a `codemap/` substrate module** for coding-instance types, modeled on Graphify's knowledge-graph approach. Stored under `.acw/codemap/`. Replaces or augments raw codebase re-reads with a pre-computed, AI-consumable map.
3. **Modularizes existing substrate** so instances can adopt à la carte. Each module declares what it produces and the contract it honors; instances opt in via `acw-state.yaml::profile` and `acw-state.yaml::modules`.

Pre-requisite: companion proposal `2026-05-21-absorption-acw-substrate-under-dotfolder.md` (the `.acw/` dotfolder convention). This proposal extends that one.

## Why this matters now

The framing has shifted. ACW is no longer "the substrate for spec-shaped projects." It's the substrate convention for **any directory-based work where humans and AI both read and write**. That includes:

- **Org brains** (synapse-shaped) — entire organizational knowledge management
- **Spec projects** (cs-ops-spec, frank-context) — design substrate, decision-heavy
- **Coding projects** (cs-atlas, gsg-cs-chatbot, gsg-cs-atlas-mcp) — code + substrate hybrid
- **Libraries** (smaller code projects with minimal substrate)
- **Future types** we haven't built yet

A one-size-fits-all substrate shape underserves all of them. A library shouldn't carry `briefings/` and `inbox/`. A coding project needs `codemap/` that the spec project doesn't. An org brain needs a different research/curation flow than a spec project's research/queries pipeline.

## Proposed: instance-type profiles

Declare in `acw-state.yaml`:

```yaml
project:
  name: "..."
  code: "..."
  domain: "..."

profile: coding-project           # NEW — one of: org-brain | spec-project |
                                  # coding-project | library | custom
modules:                          # NEW — declare which substrate modules
  - decisions                     # the instance uses
  - sessions
  - tasks-status
  - incidents
  - codemap                       # only for coding-project / library
  - raw
  # glossary, briefings, inbox, build-log, etc. omitted = not adopted
```

ACW skills consult `profile` and `modules` to know which substrate paths to read, write, and audit. Modules absent from the declaration are not expected — `/acw-instance audit` won't flag them as missing.

### Recommended default modules per profile

| Profile | Default modules |
|---|---|
| `org-brain` | decisions, sessions, glossary, build-log, incidents, raw, plans, briefings, inbox, archives |
| `spec-project` | decisions (entries + open-questions + constraints), sessions, glossary, tasks-status, incidents, raw, plans, build-log |
| `coding-project` | decisions, sessions, tasks-status, incidents, codemap, raw, build-log |
| `library` | decisions, codemap, raw, build-log |
| `custom` | as declared — no defaults |

Instances can deviate from defaults by editing `modules:` directly. The profile is a starting shape, not a lock-in.

## Proposed: `codemap/` substrate module

For coding-project and library instances, introduce `codemap/` under `.acw/`:

```
.acw/
├── codemap/
│   ├── GRAPH_REPORT.md          # the AI-consumed summary (auto-loaded)
│   ├── nodes.json               # raw graph nodes
│   ├── edges.json               # raw graph edges with confidence tags
│   ├── communities.json         # cluster analysis (god nodes, hubs)
│   ├── surprising-connections.md # human-readable insights
│   └── .cache/                  # per-file incremental rebuild cache
└── ...
```

### Why codemap belongs in `.acw/` and not at repo root

The codemap is **metadata about the code, not the code itself**. Same principle that put decisions/sessions/glossary in `.acw/`. A consumer who clones the repo to use the artifact (a library, a service) doesn't need the codemap; an agent that reads the code does. Hide it behind `.acw/` so the public-facing repo stays clean.

### Build pattern (Graphify-modeled)

Two-stage extraction, ACW-adapted:

**Stage 1 — Deterministic (Tree-sitter or equivalent AST tool).**
Extracts structural facts: files, functions, classes, imports, call graph, docstring presence. Edges tagged `EXTRACTED` with confidence 1.0. Reproducible, language-aware, no LLM cost.

**Stage 2 — Semantic (LLM).**
Reads README, AGENTS.md, decisions log, design docs, doc-strings, rationale comments. Produces edges tagged `INFERRED` with variable confidence (0.0–1.0). Surfaces architectural intent: "this function implements decision D-CATL-003," "this module is the customer-facing boundary." LLM runs locally where possible (gsg-rag substrate already in place for GSG instances).

Edges flagged `AMBIGUOUS` route to human review — same governance shape as the audit-ingest pipeline cs-atlas already uses.

### Freshness

File-level cache. On commit, only changed files re-extract through Stage 1. Stage 2 re-runs only when changed files touch documented rationale or when a new decision lands in `.acw/decisions/`. Cheap incremental rebuild.

### What the agent loads

Only `GRAPH_REPORT.md` and `communities.json`. The rest (`nodes.json`, `edges.json`, `.cache/`) is backing storage the report summarizes. Same enrichment shape every other ACW substrate module uses: thin index loaded, fat data on disk.

### Why not just RAG?

Graphify makes the case explicitly: AST + labeled edges + community structure beats embedding similarity for code navigation. Embeddings answer "what's similar" — graph traversal answers "what calls what, what depends on what, what was decided where." For code, the latter is what an agent needs. RAG over docs stays useful for prose retrieval (HC articles, SOPs); codemap covers structural retrieval.

The two compose. gsg-rag handles prose. codemap handles code. Both feed the agent.

## Cross-cutting principle borrowed from Graphify: confidence-tagged edges

Worth absorbing into ALL substrate modules, not just codemap:

| Tag | Meaning | Example use |
|---|---|---|
| `EXTRACTED` | Deterministic fact from source. Confidence 1.0. | Decision `supersedes:` cross-ref read from frontmatter |
| `INFERRED` | LLM-derived from prose. Variable confidence 0.0–1.0. | "This decision implements the intent of OQ-COPS-008" derived from prose similarity |
| `AMBIGUOUS` | Flagged for human review. Confidence withheld. | Two decisions appear to contradict — operator resolves |

Apply to: decision dependency graphs, glossary term relationships, codemap edges, incident-to-decision links.

This makes substrate hygiene auditable. `/acw-instance audit` can report "N edges are AMBIGUOUS — please review" instead of silently mixing facts and inferences.

## Skill-level implications

Skills need to read `profile` and `modules` from `acw-state.yaml` before acting on substrate. Patterns:

```python
state = load_acw_state()
if "glossary" not in state.modules:
    return  # this instance doesn't use glossary; skip
glossary_path = state.paths.glossary_index
```

Skills that currently assume every substrate module is present need a guard pass.

## Open questions for the canonical to resolve

1. **Where does the `profile:` enum live?** In `acw-state.yaml` itself (flexible, per-instance), or in `rules/instance-current-manifest.md` (canonical-controlled enum)? Recommendation: declare in `acw-state.yaml`, validate against a canonical enum in `rules/instance-types.md` (new rule file).

2. **`custom` profile escape hatch — how strict?** If an instance declares `profile: custom`, does `/acw-instance audit` skip module-expectation checks entirely, or still validate module-internal contracts? Recommendation: skip cross-module expectations, still validate within each declared module.

3. **Backward compat for instances without `profile:` declared.** Default to `spec-project` (closest to current canonical shape) and emit a warning prompting the operator to declare explicitly.

4. **Codemap implementation — adopt Graphify directly or reimplement?** Graphify is MIT-licensed and Python-based. Could be wrapped as an ACW skill (`/codemap rebuild`) that runs Graphify and routes output to `.acw/codemap/`. Recommendation: wrap, don't reimplement. Graphify's edge-tagging and community-detection logic is the load-bearing part; don't reinvent it.

5. **Codemap freshness trigger.** Pre-commit hook (cs-atlas style), post-commit hook, scheduled rebuild, or operator-on-demand? Recommendation: pre-commit for AST stage (cheap, deterministic, must-pass-before-push); on-demand for LLM stage (operator decides when to refresh semantic layer).

## Migration cost across existing instances

Low-to-medium per instance:

- **synapse:** Adopt `profile: org-brain`. Declare all currently-used modules. No structural changes.
- **cs-ops-spec:** Adopt `profile: spec-project`. Declare current modules. No structural changes (already migrated to `.acw/` per companion proposal).
- **cs-atlas:** Adopt `profile: coding-project`. Add `codemap/` module (initial build); add codemap to declared modules. Light structural work.
- **gsg-cs-chatbot (future):** Born as `coding-project` from day one. Codemap from first commit.
- **frank-context:** Adopt `profile: spec-project`. Declare current modules.

Canonical absorption effort is the heavy lift: enum definition, skill audit for module-aware reads, default profile resolution, codemap skill wrapper.

## Cross-references

- Companion proposal: `2026-05-21-absorption-acw-substrate-under-dotfolder.md` (the `.acw/` dotfolder convention). This proposal extends that one and shares its review timeline.
- Influence: Graphify — https://graphify.net (codebase knowledge graph)
- Influence: `synapse/Rules/Procedures/enrichment-vs-memory.md` — the principle that makes the codemap shape coherent with the rest of ACW substrate.
- Influence: D-COPS-035 (`.acw/` decision in cs-ops-spec), D-CATL-001 (`.acw/` decision in cs-atlas).

## Status

Pending review by ACW canonical operator (Ben). Filed to `~/projects/acw/_buffer/` per ACW's `/exfil`-equivalent routing. To be reviewed alongside the companion `.acw/` dotfolder proposal.
