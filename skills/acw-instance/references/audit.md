# audit

Read-only verb on substrate. Walks Mode A (canonical-conventions comparison) then Mode B (organic substrate discovery), prompting the operator interactively for routing on each finding. Writes absorption candidates to ACW's `_buffer/` immediately on operator routing to `[b]`. Aggregates final report at end.

## After the spine

The orchestrator's Step 5 produces the routing table. Audit's job is to walk it, prompt the operator per-finding, write absorption candidates as the operator confirms, and emit the final report.

## Walk order

1. Mode A — canonical comparison (every canonical substrate type the workspace has a counterpart for).
2. Mode A — skills audit (every directory under `skills/` validated against `rules/skill-format.md`).
3. Mode B — organic substrate discovery (substrate-like patterns ACW canonical doesn't know about).
4. Final aggregated report.

Within Mode A and Mode B, each finding is **interactive** — prompt the operator before moving to the next finding. Writes happen during the walk, not after.

## Mode A — canonical comparison

For each canonical substrate type the workspace has a counterpart for:

1. Identify the canonical rule file (e.g., `rules/decision-tracking.md`) and template (e.g., `tools/templates/decision-log.md.tmpl`) governing this substrate type.
2. Fetch both from GitHub canonical.
3. Compare the workspace's file:
   - **Frontmatter** — does it have the expected fields per the rule? Missing fields go in the report.
   - **Sections** — does it follow the section conventions per the rule?
   - **Id format** — does it use the canonical id format (e.g., `D-{CODE}-NNN`)?
   - **Append-only discipline** — for files declared append-only in canonical, does the workspace's file show evidence of past edits?
4. Classify the file: canonical-shape OK / canonical-shape incomplete / divergent-fix-canonical / divergent-better-absorb.

The audit verb does the comparison the same way an agent would do it manually: read the rule, read the file, spot the differences. No new schema artifact is needed.

For `divergent-better-absorb` cases, immediately surface the absorption prompt (see "Absorption flow" below) and act on operator response before continuing.

## Mode A — skills audit (part of the spine, not a follow-up)

For each subdirectory under `skills/` that is not marked `status: superseded`:

1. Check that `SKILL.md` exists. Missing → flag.
2. Validate `SKILL.md` frontmatter against `rules/skill-format.md`:
   - Required fields: `name`, `description`, `role`, `capabilities`.
   - `role` must match one of the four normative groups (`orchestrator`, `pipeline-worker`, `guardian`, `broker-sideband`).
   - `description` is third-person, names when-to-fire and when-NOT-to-fire, names artifact and destination.
3. Check that the **classification table** (Domain / 6C Primary / Governance) exists immediately after frontmatter.
4. Check that `gotchas.md` exists with at least one entry.
5. For orchestrators with command tables, check that every command has a matching `references/<command>.md` and that no reference file redeclares the spine (the latter is a heuristic — flag if a reference file is over ~80 lines and looks workflow-shaped).

Each finding becomes a row in the final report under "Skills compliance." No interactive prompt for skill findings — they're enrichment proposals for the upgrade verb to walk.

## Mode B — organic substrate discovery

After Mode A completes, walk the workspace looking for substrate-like patterns not covered by canonical types:

- Markdown files with frontmatter that aren't in any canonical substrate location.
- Dated-prefix filenames (`YYYY-MM-DD-*.md`) suggesting append-only or session patterns.
- Structured directories (numbered files, ordered patterns).
- Any directory at the workspace root that looks like substrate (briefings/, journals/, custom-named-substrate/).

For each finding, **immediately surface the four-option prompt to the operator and wait for input.** Do not auto-classify; do not produce a static report with proposed routings. The default is "ask, don't guess."

```
Substrate-like pattern detected: <path>
Pattern shape: <brief description — frontmatter? dated? structured?>
Comparison to canonical: <closest canonical type if any, or "no canonical equivalent">

Route to:
  [a] Adopt-as-canonical — similar to a canonical type but uses different conventions; route via Mode A migration flow
  [b] Absorption candidate — net-new pattern ACW doesn't have but maybe should; flag for upstream review
  [s] Instance-specific — uniquely this workspace's; declare in instance_specific_substrate
  [n] Not substrate — project work, ignore
```

Process the operator's choice immediately:

- **`[a]`** → Add to "Mode A migration" list for the upgrade verb.
- **`[b]`** → Run absorption flow (next section). Write the candidate to ACW `_buffer/` now; record locally for the report.
- **`[s]`** → Record locally; on next `/acw-instance upgrade`, propose adding to `instance_specific_substrate` with operator-supplied rationale and decision-log reference.
- **`[n]`** → Drop from the report.

After all Mode B findings have been routed, continue to the final report.

## Absorption flow

Fires for `divergent-better-absorb` (Mode A) and `[b] Absorption candidate` (Mode B). Identical mechanics in both cases.

1. **Verify cross-repo write authority.** Check this workspace's `acw-state.yaml::cross_repo_writes` for the absolute path of ACW's `_buffer/` directory.
   - If declared → proceed.
   - If not declared → surface the required path and prompt: *"Cross-repo write to ACW's `_buffer/` requires declaration in `cross_repo_writes`. Add now? [y/N]"* If `y`, write the path to `cross_repo_writes` (creating the block if absent) and continue. If `n`, skip the absorption write and note in report.
2. **Write the absorption candidate** to ACW `_buffer/YYYY-MM-DD-<workspace>-<topic-slug>-absorption-candidate.md` per the format in `rules/multi-instance-topology.md` § "Absorption candidate format."
3. **Record divergence locally:**
   - If this workspace is registered (has `acw-state.yaml`) → append to `divergent_pending_review` with `status: pending`, `sent_date: <today>`, `absorption_candidate: <path>`.
   - If unregistered (audit running pre-adoption) → record the pending entry to a transient list; the upgrade verb materializes it into `divergent_pending_review` when it writes the new `acw-state.yaml`.

Absorption candidates flow upstream regardless of registration status. The flow is not gated on adoption.

## Final aggregated report

Print to chat at the end of the walk:

```
ACW Instance Audit — <workspace name> (<workspace path>)
Reconciled to ACW <last_reconciled_version> as of <last_reconciled>.
Current ACW canonical: <version-from-fetched-manifest>.
Registration status: <REGISTERED | UNREGISTERED with N/6 substrate signals>.

Substrate Routing Table

Canonical-shape OK (<N>):
  - <path>

Canonical-shape incomplete (<N>; enrichment proposed for upgrade):
  - <path> — missing: <fields>

Divergent — fix to canonical (<N>; migration with backup proposed for upgrade):
  - <path> — divergence: <summary>

Divergent — absorbed upstream (<N>; absorption candidates written this run):
  - <path> → ACW _buffer/<filename>

Skills compliance (<N> issues):
  - skills/<name>/SKILL.md — <issue>

Organic substrate (<N> findings):
  - <path> — operator routed to: <choice>
  - (any [b] entries link to absorption candidates written above)

Pending review (existing divergent_pending_review entries; <N>):
  - <path> — sent <date> — status: <pending|absorbed|rejected>

Instance-specific (existing instance_specific_substrate entries; <N>):
  - <path>

Absorption candidates written this run: <N>
Cross-repo writes declared: <yes|no>

Run /acw-instance upgrade to act on enrichments, migrations, and Mode B routings recorded above.
```

## When NOT to fire (verb-specific)

- Workspace has no substrate at all (orchestrator Step 2 bails first).
- Operator wants only Mode A and not Mode B (not currently supported as a flag; future earn-by-incident if requested).

## Output

Interactive prompts during walk. Routing-table report to chat at end. Zero-or-more absorption candidate files in ACW `_buffer/`. Optionally: appends to `divergent_pending_review` in this workspace's `acw-state.yaml`, or to `cross_repo_writes` if the operator authorized it during the absorption flow. No other writes.
