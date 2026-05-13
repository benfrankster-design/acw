# Gotchas

- **Spine missing `_buffer/`.** If `paths.buffer_dir` doesn't exist, Step 3 of the spine skips silently. → Run `/acw-instance upgrade` to backfill `_buffer` or create `_buffer/.gitkeep` manually.

- **Substrate-mode mismatch between `paths` keys and `decision_tracking.mode` / `glossary.mode`.** If `paths.decisions_log` is set (single-file mode) but `decision_tracking.mode: wiki`, or vice versa, the skill emits a warning and prefers the mode field. → Reconcile `acw-state.yaml`: either migrate substrate to match the mode or revert the mode field. The skill never silently picks one shape over the other when both signals exist.

- **`end` verb edits canonical file in a child instance.** If `is_canonical_source` is false (the default), the warning fires but the skill doesn't block the edit. → Operator's responsibility to back the edit out, or raise it upstream in ACW for absorption.

- **`end` Phase 2 attempts cross-repo write without `cross_repo_writes` declaration.** Phase 2 refuses the write and surfaces the path. → Declare the path in `acw-state.yaml::cross_repo_writes`, then re-run `/acw-session end` (resume token will pick up where it left off).

- **`start` verb's drift check runs against stale local cache.** Drift comparison uses `rules/instance-current-manifest.md` from the local copy (refreshed by `/acw-instance upgrade`). → Run `/acw-instance upgrade` periodically.

- **Phase 5 fired when nothing to research — FIXED.** Phase 5 now checks Track A and Track B emptiness before surfacing the operator prompt. Both empty → emit `[phase5] SKIPPED(empty-tracks)` and exit. Track C alone never justifies firing.

- **Manifest classification skipped silently.** If `template_layer` / `instance_layer` / `meta_layer` blocks are absent or empty, Phase 2's classification step doesn't fire. → Declare the blocks in `acw-state.yaml`, or accept the silent skip. The run banner now shows `[phase2] SKIPPED(manifest-classification, blocks-empty)` so the skip is visible.

- **Sonnet subagent (`session-end-judgment`) cold-cache penalty.** First invocation in a session rebuilds cache. → Acceptable cost for judgment-quality gain; the alternative (uniform Sonnet for whole skill) overpays for mechanical Phases 1-2. If the subagent fires twice (Phase 3 + Phase 5), it benefits from warm cache between the two within the 5-minute TTL window.

- **Resume token mismatch after manual substrate edits.** If the operator edits substrate between phases of a single `end` run, the resume token's `session_hash` will not match on re-invocation. The skill re-runs from Phase 1 (safe: idempotent writes per content-hash dedup). → Don't hand-edit substrate mid-`end`; let the skill finish or use `--force-restart` (not implemented; manual fix is to clear `.current-session`).

- **Pre-flight context check estimate is heuristic.** If no `/context`-equivalent tool is available, the skill estimates from auto-load size + conversation length. May underestimate. → If `end` aborts with the context warning at ~70%, trust the abort; run `/compact focus on the current session` and retry.

- **`paths.decisions_log` still in older `acw-state.yaml`.** Instances that adopted the skill before D-CMD-025 (wiki migration) have the old key. The skill's spine accepts both key sets and infers mode from which keys are present (cross-checking `decision_tracking.mode`). New instances should declare `decision_tracking.mode` explicitly.
