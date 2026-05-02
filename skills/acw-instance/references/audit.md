# audit

Read-only verb. Produces a per-file routing-table report. Optionally writes absorption candidates to ACW's `_inbox/` per operator routing. Never writes to the instance's substrate.

## After the spine

The orchestrator's Step 5 produces the routing table. Audit's job is to surface it to the operator and write any absorption candidates the operator confirms.

## Mode A — canonical comparison detail

For each canonical substrate type the workspace has a counterpart for:

1. Identify the canonical rule file (e.g., `rules/decision-tracking.md`) and template (e.g., `tools/templates/decision-log.md.tmpl`) governing this substrate type.
2. Fetch both from GitHub canonical.
3. Compare the workspace's file:
   - **Frontmatter** — does it have the expected fields per the rule? Missing fields go in the report.
   - **Sections** — does it follow the section conventions per the rule?
   - **Id format** — does it use the canonical id format (e.g., `D-{CODE}-NNN`)?
   - **Append-only discipline** — for files declared append-only in canonical, does the workspace's file show evidence of past edits?
4. Classify per the routing-table categories in the orchestrator's Step 5.

The audit verb does the comparison the same way an agent would do it manually: read the rule, read the file, spot the differences. No new schema artifact is needed.

## Mode B — organic substrate discovery

After Mode A completes, walk the workspace looking for substrate-like patterns not covered by canonical types:

- Markdown files with frontmatter that aren't in any canonical substrate location
- Dated-prefix filenames (`YYYY-MM-DD-*.md`) suggesting append-only or session patterns
- Structured directories (numbered files, ordered patterns)
- Any directory at the workspace root that looks like substrate (briefings/, journals/, custom-named-substrate/)

For each finding, surface to the operator:

```
Substrate-like pattern detected: <path>
Pattern shape: <brief description — frontmatter? dated? structured?>
Route to:
  [a] Adopt-as-canonical (similar to a canonical type but uses different conventions; route via Mode A flow)
  [b] Absorption candidate (net-new pattern ACW doesn't have but maybe should; flag for upstream review)
  [s] Instance-specific (uniquely this workspace's; declare in instance_specific_substrate)
  [n] Not substrate (project work, ignore)
```

Mode B is heuristic; the operator's routing is the authoritative classification.

## Routing-table report format

Print to chat:

```
ACW Instance Audit — <workspace name> (<workspace path>)
Reconciled to ACW <last_reconciled_version> as of <last_reconciled>.
Current ACW canonical: <version-from-fetched-manifest>.

Substrate Routing Table

Canonical-shape OK (<N> files):
  - <path>
  - ...

Canonical-shape incomplete (<N> files; enrichment proposed):
  - <path> — missing: <fields>
  - ...

Divergent — fix to canonical (<N> files; migration with backup proposed):
  - <path> — divergence: <summary>
  - ...

Divergent — better than canonical (<N> files; absorption candidate proposed):
  - <path> — pattern: <summary>
  - ...

Organic substrate (<N> findings; operator routing required):
  - <path> — pattern shape: <summary> — operator routed to: <choice>

Pending review (existing divergent_pending_review entries; <N>):
  - <path> — sent <date> — status: <pending|absorbed|rejected>

Instance-specific (existing instance_specific_substrate entries; <N>):
  - <path>

Run /acw-instance upgrade to act on this table.
```

## Absorption candidate writes (only when operator routes to absorb)

For each item the operator routes to absorb (Mode A `divergent-better-absorb` or Mode B `[b] Absorption candidate`):

1. Verify ACW's `_inbox/` path is in this workspace's `acw-state.yaml::cross_repo_writes`. If not, surface the path and skip the write — don't proceed without declared scope.
2. Write the absorption candidate per the format in `rules/multi-instance-topology.md` § "Absorption candidate format" to ACW's `_inbox/YYYY-MM-DD-<workspace>-<topic-slug>-absorption-candidate.md`.
3. Append the workspace's file to `divergent_pending_review` in `acw-state.yaml` with `status: pending`, `sent_date: <today>`, `absorption_candidate: <path to inbox note>`.

## When NOT to fire (verb-specific)

- Workspace has no substrate at all (orchestrator Step 2 bails first).
- Operator just wants the routing table without committing to write any absorption candidates — that's the default; audit doesn't write absorption candidates without explicit operator routing.

## Output

Routing-table report to chat. Optionally: zero-or-more absorption candidate files in ACW `_inbox/`. Optionally: appends to `divergent_pending_review` in this workspace's `acw-state.yaml`. No other writes.
