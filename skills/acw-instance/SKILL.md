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

Count substrate signals across two surfaces:

1. **Canonical-shape signals** (workspace already looks ACW-shaped, just unregistered): `decisions/decision-log.md`, `rules/` (any `.md`), `incidents.jsonl`, `glossary.md`, `research/` (any `.md`), bookend skills under `skills/`. Threshold: 3 of 6.
2. **Substrate-shaped patterns** (workspace has persistent-memory content not in canonical paths): root-level markdown files with frontmatter, dated capture files (`YYYY-MM-DD-*.md`), structured directories that look substrate-like (`briefings/`, `runbooks/`, `notes/`, `journal/`, `context/`, `inbox/`, `integrations/`, etc.), `.jsonl` logs.

Both surfaces matter:

- **No canonical signals AND no substrate-shaped patterns** → bail: *"not an ACW instance and no substrate detected. Run `tools/scaffold-instance.py` from ACW canonical to scaffold a new instance."*
- **Canonical signals at-or-above 3 OR substrate-shaped patterns present** → workspace has substrate the verb must handle. Proceed.

The substance scan is generous on detection; routing decisions happen in Step 5.

### Step 3 — Fetch canonical from GitHub

Single source of truth: `https://github.com/benfrankster-design/acw`. Private repo; use `gh` CLI:

```bash
gh api -H "Accept: application/vnd.github.raw" \
   repos/benfrankster-design/acw/contents/rules/instance-current-manifest.md
```

Fall back to `urllib.request` with `Authorization: Bearer $GITHUB_TOKEN` if `gh` is unavailable. Fail closed on neither path: *"cannot fetch canonical manifest from GitHub. Install `gh` and authenticate, or set `GITHUB_TOKEN`, then re-run."*

Both verbs also fetch canonical rule files and templates needed for shape comparison (e.g., `rules/decision-tracking.md`, `rules/manifest-discipline.md`, `tools/templates/decision-log.md.tmpl`, `tools/templates/CLAUDE.md.tmpl`, `tools/templates/build-log.md.tmpl`, `tools/templates/tasks-status.md.tmpl`). Fetch on demand, cache in memory for the duration of the run.

### Step 4 — Identify the substrate boundary

The verb operates only on substrate. Project content (source code, tests, configs, data, dependencies, build artifacts) is explicitly skipped.

**Substrate (in-scope for the verb):**

- **Recognized canonical paths** at workspace root or under their canonical parents: `decisions/`, `rules/`, `research/`, `briefings/`, `runbooks/`, `integrations/`, `context/`, `inbox/`, `_buffer/`, `skills/`, `tools/` (when ACW-style stdlib substrate tools), `glossary.md`, `tasks-status.md`, `build-log.md`, `incidents.jsonl`, `CLAUDE.md`, `AGENTS.md`, `acw-state.yaml`, `threat-model.md`, `LAYERS.md` (legacy; folded into README in v0.5.1+), `LINEAGE.md`, `ORCHESTRATION.md`, `SKEPTIC.md`, `CHANGELOG.md`, `README.md`, `DEFERRED.md`, `deferred/`.
- **Substrate-shaped patterns at root or in non-code directories**: markdown files with class/authority/stability frontmatter, dated capture files, jsonl logs, structured ordered files, README files describing operational intent rather than build/install instructions.
- Workspace-named substrate directories the operator created (`notes/`, `journal/`, `kb/`, etc.) — substrate-shaped, but not in canonical paths.

**Project content (out-of-scope; never touched by the verb):**

- `src/`, `lib/`, `test/`, `tests/`, `spec/`, `app/`, `pkg/`, `cmd/`, `internal/`, `dist/`, `build/`, `out/`, `target/`, `bin/`, `obj/`, `.next/`, `node_modules/`, `__pycache__/`, `.venv/`, `venv/`, `env/`, `vendor/`, `deps/`, `coverage/`, `.git/`, `.github/` (CI/CD config), `.vscode/`, `.idea/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.tox/`.
- Manifest and config files: `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile`, `Pipfile.lock`, `requirements.txt`, `Cargo.toml`, `Cargo.lock`, `go.mod`, `go.sum`, `pom.xml`, `build.gradle`, `tsconfig.json`, `.eslintrc*`, `.prettierrc*`, `.editorconfig`, `.gitignore`, `.gitattributes`, `Makefile`, `Dockerfile`, `docker-compose.yml`, `*.lock`, `.env*`.
- Source files by extension: `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.rs`, `.go`, `.java`, `.kt`, `.swift`, `.cpp`, `.c`, `.h`, `.rb`, `.php`, `.cs`, `.scala`, `.clj`, `.ex`, `.exs`, `.elm`, `.hs`, `.ml`, `.html`, `.css`, `.scss`, `.sql` — unless the file lives inside `tools/` and the workspace is ACW-style stdlib substrate tooling.

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
