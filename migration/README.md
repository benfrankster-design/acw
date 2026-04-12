---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Migration — Brownfield Audit

This folder is how you bring an existing workspace under ACW discipline. It is deliberately slower and more cautious than `bootstrap/` because an existing workspace has existing state that can be damaged by an enthusiastic rewrite.

## Prerequisites

- The prerequisites from `bootstrap/README.md`
- A committed snapshot of the target workspace (so you can roll back)
- At least one empty afternoon — migration is not a fifteen-minute task

## Step 1 — Run the audit checklist

Do not edit anything yet. Read through the workspace with ACW's shape in mind and answer every item below in writing. The output is a drift report, not a rewrite.

**Survey existing rule files.** What rules already exist? Where do they live? Are any of them stop-work rules that should migrate to `rules/instance-hard-rules.md`? Are any of them vocabulary rules that belong in `rules/canon.yaml`? Write the inventory.

**Survey existing skills for `role:` field.** Open every skill definition in the workspace. Which ones already declare a role? Which ones have no role declared? Which ones would violate the "exactly one role" rule if forced to declare? Write the inventory. Skills that cannot cleanly declare a single role are split candidates.

**Survey existing vocabulary.** What terms are in use across the workspace? Are the same concepts named different things in different places? Are different concepts named the same thing? This is the drift that ACW's canon is designed to catch. Write the inventory.

**Survey credential storage.** Where are credentials stored right now? Plain-text config files? Environment variables? A secrets manager? Is any credential accessible to a skill that does not need it? Write the inventory. Broker activation is almost always the first earned promotion from an honest migration audit.

**Survey decision tracking.** Where are decisions currently recorded? Are they recorded? Can you find the rationale for a decision made three months ago? If not, every undocumented decision is a future incident. Write the inventory.

## Step 2 — Produce a drift report

Take the five inventories and rank every item by severity: `critical`, `moderate`, `low`. A critical drift is one that could damage an asset or leak a credential. A moderate drift causes friction but is not dangerous. A low drift is cosmetic. The drift report is the only deliverable of this step. Do not fix anything yet.

## Step 3 — Execute fixes incrementally

Work through the drift report one item at a time, highest severity first. Every fix gets logged as an incident in `incidents.jsonl` via `python tools/log-incident.py log <primitive> <severity> <symptom>`. This is how migration generates the first real incident data for your instance — the incidents are earned genuinely rather than fabricated to justify a future ship.

After each fix, run the lint and the tests. Commit. Move to the next item. Do not batch.

## Hard rules for migration

- **Never overwrite read-only content.** If the workspace has declared read-only paths, they stay read-only through the entire migration.
- **Never move silently.** Every file relocation is recorded in the decision log with the old path, the new path, and the reason.
- **Never delete history.** If a file is being removed, keep the git commit that records its last content. `git rm` is allowed; `rm -rf && git add -A` is not.
- **Never fix a drift you did not audit.** If you catch something mid-migration that is not in the drift report, add it to the report and come back to it. Do not scope-creep into adjacent cleanup.
