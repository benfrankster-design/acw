# Gotchas — upgrade-instance

> **Path resolution.** Throughout, `paths.X` resolves from `acw-state.yaml::paths::X` per the bookend skills' path-resolution convention. `section_conventions.X` resolves from the target file's frontmatter.

- **Comparing versions vs dates.** `last_reconciled` is a date; `last_reconciled_version` is a semantic version. The drift check uses the version field. Do not compare dates against versions or vice versa. If `last_reconciled_version` is missing from a very old instance state file, treat it as `"0.0.0"` — every recommended block whose earned-in is set will surface as a gap, which is the noisy-but-correct first run.

- **Present-but-empty is a deliberate opt-out.** A block like `template_layer: []` is the operator saying "this instance has no template layer use." Do NOT flag it as missing. Only flag blocks that are completely absent from the state file.

- **`manifest.append` for upsert on dict blocks.** When adding a block like `paths`, the canonical default has multiple keys. Append them one at a time using the `(key, value)` tuple form. Don't try to add the entire block as a single value.

- **Top-level scalar fields may not be supported by `manifest.append`.** `last_reconciled` and `last_reconciled_version` are top-level scalars, not list/dict blocks. `tools/manifest.py` v1 supports only the registered list/dict blocks; for top-level scalars, fall back to a direct edit of the state file (preserve all other content). Document this in the decision-log entry if the fallback is used.

- **Operator may modify a default before adding.** When the operator picks `m` (modify), the resulting block is whatever the operator provides — not necessarily the canonical default. Validate well-formedness (yaml parses, shape matches the registry's "How to add"), but don't enforce equality with the canonical default. The instance is allowed to override.

- **Aborted mid-pass is OK.** Step 4 bumps `last_reconciled_version` only after the full gap pass completes. If the operator quits halfway, the partial writes from Step 3 are kept (additive, safe), but `last_reconciled_version` stays at its old value — so the next `/resume-session` will still surface the remaining gaps. This is correct: don't claim reconciliation that didn't happen.

- **Decision-log id format follows project.code fallback.** If `project.code` is set, use `D-{CODE}-NNN`. If absent, use `D-NNN` (continuing whatever unprefixed numbering the instance already uses). Never invent a prefix.

- **Don't write blocks that aren't in the registry.** The skill writes only blocks declared in `rules/instance-current-manifest.md`. If the operator asks to add an arbitrary block, decline and direct them to add the entry to the registry first (via decision-log entry per `rules/manifest-discipline.md`).

- **Re-running after a successful pass is a no-op.** If `last_reconciled_version` already matches the current ACW version, Step 2 produces an empty gap list and the skill exits at "Instance is already current." That's correct.

- **Partial blocks are honored, not topped up.** If a block has some-but-not-all canonical keys (e.g., `paths` with 2 of 14 keys), Step 2 treats it as PRESENT and skips. Runtime `manifest.load` merges canonical defaults for absent keys at read time, so the partial declaration plus defaults gives full coverage. The skill does not propose adding missing keys to a partial block — that would override the operator's deliberate choice to declare only some keys explicitly.

- **Malformed blocks halt the pass.** A block that exists but has the wrong shape (e.g., `paths: "not-a-dict"`, or `template_layer:` declared as a dict instead of a list) is a state-file integrity problem, not a drift gap. Step 2 stops and asks the operator to fix `acw-state.yaml` by hand before re-running. Don't attempt shape repair — repairs are operator decisions, and the skill's job is reconciliation, not validation cleanup.
