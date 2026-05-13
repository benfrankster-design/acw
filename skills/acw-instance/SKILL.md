---
name: acw-instance
description: >
  Object-centered orchestrator for ACW instance management. Two verbs over
  one shared spine: `audit` (read-only migration plan) and `upgrade`
  (executes the migration plan with one approval gate). Both fetch canonical
  from the ACW GitHub repo, perform the registration check, identify the
  substrate boundary, and produce a per-file migration plan. Verbs diverge
  after the spine.

  Triggered by the operator running /acw-instance audit or /acw-instance
  upgrade. Never fires automatically.

  Mental model: ACW is the gold standard for substrate shape. Every project
  that adopts ACW ends up structurally identical to ACW (same folder names,
  same file shapes, same conventions). Adoption is migration, not
  coexistence — the project's pre-ACW persistent-memory content moves into
  ACW-canonical destinations, reshaped to canonical format. Source files
  delete after content lands. Project-specific code, data, configs, tests,
  and infrastructure stay untouched.

  Audit produces a migration plan. Upgrade executes it under one approval
  gate, with `git mv` for tracked workspaces and a recommended pre-migration
  safety commit.
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | Highest |

# acw-instance

Object-centered orchestrator. Object: this ACW instance's lifecycle. Verbs: operations on it.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `audit` | Read-only. Identifies the substrate boundary, compares against ACW canonical, and produces a per-file migration plan (source → canonical destination → action: move / merge / reshape / delete / leave-untouched / declare instance-specific / absorption-candidate). Reserves interactive prompts only for genuinely ambiguous routings, flagged `[?]` in the plan. Writes nothing. | `references/audit.md` |
| `upgrade` | Executes a migration plan. Single approval gate. After the operator approves the plan, full migration runs without per-file prompts (unless `[?]` rows remain). Uses `git mv` on tracked workspaces. Recommends a pre-migration safety commit. Refreshes `rules/instance-current-manifest.md` from canonical, bumps `last_reconciled_version`, logs a decision-log entry. | `references/upgrade.md` |

Routing rules: argument required. `/acw-instance` with no command prints the table. Unknown command errors with the table.

## Shared spine (every verb runs these in order)

### Step 1 — Registration check

- `acw-state.yaml` exists at workspace root? Read it.
- `rules/instance-current-manifest.md` exists locally? Note presence.
- Both present → registered instance, proceed.
- Either absent → unregistered, perform substance scan.

### Step 2 — Substance scan (only when registration is missing)

Authoritative source for canonical paths: the fetched canonical `acw-state.yaml` blocks `template_layer`, `instance_layer`, `paths`, `empty_dirs`, plus the `decision_tracking.*` and `glossary.*` blocks. The skill does not carry its own copy.

Count substrate signals across two surfaces:

1. **Canonical-shape signals.** Existence-check each path declared in canonical `instance_layer[].path` and `paths.*`. Wiki shape (`decisions/INDEX.md`, `decisions/entries/`, `glossary/INDEX.md`, `glossary/entries/`) is canonical (v0.9.8+, D-ACW-048). Threshold: ≥ 3 distinct canonical paths present.
2. **Substrate-shaped patterns.** Root-level markdown files with `class/authority/stability/loaded_by_agent` frontmatter, dated capture files (`YYYY-MM-DD-*.md`), `.jsonl` logs, single-file legacy shapes (`decisions/decision-log.md`, `glossary.md`), and any directory whose name matches a canonical `paths.*_dir` key but lives at a non-canonical location.

If both surfaces are empty → bail: *"not an ACW instance and no substrate detected. Run `tools/scaffold-instance.py` from ACW canonical to scaffold a new instance."*

Either surface non-empty → proceed. Single-file legacy shape (pre-v0.9.8) is detected and routed for mandatory migration to wiki in the plan.

### Step 3 — Fetch canonical from GitHub

Single source of truth: `https://github.com/benfrankster-design/acw`. Private repo; use `gh` CLI:

```bash
gh api -H "Accept: application/vnd.github.raw" \
   repos/benfrankster-design/acw/contents/rules/instance-current-manifest.md
```

Fall back to `urllib.request` with `Authorization: Bearer $GITHUB_TOKEN` if `gh` is unavailable. Fail closed on neither path: *"cannot fetch canonical manifest from GitHub. Install `gh` and authenticate, or set `GITHUB_TOKEN`, then re-run."*

Templates and rule files needed for shape comparison are named in canonical `acw-state.yaml` itself: `template_layer` (rule and tool paths), `instance_layer[].template` (per-substrate-file template), `recommended_blocks` registry (per `rules/instance-current-manifest.md`), and `decision_tracking.regenerate_index_cmd` + `glossary.regenerate_index_cmd` for wiki-shape tooling.

Wiki mode is the only mode (v0.9.8+, D-ACW-048). The `instance_layer` rows for `decisions/INDEX.md` and `glossary/INDEX.md` are the canonical templates; pre-v0.9.8 single-file shape detected in a workspace is routed for migration.

