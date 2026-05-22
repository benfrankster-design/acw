---
id: D-ACW-053
title: /acw-instance emits three cross-repo signal kinds to ACW/.acw/raw/
date: 2026-05-21
status: accepted
kind: decision
updated: 2026-05-21
---

# /acw-instance emits three cross-repo signal kinds to `ACW/.acw/raw/`

## Decision

The `/acw-instance` skill is extended so that an upgrade run emits three sibling kinds of cross-repo signal to the canonical destination `ACW/.acw/raw/`, under one shared authority check (`acw-state.yaml::cross_repo_writes`):

| Kind | Trigger | Filename suffix |
|---|---|---|
| `absorption` | Substrate-shape pattern in the workspace that is net-new to canonical or judged better than canonical. (Pre-existing concept; renamed under the unified signal model.) | `-absorption-candidate.md` |
| `bug` | Defect in canonical detected during execution: template file out-of-sync with doctrine, tool errors on canonical input, canonical spec contradicts another canonical spec, recommended-block path missing. | `-canonical-bug.md` |
| `issue` | Operator-facing concern, ambiguity, or follow-up worth ACW's attention but not a defect. Operator may add at plan-approval time; verb may auto-detect for soft cases (e.g., `synced_to` lag, manifest warnings). | `-canonical-issue.md` |

All three share filename pattern `YYYY-MM-DD-<workspace-slug>-<topic-slug><kind-suffix>` and a minimum frontmatter (`kind`, `source_workspace`, `source_workspace_code`, `source_run`, `source_date`, `source_acw_version`, `status: pending`).

Bugs and issues captured mid-execution land in an in-memory run buffer and flush at end-of-run (step 10 of bulk execution order). Bugs do not halt the run unless the defect hard-blocks the current row.

Pre-v0.10.0 destination path `_buffer/` is retired in favor of `.acw/raw/` throughout the skill (per D-ACW-050 substrate relocation).

## Rationale

Prior to this change, the `/acw-instance` skill only specced one cross-repo write path: `absorption-candidate`. In practice (2026-05-21 frank-context v0.9.9 → v0.10.0 upgrade run), canonical defects surfaced during execution had no specified destination — they ended up in workspace-local decision-log follow-up notes that ACW would never see unless the operator hand-ferried them back. The frank-context run found exactly this: `tools/templates/load-context.py.tmpl` still hardcoded `STATE = ROOT / "acw-state.yaml"` despite v0.10.0 relocation to `.acw/acw-state.yaml`. The defect was real, the verb had no route to surface it upstream.

The fix is to unify three sibling concepts under one mechanism: same destination, same authority check, same filename convention, same note body shape. Different triggers, different filename suffix. Operator declares `cross_repo_writes` once and all three kinds become routable.

Bugs do not halt execution because most defects are non-blocking (a misaligned template, a stale doctrine reference, a recommended-block path that resolves to nothing). Halting would convert every drift into operator triage. Buffering keeps the run moving and surfaces everything in one place at the end.

## Source

- Operator request: "I need to have acw/ fix that in acw-instance so that bugs, issues, as well as absorbtion candidates after running acw instnace get sent to acw/raw/"
- Triggering observation: frank-context D-FC-005 "Follow-up notes" recorded a canonical-template bug with no path to ACW
- Files edited in this run:
  - `skills/acw-instance/SKILL.md` — action-table row + Safety bullet
  - `skills/acw-instance/references/upgrade.md` — plan-summary, bulk-execution order, new "Cross-repo signal emission" section, final-summary template, Output, Safety
  - `skills/acw-instance/references/audit.md` — head paragraph, plan-output template, Output
  - `skills/acw-instance/gotchas.md` — replaced `_buffer/`-scoped gotcha, added bug-buffering gotcha

## Follow-up

- `rules/multi-instance-topology.md` § "Absorption candidate format" should add note-body schemas for the new `bug` and `issue` kinds. (Tracked separately; this entry only specs the skill behavior.)
- Existing instances that adopted v0.10.0 before this change (frank-context as of 2026-05-21) carry a `cross_repo_writes: []`. Next `/acw-instance upgrade` run will prompt them once to declare `ACW/.acw/raw/`.
