---
class: absorption-candidate
authority: instance
stability: proposed
date: 2026-05-21
origin_instances:
  - cs-ops-spec (D-COPS-035, C-COPS-001, OQ-COPS-019)
  - cs-atlas (D-CATL-001, single-file decision log)
operator: Ben Frank
proposes: convention change
scope: substrate-shape (cross-cutting)
review_status: pending
---

# Absorption Candidate — Relocate ACW Operator-Metadata Substrate Under `.acw/` Dotfolder

## TL;DR

Two downstream instances (cs-ops-spec and cs-atlas) independently adopted a convention where all ACW operator-metadata substrate lives under a single `.acw/` dotfolder at the project root, rather than scattered flat at root. **Companion rename:** `_buffer/` is renamed to `raw/` to align with the enrichment-vs-memory principle (raw → metabolize → enriched). The `acw-state.yaml` path key `buffer_dir:` is correspondingly renamed to `raw_dir:`.

This recommendation proposes ACW canonical absorb both changes so they become standard across all instances on the next `/acw-instance upgrade`.

## The convention

```
<project>/
├── .acw/                                # all ACW operator-metadata substrate
│   ├── acw-state.yaml
│   ├── decisions/
│   │   ├── entries/
│   │   ├── open-questions/
│   │   ├── constraints/
│   │   └── INDEX.md
│   ├── glossary/
│   │   ├── entries/
│   │   └── INDEX.md
│   ├── sessions/
│   │   ├── YYYY-MM-DD--*.md
│   │   └── .current-session
│   ├── raw/                             # was _buffer/ — renamed in this proposal
│   ├── plans/
│   ├── deferred/
│   ├── briefings/
│   ├── inbox/
│   ├── archives/
│   ├── build-log.md
│   ├── incidents.jsonl
│   ├── tasks-status.md
│   ├── DEFERRED.md
│   └── CHANGELOG.md
│
├── rules/                               # NOT moved (see "Open question" below)
├── AGENTS.md, CLAUDE.md, README.md      # entry-point docs, root
└── <project-specific content>           # code, data, research artifacts, etc.
```

## Rationale

**1. Convention familiarity.** Dotfolders signal "tooling state, not artifact" universally. `.git/` holds git state. `.github/` holds CI config. `.vscode/` holds editor config. `.claude/` holds Claude Code config. ACW operator substrate is the same shape of thing — metadata about the project, managed by tooling — and following the convention removes a category of mental friction.

**2. Public-facing repo legibility.** Anyone who clones an instance to consume the artifact (Robert reading cs-atlas to build the MCP server, a future engineer reading cs-ops-spec to implement the spec) sees only the artifact at root. The operator's working memory — decision-by-decision history, session captures, in-progress tasks, raw research notes — is hidden behind a dotfolder where it doesn't compete for attention.

**3. Single mass to ignore or exclude.** One `.gitignore` line, one `pyproject.toml` exclude rule, one `rsync --exclude='.acw/'` shipping rule. Today, an instance that wants to publish or distribute its artifact has to enumerate every substrate dir individually. After absorption, it's one rule.

**4. Editor access unchanged.** Obsidian, VS Code, JetBrains IDEs, vim — none of them care that the folder starts with a dot. Hiding is a file-browser-time behavior, not an editor-time behavior. Operators continue working in the substrate exactly as before.

**5. Tooling configurability already exists.** ACW skills read paths from `acw-state.yaml`'s `paths:` block. Re-pointing every key with a `.acw/` prefix is a one-line-per-key edit. Skill code itself does not need to change.

## Migration mechanics (proven in the two downstream instances)

Per-instance:

```bash
mkdir -p .acw
git mv decisions glossary sessions _buffer plans deferred briefings inbox \
       acw-state.yaml build-log.md incidents.jsonl tasks-status.md \
       DEFERRED.md CHANGELOG.md .acw/
git mv .acw/_buffer .acw/raw          # companion rename
```

Then edit `.acw/acw-state.yaml`:
- `paths:` block — prefix every value with `.acw/` except `threat_model:` and any project-artifact paths
- `auto_load_at_session_start:` block — prefix every `.acw/`-scoped path
- `canonical_runtime_files:` — same

