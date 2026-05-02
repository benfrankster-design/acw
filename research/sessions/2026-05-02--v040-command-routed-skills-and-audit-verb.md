---
date: 2026-05-02
participants: [operator, agent]
topic: v0.4.0 — command-routed skills and audit verb
decisions_made:
  - D-ACW-016
  - D-ACW-017
  - D-ACW-018
  - D-ACW-019
  - D-ACW-020
  - D-ACW-021
  - D-ACW-022
conceptual_shifts: yes
linked_files:
  - rules/skill-format.md
  - rules/multi-instance-topology.md
  - rules/instance-current-manifest.md
  - rules/task-tracking.md
  - acw-state.yaml
  - tools/templates/acw-state.yaml.tmpl
  - tools/templates/README.md.tmpl
  - AGENTS.md
  - CLAUDE.md
  - skills/acw-instance/SKILL.md
  - skills/acw-instance/references/audit.md
  - skills/acw-instance/references/upgrade.md
  - skills/acw-instance/gotchas.md
  - skills/acw-session/SKILL.md
  - skills/acw-session/references/start.md
  - skills/acw-session/references/end.md
  - skills/acw-session/gotchas.md
  - skills/upgrade-instance/SKILL.md
  - skills/resume-session/SKILL.md
  - skills/capture-and-metabolize/SKILL.md
  - decisions/decision-log.md
  - tasks-status.md
  - build-log.md
duration_minutes: 240
---

# v0.4.0 — Command-routed skills and audit verb

## 1. Topic & Goal

Started as a continuation of v0.3.0 work (multi-instance topology, GitHub-first canonical, adopt mode shipped earlier in same day). Operator brought back a cs-copilot session where `/upgrade-instance` correctly bailed because cs-copilot pre-dates registration. The conversation surfaced the deeper question — what about workspaces with **organic substrate** (`_Command`-shape) that have evolved their own conventions? Adopt-mode steamrolling those would destroy institutional learning.

Goal: ship the safety mechanism (audit verb, hard-stop threshold, divergence markers, absorption flow), restructure the bookend skills to fit the command-routed orchestrator pattern, and tighten the skill-format rule that produced a false-flag during the design conversation.

## 2. What was decided

- **D-ACW-016** — Tightened `rules/skill-format.md`: ported command-routed orchestrator material from synapse global into ACW canonical with three corrections. Reframed "same invariant workflow" as "same shared spine" (setup gates + shared-context loading); split the strongest-version rule by orientation (operation-centered = parameterization of same operation; object-centered = sibling specialist operations on same object); scoped deltas-are-configuration to the spine only.
- **D-ACW-017** — Expanded `rules/multi-instance-topology.md` with absorption mechanics: three-flow resolution model (adopt / absorb / instance-specific), absorption candidate format for `_inbox/` payloads, divergence markers (`divergent_pending_review` temporary, `instance_specific_substrate` permanent), re-adoption flow, cross-repo write governance.
- **D-ACW-018** — Shipped `/acw-instance` as object-centered command-routed orchestrator with verbs `audit` (read-only Mode A canonical comparison + Mode B operator-routed organic discovery + absorption candidate writes) and `upgrade` (gap walk with adopt-mode hard-stop, divergence-marker respect).
- **D-ACW-019** — Shipped `/acw-session` as object-centered command-routed orchestrator with verbs `start` (load context, drift check, surface inbox) and `end` (five-phase capture-distribute-metabolize). Verb-routed because shared spine (load `acw-state.yaml`, resolve `paths`, check `_inbox/`, identify recent captures) is the same; specialist work after the spine diverges (Impeccable pattern).
- **D-ACW-020** — Audit Mode B ships in v0.4.0 as operator-routed organic substrate discovery (not deferred). Walks for substrate-like patterns; surfaces four-option route per finding (adopt-as-canonical / absorption candidate / instance-specific / not-substrate). Skill never auto-routes Mode B findings.
- **D-ACW-021** — Audit Mode A uses ACW rules + templates as the schema (no new artifact). Audit fetches `rules/decision-tracking.md`, `tools/templates/decision-log.md.tmpl`, etc. from GitHub canonical and compares the workspace's substrate file against them inline.
- **D-ACW-022** — Hard-stop threshold for adopt-mode set at 5 non-canonical markdown files in `decisions/` or `rules/`. Below catches cs-copilot-shape (canonical-shaped, just unregistered); at-or-above catches `_Command`-shape (substantial organic substrate).

