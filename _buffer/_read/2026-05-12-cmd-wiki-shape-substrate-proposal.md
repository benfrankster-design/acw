---
from_instance: _Command
date: 2026-05-12
proposing: wiki-shape substrate for decisions + glossary (alternative to canonical single-file mode)
related: D-CMD-025 (in _Command/decisions/entries/)
read: true
absorbed_in: decisions/decision-log.md::D-ACW-043 (superseded by 2026-05-12 comprehensive proposal; wiki-shape Path B absorbed)
status: absorbed
---

# Absorption Proposal — Wiki-shape decisions + glossary

## What changed in _Command

Migrated `decisions/decision-log.md` (monolithic, 28KB) and `glossary.md` (monolithic, 16KB) into atomic per-entry Karpathy-wiki shape:

```
decisions/
  INDEX.md                                # auto-loaded; ~3.5KB
  entries/D-CMD-NNN-slug.md               # one decision per file
  open-questions/OQ-NNN-slug.md
  constraints/CG-NNN-slug.md
  decision-log-YYYY-Q*.md                 # archive untouched
glossary/
  INDEX.md                                # auto-loaded; ~2.6KB
  entries/<slug>.md                       # one term per file
```

Auto-load swap in `acw-state.yaml::auto_load_at_session_start`: monolithic files → INDEX files. CLAUDE.md `@-imports` mirrored. `acw-state.yaml::decision_tracking.mode` set to `wiki` with new fields (`index`, `entries_dir`, `open_questions_dir`, `constraints_dir`, `archive_pattern`, frontmatter schema, status/kind enums).

Net auto-load savings: ~38KB per session-start in _Command.

Full decision rationale: see `_Command/decisions/entries/D-CMD-025-substrate-migrated-to-karpathy-wiki-shape.md`.

## Why ACW should consider absorbing this upstream

1. **The motivating problem isn't cockpit-specific.** Any ACW instance whose auto-loaded decision-log grows past ~15-20KB will hit the same "Prompt is too long" symptom that triggered both D-CMD-024 (rolling-window archive tightening) and D-CMD-025 (this migration). Rolling-window archiving treats symptoms; shape change addresses the root: a monolithic narrative ledger is the wrong primitive for auto-loaded substrate. The enrichment principle (D-CMD-015, codified at `synapse/Rules/Procedures/enrichment-vs-memory.md`) makes this explicit — INDEX is the dense surface, bodies are the substrate, raw chronology dissolves.

2. **Industry canon is settled atomic.** Every authoritative 2025-2026 ADR source (Nygard, MADR 4.0.0, adr-tools, log4brains, AWS Prescriptive Guidance, Azure Well-Architected, joelparkerhenderson, Structured MADR 1.0 [2026-01-15]) assumes one decision per file. None endorse a monolithic log. ACW's current `decision_tracking.mode: single-file` is at odds with where the broader practice has converged. Research artifact: `Cortex/Resources/research/2026-05-12--decision-log-as-llm-wiki-synthesis.md` (62 sources).

3. **Agent retrieval works better against atomic.** Convergent across 2025-2026 sources: markdown heading-aware chunking (+5-10pp on retrieval per Snowflake finance RAG study); Vectara/NAACL 2025 "context cliff" at ~2,500 tokens (monolithic logs blow past routinely); supersedes-as-graph-edge (Graphiti, AgenticAKM) outperforms supersedes-as-string-field. For ACW instances exposing decisions to consumer agents, atomic is the better retrieval target.

4. **MADR 4.0.0 is a stable, well-documented frontmatter standard.** ACW could adopt or reference it directly: `status | date | decision-makers | consulted | informed`. Structured MADR 1.0 extends with `tags | related | supersedes | superseded_by` for machine-readable navigation. Either is a closer fit for ACW's frontmatter-discipline pattern than the current bespoke header style.

## Proposed canonical shape (for ACW review)

Two paths forward, both worth weighing:

### Path A — Make wiki the new canonical default

`decision_tracking.mode: wiki` becomes the canonical default. `single-file` remains as an opt-in for tiny instances (≤ ~10 entries) that don't justify the index overhead. Existing instances on `single-file` migrate at upgrade time via an `/acw-instance upgrade` step that runs the equivalent of `_Command/tools/migrate_to_wiki.py`.

