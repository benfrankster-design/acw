# Gotchas

- **Prose-mention false positives.** Code blocks, URLs, and quoted text inside an entry can contain ID-shaped strings that aren't real references. Strip code blocks and URLs before regex-matching. Still expect occasional noise; flag low-confidence prose mentions with confidence ≤ 0.4 and let the operator triage.

- **Output is overwritten, not appended.** `.acw/substrate-map.md` is fully regenerated each run. Operator hand-edits to the rendered file are lost on next run. Operator-authored navigation notes belong in entries, not in the map.

- **Performance on large substrate.** Instances with thousands of entries will produce a long rendered file. Use `--module=` or `--node=` filters for targeted views. Future enhancement (deferred): split the rendered output into per-module files if the single-file render exceeds ~5000 lines.

- **Frontmatter parser brittleness.** YAML frontmatter with non-standard indentation or unicode quirks can fail parse. Skill emits a warning per failed entry but continues. Operator fix is to clean up the frontmatter in the offending entry.

- **AMBIGUOUS edges accumulating.** If the skill repeatedly reports the same AMBIGUOUS edges across runs without resolution, that's a signal the operator should triage them or the LLM-inferred ambiguity detection is too sensitive. Adjust thresholds or resolve substrate; don't silently filter.

- **Confusion with /codemap.** Operator may invoke `/substrate-map` expecting code navigation; the skill covers substrate (decisions/glossary/incidents), not source code structure. Codemap is `/codemap`. Both can run; they don't overlap.
