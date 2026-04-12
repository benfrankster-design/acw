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

All decisions live in a single file at `decisions/decision-log.md`, organized into four top-level sections: Open Questions, Decisions and Rationale, Constraints and Gotchas, and Resolved Questions. The template ships this file scaffolded with the four section headings and no entries.

When the log grows too large to navigate as a single file, the operator splits it into four separate files (`open-questions.md`, `decisions-and-rationale.md`, `constraints-and-gotchas.md`, `resolved-questions.md`) via the promotion ritual in `rules/promotion-ritual.md`. The split is earned by operational friction, not scheduled.

### Required entry frontmatter (within the log, per entry):

```yaml
id: YYYY-MM-DD-short-slug
date: YYYY-MM-DD
status: proposed | accepted | superseded | deprecated
approval_authority: operator | <any declared authority in instance-hard-rules.md>
superseded_by: (id of later decision, if applicable)
```

### Required body sections (per entry):

1. **Context** — one to three paragraphs describing what prompted the decision. What was tried, what failed, what pressure forced the choice.
2. **Decision** — one sentence stating what was decided. No hedging.
3. **Rationale** — why this choice over the alternatives that were considered.
4. **Rejected alternatives** — brief description of other options considered and why they were not chosen.
5. **Consequences** — what downstream work this enables, blocks, or forces.

Entries are separated by horizontal rules (`---`) within the log file.

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
