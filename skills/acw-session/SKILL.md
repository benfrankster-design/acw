---
name: acw-session
description: >
  Object-centered orchestrator for the ACW session lifecycle. Three verbs
  over one shared spine: `start` (load context for a new session, initialize
  the active capture file, surface state, read buffer, run drift check),
  `update` (mid-session checkpoint — append timestamped note to the active
  capture file), and `end` (capture transcript, distribute findings into
  substrate, metabolize stale entries, optionally append a synapse session
  log, optionally build a next-session research prompt). Both `start` and
  `end` read the full spine; `update` reads only `paths.session_captures_dir`.

  `end` defaults to **quick mode** (Phase 1 + minimal Phase 2 + Phase 3
  auto-update sweep, Haiku-grade). `/acw-session end full` runs all five
  phases as previously documented. `--synapse` and `--research` flags
  surface their respective phases inside quick mode.

  Replaces /resume-session, /capture-and-metabolize, and /capture-session
  from prior versions. Triggered by the operator running /acw-session
  start, update, or end. Never fires automatically.

  Produces, per verb: state surfacing and drift report (start), one
  appended note to the active capture file (update), or up to five
  artifacts in the instance's substrate (end).
role: orchestrator
capabilities: []
model: claude-haiku-4-5
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# acw-session

Object-centered orchestrator. Object: this ACW instance's session lifecycle. Verbs: boundary operations on it.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `start` | Loads context for a new session. Initializes the active capture file (`sessions/YYYY-MM-DD--<name>.md`) and writes its path to `<sessions_dir>/.current-session`. Reads recent captures, runs drift check against `rules/instance-current-manifest.md`, surfaces unread `_buffer/` notifications, reports state to the operator. | `references/start.md` |
| `update` | Mid-session checkpoint. Reads `.current-session`; if missing, self-bootstraps. Appends a timestamped note under `## Updates` in the active capture file. Cheap by design — Haiku-grade end-to-end, no metabolize, no distribute. | `references/update.md` |
| `end` | Default: **quick mode** — Phase 1 (capture) + minimal Phase 2 (append-only writes only) + Phase 3 auto-update sweep. `/acw-session end full` runs all five phases as previously documented. `/acw-session end [quick] --synapse` and `/acw-session end [quick] --research` surface those phases inside quick mode. Always clears `.current-session` on completion. | `references/end.md` |

Routing rules: argument required. `/acw-session` with no command prints the table. Unknown command errors with the table.

### Tracker convention — `.current-session`

The active capture file is tracked via a single tiny file at `<paths.session_captures_dir>/.current-session`. Contents: one line — the relative filename of the active capture (e.g., `2026-05-04--bookend-efficiency.md`).

- **`start`** writes the tracker (and creates the capture file).
- **`update`** reads the tracker (or self-bootstraps if missing).
- **`end`** clears the tracker (writes empty content, preserves file as a marker of "no active session").

The tracker exists only because `update` needs to know which file to append to without taking the filename as an argument. Pure machine state; never read by humans. Stays in `.gitignore` if the instance considers its presence noise; default is to commit it.

## Shared spine (every verb runs these in order)

### Step 1 — Read configuration from `acw-state.yaml`

Read once and resolve:

- `paths` → substrate file locations. Read keys via `tools/manifest.py::load(state_file, "paths")`, which merges file overrides with canonical defaults.
- `auto_load_at_session_start` → files already in context; never re-read inside this skill.
- `project.code` / `project.name` / `project.domain` → optional; used for id prefixing and narrative output. If absent, fall back to unprefixed ids (`D-NNN`) and the repo's directory name.
- `synapse_log_path` → optional Phase 4 destination for the `end` verb. Null/absent disables Phase 4 silently.
- `cross_repo_writes` → list of paths outside the project repo this skill may write to.
- `voice` → list of voice-reference files for transcript cleanup.
- `template_layer` / `instance_layer` / `meta_layer` → if present and non-empty, three-layer manifest discipline applies.
- `is_canonical_source` → boolean, default `false`. Gates the canonical-edit detection branch in the `end` verb.
- `divergent_pending_review` / `instance_specific_substrate` → respected by drift check in `start` and substrate handling in `end`.

### Step 2 — Resolve substrate locations

For each substrate key needed by the active verb, resolve the path via the merged `paths` view from Step 1. Never hardcode paths. Section headings inside substrate files resolve via `section_conventions.<name>` per each file's frontmatter (with documented defaults).

### Step 3 — Check `_buffer/` for cross-project notifications

Walk `paths.buffer_dir` (top level only; do not descend into a `_read/` subdirectory). For each file present:

- Read its frontmatter and a one-line summary.
- Note whether `read: false` or absent (treat as unread).
- Pass the buffer state to the active verb.

If `paths.buffer_dir` does not exist, skip silently — the lattice handoff design assumes its presence but a workspace can run without one.

### Step 4 — Read recent session captures (cap at 3)

The active verb may need recent-session context. Walk `paths.session_captures_dir` for the 3 most recent capture files (sorted by filename / date). Pass their paths to the verb; verb decides whether to read content.

### Step 5 — Verb dispatch

The orchestrator hands off to the verb's reference file. Verbs consume the spine output (config, paths, buffer state, recent captures) and execute their specialist work.

## When NOT to fire

- `start` mid-session — defeats the bookend purpose; use only at session-start.
- `end` before substantive work has accumulated — wait until decisions, conceptual shifts, or completed work exist to capture.
- `end` for conversation-only sessions with no decisions, no shifts, no completions.
- Either verb when the operator explicitly says "don't capture this session."

## Safety

- Spine is read-only on substrate. All writes happen in verb-specific specialist work, gated per the verb's reference file.
- Cross-repo writes refuse without `cross_repo_writes` declaration.
- Append-only files (build-log, incidents, evolution, captures, Done blocks) are never edited past entries.
- The `end` verb's canonical-edit detection branches on `is_canonical_source` per `rules/instance-current-manifest.md` — publishers prompt for version bump and push; consumers warn that local edits won't propagate.

## Output

Per verb. See reference files.
