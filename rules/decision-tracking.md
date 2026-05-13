---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# Decision Tracking — ADR-lite

**Version:** 0.1.0
**Status:** Normative. Any decision that affects downstream behavior, governance, or the deferred library promotion state MUST be recorded.

---

## When this applies

Any decision whose reversal would require work, coordination, or explanation.

### Applies to:
- Terminology choices (canon entries, forbidden synonyms, domain boundaries)
- Role assignments for non-obvious skills
- Promotion of a deferred primitive
- Instance hard-rule additions or removals
- Schema changes to `rules/canon-schema.yaml`
- Cross-domain concept merges or splits

### Does not apply to:
- Typos, formatting fixes
- Trivial bug patches
- Single-session task state

---

## The format

**Wiki mode is canonical (v0.9.8+, D-ACW-048).** Every decision, open question, and constraint is its own file. Single-file mode is retired; ACW does not support it as a sanctioned shape.

Layout:

```
decisions/
  INDEX.md                           # auto-loaded thin index
  entries/D-<CODE>-NNN-<slug>.md     # one file per decision
  open-questions/Q-NNN-<slug>.md     # one file per open question
  constraints/C-NNN-<slug>.md        # one file per constraint
```

The scaffolder ships `decisions/INDEX.md` with empty sections plus the three empty subdirectories. Regenerate INDEX with `python tools/migrate_to_wiki.py`. The same shape applies to `glossary/` (INDEX + `entries/<slug>.md`).

### Required entry frontmatter (per file):

```yaml
---
id: D-<CODE>-NNN          # or Q-NNN, C-NNN
title: <short title>
date: YYYY-MM-DD
status: proposed | accepted | superseded | deprecated | rejected | open | partial-resolved | resolved
kind: decision | open-question | constraint
updated: YYYY-MM-DD
approval_authority: operator | <any declared authority in instance-hard-rules.md>
superseded_by: D-<CODE>-NNN   # optional
---
```

Canonical enum values live in `acw-state.yaml::decision_tracking.status_values` and `kind_values`.

### Required body sections (per entry):

1. **Context** — one to three paragraphs describing what prompted the decision. What was tried, what failed, what pressure forced the choice.
2. **Decision** — one sentence stating what was decided. No hedging.
3. **Rationale** — why this choice over the alternatives that were considered.
4. **Rejected alternatives** — brief description of other options considered and why they were not chosen.
5. **Consequences** — what downstream work this enables, blocks, or forces.

---

## Why ADR-lite rather than full ADRs

Full Architecture Decision Records (Nygard 2011) prescribe a more elaborate structure including status transitions, related decisions, and formal review. At the scale a single-operator instance operates, the overhead crowds out the recording. ADR-lite keeps the core load-bearing elements (context, decision, rationale, rejected alternatives, consequences) and drops the ceremony.

When an instance grows beyond a single operator, upgrading to full ADRs is a promotion candidate. See `rules/promotion-ritual.md`.

---

## Integration with other rules

### With `rules/canon-governance.md`:
Canon approval workflow operates on top of decision tracking. A canon entry moving from `proposed` to `approved` status creates a decision record in the appropriate approval bucket. The decision record is the audit trail the canon governance relies on.

### With `DEFERRED.md`:
Promoting a deferred primitive requires a decision record. The promotion ritual in `rules/promotion-ritual.md` prescribes the shape.

### With `rules/instance-hard-rules.md`:
Adding or removing a hard rule requires a decision record. Hard rules are intentionally difficult to modify; the friction is the point.

---

## Review and maintenance

Decision records are append-only in spirit but not strictly immutable. A decision whose context has materially changed can be marked `superseded` and pointed at a later decision. The original is not deleted. Git history preserves the sequence.

Periodic review is the operator's job. A session where the operator reads through recent decisions is a cheap way to catch drift between intent and practice.

## Auto-load surface

Only `decisions/INDEX.md` is auto-loaded at session start (per `acw-state.yaml::auto_load_at_session_start` and `rules/auto-load-discipline.md`). The index is a thin pointer to entries; bodies in `entries/`, `open-questions/`, and `constraints/` load on demand.

Wiki mode does not use rolling-window archives. Each entry is already its own file. INDEX sorts entries by date descending; cold entries naturally fall to the bottom of a sorted list. No archive shuffling required.

Historical archives from pre-v0.9.6 single-file instances (`decisions/decision-log-YYYY-Q*.md`) are migrated to per-entry wiki files via `python tools/migrate_to_wiki.py --archive=<path>` when an instance adopts wiki mode through `/acw-instance upgrade`. After migration, no archive files remain.

---

## What this file does NOT do

- It does not prescribe a review meeting or a voting process.
- It does not define how decisions are contested.
- It does not gate commits.
- It does not integrate with any external issue tracker or board.

All of those are optional extensions the operator adds when the instance grows to a scale that requires them.

---

## Changelog

- **v0.1.0 — 2026-04-11** — Initial release. ADR-lite format with five required body sections.
