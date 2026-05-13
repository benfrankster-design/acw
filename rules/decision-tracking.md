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

## Rolling-window discipline

`decisions/decision-log.md` is auto-loaded at session start (per `acw-state.yaml::auto_load_at_session_start` and `rules/auto-load-discipline.md`). Inline entries cost context every chat, every agent, every workspace where the file is loaded. To keep the file lean:

- **Cadence: weekly.** Entries dated more than 7 days old are candidates for archive on the next maintenance pass. The cadence is a maintenance schedule, not a strict freshness boundary — older entries don't auto-archive the moment they age out. Operator (or `/acw-session end`) makes the archive call when the schedule fires or when the threshold trigger fires, whichever comes first.
- **Threshold trigger.** If the live file exceeds ~15k tokens before the weekly cadence fires, archive aggressively (as many entries as needed to bring the file back under threshold) regardless of entry dates. The threshold is the secondary fire condition declared in `rules/auto-load-discipline.md`.
- **Archive file pattern.** `decisions/decision-log-YYYY-Q*.md` (e.g. `decision-log-2026-Q2.md`). Lives alongside the live file in `decisions/`. Frontmatter: `class: archive, authority: derived, stability: stable, loaded_by_agent: no`. Classified `meta_layer` in `acw-state.yaml` (about this instance's history, not propagated to children).
- **What archives: entries from "Decisions and Rationale" only.** Open Questions, Constraints and Gotchas, and Resolved Questions sections do not archive. They're active surfaces, not historical narrative — Open Questions track unresolved work, Constraints track active gotchas to remember, Resolved Questions are the operator's "we already checked" file. All three benefit from staying inline.
- **Pointer line in the live file.** Replace the archived block with one italicized line: *"(Entries D-XXX through D-YYY, dated YYYY-MM-DD to YYYY-MM-DD, archived to `decisions/decision-log-YYYY-Q*.md` per the weekly rolling-window discipline in `rules/decision-tracking.md`.)"*
- **Append, don't replace within quarter.** Multiple weekly archive runs in the same quarter append to the same `decision-log-YYYY-Q*.md`. New quarter → new file.
- **Wiki mode (`decision_tracking.mode: wiki`) does NOT use rolling-window archives.** Each entry is already its own file in `decisions/entries/`; auto-load surface is `decisions/INDEX.md` (a thin index, not the bodies). The rolling-window discipline applies only to single-file mode.
- **Single-file → wiki migration re-splits historical archives.** When an instance migrates from single-file to wiki mode, every pre-existing quarterly archive (`decisions/decision-log-YYYY-Q*.md`) is split into per-entry wiki files in `decisions/entries/`, and the archive file is deleted. The migration tool `tools/migrate_to_wiki.py --archive=<path>` performs this. Doctrine: in wiki mode, ALL decisions live in `decisions/entries/` with no exceptions. The auto-load surface (INDEX) sorts by date descending; cold pre-migration entries naturally fall to the bottom — they don't clutter, they're at the end of a sorted list. Earned-by-incident: the prior "archives stay archived" doctrine (D-ACW-043 expedient) made the wiki promise conditional and required readers to learn an exception. Retired in v0.9.6.

Archival is operator-driven; `/acw-session end` may propose archive when the cadence or threshold fires, but the move is not automatic.

This discipline mirrors the rolling-window pattern in `rules/task-tracking.md` for single-file mode (weekly cadence + threshold). Tasks-status archive shape diverges in v0.9.5+ (`archives/tasks-status/YYYY-MM.md`, monthly file) because tasks-status carries no equivalent of wiki-mode-per-entry-file relief.

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
