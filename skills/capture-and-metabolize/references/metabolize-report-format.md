# Metabolize Report Format

Appended to the new session's `build-log.md` entry under a `### Metabolize report` subheading.

## Three subsections, always present

```
### Metabolize report

**Auto-updated** (executed):
- <file>:<location> — <action> — <why>

**Proposed for operator review** (not executed):
- <file>:<location> — <proposed action> — <why> — <recommend approve / hold>

**Skipped** (intentionally not touched):
- <file>:<location> — <reason for skipping>
```

If a subsection has no entries, write `(none)` underneath the heading. Do not omit subsections.

## Examples

### Auto-updated entries

```
**Auto-updated** (executed):
- tasks-status.md::Pending — moved "Build pipeline/copilot.py" to Done — file exists at pipeline/copilot.py and is referenced from README
- decisions/decision-log.md::Open Questions — OQ-001 resolved by new D-003; moved to Decisions section
- decisions/decision-log.md::Open Questions — OQ-002 resolved by new D-004; moved to Decisions section
```

### Proposed for operator review

```
**Proposed for operator review** (not executed):
- glossary.md — propose deprecation of "Front Agent" (legacy v0.4 term, no longer load-bearing in v0.5) — recommend hold (term still relevant for understanding legacy code)
- decisions/decision-log.md::Constraints — propose removing C-002 "Platform engineering is a real implementation dependency" — recommend hold (constraint still active)
- runbooks/phase-1-eval-seed.md — references Front Agent / Data Agent / Response Agent which are now legacy — recommend approve (update terminology to "unified copilot")
```

### Skipped

```
**Skipped** (intentionally not touched):
- build-log.md past entries — append-only history
- research/sessions/* — frozen once written
- pipeline/, tests/, wiki/, eval/rubrics/, eval/red-team/ — out of scope (own governance)
- decisions/decision-log.md::Decisions D-001 through D-004 — past decisions never edited
```

## When everything was clean

If nothing changed, all three subsections are `(none)` and the entry stands as proof that the metabolize pass ran and found no drift. This is itself valuable signal.

## When the report is long

If the report exceeds ~50 lines, it indicates the project has accumulated significant drift and the operator should review more carefully. Add a note at the top: `**NOTE:** Large metabolize delta this session — review proposed actions carefully before approving.`
