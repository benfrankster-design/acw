# upgrade

Interactive verb. Reconciles instance state with ACW canonical. Walks gaps in `acw-state.yaml`, applies adopt-mode for unregistered workspaces (with hard-stop above the organic threshold), respects divergence markers. Writes `acw-state.yaml`, refreshes `rules/instance-current-manifest.md` from canonical, logs a decision-log entry.

## After the spine

The orchestrator's Step 5 produces the routing table. Upgrade's job is to walk it action-by-action with operator confirmation, then bump versions and log.

## Adopt-mode hard-stop (only when registration is missing)

If Step 2 of the spine flagged this workspace as unregistered (substrate signals at-or-above 3), check the `adopt_mode_organic_threshold` in canonical defaults (default 5):

- Count markdown files in `decisions/` and `rules/` excluding any files that are byte-identical or near-identical to ACW canonical copies (i.e., excluding files that came from an earlier scaffold).
- If the count in either directory is at-or-above the threshold → bail:
  > This workspace has substantial existing substrate (`<N>` files in `<directory>`). Adopt-mode could overwrite or conflict with organic conventions. Run `/acw-instance audit` first to route divergences before any writes fire.
- If the count is below the threshold → proceed to adoption.

### Adoption sequence

Surface the prompt:

```
This workspace looks like an ACW instance that pre-dates registration.

Detected substrate signals: <list>
Existing substrate files: <count> (below organic threshold of <threshold>)

Adopt as a formal ACW instance? This will:
  - Write the GitHub-fetched canonical to your local rules/instance-current-manifest.md
  - Create acw-state.yaml with last_reconciled_version: "0.0.0" (drives noisy first reconciliation)
  - Walk you through reconciling each recommended block

[y/N]
```

On `y`:
1. Write fetched canonical manifest to `<workspace>/rules/instance-current-manifest.md`. Create `rules/` if absent.
2. Write minimal `acw-state.yaml` with: `version` (from canonical's "current ACW version"), `last_reconciled: <today>`, `last_reconciled_version: "0.0.0"`, `is_canonical_source: false`, minimal `paths:` block matching detected substrate files.
3. Print: `Adoption complete. Now reconciling against current ACW canonical.` Continue to "Walk gaps."

On `n` (or empty): exit cleanly.

## Walk gaps

For each gap entry from the routing table:

```
─────────────────────────────────────
Block: <name>
Earned in: <version>
Required: <yes / no>

What: <description from registry>
Why it helps: <rationale from registry>

Proposed default content:
<canonical default block>

Options:
  [a] Add as proposed (write to acw-state.yaml or copy file from canonical)
  [m] Modify before adding (operator provides the value)
  [s] Skip (block stays absent on this pass)
─────────────────────────────────────
```

- **`a`** — write the default. For dict-shaped blocks with canonical defaults (`paths`), upsert each key. For list-shaped blocks (`auto_load_at_session_start`, `empty_dirs`), append each entry. For file-naming blocks (`rules/multi-instance-topology.md`), fetch the file from GitHub and write to the instance's `rules/` directory, then add to `template_layer` and `auto_load_at_session_start` per the registry entry's "How to add" guidance. For blocks with no canonical default (e.g., `project` with `name`/`code`/`domain` placeholders), force the `[m]` path.
- **`m`** — prompt for value, validate per the registry's "How to add" shape, write via `manifest.append`.
- **`s`** — no write. Note for summary.

Honor the routing table's existing markers:
- Files in `divergent_pending_review` → no canonical proposal; surface "pending review of absorption candidate sent <date>; not modifying."
- Files in `instance_specific_substrate` → no canonical proposal; surface "instance-specific per <decision_ref>; not modifying."

## Resolve divergent_pending_review entries

After the gap walk, for each existing `divergent_pending_review` entry with `status: pending`:

- Compare the entry's file shape against the freshly-fetched canonical. If canonical now matches the workspace's shape → mark `absorbed`, surface to operator, clear the entry.
- If a rejection notification exists in this workspace's `_inbox/` from ACW (filename pattern `acw-rejection-<topic>.md`) → mark `rejected`, surface to operator, route to adopt flow on next run.
- Else → keep `pending`, surface a one-line status reminder.

## Refresh canonical cache

Overwrite `<workspace>/rules/instance-current-manifest.md` with the fetched canonical content. The local file is now an up-to-date snapshot of "what canonical looks like at last reconciliation."

## Bump versions

1. Set `last_reconciled` to today's date (UTC, `YYYY-MM-DD`).
2. Set `last_reconciled_version` to the canonical's current `<version>`.

Use `manifest.append` (key/value upsert) or direct edit. Preserve all other content.

## Log a decision-log entry

Append to `paths.decisions_log` `section_conventions.decisions`:

```markdown
### D-<CODE>-NNN — Instance reconciled to ACW <version>

**Date:** YYYY-MM-DD
**Decision:** Reconciled this instance to ACW recommended-blocks registry as of version <version>. <N> blocks added: <names>. <M> blocks skipped: <names>. <K> divergence markers respected. Canonical manifest fetched from GitHub and cached locally.
**Rationale:** Drift alert from /acw-session start prompted reconciliation.
**Source:** /acw-instance upgrade run on <date>.
```

If this run was an adoption, prepend an additional entry recording the adoption itself.

## Report

Print summary:

```
Instance reconciliation complete.

[Adopted from unregistered substrate-shaped workspace.]   <-- only on adoption
Reconciled to ACW <version> as of <date>.
Canonical manifest cache: refreshed from GitHub.
Added: <list>
Skipped: <list>
Pending review (respected): <list>
Instance-specific (respected): <list>
Logged: <decision-log entry id(s)>

The /acw-session start drift alert will quiet for blocks at-or-before <version>.
```

## Safety

- Writes to `acw-state.yaml`, `rules/instance-current-manifest.md` (cache refresh), and `paths.decisions_log`. On adoption, also writes to canonical paths the canonical manifest names.
- Never demotes a layer or removes a block. Pure additive reconciliation plus marker respect.
- Operator confirms each block individually. The skill never silently writes recommended blocks. Adoption requires explicit operator confirmation; substance below threshold bails; substance above organic threshold also bails.
- If operator aborts mid-pass, partial state is fine: blocks already added stay; skipped/unprocessed remain on gap list. `last_reconciled_version` bumped only after the full pass completes.

## Output

Edits to `acw-state.yaml`. Refresh of `rules/instance-current-manifest.md`. One or two decision-log entries. Chat summary report.
