---
status: superseded
superseded_by: skills/acw-instance/
superseded_in: 0.4.0
name: upgrade-instance
description: >
  Reconciles an ACW instance with the current ACW recommended-blocks registry.
  Fetches the canonical `rules/instance-current-manifest.md` from the ACW
  GitHub repo on every run (single source of truth), compares against this
  instance's `acw-state.yaml`, and walks the operator through adding any
  missing blocks one at a time (each with its canonical default; operator
  picks add-as-proposed, modify, or skip). After the pass, bumps
  `last_reconciled` and `last_reconciled_version` so the drift alert in
  /resume-session quiets down.

  Also supports an adopt mode for substrate-shaped workspaces that pre-date
  ACW registration: when `acw-state.yaml` and/or `rules/instance-current-manifest.md`
  are missing but other substrate signals are present, the skill offers to
  adopt the workspace as a formal ACW instance by writing the missing
  registration files.

  Triggered by the operator running /upgrade-instance, typically after
  /resume-session surfaces a drift alert. Also valid to run on demand at any
  time. Never fires automatically.

  Produces edits to acw-state.yaml and (on adoption or after each successful
  pass) writes the GitHub-fetched canonical to the instance's local
  rules/instance-current-manifest.md. Logs a decision-log entry recording the
  reconciliation pass.
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# upgrade-instance

Walks the operator through reconciling instance state with the current ACW recommended-blocks registry. Closes the loop on the drift detection in `/resume-session`.

## Path resolution

This skill writes to `acw-state.yaml`, `rules/instance-current-manifest.md`, and `paths.decisions_log`. Substrate paths resolve at runtime per the bookend skills' path-resolution convention. The skill never hardcodes a path.

## Single source of truth: GitHub

The canonical `rules/instance-current-manifest.md` lives in the ACW GitHub repo at:

```
https://github.com/benfrankster-design/acw → rules/instance-current-manifest.md
```

This skill fetches the canonical on every run. The instance's local copy is a write-once cache representing "the last canonical I reconciled to" — never used as comparison yardstick except in extreme offline-degraded mode (not currently shipped).

**Fetch path (private repo).** Use the `gh` CLI, which inherits the operator's authenticated GitHub session:

```bash
gh api -H "Accept: application/vnd.github.raw" \
   repos/benfrankster-design/acw/contents/rules/instance-current-manifest.md
```

If `gh` is unavailable, fall back to `urllib.request` with `Authorization: Bearer $GITHUB_TOKEN` reading from a `GITHUB_TOKEN` env var. If neither path works, fail closed with: `cannot fetch canonical manifest from GitHub. Install gh and authenticate, or set GITHUB_TOKEN, then re-run.`

## Instructions

When invoked, execute the steps below in order. Operator confirmation is required at each block in Step 4.

### Step 0 — Detect registration state

Before anything else, check whether this workspace is a registered ACW instance:

1. Does `acw-state.yaml` exist at the workspace root? Read it if so.
2. Does `rules/instance-current-manifest.md` exist locally?

**Case A — both present:** registered instance. Proceed to Step 1.

**Case B — both absent (or one absent):** unregistered. Proceed to Step 0a (substance scan).

### Step 0a — Substance scan (only when registration is missing)

Walk the workspace looking for substrate signals:

| Signal | Path |
|---|---|
| Decisions | `decisions/decision-log.md` |
| Rules dir | `rules/` (any `.md` file) |
| Incidents | `incidents.jsonl` |
| Glossary | `glossary.md` |
| Research dir | `research/` (any `.md` file) |
| Bookend skills | `skills/capture-and-metabolize/` or `skills/resume-session/` (or local equivalents) |

Count signals present. **Threshold: 3 of 6 → substrate-shaped.**

**If below threshold:** print `this workspace doesn't appear to be an ACW instance. To start one, run \`tools/scaffold-instance.py\` from ACW canonical.` Exit.

**If at-or-above threshold:** print a one-line summary of detected signals, then prompt the operator:

```
This workspace looks like an ACW instance that pre-dates registration.

Detected substrate signals:
  - <each signal found>

Adopt as a formal ACW instance? This will:
  - Fetch the current canonical rules/instance-current-manifest.md from GitHub
  - Write it to your local rules/ directory
  - Create acw-state.yaml with last_reconciled_version: "0.0.0" (drives a noisy first reconciliation)
  - Then walk you through reconciling each recommended block

[y/N]
```

