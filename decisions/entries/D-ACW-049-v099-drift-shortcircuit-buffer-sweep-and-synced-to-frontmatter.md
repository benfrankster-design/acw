---
class: operational
authority: canonical
stability: stable
loaded_by_agent: no
date: 2026-05-13
status: accepted
id: D-ACW-049
version: 0.9.9
title: "v0.9.9: drift-walk short-circuit + buffer-sweep convention + synced_to: frontmatter on instance-current-manifest"
kind: decision
updated: 2026-05-13
---

# D-ACW-049 — v0.9.9: drift-walk short-circuit + buffer-sweep convention + `synced_to:` frontmatter on instance-current-manifest

## Context

`/acw-session start` Step 5 walked the full body of `rules/instance-current-manifest.md` (~390 lines, ~10–12k tokens) on every session start to detect drift. cs-ops-spec (cops) flagged this as wasted context in a `_buffer/` note: when `acw-state.yaml::last_reconciled_version == ACW current version`, every entry's earned-in version is at-or-before reconciled by definition, so the walk is structurally guaranteed to surface zero gaps.

The deeper observation: `/acw-instance upgrade` writes the local manifest cache and bumps `last_reconciled_version` atomically. In normal operation those surfaces never disagree — the drift walk is dead code outside of broken-upgrade or manual-edit edge cases.

Separately, `_buffer/` notes had no lifecycle close. Operators acting on a note had to manually move it to `_read/`, which bit-rotted: cops's note from this morning was still sitting in `_buffer/` after ACW agents had read it multiple times. The folder accumulated "this was already handled" cruft.

## Decision

Three coupled changes ship as v0.9.9:

1. **Drift-walk short-circuit.** `/acw-session start` Step 5 reads only the manifest's frontmatter (cheap, ~10 lines). When `synced_to == acw-state.yaml::last_reconciled_version`, skip the walk and emit "no drift" silently. Fall through to the full walk only when `synced_to` is absent or mismatches.

2. **Buffer-sweep convention.** Capture file gains a `## Buffer notes acted on` section listing source filenames the operator (or agent) acted on this session. `/acw-session end` Phase 2 append-only subset reads that section and moves each listed file from `_buffer/` to `_buffer/_read/`. Closes the lifecycle of cross-instance notes.

3. **`synced_to:` frontmatter on `rules/instance-current-manifest.md`.** A string field in the manifest cache's frontmatter declaring which ACW version the cache snapshot represents. Written by `/acw-instance upgrade` whenever it overwrites the file. Read by the start verb's short-circuit. Hardens the correctness signal from a file-mtime heuristic (v0.9.8 mid-session patch attempt) to an explicit version stamp that survives `git pull`, file syncs, and workspace copies.

Bump `acw-state.yaml::version`, `last_reconciled_version`, and manifest `synced_to:` to `0.9.9` together.

## Rationale

- **Short-circuit is structural, not optimization.** The drift walk is dead code in normal operation; making it free is a correctness clarification, not a perf hack. Saves ~10k tokens per session start across every reconciled instance.
- **`synced_to:` over mtime.** File timestamps lie — `git pull` resets them, sync clients shuffle them, workspace copies destroy them. Explicit version stamp written by upgrade is bulletproof.
- **Buffer sweep formalizes a convention that already existed in prose.** start.md Step 4 always said "operator decides per file: act on it, archive (move to `_read/`), or ignore." The sweep automates the move when the operator chose "act on it" and the work landed.
- **All three changes ship together** because they're conceptually one shift: tighten the contract between `/acw-instance upgrade`, `/acw-session start`, and `_buffer/` lifecycle so the cheap path is always available.

## Rejected alternatives

- **Mtime heuristic alone.** Tested mid-session as the v0.9.8 patch shape. Operator flagged the brittleness immediately. `synced_to:` is the right primitive.
- **Drop the drift walk entirely.** Considered. Rejected because the broken-upgrade and manual-edit cases are real; the full walk as a fallback for the failure cases is cheap insurance.
- **Per-buffer-note `read: true` flag toggled by the agent.** Rejected as redundant — the capture file's `## Buffer notes acted on` section is the same information, lives where the rest of the session record lives, and naturally tracks "acted on in THIS session" rather than ambient state.

## Consequences

- `acw-state.yaml::version` bumped to 0.9.9; `last_reconciled_version` to 0.9.9.
- `rules/instance-current-manifest.md` carries `synced_to: "0.9.9"` in frontmatter; new registry entry documents the field's contract; header paragraph explains the start-verb integration.
- `skills/acw-session/references/start.md` Step 5 short-circuits on `synced_to == last_reconciled_version`; Step 4 documents the acted-on tracking convention.
- `skills/acw-session/references/end.md` Phase 2 append-only subset gains a "Buffer sweep" line item.
- `skills/acw-instance/references/upgrade.md` refresh-canonical-cache step writes `synced_to:` after overwriting the file.
- Pre-v0.9.9 instances (anything that hasn't run upgrade since this ship): `synced_to:` absent, short-circuit falls through to the full walk. Functionally identical to pre-v0.9.9 behavior. Field lands automatically on next `/acw-instance upgrade`.
- Downstream instances queued for v0.9.9 reconciliation on their next `/acw-instance upgrade`.

## Source

cops `_buffer/` note (2026-05-13), operator directive (in-session). Manually moved cops note to `_buffer/_read/` to dogfood the new sweep convention.
