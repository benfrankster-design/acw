---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# Vocabulary Lint — How `tools/lint-vocab.py` Decides

**Version:** 0.1.0
**Status:** Normative. Describes the rule set the vocabulary lint tool enforces.

---

## What the lint tool does

`tools/lint-vocab.py` is a regex-based linter that walks a content directory and flags any occurrence of a forbidden synonym defined in `glossary.md` or, optionally, a `hidden_labels` entry in `rules/canon.yaml`. It does not mutate content. It reports violations and exits non-zero if any are found.

---

## Inputs

The tool takes one required argument and two optional arguments:

- **`<glossary.md>`** (required) — path to the glossary file. The tool parses this file for term blocks and extracts `forbidden synonyms:` lines.
- **`--canon <path>`** (optional) — path to a canon.yaml file. If supplied, the tool loads the file and extracts `hidden_labels` for all entries whose status is `approved`. Hidden labels from draft, proposed, or deprecated entries are ignored.
- **`--content-dir <path>`** (optional, default: current directory) — directory to walk. All `.md` files under this directory are scanned.

---

## Rule set

1. **Forbidden-synonym detection.** For each term in `glossary.md` that has a `forbidden synonyms:` line, every synonym on that line becomes a regex pattern. A content file containing any of those patterns emits a violation.

2. **Hidden-label detection.** If `--canon` is supplied, every string in a `hidden_labels` list of an approved canon entry becomes a regex pattern. Same rule as forbidden synonyms.

3. **Word-boundary matching.** All patterns are wrapped in `\b` word boundaries so `doc` does not match inside `document` or `docker`. Operators can bypass this by escaping the intent in a term definition.

4. **Case-insensitive by default.** Lint matches are case-insensitive. To require case-sensitivity on a specific term, the operator adds a `(case-sensitive)` annotation on the synonym line.

5. **UTF-8 only.** Files are opened with explicit `encoding='utf-8'`. A file that fails to decode as UTF-8 causes the lint to exit code 2 (bad input) and report the offending path.

---

## Exit codes

- **0** — clean. Zero violations across all scanned files.
- **1** — violations found. The tool prints one line per violation in the form `file:line:column: synonym 'X' (use 'Y')`.
- **2** — bad input. One of: missing glossary file, malformed glossary, malformed canon.yaml, UTF-8 decoding failure, missing content directory.

---

## Output format

Violations are printed one per line. Each line has the shape:

```
<relative-path>:<line-number>:<column>: forbidden synonym '<found>' (canonical: '<term>')
```

At the end of a run, a summary line:

```
Scanned N files, found M violations in K files, 0.XXs
```

All output goes to stdout. Errors go to stderr.

---

## What the lint does NOT do

- It does not rewrite content. Fixing is manual.
- It does not enforce capitalization beyond what the synonym literal specifies.
- It does not understand context (a quoted occurrence of a forbidden synonym inside a code block is still flagged — the lint is intentionally strict).
- It does not check the canon schema itself. That is the job of a canon-schema validator, which is deferred.
- It does not understand markdown structure beyond line-level regex. An operator whose glossary terms overlap with code-block content should either rename the term or use word-boundary tricks.

---

## Performance notes

The lint is O(files × terms × content-length). On a workspace with 100 files and 50 terms, expect sub-second runtime. On a workspace with 10000 files, expect a few seconds. The tool is single-process; concurrent invocations are the caller's responsibility.

---

## When to run

- **Pre-commit hook.** The canonical place. A lint failure blocks the commit.
- **Ad-hoc.** Before opening a pull request.
- **Post-edit.** After a bulk find-and-replace operation that introduced new terms.

---

## Extension path

When the `tools/lint-vocab.py` regex approach becomes insufficient (for example, when the operator wants to enforce canonical ordering, cross-reference hygiene, or structural canon rules), the successor tool is a canon-schema validator documented in `DEFERRED.md` under the `contract-registry` and `conformance-test` primitives.

---

## Changelog

- **v0.1.0 — 2026-04-11** — Initial release. Regex-based, UTF-8, word-boundary, case-insensitive by default, exit codes 0/1/2.
