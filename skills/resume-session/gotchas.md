# Gotchas

- **Globbing `research/queries/*.md` must NOT descend into `_consumed/`.** Top-level glob only. Consumed prompts have already been answered and re-loading them wastes context. The `*` pattern in most shells doesn't recurse, but if using a recursive glob library, restrict depth to 1.

- **§5–§7 section detection in session captures relies on `## ` heading patterns.** If a session capture file diverges from the format defined in `references/session-capture-format.md` (used by `/capture-and-metabolize`), section parsing may fail. Fall back to whole-file read; do not error out and refuse to load.

- **There is no `research/synthesis/` directory.** The prompt and its findings live in the same file. Detection of "answered vs. unanswered" is content-based (look for `## Findings` heading), not filename-based. If you see the synthesis directory mentioned in older docs, that is stale and should be corrected.

- **Don't re-read auto-loaded substrate.** CLAUDE.md `@`-imports already load decisions, hard rules, tasks-status, glossary, evolution, sources, research-state, problem-framing, and incidents. This skill must NOT read those files again. Doing so doubles substrate cost.

- **Session captures' §1–§4 are already in the substrate.** §2 decisions are in decision-log; §3 conceptual shifts are in evolution; §4 file changes are in build-log. Reading those sections again is duplication. Only §5 (open questions), §6 (verbatim operator directives), and §7 (cleaned transcript) are unique to the capture.
