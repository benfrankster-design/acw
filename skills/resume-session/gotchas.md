# Gotchas

> **Path resolution.** Throughout, `paths.X` resolves from `acw-state.yaml::paths::X` per the SKILL.md preamble.

- **Globbing `paths.research_queries_dir` must NOT descend into `paths.research_queries_consumed_dir`.** Top-level glob only. Consumed prompts have already been answered and re-loading them wastes context. The `*` pattern in most shells doesn't recurse, but if using a recursive glob library, restrict depth to 1.

- **§5–§7 section detection in session captures relies on `## ` heading patterns.** If a session capture file diverges from the format defined in `references/session-capture-format.md` (in the capture-and-metabolize skill), section parsing may fail. Fall back to whole-file read; do not error out and refuse to load.

- **There is no synthesis subdirectory.** The prompt and its findings live in the same file. Detection of "answered vs. unanswered" is content-based (look for `## Findings` heading), not filename-based. If you see a synthesis directory mentioned in older docs, that is stale and should be corrected.

- **Don't re-read auto-loaded substrate.** The host's auto-load mechanism (per `acw-state.yaml::auto_load_at_session_start`) already loads the canonical substrate. This skill must NOT read those files again. Doing so doubles substrate cost.

- **Session captures' §1–§4 are already in the substrate.** §2 decisions are in `paths.decisions_log`; §3 conceptual shifts are in `paths.evolution`; §4 file changes are in `paths.build_log`. Reading those sections again is duplication. Only §5 (open questions), §6 (verbatim operator directives), and §7 (cleaned transcript) are unique to the capture.

- **Drift check requires `acw-state.yaml::last_reconciled` to be present.** If the field is absent, the drift check assumes the instance is at version 0 and surfaces every recommended block as a gap. That's a noisy first run, but correct — the operator can run `/upgrade-instance` once and the alert quiets thereafter.

- **Hardcoding a path** → Never. Use `paths.X` shorthand. The skill ships in the template and runs in instances that may have different paths declared in `acw-state.yaml::paths`.
