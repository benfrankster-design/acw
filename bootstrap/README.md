---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Bootstrap — Greenfield Instantiation

This folder is how you stand up a new ACW instance from nothing. If you already have an existing workspace you want to bring under ACW discipline, go to `migration/` instead.

## Prerequisites

- Python 3.9 or newer
- Git
- A markdown-capable text editor
- A UTF-8 terminal

Nothing else. No database, no daemon, no external services. ACW is plain-text infrastructure by design.

## Step 1 — Clone and initialize

Clone ACW to a new directory, remove the existing `.git` if present, and initialize your own:

```
git clone <acw-source> my-instance
cd my-instance
rm -rf .git
git init
```

## Step 2 — The seven-question interview

Before you touch any file, answer these eight questions in writing. Paste the answers into `decisions/decision-log.md` under "Decisions and Rationale" as your first entry. They will drive every subsequent edit.

1. **What is the name of this instance?** A short identifier, not a sentence. This name goes into commit messages, decision-log headers, and any future export.
2. **What kind of instance is this?** See `research/07-instance-types.md` for the full framework. The short version: does this workspace accumulate state (knowledge, vocabulary, assets that persist across sessions), or is it a session-scoped console that reads from and writes to other systems? If it accumulates state, it's a **full instance** — proceed with all eight questions. If it's a session-scoped console, it's a **cockpit** — apply universal hygiene only (roles, headers, incidents.jsonl, hard rules) and skip canon, deferred library, and research scaffolding. If you're unsure, start as a full instance — you can always strip scaffolding later, but you can't recover lost incident data.
3. **What domains?** Between four and eight mutually exclusive areas of work this instance covers. Domains are the top-level MECE partition. If you cannot name them without overlap, stop and think harder — overlap here cascades into every downstream primitive.
4. **What surfaces?** The read and write targets this instance will touch. Examples: a folder on disk, a ticketing system, a chat surface, a docs surface. List each one explicitly. Unknown surfaces are future incidents.
5. **What hard rules are non-negotiable?** Things that are stop-work if violated. A read-only directory, a forbidden write path, a forbidden external call. Every hard rule goes into `rules/instance-hard-rules.md` with a decision-log pointer.
6. **What is your primary agent?** The model or agent that will be reading this workspace. ACW ships as AGENTS.md rather than a vendor-specific file so the workspace is portable, but you still need to name the primary consumer for capability scoping.
7. **What authority set?** The valid values for `approval_authority` in your canon. Single-operator default is `operator`. Multi-tier instances declare their own set. See `rules/canon-governance.md` for three worked examples.
8. **When and how often will you review the incident log and run the lint?** The earn-by-incident discipline only works if the incident log is actually reviewed. Put a recurring calendar entry on your schedule — weekly at minimum, daily for the first month. Without this review cadence, ACW degrades into documentation instead of governance.

## Step 3 — Fill in `rules/instance-hard-rules.md`

Declare your `authority_set`, your `domains`, and your first hard rules. Every rule references its decision-log entry. If you do not have a decision-log entry for a rule, write the entry first and the rule second.

## Step 4 — Seed `rules/canon.yaml`

Start with five to ten concepts that already exist in your head as load-bearing. Do not try to enumerate your entire vocabulary on day one. The canon grows by incident — when a drift is caught, the term gets added.

## Step 5 — Run the lint

```
python tools/lint-vocab.py glossary.md --content-dir .
```

Exit code 0 means clean. Exit code 1 means you have forbidden synonyms in committed content — fix them or update the canon. Exit code 2 means bad input.

## Step 6 — Run the tests

```
python -m unittest discover tests
```

All tests should pass on an unmodified ACW clone. If any fail on your platform before you have edited anything, that is an incident — log it.

## Step 7 — Commit v0.1.0-instance

```
git add .
git commit -m "bootstrap: v0.1.0 instance of ACW for <instance-name>"
git tag v0.1.0-instance
```

## Step 8 — Schedule the review

Per question 7, put the review cadence on your calendar. This is the single most important step and the one most likely to be skipped. Without it, every other step here was theater.
