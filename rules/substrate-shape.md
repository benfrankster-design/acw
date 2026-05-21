---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Substrate shape

Canonical guidance for choosing the file shape of each substrate module. Three shapes are recognized: **wiki**, **flat**, and **transient**. The choice is per-module, not per-instance — substrate modules have inherent shapes that don't change across the instances that adopt them.

## The three shapes

### Wiki shape

One file per entry. Frontmatter-typed. Bodies are prose. INDEX.md is a thin, auto-loaded navigable map; bodies load on demand.

```
.acw/<module>/
├── INDEX.md
├── entries/
│   ├── ENTRY-NNN-slug.md
│   └── ...
├── (open-questions/, constraints/, etc. as sub-collections if applicable)
```

Modeled on the Karpathy LLM-wiki pattern: every entry is a discoverable, persistent, cross-referenced page. The wiki is what the LLM navigates; the INDEX is what auto-loads at session start.

### Flat shape

Single file. Sectioned by convention. Continuously edited or appended.

```
.acw/<module>.md   (or .acw/<module>.jsonl for structured logs)
```

The file IS the substrate. No INDEX, no sub-files. Auto-loaded if small and load-bearing.

### Transient shape

Folder of files awaiting routing or metabolization. Contents are by definition not load-bearing as substrate — they're inputs to metabolize step that produces enriched substrate elsewhere.

```
.acw/raw/             (formerly _buffer/)
.acw/inbox/
.acw/deferred/
```

Not auto-loaded. Surfaced at session start as a "raw inputs awaiting routing" pointer, not as load-bearing content.

## Selection criteria

Apply three tests per module:

1. **Are entries discrete and named?** (Decision = yes. Build-log narrative arc = no.)
2. **Are entries persistent past the session that created them?** (Glossary term = yes. Task = no, it moves states.)
3. **Are there enough entries that an INDEX earns its weight?** (Decisions at 35+ = yes. A single-page log = no.)

All three yeses → **wiki**.
Discrete + persistent but small count → **wiki** when entries are referenced from outside the module, **flat** when they're internal-only.
Continuous narrative or dashboard → **flat**.
Routing-stage content → **transient**.

## Module shape assignments

Canonical per-module shape. Instances inherit these and should not deviate.

| Module | Shape | Rationale |
|---|---|---|
| `decisions` | **wiki** | Many entries, each load-bearing, dense cross-references. Sub-collections: `entries/`, `open-questions/`, `constraints/`. |
| `glossary` | **wiki** | Many terms, cross-references between them, each persistent. |
| `sessions` | **wiki** | One file per session. Each persists as a discoverable artifact. Add INDEX once count exceeds ~20 captures. |
| `plans` | **wiki** | Each plan is a discrete document. INDEX justified once multiple plans exist. |
| `research` artifacts | **wiki** | Each research artifact is a discrete dated document. |
| `briefings` | **wiki** when persistent reference; **transient** during routing phase. Per-instance call. |
| `runbooks` | **wiki** | Each runbook is a discrete, persistent procedure document. |
| `tasks-status` | **flat** | Dashboard of Pending / Done / Parked. Tasks move states; wiki-shape creates churn. |
| `build-log` | **flat** | Narrative arc, append-only. Fragmenting kills the story. |
| `incidents` | **flat** (`.jsonl`) | Structured append-only log. Queryable as JSONL in ways markdown isn't. |
| `DEFERRED.md` | **flat** | Append-only deferred items list. |
| `CHANGELOG.md` | **flat** | Append-only version history. |
| `codemap` | **flat** (with sidecar JSON) | `GRAPH_REPORT.md` is the auto-loaded report; `nodes.json` + `edges.json` are backing storage. |
| `raw` | **transient** | Unmetabolized inputs awaiting routing. |
| `inbox` | **transient** | Inbound routing-stage content. |
| `deferred` | **transient** view (derived from `DEFERRED.md`). |
| `archives` | **transient**-archive (read-only after archival). |

## Why this is canonical, not per-instance

Shape choice is a property of the *kind* of content, not the *project domain*. A glossary entry in synapse is the same shape as a glossary entry in cs-ops-spec — both are discrete named persistent terms. Allowing per-instance shape deviation would fragment the substrate convention and break cross-instance tooling.

The instance-level choice is **which modules to adopt** (per `rules/instance-types.md`), not what shape they take.

## Wiki shape mechanics

For modules in wiki shape:

1. Each entry lives at `.acw/<module>/<sub-collection>/<ID>-<slug>.md`.
2. Each entry has frontmatter declaring `id`, `title`, `date`, `kind`, `status`, plus module-specific fields.
3. INDEX.md at `.acw/<module>/INDEX.md` is the thin auto-loaded surface. Format: bulleted list of entries with status annotations.
4. INDEX.md is regenerable from entries (via `tools/build_indexes.py` or skill equivalent). Manual edits to INDEX are an anti-pattern — edit entries, regenerate.
5. Cross-references between entries use canonical IDs, not file paths.

## Flat shape mechanics

For modules in flat shape:

1. The file IS the module. No sub-files.
2. If sectioned (tasks-status has Pending/Done/Parked), section names are declared in the file's frontmatter under `section_conventions:` so skills can read them programmatically.
3. JSONL logs have one record per line, schema declared in the corresponding `rules/*.md` file.

## When to promote flat → wiki

Sometimes a flat module grows large enough to deserve wiki treatment. Triggers:

- File exceeds ~1500 lines and is hard to navigate.
- Operators are routinely asking "where's the entry about X" inside the flat file.
- Cross-references into the flat module from outside need stable anchors.
- Audit reveals the flat file is hiding entries that should be discrete.

Promotion is a major-version bump and requires a migration decision-log entry.

## When to demote wiki → flat

Rare. Justified only when:

- Wiki module has fewer than ~5 entries and is unlikely to grow.
- Cross-references into the module are negligible.
- INDEX.md is paying more overhead than it saves.

Don't preemptively demote. Wiki shape is the default for discrete-entry content; demotion needs strong evidence.
