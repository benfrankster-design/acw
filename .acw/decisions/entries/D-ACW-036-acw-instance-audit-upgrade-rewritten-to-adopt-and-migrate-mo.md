---
id: D-ACW-036
title: "`/acw-instance audit|upgrade` rewritten to adopt-and-migrate model; `integrations/` scope refined; ship as v0.7.0"
date: 2026-05-03
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-036 — `/acw-instance audit|upgrade` rewritten to adopt-and-migrate model; `integrations/` scope refined; ship as v0.7.0

**Date:** 2026-05-03
**Decision:** Three changes ship together as v0.7.0:

1. `skills/acw-instance/` rewritten to embody the adopt-and-migrate mental model. Audit produces a migration plan (per-file table: source → canonical destination → action) instead of an interactive Mode A/B walk. Upgrade executes the plan under a single approval gate, performing renames, format reshapes, content merges, and source deletions in one bulk operation. Substrate boundary made explicit: migration applies to recognized canonical paths (decisions/, rules/, research/, briefings/, runbooks/, integrations/, context/, inbox/, _buffer/, skills/, tools/, glossary.md, tasks-status.md, build-log.md, incidents.jsonl, CLAUDE.md, AGENTS.md, acw-state.yaml) plus substrate-shaped patterns (frontmatter class/authority/stability, dated capture files, jsonl); everything else (project code, data, configs, tests) stays untouched. For coding projects: substrate scaffolds alongside untouched code. Pre-migration safety commit recommended (offered when workspace is git-untracked); plan approval gate is the load-bearing safety surface. Interactive prompts reserved only for ambiguous routings flagged `[?]`; default behavior makes the routing call from canonical knowledge.

2. `integrations/` scope refined: `integrations/<system>/` covers BOTH documentation AND integration-specific operational scripts that are tightly coupled to one external system (bulk-push tools, sync utilities, data extractors, auth helpers). Boundary with `tools/`: tools/ holds general-purpose utilities; integrations/<system>/ holds tooling that exists only because the integration exists ("if you removed the integration, the script would be deleted with it"). Updated in `tools/templates/integrations-README.md.tmpl` and `rules/instance-current-manifest.md` § integrations entry.

3. ACW version bumped 0.6.1 → 0.7.0 reflecting the substantive `/acw-instance` behavior change. No new manifest registry entries earned; existing recommended-blocks list is unchanged. Downstream instances at `last_reconciled_version` 0.6.1 stay drift-clean (no new earned-in entries to flag).

**Rationale:** Today's `_Command` migration dogfood produced the earned-by-incident evidence for both refinements. The v0.4.0/v0.5.0 interactive Mode B walk forced the operator into nine routing prompts when six of the nine had clear canonical destinations after v0.6.0 absorbed the cockpit cluster. Operator's directive verbatim: *"that's what I want the skill to do. I want the skill to really perfectly ACW can absorb everything we have here, and it's going to do it. We've been doing better when I lose any context. It's going to actually keep it all but make it all better."* The `_Command/integrations/zoho-desk/push_direct.py` finding (an operational direct-HTTP pusher co-located with Zoho integration docs) revealed that `integrations/<system>/` wants both docs and integration-coupled scripts; current canonical README implied scripts did not belong. Migration model proves out under load: 18 file moves, 11 reshapes, 11 new canonical files, 9 deletes, one-shot via subagent-parallelized authoring + sequential write+delete, with pre-migration commit at cb39d32 as rollback path.

**Source:** Operator session 2026-05-03; `_Command` migration commits at cb39d32 (pre-migration), 7ea96e7 (migration), e179bbf (missing template_layer rules backfill). Workstream B subagent rewrite of `skills/acw-instance/SKILL.md`, `references/audit.md`, `references/upgrade.md`. Companion D-CMD-001 in `_Command/decisions/decision-log.md`.

**Open follow-ups (per Workstream B subagent):**
- Plan persistence: not persisted to disk between audit and upgrade (deterministic regeneration). May earn a `--save-plan` flag if substrate races become an incident.
- Adopt-mode hard-stop (D-ACW-022) is now structurally redundant with the plan-approval gate. Schema retained for backward compat; formal retirement deferred to a future decision-log entry.
- "Verify content at destination before deleting source" is documented but not mechanically enforced; may earn a checksum step from a future incident.
- Cross-repo writes still rely on `cross_repo_writes` declaration; capability broker (deferred per `rules/capability-broker.md`) remains the eventual replacement.
