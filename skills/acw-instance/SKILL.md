---
name: acw-instance
description: >
  Object-centered orchestrator for ACW instance management. Two verbs over
  one shared spine: `audit` (read-only routing-table report) and `upgrade`
  (interactive reconciliation with writes). Both fetch canonical from the
  ACW GitHub repo, perform the registration check, run the substrate scan,
  and build a per-file routing table. Verbs diverge after the spine.

  Replaces /upgrade-instance from v0.3.0. Triggered by the operator running
  /acw-instance audit or /acw-instance upgrade. Never fires automatically.

  Produces routing reports (audit) or edits to acw-state.yaml plus a refresh
  of rules/instance-current-manifest.md plus optional absorption candidates
  written to ACW's _inbox/ (upgrade), with a decision-log entry recording
  the run.
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# acw-instance

Object-centered orchestrator. Object: this ACW instance. Verbs: operations on it.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `audit` | Read-only. Walks substrate, compares against ACW canonical (Mode A) and surfaces non-canonical substrate-like patterns (Mode B), produces a per-file routing report, optionally writes absorption candidates to ACW's `_inbox/` per operator routing. Never modifies the instance's substrate. | `references/audit.md` |
| `upgrade` | Reconciles instance state with ACW canonical. Walks gaps in `acw-state.yaml`, applies adopt-mode for unregistered workspaces (with hard-stop above the organic threshold), respects `divergent_pending_review` and `instance_specific_substrate` markers. Writes `acw-state.yaml` and refreshes `rules/instance-current-manifest.md` from canonical. | `references/upgrade.md` |

Routing rules: argument required. `/acw-instance` with no command prints the table. Unknown command errors with the table.

## Shared spine (every verb runs these in order)

### Step 1 — Registration check

- `acw-state.yaml` exists at workspace root? Read it.
- `rules/instance-current-manifest.md` exists locally? Note presence.
- Both present → registered instance, proceed.
- Either absent → unregistered, perform substance scan.

### Step 2 — Substance scan (only when registration is missing)

Count substrate signals: `decisions/decision-log.md`, `rules/` (any `.md`), `incidents.jsonl`, `glossary.md`, `research/` (any `.md`), bookend skills under `skills/`. Threshold: 3 of 6.

- Below threshold → bail: `not an ACW instance. Run \`tools/scaffold-instance.py\` from ACW canonical.`
- At-or-above threshold → workspace is substrate-shaped. Verbs handle differently — audit reports findings; upgrade offers adoption per `references/upgrade.md`.

### Step 3 — Fetch canonical from GitHub

Single source of truth: `https://github.com/benfrankster-design/acw`. Private repo; use `gh` CLI:

```bash
gh api -H "Accept: application/vnd.github.raw" \
   repos/benfrankster-design/acw/contents/rules/instance-current-manifest.md
```

Fall back to `urllib.request` with `Authorization: Bearer $GITHUB_TOKEN` if `gh` is unavailable. Fail closed on neither path: `cannot fetch canonical manifest from GitHub. Install gh and authenticate, or set GITHUB_TOKEN, then re-run.`

Audit also fetches the canonical rule files and templates needed for Mode A comparisons (e.g., `rules/decision-tracking.md`, `tools/templates/decision-log.md.tmpl`) on demand from the same repo path.

### Step 4 — Read instance state and parse canonical

Read `acw-state.yaml`. Note `version`, `last_reconciled`, `last_reconciled_version`, declared blocks, divergence markers (`divergent_pending_review`, `instance_specific_substrate`), and `adopt_mode_organic_threshold` (default 5).

Parse the fetched canonical manifest: each `## <block name>` heading is one entry with What / Why it helps / Required / How to add / Earned in fields.

### Step 5 — Build the per-file routing table

For each substrate file in the workspace, classify:

- **canonical-shape** — file matches canonical rule + template; no action needed
- **canonical-shape-incomplete** — present but missing frontmatter / section conventions / id format; enrichment-style fix needed
- **divergent-fix-canonical** — substantively different shape; ACW canonical is the right shape; migration with `.pre-acw-backup` needed
- **divergent-better-absorb** — substantively different shape; the workspace's pattern is judged better; absorption candidate flow
- **organic-instance-specific** — substrate-like but not in canonical types; intentionally divergent; declare in `instance_specific_substrate`
- **organic-absorb-candidate** — substrate-like but not in canonical types; pattern would generalize; absorption candidate flow

For each entry in `divergent_pending_review`, mark the corresponding file as `pending-review` regardless of current shape.

For each entry in `instance_specific_substrate`, mark the file as `instance-specific` and skip routing.

For each registry block from canonical, also classify state-file presence per the comparison rules in `references/upgrade.md` (absent / present-but-empty / present-and-populated / malformed).

The routing table is the spine output. Verbs consume it differently — audit reports it; upgrade walks it action-by-action with operator confirmation.

## When NOT to fire

- Operator just wants to read about drift without acting. `/acw-session start` already surfaces the drift alert.
- Workspace is not substrate-shaped (Step 2 bails on this case).
- GitHub unreachable and offline-degraded mode is not currently shipped.

## Safety

- Audit verb writes only absorption candidates to ACW's `_inbox/` (and only on operator routing). No other writes.
- Upgrade verb writes `acw-state.yaml`, `rules/instance-current-manifest.md` (cache refresh), and `paths.decisions_log`. Hard-stop above `adopt_mode_organic_threshold` prevents steamrolling.
- Single source of truth: GitHub. The skill never reads the local cache as comparison yardstick; fail-closed on GitHub unreachable.

## Output

Per verb. See reference files.