Pros: ends the auto-load-bloat root cause across all instances; matches industry canon; agent-retrieval-friendly.
Cons: structural change touching most instances; needs a migration runbook in canonical docs.

### Path B — Add wiki as a sanctioned variant

Keep `single-file` as default. Document `wiki` as a second sanctioned mode in `rules/decision-tracking.md`. Instances opt into wiki by setting `decision_tracking.mode: wiki` and pointing to entries dir, index, archive pattern, etc.

Pros: smaller blast radius; lets instances grow into wiki shape as they earn the size; no forced migration.
Cons: split convention may produce drift between instances; auto-load-bloat keeps recurring as the implicit default.

**_Command's lean:** Path A is the cleaner long-term answer. The single-file mode produces the exact failure mode (auto-load bloat) that the enrichment principle was named to prevent. Keeping it as default invites every instance to repeat the same migration in 6-18 months. But Path B is the lower-risk first step — canonicalize wiki as a sanctioned mode now; revisit defaulting later when more instances have adopted.

## What _Command did concretely (reference implementation)

Frontmatter schema landed in `_Command/decisions/entries/`:

```yaml
---
id: D-CMD-NNN
title: "..."
date: YYYY-MM-DD
status: accepted        # proposed | accepted | superseded | deprecated | rejected | open | partial-resolved | resolved
kind: decision          # decision | open-question | constraint
tags: [...]             # optional
related: [...]          # optional
supersedes: null
superseded_by: null
updated: YYYY-MM-DD
---
```

Migration script: `_Command/tools/migrate_to_wiki.py` (idempotent INDEX regeneration; one-shot parse + emit for the initial split from monolithic). Operates by hardcoded ROOT — needs generalization (CLI arg or env var) before it could ship as canonical tooling.

Living-document mutability chosen over strict-immutable-supersede-only. Git is the audit trail. Supersession reserved for genuine reversal, not corrections. This is a deliberate divergence from AWS/MADR canon; matches single-operator operating reality.

Companion migrations in same session (less load-bearing, surface as datapoints):
- `glossary.md` → `glossary/INDEX.md` + `glossary/entries/<slug>.md` (31 terms)
- `context/contacts/INDEX.md` generated over already-wiki-shaped contact files
- `inbox/ideas/INDEX.md` generated over already-wiki-shaped idea files

## Open questions for ACW

1. **Frontmatter schema.** Adopt MADR 4.0.0 verbatim, or define an ACW-flavored extension? _Command picked a small extension (`kind`, `related`, `supersedes`, `superseded_by`, `updated`) but kept it close to MADR.
2. **Filename convention.** Legacy id in filename (`D-CMD-024-slug.md`) or MADR sequential (`0024-slug.md` + `aliases:` frontmatter)? _Command picked the former — zero-friction for in-flight cross-references. MADR canon prefers the latter.
3. **Mutability default.** Living-document with date-stamped amendments (_Command's choice; pragmatic for small instances) or strict-immutable-supersede-only (MADR/AWS canon; better for multi-author large corpora)? Canonical should probably ship as living-document with the strict variant as opt-in.
4. **INDEX regeneration trigger.** Manual via script today. Worth a hook? Probably not until a second instance adopts and the regen friction earns its mention in incidents.jsonl.
5. **Migration runbook.** If Path A: needs a `/acw-instance upgrade` step. If Path B: needs documentation in `rules/decision-tracking.md` for instances that opt in.

## Receipts

- `_Command/decisions/entries/D-CMD-025-substrate-migrated-to-karpathy-wiki-shape.md` — full decision in the new shape (dogfood gate).
- `_Command/decisions/INDEX.md` — example INDEX.
- `_Command/tools/migrate_to_wiki.py` — reference migration script.
- `_Command/acw-state.yaml::decision_tracking` (lines 130-141) — wiki-mode config block.
- `Cortex/Resources/research/2026-05-12--decision-log-as-llm-wiki-synthesis.md` — 62-source research synthesis driving the decision.
- `Cortex/Resources/research/2026-05-12--atomic-per-decision-wiki-shapes.md` — companion sub-agent artifact (atomic-adoption strand).

ACW reviews on its own cadence; _Command will keep operating on the wiki shape regardless.
