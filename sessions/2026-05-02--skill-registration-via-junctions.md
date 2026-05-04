---
date: 2026-05-02
participants: [ben, claude]
topic: skill registration via user-level junctions
decisions_made: [D-ACW-011]
conceptual_shifts: no
linked_files:
  - acw/skills/capture-and-metabolize/
  - acw/skills/resume-session/
  - acw/skills/upgrade-instance/
duration_minutes: ~20
---

# Session — Skill Registration via User-Level Junctions

## 1. Topic & Goal

Slash commands `/resume-session`, `/capture-and-metabolize`, `/upgrade-instance` weren't firing despite the skills being shipped at `acw/skills/<name>/`. Operator surfaced this with "slash resume-session isnt working." Goal: register the skills so they fire as slash commands from any Claude Code session, ideally without polluting ACW's structure or causing collision with child instances that ship their own copies of the same skills via template_layer propagation.

## 2. What was decided

- **D-ACW-011 — ACW skills are registered globally via user-level directory junctions.** `~/.claude/skills/<name>/` becomes a junction pointing at `c:\Users\benja\projects\acw\skills\<name>/` for each of the three bookend-arc skills. ACW's `skills/` directory is the canonical source. Child instances scaffolded via `tools/scaffold-instance.py` continue to receive their own copies of the skills as part of template_layer propagation — those copies are passive on disk (self-contained distribution surface for the workspace) but are not the registered runtime copy on the operator's machine. Edits to ACW's source propagate immediately to every workspace the operator works in, since all of them resolve through the same user-level junction.

Operator-supplied directive that locked the choice: *"just do the wisest approach here. I want to make sure that the skill is registered so that I can use it from every project, and it's probably best to just have the canonical synapse point from this project ACW for ACW-specific skills for the ACW skills that generate in a new instance. Those can just be stored there, but they won't be the registered copy."*

Three junctions created:
- `~/.claude/skills/capture-and-metabolize/` → `acw/skills/capture-and-metabolize/`
- `~/.claude/skills/resume-session/` → `acw/skills/resume-session/`
- `~/.claude/skills/upgrade-instance/` → `acw/skills/upgrade-instance/`

This mirrors the existing pattern operator uses for synapse-domain skills (junctions at `~/.claude/skills/<name>/` → `~/synapse/Skills/<name>/`). Same registry, additional source directory.

## 3. What changed in the conception

No conceptual shift. The framework-agnostic skill design from rc4 already supports one canonical source serving every workspace; this session just chose user-level registration as the operational realization of that design. The alternative (project-level junctions per workspace) was discussed and rejected — operator preferred a single canonical source over per-workspace local overrides, on the reasoning that skill edits should flow to every workspace immediately and overrides can be added project-level on demand if needed (Claude Code resolves project-level skills before user-level).

## 4. What was built / changed

- Created three user-level directory junctions in `~/.claude/skills/`. No git-tracked files modified.
- ACW's `skills/` directory is unchanged; remains the canonical source.

## 5. Open questions left — structured

#### OQ-ACW-006 — Should `tools/scaffold-instance.py` optionally create skill junctions at scaffold time?

**Question:** A new ACW operator scaffolds a fresh instance, runs `claude code`, fires `/resume-session` — and nothing happens because the skills aren't registered on their machine. They have to manually run `mklink /J` (Windows) or `ln -s` (POSIX) for each skill. The operator who hit this in this session knew to investigate, but a less-savvy operator would interpret it as "ACW is broken." Should the scaffold tool offer a `--register-skills` flag (or do it by default with `--no-register-skills` to opt out) that creates the junctions at scaffold time?

**Candidates considered:**
- **Default-on registration.** Scaffold creates junctions automatically pointing at the new instance's `<target>/skills/<name>/`. Each instance has its own registered skills. Conflicts with the "single canonical source" choice from D-ACW-011 — multiple ACW-derived workspaces would each register their own copy, last-scaffolded wins, child instances would override ACW's authoritative source. Bad.
- **Default-off, opt-in flag.** Scaffold doesn't register by default. Operator passes `--register-skills` to set up junctions for the new instance. Useful for a one-off project that wants its own skill copy.
- **Document, don't automate.** Scaffold prints a one-liner reminder at end: "to register skills locally, run: mklink /J ~/.claude/skills/<name> <target>/skills/<name>". Operator picks their poison: register the new instance, register from ACW (canonical source), or skip.

**Why unresolved:** Each option has a real tradeoff. The right answer depends on the consumption pattern of derived workspaces (single-operator collaborating across many workspaces vs. multi-operator with each operator wanting their own canonical source). One cycle of evidence (this session) is not enough.

**Who needs to weigh in:** Operator, after the second downstream instance scaffolds and either hits the same friction or doesn't.

## 6. Operator directives (verbatim)

> "slash resume-session isnt working." (turn 1) — surfaced the missing-registration condition that drove the session.

> "I mean, can you have a junction from ACW skills to .claud skills, and then .claud skills has a junction to synapse skills? I mean, for the same skill. ... What if I fire up another instance which packages the ACW skills in it? I wouldn't want those skills to also junction to the same skill. That seems like it would kind of break something." (turn ~5) — surfaced the multi-instance pollution concern; drove the preliminary plan toward project-level junctions before the operator's later directive picked user-level.

> "just do the wisest approach here. I want to make sure that the skill is registered so that I can use it from every project, and it's probably best to just have the canonical synapse point from this project ACW for ACW-specific skills for the ACW skills that generate in a new instance. Those can just be stored there, but they won't be the registered copy. Just go ahead and register this now." (turn ~7) — locked D-ACW-011: single canonical source at user level; child copies are passive.

## 7. Cleaned transcript excerpt

*(Skipped — short session; operator directives in §6 carry the load-bearing wording.)*