## 3. What changed in the conception

Several conceptual shifts captured in `research/evolution.md` candidates:

- **Permanent divergence is a smell, not a feature.** Earlier draft of the lattice topology had `keep-divergent` as a third terminal flow alongside adopt and absorb. Operator pushed back: ACW canonical is presumed best; divergence is always temporary, pending review. Two terminal states only — workspace canonical-shaped, or ACW canonical-shaped after absorbing the workspace's better pattern.
- **Object-centered orchestrators have a shared spine, not identical workflows.** The skill-format rule's strict-voice ("same invariant workflow, same reasoning steps, same order") prohibited Impeccable-shape. The permissive-voice ("command-count ladder allows 10+ in object-centered") allowed it. Closing the contradiction: spine is setup gates + shared-context loading; specialist work after the spine may diverge in object-centered.
- **Audit doesn't need a new schema; the rules ARE the schema.** Mode A fetches ACW canonical rule files and templates from GitHub and compares the workspace's substrate file inline. Same way an agent or operator would do it manually. Building a structured schema would duplicate the rule and risk drift.
- **Mode B doesn't need heuristics; it needs the operator in the loop.** Earlier framing was "Mode B is hard, defer until heuristics earn." Operator pushback: walk for substrate-like patterns, surface to operator with four-option route. The judgment call (does this generalize?) is the operator's.

## 4. What was built / changed

**New files:**
- `skills/acw-instance/SKILL.md` — orchestrator with shared spine
- `skills/acw-instance/references/audit.md` — audit verb (Mode A + Mode B)
- `skills/acw-instance/references/upgrade.md` — upgrade verb (gap walk, adopt-mode, divergence respect)
- `skills/acw-instance/gotchas.md`
- `skills/acw-session/SKILL.md` — orchestrator with shared spine
- `skills/acw-session/references/start.md` — start verb
- `skills/acw-session/references/end.md` — end verb (five phases)
- `skills/acw-session/gotchas.md`
- `skills/acw-session/references/<9 sub-references>` — carried over from old `capture-and-metabolize/references/`
- This session capture file

**Substantive edits:**
- `rules/skill-format.md` — ~109 lines added porting command-routed material with corrections
- `rules/multi-instance-topology.md` — ~103 lines added covering absorption mechanics
- `rules/instance-current-manifest.md` — four new registry entries; internal renames `/upgrade-instance` → `/acw-instance upgrade` and `/resume-session` → `/acw-session start`
- `rules/task-tracking.md` — internal rename
- `acw-state.yaml` — version 0.3.0 → 0.4.0, last_reconciled_version 0.4.0, four new blocks, template_layer/meta_layer updated
- `tools/templates/acw-state.yaml.tmpl` — template baseline matches
- `tools/templates/README.md.tmpl` — child instance README references new skill names
- `AGENTS.md` — directive 7 names new skill
- `CLAUDE.md` — references new skill names
- `decisions/decision-log.md` — D-ACW-016 through D-ACW-022 added (seven entries)
- `tasks-status.md` — Pending rebuilt, new Done block for Session 7
- `build-log.md` — new session entry

**Marked superseded (awaiting manual delete):**
- `skills/upgrade-instance/SKILL.md` — `status: superseded`, `superseded_by: skills/acw-instance/`
- `skills/resume-session/SKILL.md` — `status: superseded`, `superseded_by: skills/acw-session/ (verb: start)`
- `skills/capture-and-metabolize/SKILL.md` — `status: superseded`, `superseded_by: skills/acw-session/ (verb: end)`

**User-level junctions:** deleted `~/.claude/skills/upgrade-instance,resume-session,capture-and-metabolize`; created `~/.claude/skills/acw-instance,acw-session`.

## 5. Open questions left — structured