- **`n` (or empty):** exit cleanly. Operator may scaffold formally via `tools/scaffold-instance.py` or come back later.
- **`y`:** continue.

Adoption sequence:

1. Fetch the canonical `rules/instance-current-manifest.md` from GitHub via the path documented above.
2. Write it to `<workspace>/rules/instance-current-manifest.md`. If `rules/` doesn't exist, create it.
3. Write a minimal `acw-state.yaml` at the workspace root containing:
   - `version: "0.3.0"` (current ACW version, taken from the fetched canonical's "current ACW version" reference)
   - `last_reconciled: <today's date>`
   - `last_reconciled_version: "0.0.0"` (drives noisy first reconciliation)
   - `is_canonical_source: false`
   - Minimal `paths:` block matching the canonical defaults for any substrate files actually detected in the substance scan (e.g., if `decisions/decision-log.md` exists, declare it; otherwise skip)

4. Print: `Adoption complete. Now reconciling against current ACW canonical.` Continue to Step 1.

### Step 1 — Fetch canonical and read instance state

1. **Fetch canonical** `rules/instance-current-manifest.md` from GitHub per the path above. On failure, fail closed with the documented error message.
2. **Read instance state** from `acw-state.yaml`. Note `version`, `last_reconciled`, `last_reconciled_version`, and which recommended blocks are present (populated, present-but-empty, or absent).
3. Parse the fetched canonical: each `## <block name>` heading is one entry, with What / Why it helps / Required / How to add / Earned in fields.

### Step 2 — Build the gap list

For each entry in the fetched canonical:

- Compare its **earned in** version to `last_reconciled_version` (semantic-version comparison; rc-suffixes are pre-release, so `0.2.0-rc1 < 0.2.0-rc2 < 0.2.0`). If `last_reconciled_version` is absent in the state file, treat as `"0.0.0"`.
- If the entry's earned-in is at-or-before `last_reconciled_version`, skip — already reconciled.
- If the entry is absent from the state file, add to the gap list.
- If the entry is present-but-empty (`block: []` or `block: {}`), skip — deliberate opt-out.
- If the entry is present and populated (at least one entry/key), skip — the operator has customized this block. For dict blocks like `paths`, runtime `manifest.load` merges canonical defaults for absent keys, so a partial declaration is fully functional. The skill does NOT propose adding missing keys to a partial block; the operator's partial declaration is honored.
- If the entry is present but malformed (wrong shape — e.g., `paths` declared as a string instead of a dict, or a list block declared as a dict), STOP. Print an error naming the malformed block and direct the operator to fix `acw-state.yaml` by hand before re-running. Do not attempt to repair shape.

If the gap list is empty (and no malformed blocks), continue to Step 5 to write the fetched canonical to local cache and bump versions, then exit with `Instance is already current with ACW <version>. Local cache refreshed.`

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
  [a] Add as proposed (write the default into your acw-state.yaml or copy the file from canonical)
  [m] Modify before adding (operator provides the value to write)
  [s] Skip (do not add; this block stays absent on this pass)
─────────────────────────────────────
```

Wait for operator input. Process per choice:

- **`a`** — Use `tools/manifest.py::append` (or the equivalent in the runtime) to write the default block. For dict-shaped blocks with canonical defaults (`paths`), append each key. For list-shaped blocks with canonical defaults (`auto_load_at_session_start`), append each entry. **For blocks that name a file (e.g., `rules/multi-instance-topology.md`), `[a]` fetches the file from the ACW GitHub repo (same path mechanism as the manifest fetch) and writes it to the instance's `rules/` directory, then adds the path to `template_layer` and `auto_load_at_session_start` per the registry entry's "How to add" guidance.** **For blocks with no canonical default (`project`, where each instance picks its own `name` / `code` / `domain`), `[a]` is not valid — the skill must force the `[m]` path for that block, prompting for operator-supplied values.** If the registry entry's "How to add" section contains placeholders like `<human-readable name>`, treat the block as "no canonical default" and prompt for modify input.
- **`m`** — Prompt the operator for the value. Validate (well-formed yaml, correct shape per the registry's "How to add" section). If valid, write via `manifest.append`. If not valid, re-prompt.
- **`s`** — No write. Note this block as "skipped this pass" for the summary.

Move to the next gap. Repeat until all gaps processed.

### Step 4 — Write fetched canonical to local cache

Overwrite `<workspace>/rules/instance-current-manifest.md` with the canonical content fetched in Step 1. The local file is now an up-to-date cache of "what canonical looked like at last reconciliation."

### Step 5 — Bump `last_reconciled` and `last_reconciled_version`

After the gap pass and cache refresh:

1. Set `last_reconciled` to today's date (UTC, `YYYY-MM-DD`).
2. Set `last_reconciled_version` to the value of `acw-state.yaml::version` (the current ACW version this instance now reconciles to).

Use `manifest.append` (key/value upsert) for both fields if the manifest tooling supports top-level scalar fields, or fall back to a direct edit of `acw-state.yaml` if it doesn't. Either way, preserve all other content in the state file.

### Step 6 — Log a decision-log entry

Append a new entry to `paths.decisions_log` `section_conventions.decisions` recording the reconciliation. Format:

```markdown
### D-<CODE>-NNN — Instance reconciled to ACW <version>

**Date:** YYYY-MM-DD
**Decision:** Reconciled this instance to ACW recommended-blocks registry as of version <version>. <N> blocks added: <names>. <M> blocks skipped on this pass: <names>. Canonical manifest fetched from GitHub and written to local cache.
**Rationale:** Drift alert from /resume-session prompted reconciliation. New blocks earn portability and machinery-availability per `rules/instance-current-manifest.md`.
**Source:** /upgrade-instance run on <date>.
```

If `project.code` is absent, use `D-NNN` (unprefixed) per the bookend skill's id-format fallback.

If this run was an **adoption** (Step 0a fired), prepend an additional entry recording the adoption itself:

```markdown
### D-<CODE>-NNN — Workspace adopted as formal ACW instance

**Date:** YYYY-MM-DD
**Decision:** Adopted this substrate-shaped workspace as a formal ACW instance via /upgrade-instance adopt mode. Wrote acw-state.yaml and copied canonical rules/instance-current-manifest.md from GitHub.
**Rationale:** Workspace had <N> of 6 substrate signals indicating pre-registration ACW use. Adoption brings it under formal management without manual scaffold work.
**Source:** /upgrade-instance run on <date>.
```

### Step 7 — Report

Print a summary:

```
Instance reconciliation complete.

[Adopted from unregistered substrate-shaped workspace.]   <-- only on adoption
Reconciled to ACW <version> as of <date>.
Canonical manifest cache: refreshed from GitHub.
Added: <list of block names added>
Skipped: <list of block names skipped (with operator reason if given)>
Logged: <decision-log entry id(s)>

The /resume-session drift alert will now quiet for blocks at-or-before <version>.
Future ACW versions may surface new drift entries; re-run /upgrade-instance when alerted.
```

## When NOT to fire

- The operator wants to read about drift but not act on it. (`/resume-session` shows the alert; the operator can read the registry without invoking this skill.)
- The workspace is not substrate-shaped and the operator hasn't opted to scaffold. (The adopt-mode prompt handles this case explicitly.)
- The instance was scaffolded with custom-shaped state that intentionally diverges from the registry. In that case the operator may prefer to manage `last_reconciled_version` by hand and skip the skill.
- GitHub is unreachable AND no offline-degraded mode is shipped. The skill fails closed rather than running on a stale local cache.

## Safety

- Writes to `acw-state.yaml`, `rules/instance-current-manifest.md` (cache refresh), and `paths.decisions_log`. On adoption, also writes new files only at canonical paths the canonical manifest names.
- Never demotes a layer or removes a block. Pure additive reconciliation.
- Operator confirms each block individually. The skill never silently writes recommended blocks. Adoption requires explicit operator confirmation; substance below threshold bails.
- If the operator aborts mid-pass, partial state is fine: blocks already added stay; skipped/unprocessed blocks remain on the gap list for a future run. `last_reconciled_version` is bumped only at Step 5, after the full pass — so an aborted run doesn't claim reconciliation that didn't happen.
- Single source of truth: GitHub. The skill never reads the local cache as comparison yardstick. If GitHub is unreachable, the skill fails closed.

## Output

Edits to `acw-state.yaml` per operator confirmation. Refresh of `rules/instance-current-manifest.md` from GitHub canonical. One (or two, on adoption) decision-log entries. Chat summary report.
