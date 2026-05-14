---
class: buffer
authority: handoff
stability: in-progress
date: 2026-05-13
from_instance: cops
to_instance: acw
kind: incident-candidate
severity: low
read: false
---

# `/acw-session start` reads full instance-current-manifest.md even when no drift is possible

**Summary:** The drift-check step (Step 5 of `references/start.md`) reads `rules/instance-current-manifest.md` in full and walks every entry. When `acw-state.yaml::last_reconciled_version == ACW current version`, every entry's earned-in version is at-or-before `last_reconciled_version` by definition, so the walk is guaranteed to produce zero gaps. The full read (~390 lines, ~10–12k tokens in the cops instance) is wasted context.

## Observed

- Instance: cops (cs-ops-spec)
- ACW version: 0.9.8
- `last_reconciled_version`: 0.9.8
- Outcome: full file read, drift walk ran, zero gaps surfaced (correctly), ~10–12k tokens consumed in Messages bucket for no informational gain.

## Proposed fix (for ACW canon to consider)

Add a short-circuit at the top of Step 5 in `skills/acw-session/references/start.md`:

> If `last_reconciled_version` equals current ACW version (read from a known surface — `acw-state.yaml::version` of the canonical publisher, or a constant in the skill), skip the manifest read entirely and emit "no drift" silently.

Alternative: read only the file's frontmatter + entry version-headings (cheap scan) and only load full entry bodies when an entry's earned-in version > `last_reconciled_version`.

Either path eliminates the redundant load for the common case (instance recently reconciled).

## Why this is buffer-worthy, not a local-only fix

The skill ships from ACW canonical. A local edit on cops would drift from upstream and get overwritten on next `/acw-instance upgrade`. The fix belongs in the canonical skill.

## Severity

Low. ~10k tokens per session-start is real cost at scale (across all instances × all session starts) but no correctness impact and no operator-visible failure. Earn-by-incident threshold is med/3-count; logging here as a single low-severity candidate awaiting either a second incident or operator judgment to escalate.

## Provenance

- Surfaced by operator question during cops session 2026-05-13.
- No ACW-side incident filed yet; this buffer note is the handoff.