Git history is preserved across the move (rename detection fires for unchanged files; high-change files still trackable via `git log --follow`).

## What stays at root (and why)

| Path | Reason it stays |
|---|---|
| `rules/` | Load-bearing convention; many ACW skills hard-code `rules/...` paths. Migration requires either adding `rules_dir` to `acw-state.yaml::paths` and updating every skill, or a canonical change at the ACW level. **Filed as an open question** in cs-ops-spec (OQ-COPS-019) — answer should land here. |
| Entry-point docs (`AGENTS.md`, `CLAUDE.md`, `README.md`) | Must be discoverable on clone. |
| Project artifact directories | Whatever the instance actually produces (code, spec, catalogs, etc.) — those are not ACW metadata. |
| Project-domain reference files | Per-instance call; e.g., `threat-model.md` in cs-ops-spec is the spec's threat model, not ACW machinery. |

## Cross-references

- **cs-ops-spec:** D-COPS-035 (decision), C-COPS-001 (constraint), OQ-COPS-019 (rules/ migration question).
- **cs-atlas:** D-CATL-001 (decision, in single-file `.acw/decisions/decision-log.md`).
- Both migrations done 2026-05-21, same session.

## Recommended absorption path

1. **ACW canonical decision** — author a `D-ACW-NNN` accepting the convention. Source `acw-state.yaml.template`, `AGENTS.md`, and any rule files that reference substrate paths from a root-relative position. Re-point all to `.acw/`-prefixed paths.

2. **Skill audit** — sweep `/acw-session start | update | end`, `/acw-instance audit | upgrade`, `/metabolize`, `/exfil` (if it touches ACW substrate), any other skill that opens substrate files. Confirm each reads paths from `acw-state.yaml::paths` rather than hardcoding `decisions/`, `sessions/`, etc. Patch hardcodes.

3. **`/acw-instance upgrade` migration path** — add a phase that creates `.acw/` and `git mv`s the substrate. Idempotent: skip if `.acw/` already exists.

4. **Documentation update** — `AGENTS.md`, `rules/instance-current-manifest.md`, and any onboarding docs that describe the substrate shape need a sweep.

5. **Decide `rules/` question (OQ-COPS-019)** — pick one of:
   - **Keep at root.** Codify in the canonical that `rules/` is part of the *contract*, not the *substrate*. Skills continue reading from `rules/`.
   - **Move to `.acw/rules/`.** Add `rules_dir` to `paths:` block. Audit and patch every skill that reads rules to honor the path. Costlier but consistent.

   Recommendation: **keep at root** for now. Rules are closer in shape to `pyproject.toml` (project config the tool reads) than to `session-log.md` (operator journal). The "metadata" framing fits decisions/sessions/tasks more cleanly than it fits contracts.

## Risks and counterarguments considered

**"It hides important substrate from operators."**
False in practice. Obsidian, VS Code, vim, all standard editors open dotfolder files transparently. The hidden-by-default rule only applies to file browsers and `ls` without `-a`, neither of which is how operators access ACW substrate day-to-day.

**"It complicates migration for existing instances."**
True but bounded. The migration is mechanical (one `git mv` block + one `acw-state.yaml` patch). The two downstream instances completed migration in a single session each with no skill changes. `/acw-instance upgrade` can automate this.

**"It diverges from prior ACW canonical shape."**
True. That's why it's filed as absorption rather than executed unilaterally. If ACW canonical rejects this, the two downstream instances stay divergent (flagged via `divergent_pending_review:` in their respective `acw-state.yaml`) until reconciled either way.

**"`.acw/` could collide with future Claude Code or other tool conventions."**
Possible. `.claude/` is already taken by Claude Code's own config dir, which is adjacent in concept. The names are distinct (`.acw/` vs `.claude/`) and serve different layers (ACW = substrate convention; Claude Code = harness config). No collision today; worth a sanity check during absorption review.

## Status

Pending review by ACW canonical operator (Ben). Filed to `~/projects/acw/_buffer/` per ACW's `/exfil`-equivalent routing.
