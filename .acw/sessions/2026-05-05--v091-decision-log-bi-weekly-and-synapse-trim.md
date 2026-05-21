---
date: 2026-05-05
participants: [operator, agent]
topic: v0.9.1 bi-weekly rolling-window for decision-log + global synapse trim
decisions_made: [D-ACW-042]
conceptual_shifts: yes
linked_files:
  - decisions/decision-log.md
  - decisions/decision-log-2026-Q2.md (new — archive)
  - rules/decision-tracking.md
  - rules/task-tracking.md
  - rules/auto-load-discipline.md
  - rules/instance-current-manifest.md
  - acw-state.yaml
  - tools/templates/acw-state.yaml.tmpl
  - tasks-status.md
  - ~/synapse/Reference/acw-canonical/ (new — moved from synapse/Rules/)
  - ~/.claude/CLAUDE.md (Rules Index updated)
duration_minutes: ~75
---

# Session 15 — v0.9.1 bi-weekly rolling-window + global synapse trim

## 1. Topic & Goal

Two structural problems surfaced via screenshot:

1. `_Command` session loading at 150k. Cause: `tasks-status.md` not yet migrated to v0.9.0 archive discipline (134KB inline) + harness baseline overhead.
2. ACW workspace memory files at 79.2k. Cause: `~/synapse/Rules/` auto-loaded globally via `~/.claude/rules` junction, including 35.8k of `instance-current-manifest.md` plus 5 other ACW-canonical duplicates totaling ~85k. Plus ACW's own `decisions/decision-log.md` over the v0.9.0 15k threshold (24k).

Goal: clear both bloat sources structurally. Operator override on the v0.9.0 "nothing before 1.0.0" directive: ship v0.9.1 as doctrine-completion patch (close the rolling-window mechanism gap that v0.9.0 left under-specified for decision-log) and apply it to ACW immediately. Bi-weekly cadence chosen as unifying cadence for both decision-log and tasks-status.

## 2. What was decided

- **D-ACW-042 — v0.9.1 ship.** Five-change bundle: `rules/decision-tracking.md` gains Rolling-window discipline section (bi-weekly + ~15k threshold trigger; archive shape `decisions/decision-log-YYYY-Q*.md`; Open Questions/Constraints/Resolved sections do not archive); `rules/task-tracking.md` cadence aligned to bi-weekly; `rules/auto-load-discipline.md` caveats updated; `rules/instance-current-manifest.md` gains earned-in-0.9.1 entry for decision-log archive shape + revised tasks-status entry; ACW substrate split applied (D-ACW-034 down through D-004 → archive); companion global-layer trim (six ACW-canonical duplicates moved out of `~/synapse/Rules/`). Records the structural-prevention reasoning and the operator override.

## 3. What was built / changed

- `decisions/decision-log-2026-Q2.md` created (archive frontmatter, 30 entries D-ACW-034 down to D-004).
- `decisions/decision-log.md` sliced (now 8 entries inline including new D-ACW-042); pointer line replaces archived block.
- `rules/decision-tracking.md`: new "Rolling-window discipline" section parallel to `rules/task-tracking.md`.
- `rules/task-tracking.md`: rolling-window cadence updated bi-weekly.
- `rules/auto-load-discipline.md`: both decision-log and tasks-status canonical-recommendation caveats updated.
- `rules/instance-current-manifest.md`: tasks-status archive entry text revised to bi-weekly cadence; new earned-in-0.9.1 entry for `decision-log-YYYY-Q*.md`.
- `acw-state.yaml`: version 0.9.1, last_reconciled 2026-05-05, last_reconciled_version 0.9.1, archive added to meta_layer.
- `tools/templates/acw-state.yaml.tmpl`: baseline last_reconciled_version 0.9.1.
- `tasks-status.md`: Session 15 Done block; new Pending items (cs-copilot citation drift, downstream upgrade dogfood); preamble updated for bi-weekly cadence.
- `~/synapse/Rules/` → `~/synapse/Reference/acw-canonical/`: six files moved (`instance-current-manifest.md`, `auto-load-discipline.md`, `Procedures/{skill-format, pipeline-roles, capability-broker, decision-tracking}.md`).
- `~/.claude/CLAUDE.md`: Rules Index updated; new pointer to `synapse/Reference/acw-canonical/`.

## 4. What changed in the conception

**Bi-weekly as unifying cadence.** v0.9.0 used "Sessions ≥ N-2" for tasks-status (a session-count placeholder when the cadence question was unresolved). Bi-weekly gives a clean date-based cutoff that works across both decision-log and tasks-status under one rule shape. The two surfaces drift independently but share the same pattern. Mirrors the unified-doctrine approach that v0.9.0 brought to auto-load discipline.

**Junction-as-auto-load is a structural attack surface.** The `~/.claude/rules` → `~/synapse/Rules/` junction was load-bearing for cross-workspace identity rules but silently doubled-loading any ACW-canonical content the operator placed in `synapse/Rules/`. Earn-by-incident already fired (this session's screenshot was the named, dated, documented incident). The fix is structural: ACW canonical lives in ACW workspaces, not in the global auto-load path. Reference copies (for grep/read) move to a sibling location not under the junction.

**Doctrine-completion patches.** v0.9.0 was declared the "last pre-promotion substantive ship" but left a specification gap (decision-log threshold named, mechanism missing). v0.9.1 establishes the pattern: a doctrinal patch that closes a v0.9.0 specification gap is not "new content" — it's completing what v0.9.0 already started. Distinct from an additive feature ship. Future v0.9.x patches may follow the same shape if other v0.9.0 gaps surface during soak.

## 5. Unresolved design questions

- **Should the global-synapse trim itself earn an ACW canonical rule?** Right now it's an instance-specific cleanup of the operator's personal `~/synapse/` setup. If a second operator hits the same junction-bloat issue independently, the pattern would earn promotion to a canonical "what NOT to put in the global auto-load path" rule. Single incident; not yet promoted. (Not blocking v0.9.1 — separate consideration.)

- **Citation refresh policy for cs-copilot.** Five files in `~/projects/cs-copilot/` cite the moved synapse paths. Doc-only, not load-bearing. Listed in Pending; fix-on-touch. If cs-copilot is touched soon (likely, per other Pending items), the fix folds in cheaply. If not touched for weeks, the citations grow staler. Not worth a dedicated session.

## 6. Notes

- 54/54 unit tests pass. Vocab lint clean.
- Operator directive recap: per v0.9.0 ship, "nothing new ships before v1.0.0 promotion." v0.9.1 interpreted as doctrine-completion (closing a v0.9.0 specification gap), not new content. Operator confirmed by directing the ship.
- Reminder per operator's auto-memory feedback: "commit means commit-and-push" in ACW. v0.9.1 needs both before downstream `/acw-instance upgrade` runs can pick up the canonical changes.
