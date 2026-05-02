# Metabolize Report Format

Appended to the new session's `paths.build_log` entry under a `### Metabolize report` subheading.

> **Path resolution.** `paths.X` and `section_conventions.X` resolve at runtime per the SKILL.md preamble.

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
- paths.tasks_status::section_conventions.pending — moved "Build pipeline/copilot.py" to the new Done block — file exists at the named path and is referenced from the README
- paths.decisions_log::section_conventions.open_questions — OQ-001 resolved by new D-003; moved to Decisions section
- paths.decisions_log::section_conventions.open_questions — OQ-002 resolved by new D-004; moved to Decisions section
```

### Proposed for operator review

```
**Proposed for operator review** (not executed):
- paths.glossary — propose deprecation of "<legacy term>" (no longer load-bearing) — recommend hold (term still relevant for understanding legacy code)
- paths.decisions_log::section_conventions.constraints — propose removing C-002 — recommend hold (constraint still active)
- runbooks/<file>.md — references legacy terminology — recommend approve (update to current terms)
```

### Skipped

```
**Skipped** (intentionally not touched):
- paths.build_log past entries — append-only history
- paths.session_captures_dir/* — frozen once written
- project source directories — out of scope (own governance)
- paths.decisions_log::section_conventions.decisions past entries — past decisions never edited
```

## When everything was clean

If nothing changed, all three subsections are `(none)` and the entry stands as proof that the metabolize pass ran and found no drift. This is itself valuable signal.

## When the report is long

If the report exceeds ~50 lines, it indicates the project has accumulated significant drift and the operator should review more carefully. Add a note at the top: `**NOTE:** Large metabolize delta this session — review proposed actions carefully before approving.`
