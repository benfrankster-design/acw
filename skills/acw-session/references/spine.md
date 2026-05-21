---
scope: shared
---

# Shared spine

Every `/acw-session` verb runs these steps in order before its specialist work. Verb references load this file first.

## Tracker convention — `.current-session`

Active capture file tracked at `<paths.session_captures_dir>/.current-session`. Schema (YAML):

```yaml
file: 2026-05-12--my-session.md
session_hash: <sha256 of capture contents after Phase 1>
last_completed_phase: 0   # 0 → 1 → 2 → 3 → (4|5) → cleared
```

Backward compat: plain single-line filename is also accepted (treated as `{file: <line>, session_hash: null, last_completed_phase: 0}`).

- `start` writes tracker + creates capture file (phase 0).
- `update` reads (or self-bootstraps if missing); does not modify `last_completed_phase`.
- `end` updates `last_completed_phase` after each phase; on re-invocation, phases with `phase_num <= last_completed_phase` AND matching `session_hash` are skipped (idempotency); clears tracker after Phase 5 or last phase that ran.

Tracker is pure machine state; default commit; instances may `.gitignore`.

## Step 0 — Pre-flight context-budget check

Heuristic-estimate context usage. If >70% AND verb is `end`: abort with `[acw-session abort] Context at ~<N>%. /compact first, then retry. For minimal capture: /acw-session end log-only.` If >70% AND verb is `start`: warn but continue. `update`: continue.

## Step 1 — Read config from `acw-state.yaml`

Read via `tools/manifest.py::load`. Block semantics live in `rules/instance-current-manifest.md`. Blocks consumed: `paths`, `decision_tracking.mode`, `glossary.mode`, `auto_load_at_session_start`, `project.{code, name, domain}`, `synapse_log_path`, `cross_repo_writes`, `voice`, `template_layer` / `instance_layer` / `meta_layer`, `is_canonical_source`, `divergent_pending_review`, `instance_specific_substrate`.

Mode consistency: cross-check present `paths.*` key set against `decision_tracking.mode` / `glossary.mode`; warn on mismatch.

## Step 2 — Resolve substrate locations

Resolve every substrate path the active verb needs via the merged `paths` view from Step 1. Never hardcode. Section headings inside single-file substrate resolve via `section_conventions.<name>` from each file's frontmatter. Wiki mode uses folder structure as the convention.

## Step 3 — Check `_buffer/`

Walk `paths.buffer_dir` (top level only; skip `_read/`). Read frontmatter + one-line summary per file. Pass to verb. Skip silently if dir absent.

## Step 4 — Read recent session captures

Walk `paths.session_captures_dir`; collect 3 most recent paths (by filename / date). Pass paths to verb; verb decides whether to read content. Spine does not read content.

## Step 5 — Verb dispatch

Hand spine output (config, paths, mode flags, buffer state, recent captures) to the verb's reference. Verb's reference declares which additional references to load — spine itself loads none.

## Safety

- Spine is read-only on substrate. All writes happen in verb-specific work.
- Cross-repo writes refuse without `cross_repo_writes` declaration.
- Append-only files (`build_log`, `incidents`, `evolution`, captures, `<paths.archives_dir>/tasks-status/YYYY-MM.md`, wiki-mode decision entries past acceptance) are never edited past entries.
- `end` canonical-edit detection branches on `is_canonical_source` (publishers prompt for version bump + push; consumers warn local edits won't propagate).
- Idempotency: `end` uses `.current-session` resume token to skip phases already completed in a hash-matching prior run.

## When NOT to fire

- `start` mid-session.
- `end` before substantive work has accumulated.
- `end` for conversation-only sessions.
- Either verb when operator explicitly says "don't capture this session."