#### OQ-ACW-007 — How does ACW notify a workspace when it rejects an absorption candidate?

**Question:** When ACW reviews an absorption candidate and rejects it, the workspace's `divergent_pending_review` entry should resolve to `status: rejected` so the workspace's next `/acw-instance upgrade` migrates the file to canonical. The current rule says "ACW drops a notification into the workspace's `_inbox/` (cross-repo-writes-permitting), or expects the workspace to discover the rejection on its next upgrade run." But the discovery mechanism isn't specified — what does the workspace look at to know an absorption was rejected?

**Candidates considered:**
- ACW writes a typed notification to the workspace's `_inbox/` (e.g., `acw-rejection-<topic>.md`). Requires ACW to declare the workspace's `_inbox/` path in ACW's own `cross_repo_writes`. Symmetric with the absorption-candidate-write direction.
- Workspace's `/acw-instance upgrade` polls ACW canonical for changes — if its `divergent_pending_review` entry's target file shape now matches canonical, mark `absorbed`; if a rejection-marker exists in ACW's substrate at a known path (e.g., `decisions/decision-log.md` entry with a structured marker), mark `rejected`.
- Manual marking — operator updates the workspace's `divergent_pending_review` entry by hand after reading ACW's decision-log entry. No automation.

**Why unresolved:** Needs more lattice-scale evidence. With a single operator running ACW + a few workspaces, manual marking is fine. The first-class notification mechanism earns its build when there are enough absorption candidates flowing that automation matters.

**Who needs to weigh in:** Operator decision after running absorption flow at least once end-to-end. Likely informed by `_Command` audit dogfood.

#### OQ-ACW-006 — Should `tools/scaffold-instance.py` create user-level skill junctions at scaffold time?

**Question:** Carried over from session 5. When scaffolding a new instance, the scaffold tool currently does not create user-level skill junctions (`~/.claude/skills/<name>/`). Operators must create them manually after scaffold. Should the tool offer to do this automatically?

**Candidates considered:**
- Auto-create on every scaffold. Simplest. Risk: pollutes operators who use multiple workspaces with overlapping skill names.
- Prompt at scaffold time: `"Create user-level junctions for shipped skills? [y/N]"`. Lets operator decide per-instance.
- Never auto-create; document in the scaffold tool's output that junctions are next step.

**Why unresolved:** Needs second-instance evidence. ACW currently has ACW-itself + the operator's three downstream workspaces (cs-copilot, gsg-copilot, _Command). One more scaffold would surface whether the manual step recurs as friction.

**Who needs to weigh in:** Operator after next scaffold operation.

## 6. Operator directives (verbatim)

> "I don't like the idea of keeping divergent because my whole idea with ACW is that it's better. Now, if the workspace has a substrate that's better than ACW, then yes, it should write the research note and just keep them. The workspace would keep divergent until ACW takes a look at that information and decides if it's better or not, or whatever." (turn 89)

> "We should also rename resume session and capture and metabolize to fit the similar command routed shape. It should be /acw-session start|end that is amazing. Honestly, that will even help us if we ever need to break it down This actually solves the capability broker problem because we could break down acw-session into various different commands in the future." (turn ~95)

> "That's where we got the idea from in the first place" (turn 97 — re: Impeccable as the precedent for command-routed orchestrators; correcting my false-flag)

> "synthesize this entire chat. I feel like we're maybe missing some updates here as part of this. all the problems that were named in this session must have a shippable solution." (turn ~102 — forced the synthesis step that surfaced the loose items)

> "What's stopping us from doing 22? Why does it need a schema? Why doesn't it just use the acw rules files? Why doesn't it just go look at GitHub." (turn ~106 — pushed back on Mode A deferral; right call)

> "For 23, I think you're smart enough to be able to paint a picture of what organic substrate looks like. Be as high-level as you possibly can. It's not simple, and it's not difficult." (turn ~106 — pushed back on Mode B deferral; right call)

## 7. Cleaned transcript excerpt

Skipped — the substantive content is captured above. The full transcript would add ~10K tokens of conversation around correctness checks and turn-by-turn confirmation of decisions, none of which adds beyond what §2-§6 already record.
