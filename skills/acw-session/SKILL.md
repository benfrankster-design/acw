---
name: acw-session
description: >
  Object-centered orchestrator for the ACW session lifecycle. Two verbs over
  one shared spine: `start` (load context for a new session, surface state,
  read inbox, run drift check) and `end` (capture transcript, distribute
  findings into substrate, metabolize stale entries, optionally append a
  synapse session log, optionally build a next-session research prompt).
  Both verbs read the same setup spine — auto-load files, paths, inbox,
  recent captures — before specialist work fires.

  Replaces /resume-session and /capture-and-metabolize from prior versions.
  Triggered by the operator running /acw-session start at session-start or
  /acw-session end at session-end. Never fires automatically.

  Produces, per verb: state surfacing and drift report (start) or up to
  five artifacts in the instance's substrate (end).
role: orchestrator
capabilities: []
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# acw-session

Object-centered orchestrator. Object: this ACW instance's session lifecycle. Verbs: boundary operations on it.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `start` | Loads context for a new session. Reads recent session captures, runs drift check against `rules/instance-current-manifest.md`, surfaces unread `_inbox/` notifications, reports state to the operator. Read-only on substrate. | `references/start.md` |
| `end` | Five-phase pass: capture transcript, distribute findings into substrate, metabolize stale entries, optional synapse session log, optional next-session research prompt. Edits substrate per its discipline rules. | `references/end.md` |

Routing rules: argument required. `/acw-session` with no command prints the table. Unknown command errors with the table.

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

### Step 3 — Check `_inbox/` for cross-project notifications

Walk `paths.inbox_dir` (top level only; do not descend into a `_read/` subdirectory). For each file present:

- Read its frontmatter and a one-line summary.
- Note whether `read: false` or absent (treat as unread).
- Pass the inbox state to the active verb.

If `paths.inbox_dir` does not exist, skip silently — the lattice handoff design assumes its presence but a workspace can run without one.

### Step 4 — Read recent session captures (cap at 3)

The active verb may need recent-session context. Walk `paths.session_captures_dir` for the 3 most recent capture files (sorted by filename / date). Pass their paths to the verb; verb decides whether to read content.

### Step 5 — Verb dispatch

The orchestrator hands off to the verb's reference file. Verbs consume the spine output (config, paths, inbox state, recent captures) and execute their specialist work.

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
