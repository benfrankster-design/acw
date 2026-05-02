---
name: upgrade-instance
description: >
  Reconciles an ACW instance with the current ACW recommended-blocks registry.
  Reads `rules/instance-current-manifest.md`, compares against this instance's
  `acw-state.yaml`, and walks the operator through adding any missing blocks
  one at a time (each with its canonical default; operator picks add-as-proposed,
  modify, or skip). After the pass, bumps `last_reconciled` and
  `last_reconciled_version` so the drift alert in /resume-session quiets down.

  Triggered by the operator running /upgrade-instance, typically after
  /resume-session surfaces a drift alert. Also valid to run on demand at any
  time. Never fires automatically.

  Produces edits to acw-state.yaml only — no other substrate changes. Logs a
  decision-log entry recording the reconciliation pass.
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# upgrade-instance

Walks the operator through reconciling instance state with the current ACW recommended-blocks registry. Closes the loop on the drift detection in `/resume-session`.

## Path resolution

This skill writes only to `acw-state.yaml` and to `paths.decisions_log` for the reconciliation entry. Both resolve at runtime per the bookend skills' path-resolution convention. The skill never hardcodes a path.

## Instructions

When invoked, execute the steps below in order. Operator confirmation is required at each block in Step 3.

### Step 1 — Read the registry and the instance state

1. Read `rules/instance-current-manifest.md`. Parse the recommended-blocks registry (each `## <block name>` heading is one entry, with What / Why it helps / Required / How to add / Earned in fields).
2. Read `acw-state.yaml`. Note `version`, `last_reconciled`, `last_reconciled_version`, and which recommended blocks are present (populated, present-but-empty, or absent).

### Step 2 — Build the gap list

For each entry in the registry:

- Compare its **earned in** version to `last_reconciled_version` (semantic-version comparison; rc-suffixes are pre-release, so `0.2.0-rc1 < 0.2.0-rc2 < 0.2.0`). If `last_reconciled_version` is absent in the state file, treat as `"0.0.0"`.
- If the entry's earned-in is at-or-before `last_reconciled_version`, skip — already reconciled.
- If the entry is absent from the state file, add to the gap list.
- If the entry is present-but-empty (`block: []` or `block: {}`), skip — deliberate opt-out.
- If the entry is present and populated (at least one entry/key), skip — the operator has customized this block. For dict blocks like `paths`, runtime `manifest.load` merges canonical defaults for absent keys, so a partial declaration is fully functional. The skill does NOT propose adding missing keys to a partial block; the operator's partial declaration is honored.
- If the entry is present but malformed (wrong shape — e.g., `paths` declared as a string instead of a dict, or a list block declared as a dict), STOP. Print an error naming the malformed block and direct the operator to fix `acw-state.yaml` by hand before re-running. Do not attempt to repair shape.

If the gap list is empty (and no malformed blocks), print `Instance is already current with ACW <version>. Nothing to reconcile.` and exit.

### Step 3 — Walk the operator through each gap

For each gap entry, present a structured prompt:

```
─────────────────────────────────────
Block: <name>
Earned in: <version>
Required: <yes / no — fallback behavior>

What: <one-paragraph description from the registry>
Why it helps: <one-paragraph rationale from the registry>

Proposed default content:
<canonical default block from the registry>

Options:
  [a] Add as proposed (write the default into your acw-state.yaml)
  [m] Modify before adding (operator provides the value to write)
  [s] Skip (do not add; this block stays absent on this pass)
─────────────────────────────────────
```

Wait for operator input. Process per choice:

- **`a`** — Use `tools/manifest.py::append` (or the equivalent in the runtime) to write the default block. For dict-shaped blocks with canonical defaults (`paths`), append each key. For list-shaped blocks with canonical defaults (`auto_load_at_session_start`), append each entry. **For blocks with no canonical default (`project`, where each instance picks its own `name` / `code` / `domain`), `[a]` is not valid — the skill must force the `[m]` path for that block, prompting for operator-supplied values.** If the registry entry's "How to add" section contains placeholders like `<human-readable name>`, treat the block as "no canonical default" and prompt for modify input.
- **`m`** — Prompt the operator for the value. Validate (well-formed yaml, correct shape per the registry's "How to add" section). If valid, write via `manifest.append`. If not valid, re-prompt.
- **`s`** — No write. Note this block as "skipped this pass" for the summary.

Move to the next gap. Repeat until all gaps processed.

### Step 4 — Bump `last_reconciled` and `last_reconciled_version`

After the gap pass:

1. Set `last_reconciled` to today's date (UTC, `YYYY-MM-DD`).
2. Set `last_reconciled_version` to the value of `acw-state.yaml::version` (the current ACW version this instance now reconciles to).

Use `manifest.append` (key/value upsert) for both fields if the manifest tooling supports top-level scalar fields, or fall back to a direct edit of `acw-state.yaml` if it doesn't. Either way, preserve all other content in the state file.

### Step 5 — Log a decision-log entry

Append a new entry to `paths.decisions_log` `section_conventions.decisions` recording the reconciliation. Format:

```markdown
### D-<CODE>-NNN — Instance reconciled to ACW <version>

**Date:** YYYY-MM-DD
**Decision:** Reconciled this instance to ACW recommended-blocks registry as of version <version>. <N> blocks added: <names>. <M> blocks skipped on this pass: <names>.
**Rationale:** Drift alert from /resume-session prompted reconciliation. New blocks earn portability and machinery-availability per `rules/instance-current-manifest.md`.
**Source:** /upgrade-instance run on <date>.
```

If `project.code` is absent, use `D-NNN` (unprefixed) per the bookend skill's id-format fallback.

### Step 6 — Report

Print a summary:

```
Instance reconciliation complete.

Reconciled to ACW <version> as of <date>.
Added: <list of block names added>
Skipped: <list of block names skipped (with operator reason if given)>
Logged: <decision-log entry id>

The /resume-session drift alert will now quiet for blocks at-or-before <version>.
Future ACW versions may surface new drift entries; re-run /upgrade-instance when alerted.
```

## When NOT to fire

- The operator wants to read about drift but not act on it. (`/resume-session` shows the alert; the operator can read the registry without invoking this skill.)
- An ACW version newer than the instance is not yet locally cloned. (The skill compares against `acw-state.yaml::version`, not against an external "latest ACW" lookup. The instance must have been pulled to a current ACW first.)
- The instance was scaffolded with custom-shaped state that intentionally diverges from the registry. In that case the operator may prefer to manage `last_reconciled_version` by hand and skip the skill.

## Safety

- Writes only to `acw-state.yaml` and `paths.decisions_log`. No other substrate changes.
- Never demotes a layer or removes a block. Pure additive reconciliation.
- Operator confirms each block individually. The skill never silently writes.
- If the operator aborts mid-pass, partial state is fine: the blocks already added stay; the skipped/unprocessed blocks remain on the gap list for a future run. `last_reconciled_version` is bumped only at Step 4, after the full pass — so an aborted run doesn't claim reconciliation that didn't happen.

## Output

Edits to `acw-state.yaml` per operator confirmation. One decision-log entry. Chat summary report.