Fetch on demand, cache in memory for the duration of the run.

### Step 4 — Identify the substrate boundary

The verb operates only on substrate. Project content (source code, tests, configs, data, dependencies, build artifacts) is explicitly skipped.

**Substrate (in-scope).** Authoritative source: canonical `acw-state.yaml` itself.

- Every path declared in canonical `template_layer`, `instance_layer[].path`, `paths.*`, `empty_dirs`, `meta_layer`. These are the recognized canonical locations.
- Substrate-shaped patterns per Step 2 surface 2 (frontmatter-bearing markdown, dated capture files, jsonl logs) at any non-code location.

**Project content (out-of-scope).** Canonical exclusion list lives in `rules/substrate-boundary.md` (consumer-loaded by this verb). The skill does not enumerate it inline. Anything not matching a substrate-shape signal and not declared in the canonical state-file blocks above is also implicitly out of scope.

Build the in-scope file list. Print a one-line summary: *"Substrate boundary identified: N files / M directories in scope; <K> project items skipped."*

### Step 5 — Build the per-file migration plan

For each in-scope file or directory, classify and route. The verb makes the call based on canonical knowledge — operator interaction is reserved for the rare ambiguous case.

**Action enum:**

| Action | Meaning |
|---|---|
| `move` | File is canonical-shape but in the wrong location. `git mv` to canonical destination. |
| `reshape` | File holds the right content but wrong format (frontmatter missing, sections off, ids unprefixed, etc.). Rewrite in canonical format at canonical destination; original deletes after content lands. |
| `merge` | Content belongs in an existing canonical destination that already exists. Append/integrate; original deletes after content lands. |
| `write-canonical` | Canonical destination missing entirely. Render from template (or compose from operator-supplied content). No source to delete. |
| `delete` | File is empty placeholder, byte-identical canonical copy that was scaffolded but never used, or genuine cruft. Source deletes; no content to preserve. |
| `leave-untouched` | File is already canonical-shape at canonical location. No action. |
| `instance-specific` | Substrate-shaped but uniquely this workspace's. Add to `acw-state.yaml::instance_specific_substrate`; file stays in place. Requires decision-log rationale. |
| `absorption-candidate` | Substrate-shaped, judged better than ACW canonical or net-new pattern ACW lacks. Default: write candidate to ACW `_buffer/`, add to `divergent_pending_review`. Operator can decline in plan review. |
| `[?]` | Genuinely ambiguous; operator clarification needed before plan executes. |

For each block in the canonical recommended-blocks registry (from the fetched manifest), also assess `acw-state.yaml` presence per the comparison rules in `references/upgrade.md` and add gap entries to the plan as `write-canonical` actions on `acw-state.yaml`.

For each entry already in `divergent_pending_review` → mark `pending-review`, no action. For each entry in `instance_specific_substrate` → mark `instance-specific-declared`, no action.

The plan is the spine output. Audit prints it; upgrade executes it under one approval gate.

## When NOT to fire

- Operator just wants to read about drift without acting. `/acw-session start` already surfaces the drift alert.
- Workspace is not substrate-shaped and has no canonical signals (Step 2 bails on this case).
- GitHub unreachable and offline-degraded mode is not currently shipped.

## Safety

- The verb operates only inside the substrate boundary identified in Step 4. Project content is never read for content classification and never written to.
- Audit writes nothing to the workspace. Optional absorption candidates to ACW's `_buffer/` only on operator confirmation during plan review.
- Upgrade requires a single explicit operator approval before any write fires. Per-file prompts only for `[?]` rows.
- Upgrade recommends a pre-migration safety commit before destructive operations. For workspaces not yet git-initialized, the verb offers `git init` + initial commit before proceeding.
- Upgrade uses `git mv` on tracked workspaces (preserves history) and plain `mv` on untracked workspaces.
- Source files delete only after content is verified at the canonical destination.
- Pure additive on `acw-state.yaml`: new blocks added, existing blocks never demoted or removed without an operator-confirmed `[?]` row.

## Discriminator

This is an object-centered command-routed orchestrator per `rules/skill-format.md`. The four-test discriminator:

1. **Same shared spine.** Both verbs run Steps 1–5 (registration check, substance scan, canonical fetch, substrate-boundary identification, migration-plan build). Specialist work after the spine: audit prints, upgrade executes.
2. **Same failure modes.** GitHub unreachable, registration ambiguous, substrate boundary unclear — all surface identically across both verbs.
3. **Same governance class.** Highest. Both verbs touch substrate that propagates ACW conventions across the workspace.
4. **Deltas are configuration-only.** The only verb-level difference is read-only vs. write-with-approval. Specialist work (printing vs. executing) operates on the same plan structure.

The object is the ACW instance lifecycle. Verbs are operations on it. Adopt-and-migrate is the unifying mental model.

## Output

Per verb. See reference files.
