---
scope: end
---

# Metabolize Report Format

Appended to the new session's `paths.build_log` entry under a `### Metabolize report` subheading.

> **Path resolution.** `paths.X` and `section_conventions.X` resolve at runtime per the SKILL.md preamble. In wiki mode, references to `paths.decisions_log::section_conventions.X` become per-subdir operations (entries/, open-questions/, constraints/) — the report line still names the logical operation; the literal location string reflects the active substrate mode.

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

Single-file mode example:
```
**Auto-updated** (executed):
- paths.tasks_status::Pending — removed "Build pipeline/copilot.py"; dated session block written to tasks-status-YYYY-Q*.md archive (file exists at the named path; completion signal: artifact callable + referenced from README)
- paths.decisions_log::section_conventions.open_questions — OQ-001 resolved by new D-003; moved to Decisions section
```

Wiki mode example:
```
**Auto-updated** (executed):
- paths.tasks_status::Pending — removed "Build pipeline/copilot.py"; dated session block written to tasks-status-YYYY-Q*.md archive
- decisions/open-questions/OQ-001-*.md → decisions/entries/OQ-001-*.md — resolved by new D-003; status: resolved; INDEX regenerated
```

### Proposed for operator review

Single-file mode example:
```
**Proposed for operator review** (not executed):
- paths.glossary — propose deprecation of "<legacy term>" — recommend hold (term still relevant for understanding legacy code)
- paths.decisions_log::section_conventions.constraints — propose removing C-002 — recommend hold (constraint still active)
```

Wiki mode example:
```
**Proposed for operator review** (not executed):
- glossary/entries/<legacy-term>.md — propose status: deprecated — recommend hold (term still relevant)
- decisions/constraints/CG-002-*.md — propose status: resolved — recommend hold (constraint still active)
```

### Skipped

```
**Skipped** (intentionally not touched):
- paths.build_log past entries — append-only history
- paths.session_captures_dir/* — frozen once written
- project source directories — out of scope (own governance)
- decisions past entries (regardless of mode) — never edited; supersession by new entry only
```

## When everything was clean

If nothing changed, all three subsections are `(none)` and the entry stands as proof that the metabolize pass ran and found no drift. This is itself valuable signal.

## When the report is long

If the report exceeds ~50 lines, it indicates the project has accumulated significant drift and the operator should review more carefully. Add a note at the top: `**NOTE:** Large metabolize delta this session — review proposed actions carefully before approving.`
