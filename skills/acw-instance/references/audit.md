# audit

Read-only verb. Produces a per-file migration plan: source → canonical destination → action. The plan is what `/acw-instance upgrade` executes. The audit verb itself writes nothing to the workspace; optional absorption candidates to ACW's `_buffer/` are surfaced in the plan and only written on operator confirmation during plan review.

## Mental model

ACW is the gold standard for substrate shape. This verb's job is to look at the workspace's substrate, identify what's already canonical, what needs to migrate into canonical, what's genuinely workspace-specific, and what's a candidate for upstream absorption — then state all of that as one coherent plan.

The verb does NOT interrogate the operator per-finding. It uses canonical knowledge to make sensible routing calls and presents the full plan in one pass. Interactive prompting is reserved for genuinely ambiguous cases, flagged `[?]` in the plan.

This supersedes the v0.4.0 / v0.5.0 interactive Mode B walk. Today's workspaces (post-v0.6.0 absorption of the cockpit cluster — `briefings/`, `runbooks/`, `integrations/`, `context/`, `inbox/`, `_buffer/`) usually require few or zero `[?]` rows.

## After the spine

The orchestrator's Step 5 produces the migration plan structure. Audit's job is to fill it in fully and print it.

## Plan construction

Walk the in-scope substrate from Step 4 of the spine. For each file or directory, classify and route per the action enum in `SKILL.md`. The default reasoning model:

1. **Is this already canonical-shape at the canonical location?** → `leave-untouched`.
2. **Is the content right but the location wrong?** → `move` to canonical destination.
3. **Is the location right but the format wrong?** → `reshape` in place to canonical format.
4. **Does the content belong inside an existing canonical destination?** → `merge` into that destination.
5. **Is canonical missing entirely?** → `write-canonical` from template.
6. **Is the file an empty placeholder or byte-identical scaffold artifact never used?** → `delete`.
7. **Is the substrate-shaped pattern uniquely this workspace's domain, won't generalize upstream?** → `instance-specific` (record rationale; declaration goes in `acw-state.yaml::instance_specific_substrate` with decision-log entry).
8. **Is the substrate-shaped pattern net-new (ACW lacks the canonical shape) or judged better than canonical?** → `absorption-candidate`.
9. **Cannot decide between two reasonable routings?** → `[?]` with the candidate options inline.

The verb is opinionated. After v0.6.0 absorbed the cockpit cluster, well-formed substrate should route cleanly. Use `[?]` sparingly.

## Canonical comparison reference

For each canonical substrate type the workspace touches, compare the workspace's file against canonical:

