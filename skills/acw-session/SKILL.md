---
name: acw-session
description: >
  Object-centered orchestrator for the ACW session lifecycle. Three verbs
  (`start`, `update`, `end`) over one shared spine. `start` initializes the
  active capture file and surfaces drift; `update` appends a mid-session note;
  `end` distributes, metabolizes, and (per profile) writes synapse log /
  research prompt. Mode-portable: branches on `decision_tracking.mode` and
  `glossary.mode` (single-file | wiki). `end` profiles: quick (default), full,
  log-only, synapse-only, research-only. Triggered by operator invocation only.
  Produces per verb: state surface + drift report (start), one appended note
  (update), or up to five artifacts (end).
role: orchestrator
capabilities: []
model: claude-haiku-4-5
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# acw-session

Object-centered orchestrator. Object: this ACW instance's session lifecycle. Verbs: boundary operations on it. **Substrate-shape portable** — operations on decisions and glossary branch on `acw-state.yaml::decision_tracking.mode` and `glossary.mode`.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `start` | Loads context, initializes active capture file + tracker, runs drift check, surfaces buffer. | `references/start.md` |
| `update` | Mid-session checkpoint. Reads `.current-session` (self-bootstraps if missing); appends a timestamped note. Haiku-grade, no metabolize. | `references/update.md` |
| `end` | Profile-dispatched: `quick` (default) / `full` / `log-only` / `synapse-only` / `research-only`. Always clears `.current-session` on completion. | `references/end.md` |

Routing rules: argument required. `/acw-session` with no command prints the table. Unknown command errors with the table.

## Tracker convention — `.current-session`

The active capture file is tracked via a single file at `<paths.session_captures_dir>/.current-session`. Schema (YAML one-line or multi-line):

```yaml
file: 2026-05-12--my-session.md
session_hash: <sha256 of capture contents after Phase 1>
last_completed_phase: 0   # updated as end progresses: 0 → 1 → 2 → 3 → (4|5) → cleared
```

For backward compat: a plain single-line filename (no YAML) is also accepted — treated as `{file: <line>, session_hash: null, last_completed_phase: 0}`.

- **`start`** writes the tracker (and creates the capture file). `last_completed_phase: 0`.
- **`update`** reads the tracker (or self-bootstraps a fresh one if missing). Does not modify `last_completed_phase`.
- **`end`** updates `last_completed_phase` after each phase. On re-invocation, phases with `phase_num <= last_completed_phase` AND matching `session_hash` are skipped (idempotency). After Phase 5 (or last phase that ran), clears tracker by writing empty content.

The tracker is pure machine state; humans don't read it. Default is to commit it; instances may `.gitignore` it.

## Shared spine

Every verb runs spine steps in order. Spine is read-only on substrate. **The spine never loads reference files beyond what the active verb needs** (verb-scoped reference loading: spine resolves config and paths, verb's reference file declares which other refs to load).

### Step 0 — Pre-flight context-budget check

Before any other spine work, verify available context. If a context-token tool is available, query it; otherwise heuristic-estimate from auto-load size + conversation length. If context is >70% consumed AND verb is `end`, abort with operator-facing message:

```
[acw-session abort] Context at ~<N>% before skill spine fired. /compact first (or "/compact focus on the current session"), then retry. For minimal capture without distribution: /acw-session end log-only.
```

If context >70% AND verb is `start`, warn but continue (`start` is cheap). If verb is `update`, continue (lightest verb).

### Step 1 — Read configuration from `acw-state.yaml`

Read once and resolve:

- `paths` → substrate file locations. Read via `tools/manifest.py::load(state_file, "paths")` which merges file overrides with canonical defaults. **Two key sets supported:**
  - **Single-file shape:** `decisions_log`, `glossary` keys present.
  - **Wiki shape:** `decisions_index`, `decisions_entries_dir`, `decisions_open_questions_dir`, `decisions_constraints_dir`, `glossary_index`, `glossary_entries_dir` keys present.
  - The keys present determine which substrate mode is active (cross-checked against `decision_tracking.mode` and `glossary.mode` for consistency; warn on mismatch).
- `decision_tracking.mode` → `single-file` (default) or `wiki`. Drives Phase 2 + Phase 3 dispatch in `end`.
- `glossary.mode` → same.
- `auto_load_at_session_start` → already in context; never re-read.
- `project.code` / `project.name` / `project.domain` → optional; for id prefixing and narrative output.
- `synapse_log_path` → optional Phase 4 destination.
- `cross_repo_writes` → list of paths outside the project repo this skill may write to.
- `voice` → list of voice-reference files for transcript cleanup.
- `template_layer` / `instance_layer` / `meta_layer` → if non-empty, three-layer manifest discipline applies.
- `is_canonical_source` → boolean, default `false`. Gates canonical-edit detection in `end`.
- `divergent_pending_review` / `instance_specific_substrate` → respected by drift check in `start` and substrate handling in `end`.

### Step 2 — Resolve substrate locations

For each substrate key needed by the active verb, resolve the path via the merged `paths` view from Step 1. Never hardcode paths. **Section headings inside single-file substrate resolve via `section_conventions.<name>` per each file's frontmatter.** In wiki mode, section headings don't apply — folder structure is the convention.

### Step 3 — Check `_buffer/` for cross-project notifications

Walk `paths.buffer_dir` (top level only; skip `_read/`). For each file: read frontmatter and one-line summary. Pass buffer state to active verb. If `paths.buffer_dir` doesn't exist, skip silently.

### Step 4 — Read recent session captures (cap at 3, paths only)

Walk `paths.session_captures_dir` for the 3 most recent capture files (sorted by filename / date). Pass paths to the verb; verb decides whether to read content. **Spine does not read content.**

### Step 5 — Verb dispatch

Hand off to the verb's reference file. Verb consumes spine output (config, paths, mode flags, buffer state, recent captures). The verb's reference file declares which additional references to load — spine itself loads none.

## When NOT to fire

- `start` mid-session — defeats the bookend purpose; use only at session-start.
- `end` before substantive work has accumulated — wait for decisions, conceptual shifts, or completed work.
- `end` for conversation-only sessions with no decisions, no shifts, no completions.
- Either verb when operator explicitly says "don't capture this session."

## Safety

- Spine is read-only on substrate. All writes happen in verb-specific specialist work, gated per the verb's reference file.
- Cross-repo writes refuse without `cross_repo_writes` declaration.
- Append-only files (build-log, incidents, evolution, captures, tasks-status archive `tasks-status-YYYY-Q*.md`, wiki-mode decision entries past acceptance) are never edited past entries.
- The `end` verb's canonical-edit detection branches on `is_canonical_source` — publishers prompt for version bump and push; consumers warn that local edits won't propagate.
- **Idempotency.** `end` uses the `.current-session` resume token to skip phases already completed in a hash-matching prior run. Re-running `end` after a crash resumes from the last completed phase.

## Output

Per verb. See reference files.

**Every `end` invocation emits a run banner** (first line) and **per-phase status lines** (`RAN | SKIPPED(reason) | FAILED(error)`) so the operator can see exactly what happened, including silently-skipped phases.
