---
kind: bug-cluster
source_instance: cs-ops-spec (COPS)
date: 2026-05-21
status: pending
session: 2026-05-21--oq-resolutions-and-sla-research
---

# v0.10 bookend hiccups — COPS session 2026-05-21

Four friction points surfaced while running `/acw-session start` and the OQ-resolution `/acw-session end` on a v0.10.1-reconciled COPS instance. Filing as a cluster since they're small and related.

---

## Bug 1: `regenerate_index_cmd` doesn't work in wiki mode

**What:** `acw-state.yaml::decision_tracking.regenerate_index_cmd: "python tools/migrate_to_wiki.py"` implies this command regenerates the decisions INDEX from existing wiki entries. It doesn't. The tool only migrates from a single-file `decisions/decision-log.md` to the wiki shape. Once an instance is already in wiki mode (no `decision-log.md`), running the command produces no output and makes no changes.

**Impact:** After `git mv`-ing 7 resolved OQ files from `open-questions/` to `entries/`, the INDEX had to be manually edited to update the link paths. The INDEX could not be regenerated automatically.

**Expected fix:** Either (a) add a `--regenerate` flag to `migrate_to_wiki.py` that rebuilds `INDEX.md` from all files in `entries/`, `open-questions/`, and `constraints/`; or (b) document in `acw-state.yaml` and distribution-rules.md that `regenerate_index_cmd` is migration-only and wiki-mode INDEX maintenance is always manual.

---

## Bug 2: Resolved-OQ distribution creates ambiguous INDEX placement

**What:** `distribution-rules.md` says resolved OQs should be moved to `entries/` and get `kind: decision`. But `entries/` then contains a mix of D-COPS-NNN files and OQ-COPS-NNN files. The INDEX has a `## Decisions` section and an `## Open Questions` section — it's unclear whether resolved OQs belong in Decisions (where `entries/` files usually live) or whether they stay in Open Questions with updated links.

**What was done:** Kept them in the `## Open Questions` section of the INDEX with links updated to `entries/` paths. This preserves traceability (OQ id stays visible) but is inconsistent with the rule's stated intent.

**Expected fix:** distribution-rules.md should explicitly state whether resolved OQs appear in the `## Open Questions` or `## Decisions` section of the INDEX after being moved to `entries/`. Suggest: keep in `## Open Questions` with `_(status: resolved)_` annotation — the Decisions section is for D-COPS-NNN decisions, not OQ resolution records.

---

## Bug 3: Tracker conflict when `start` fires before `end` on prior session

**What:** `/acw-session start` overwrites `.current-session` with the new session. If the prior session was never closed (e.g., session ended mid-conversation without a `/acw-session end` call), running `start` orphans the old session — `end` can no longer find it via the tracker.

**What happened:** The `2026-05-21--oq-resolutions-and-sla-research.md` session had `last_completed_phase: 0`. Running `start` for today's new session overwrote the tracker. Had to manually identify the old session file and run `end` against it by name rather than tracker lookup.

**Expected fix:** `/acw-session start` should detect an existing tracker with `last_completed_phase: 0` (or any uncleared session) and surface a warning before overwriting: e.g., `[acw-session warn] Unclosed session detected: <filename>. Run /acw-session end first, or confirm start to orphan it.` Operator confirms to proceed.

---

## Bug 4: `migrate_to_wiki.py` produces silent no-op in wiki mode

**What:** Same root as Bug 1, but distinct symptom. The tool exits with code 0 and no stdout when there's nothing to migrate (wiki mode, no `decision-log.md`). A silent no-op looks identical to a successful regeneration. An operator running the command after moving files would have no signal that the INDEX was NOT updated.

**Expected fix:** Add a `print("No source file found; nothing to migrate.")` guard when the source file is absent. Or add the regeneration mode (Bug 1 fix) with explicit output confirming what was rebuilt.