- **`CLAUDE.md`** — frontmatter, auto-load imports, hard-rule pointers, structure per `tools/templates/CLAUDE.md.tmpl`.
- **`AGENTS.md`** — directives present, host-agnostic posture per ACW canonical.
- **`tasks-status.md`** — Pending-only (v0.9.3+ canonical shape) per `rules/task-tracking.md`; completed work archives on completion to `tasks-status-YYYY-Q*.md`; Parked retired (deferred-but-keep routes to `inbox/ideas/`). Three-section shape on a workspace is drift — propose `reshape` plan row to migrate to Pending-only.
- **`build-log.md`** — chronological narrative entries with date stamps per `tools/templates/build-log.md.tmpl`.
- **Decisions** — shape depends on `acw-state.yaml::decision_tracking.mode`:
  - **`single-file` mode (default):** `decisions/decision-log.md` — four sections (Open Questions / Decisions and Rationale / Constraints and Gotchas / Resolved Questions); ids prefixed `D-{CODE}-NNN` per `rules/decision-tracking.md`.
  - **`wiki` mode:** `decisions/INDEX.md` (auto-loaded thin index) + `decisions/entries/<id>-<slug>.md` (atomic per-decision files with frontmatter `id, title, date, status, kind, updated`) + `decisions/open-questions/` + `decisions/constraints/` subdirs. INDEX regenerates from entries.
  - Mode-mismatch (e.g., file shape doesn't match declared mode) → `[?]` plan row.
- **`incidents.jsonl`** — one event per line; schema per `rules/incident-tracking.md`.
- **Glossary** — shape depends on `acw-state.yaml::glossary.mode`:
  - **`single-file` mode (default):** `glossary.md` — `## <term>` sections per `tools/templates/glossary.md.tmpl`.
  - **`wiki` mode:** `glossary/INDEX.md` + `glossary/entries/<slug>.md` (frontmatter `term, status`).
- **`research/`** — `01-problem-framing.md`, `evolution.md`, `sources.md`, `research-state.yaml`, `sessions/`, `queries/`, `queries/_consumed/`.
- **`context/`** — `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`.
- **`integrations/README.md`** — present per `tools/templates/integrations-README.md.tmpl`.
- **`acw-state.yaml`** — structure per `rules/manifest-discipline.md`; recommended blocks per `rules/instance-current-manifest.md`.
- **Skills under `skills/`** — frontmatter (name, description, role, capabilities), classification table, gotchas.md presence per `rules/skill-format.md`.

Differences become plan rows: `reshape` if format is fixable in place at the canonical location, `move` if location is wrong, `write-canonical` if missing.

## Recommended-blocks registry pass

Walk every entry in the fetched canonical `rules/instance-current-manifest.md`. For each entry:

- Compare earned-in version against `acw-state.yaml::last_reconciled_version`. If earned-in ≤ last_reconciled_version, skip (already reconciled).
- If earned-in > last_reconciled_version, check the workspace's `acw-state.yaml`:
  - **Block absent** → plan row: `write-canonical` on `acw-state.yaml` (add proposed default block).
  - **Block present-but-empty** (`block: []`) → operator deliberately opted out; skip silently.
  - **Block present and populated** → already declared; skip.
  - **Block malformed** (wrong shape) → `[?]` plan row, ask operator to confirm intent.

Each plan row carries the registry entry's "How to add" content as the proposed default.

## Substrate-shaped pattern walk

For each in-scope substrate-shaped file or directory NOT covered by canonical types:

- Apply the default reasoning model above. Most cases route cleanly to one of `move` (rename into canonical destination), `reshape` (rewrite in canonical format at canonical destination), `instance-specific`, or `absorption-candidate`.
- If a file's path is suggestive of a canonical type (`my-decisions.md`, `team-todo.md`, `wiki/`, `kb/`, etc.) → propose the canonical mapping, route as `move` or `reshape`.
- If a file looks like a near-clone of a recently-absorbed v0.6.0 surface (briefings, runbooks, integrations, context, inbox) → route to that canonical destination.
- If genuinely ambiguous → `[?]` with proposed alternatives.

## Skills audit

For each subdirectory under `skills/` not marked `status: superseded`:

- Validate `SKILL.md` per `rules/skill-format.md` (frontmatter fields, classification table, body structure).
- Validate `gotchas.md` exists with at least one entry; if missing, plan row: `write-canonical` on `skills/<name>/gotchas.md` with stub content.
- For orchestrators with command tables, validate every command has a matching `references/<command>.md` that does not redeclare the spine.

Skill-shape findings become plan rows under the skill's path; default action is `reshape` for fixable frontmatter/structure issues, `write-canonical` for missing files.

## Auto-load discipline (earned in v0.9.0)

Walk the workspace's `acw-state.yaml::auto_load_at_session_start` block per `rules/auto-load-discipline.md`. The rule defines:

- **Canonical recommendations** — the four files ACW recommends with stated claims. Mode-portable: decisions surface is `decisions/decision-log.md` in single-file mode, `decisions/INDEX.md` in wiki mode. Glossary surface is `glossary.md` in single-file mode, `glossary/INDEX.md` in wiki mode. Plus `rules/instance-hard-rules.md` and `tasks-status.md` (mode-invariant).
- **Declared demotion candidates** — paths that fail the gate (consumer-skill loads them directly, single-operator-doesn't-need-it, only-audit-reads-it). Currently named in the rule: `rules/manifest-discipline.md`, `rules/instance-current-manifest.md`, `rules/multi-instance-topology.md`, `incidents.jsonl`.

For each entry in the workspace's `auto_load_at_session_start`, classify and add to the migration plan:

| Verdict | Trigger | Plan action |
|---|---|---|
| `KEEP` | Entry on canonical recommendations list, declared structured form | leave-untouched |
| `KEEP (migrate-to-structured)` | Entry on canonical recommendations list, bare-path legacy form | reshape — convert to structured form with the canonical claim |
| `KEEP (instance-specific)` | Entry not on canonical list, declared structured form with operator-supplied claim | leave-untouched |
| `DEMOTE` | Entry on declared demotion list (any form) | reshape `acw-state.yaml::auto_load_at_session_start` — remove the entry; file itself stays in workspace |
| `REVIEW` | Entry not on canonical list, bare-path legacy form (no declared claim) | `[?]` plan row — operator confirms keep (with structured claim) or demote |

If the workspace's `acw-state.yaml::auto_load_at_session_start` block is in legacy bare-path form entirely, propose ONE consolidated `reshape` plan row that migrates the whole block to structured form with verdicts applied per entry. This avoids N small plan rows for each entry.

If `rules/auto-load-discipline.md` is absent from the workspace's `rules/` directory, propose `write-canonical` per the recommended-blocks registry pass (the rule earned in v0.9.0; instances at `last_reconciled_version` < 0.9.0 will see this as drift).

Plan output format extension — add a new section after "Skills compliance":

```
Auto-load discipline (vs rules/auto-load-discipline.md):
  Current entries: <N>   form: <all-structured | all-legacy | mixed>
  Verdicts:
    KEEP                           : <N>
    KEEP (migrate-to-structured)   : <N>
    KEEP (instance-specific)       : <N>
    DEMOTE                         : <N>
    REVIEW                         : <N>
  Per-entry detail:
    <path>   form: <structured | bare-legacy>   verdict: <KEEP | KEEP (migrate-to-structured) | KEEP (instance-specific) | DEMOTE | REVIEW>   reason: <one-line>
```

The audit verb does not write to `acw-state.yaml`. Demotions and migrations execute under `/acw-instance upgrade`'s single approval gate.

## Meta-layer staleness (conditional)

Run only if `acw-state.yaml::meta_layer` is present and non-empty. For each file listed in `meta_layer`, evaluate the trigger table from `skills/acw-session/references/end.md` § "Meta-layer maintenance" against `last_reconciled_version`. Stale files become plan rows with action `reshape` and the proposed edit inline.

If `meta_layer` is absent or empty, skip silently.

## Migration-plan output format

Print to chat:

```
ACW Instance Audit — <workspace name> (<workspace path>)
Reconciled to ACW <last_reconciled_version> as of <last_reconciled>.
Current ACW canonical: <version-from-fetched-manifest>.
Registration status: <REGISTERED | UNREGISTERED — N canonical signals, M substrate-shaped patterns>.
Substrate boundary: <N> files / <M> directories in scope; <K> project items skipped.
Ambiguous routings: <count of [?] rows>

Migration Plan
──────────────────────────────────────────────────────────────────────

leave-untouched (<N>):
  - <path>

move (<N>):
  - <source path>  →  <canonical destination>
  - ...

reshape (<N>):
  - <path>  (in place)  — <one-line description of the reshape>
  - <source path>  →  <canonical destination>  — <one-line description>

merge (<N>):
  - <source path>  →  <canonical destination>  — <one-line description of merge>

write-canonical (<N>):
  - <canonical destination>  — <source: template | composed from <inputs> | rendered default block>

delete (<N>):
  - <path>  — <reason>

instance-specific (<N>):
  - <path>  — <one-line rationale; will require decision-log entry on upgrade>

absorption-candidate (<N>):
  - <path>  →  ACW _buffer/<proposed candidate filename>  — <pattern summary>

pending-review (<N>; existing divergent_pending_review entries):
  - <path>  — sent <date>; status <pending|absorbed|rejected>

instance-specific-declared (<N>; existing instance_specific_substrate entries):
  - <path>

[?] ambiguous (<N>; operator input required before upgrade):
  - <path>
      candidates:
        a) <action> → <destination>  — <rationale>
        b) <action> → <destination>  — <rationale>

──────────────────────────────────────────────────────────────────────
Recommended-blocks registry pass:
  Gaps to write to acw-state.yaml: <N>
  - <block name>  (earned in v<X>)  → <action>

Skills compliance:
  <N> issues  → see migration plan rows above

Meta-layer staleness (conditional on meta_layer block):
  <N> stale files  → see migration plan rows above

──────────────────────────────────────────────────────────────────────
Pre-upgrade recommendations:
  <if not git-initialized>: Run `git init` and create an initial commit before /acw-instance upgrade.
  <if git-initialized with uncommitted changes>: Commit current state as a pre-migration safety net before /acw-instance upgrade.
  <if [?] rows exist>: Resolve ambiguous routings (run /acw-instance upgrade interactively, or annotate manually) before bulk execution.

Run /acw-instance upgrade to execute this plan.
```

## Plan persistence

Audit does not persist the plan to disk. The plan is reproducible: `/acw-instance upgrade` re-runs the spine and rebuilds the plan from the same inputs. This avoids stale-plan-on-disk failure modes.

If the operator wants the plan saved (for review, sharing, or later execution), they can capture the chat output manually. A future earn-by-incident may add `--save-plan <path>` if persistence becomes load-bearing.

## When NOT to fire (verb-specific)

- Workspace has no substrate at all (orchestrator Step 2 bails first).
- Operator wants only canonical comparison and not pattern walk (not currently supported as a flag; future earn-by-incident if requested).

## Output

Migration plan to chat. Zero writes to the workspace. Zero writes to ACW's `_buffer/` (absorption candidates are proposed, not yet written; the upgrade verb writes them on plan execution).
