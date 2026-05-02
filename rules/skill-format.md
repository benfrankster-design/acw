---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Skill Format

The minimum contract every skill must satisfy. Instances may extend this contract with additional requirements via `rules/instance-hard-rules.md`; they may not weaken it.

## Folder convention

```
skills/<skill-name>/
  SKILL.md          # required — the skill contract
  gotchas.md        # required — at least one failure-mode entry
  references/       # optional — overflow detail, specs, examples
```

Skill name: lowercase, hyphens, max 64 characters. The folder name is the slash-command name.

## SKILL.md frontmatter (required fields)

```yaml
---
name: skill-name
description: >
  Third-person description. Must state: (1) what the skill does,
  (2) when it should fire, (3) when it should NOT fire,
  (4) what it produces and where. Disambiguate against similar skills.
role: pipeline-worker
capabilities:
  - surface.read
---
```

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Matches folder name |
| `description` | yes | Third person ("Writes...", "Audits...", "Blocks..."). Must answer when-to-fire and when-NOT-to-fire. Must name artifact type and destination. |
| `role` | yes | One of the four normative groups from `rules/pipeline-roles.md`: `orchestrator`, `pipeline-worker`, `guardian`, `broker-sideband`. |
| `capabilities` | yes | Scope declarations for the broker. Empty list `[]` is valid for skills that need no external authority. |

Instances may declare additional required frontmatter fields (e.g., `model`, `effort`, `allowed-tools`) in `rules/instance-hard-rules.md`. ACW's core contract does not require them because they are agent-platform-specific.

## Classification table (required, immediately after frontmatter)

```markdown
| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Creation | High |
```

Three orthogonal axes:

**Domain** — the subject area this skill serves. Values are declared per-instance in `rules/instance-hard-rules.md` under the `domains:` block. In a fresh ACW clone before the operator has declared domains, use a placeholder or leave blank. Domain is not the same as role: role says where in the data flow (orchestrator, pipeline-worker, guardian, broker-sideband); domain says what subject area (operations, engineering, finance, etc.).

**6C Primary** — the skill's primary AI capability type, per the ITIL 5 classification:

| 6C | What it means | Example |
|---|---|---|
| Creation | Generates new content | A composer skill drafting a document |
| Curation | Selects, organizes, maintains | An extractor skill routing knowledge |
| Clarification | Explains or interprets | A skill that answers questions about code |
| Cognition | Analyzes or reasons | A skill that audits for drift |
| Communication | Drafts messages or interacts with people | A skill that writes Slack messages |
| Coordination | Orchestrates other skills or systems | An orchestrator skill managing a pipeline |

Every skill has exactly one 6C primary. If a skill seems to have two, that is evidence it may need splitting per the single-role rule.

**Governance** — how much human oversight this skill requires. Derived from 6C:

| 6C | Governance tier |
|---|---|
| Coordination | Highest |
| Creation | High |
| Communication | High |
| Curation | Medium |
| Cognition | Medium |
| Clarification | Low |

Higher governance means more review gates, more explicit approval steps, more caution before the skill writes to shared surfaces. Governance tier is a signal to the operator and to agents reading the skill contract; it is not mechanically enforced in v0.1.0.

## Body structure

```markdown
# Skill Name

What this skill does in 1-2 sentences. Lead with the goal, not the mechanics.

## Instructions

Goal and constraints. If detailed reference material is needed, point to
`references/` rather than inlining it. Keep SKILL.md under ~80 lines total.

## Output

What the skill produces — format, location, and any post-output actions.
```

Sections beyond Instructions and Output (Workflow, Disambiguation, When to Fire / When NOT to Fire, References) are optional and added as needed. The body must stay concise; detail overflows to `references/`.

## gotchas.md (required companion)

Every skill ships with a `gotchas.md` file containing at least one entry:

```markdown
# Gotchas

- **Failure mode**: What goes wrong → What to do instead
```

If no gotchas are known at creation time, seed with the most likely misuse or confusion point. gotchas.md is the institutional memory for "things that bit us" — it grows by incident, not by anticipation.

## Command-routed orchestrators

When a skill family shares the same setup spine and differs only in target, destination, configuration, or specialist work, ship one orchestrator skill with a command table over multiple sibling skills. The orchestrator declares `role: orchestrator` in frontmatter and obeys the orchestrator definition in `rules/pipeline-roles.md`.

### Layout

```
skills/<skill-name>/
  SKILL.md                  # orchestrator: setup gates + command table + routing rules + shared spine
  references/
    <command-1>.md          # only the bits unique to command-1
    <command-2>.md          # only the bits unique to command-2
    ...
  gotchas.md
```

### SKILL.md sections

The orchestrator's SKILL.md contains, in order:

1. **Setup gates.** Checks that must pass before any command fires (source loaded, target resolved, payload schema valid).
2. **Shared spine.** The setup gates plus shared-context loading that every command performs before specialist work begins. Lives in SKILL.md, not in any reference file.
3. **Command table.** One row per command, naming the command, what it does or where it goes, and the reference file that owns the command-specific detail.
4. **Routing rules.** What to do when no command is given, when an unknown command is given, when arguments are missing. Includes any auto-classify default.
5. **Pin / unpin.** `/<skill-name> pin <command>` creates a top-level alias `/<command>` that routes through the parent. Preserves muscle memory when collapsing siblings.

### Reference files

Each `references/<command>.md` is short — typically ~40 lines. It owns command-specific configuration only: the target path, the governance rules to load, the output filename pattern, any extra files written, the per-command sanitization policy, and any command-specific Q&A or behavioral notes. **A reference file MUST NOT redeclare the spine.** The spine lives once, in SKILL.md. Reference files configure the verb-specific work that fires after the spine completes.

In **operation-centered** orchestrators, reference files configure target-specific deltas only. The workflow is invariant; deltas are paths, schemas, labels.

In **object-centered** orchestrators, reference files may describe specialist workflows that diverge after the shared spine completes. The spine is shared (same setup gates, same context-load); the specialist work is sibling operations on the same object. This is the Impeccable pattern.

Reference files have no frontmatter; they are loaded by the orchestrator at routing time and are not skills in their own right.

### Two valid orientations

The pattern can orient around either axis. Pick the axis where the variation lives.

**Operation-centered (default).** The parent is the *operation*. The commands are *targets* you perform it on. Same workflow, applied to different things.

- `/revise hc`, `/revise sop` — one revision job, two doc types.
- `/exfil product / cs / cockpit / cortex / project / gsg-brain` — one extraction job, six destination cabinets.

**Object-centered (gated).** The parent is the *thing being worked on*. The commands are *operations* you perform on it. Many things you can do, all to the same craft, sharing the same setup spine.

- `pbakaus/impeccable craft / audit / polish / distill / typeset / colorize / ...` — one frontend project, many specialist design operations on it. Spine: every command reads `PRODUCT.md` and `DESIGN.md`. Specialist work diverges after the spine.
- `/acw-instance audit / upgrade` — one ACW instance, two operations on it. Spine: registration check, GitHub canonical fetch, substrate scan, routing-table generation. Specialist work: audit reports the table; upgrade walks it action-by-action.
- `/acw-session start / end` — one session lifecycle, two boundary operations. Spine: read `acw-state.yaml::auto_load_at_session_start`, resolve `paths`, check `_inbox/`. Specialist work: start surfaces context; end captures, distributes, metabolizes.

The orientations are mirror images. Same structural pattern, perpendicular axes.

### Object-centered is gated behind tight-domain criteria

Object-centered orchestrators are easy to abuse — different operations on the same thing often have meaningfully different governance, authority, or risk. A skill family qualifies as an object-centered orchestrator only when ALL of the following hold:

1. The thing/domain is narrow and named (e.g., "frontend design," "ACW instance," not "operations").
2. The user intentionally enters that domain to invoke the skill.
3. All operations share the same governance class.
4. All operations share the same authority profile (same tools, same write surfaces, same risk class).
5. The command table improves recall rather than hiding complexity.

If any of these fails, the family is not an object-centered orchestrator — it is a junk drawer waiting to happen. Keep the operations as standalone skills.

Operation-centered orchestrators have an easier time qualifying because "same operation, different targets" naturally implies same workflow, same governance, same authority.

### When this shape fits (the discriminator)

A command-routed orchestrator is justified only when ALL of the following hold, regardless of orientation:

1. **Same shared spine.** Every command walks the same setup gates and the same shared-context loading before specialist work begins. The spine is identical across commands; what fires *after* the spine may differ.
   - In operation-centered orchestrators, work after the spine is also identical (same workflow, different target).
   - In object-centered orchestrators, work after the spine is sibling specialist operations on the same object.
2. **Same failure modes.** A given setup-spine failure surfaces the same way across commands and is recovered the same way. Specialist failures may differ in object-centered orchestrators.
3. **Same governance class.** All commands sit at the same governance tier (Highest / High / Medium / Low) — no command introduces a new risk class.
4. **Spine deltas are configuration-only.** Per-command differences in the spine are paths, schemas, labels, audience, target rules, output rules. Specialist-work divergence is allowed in object-centered orchestrators; the spine is not.

Two precise statements of the rule, one per orientation:

- **Operation-centered:** A command is a parameterization of the same operation. Same workflow end-to-end, different target.
- **Object-centered:** Commands are sibling specialist operations on the same object. They share the setup spine and operate within the same craft environment; specialist work after the spine may diverge.

### Command-count ladder

Command counts are a governance smell, not a hard cap. Use this tiered guidance:

| Commands | Action |
|---|---|
| 1–3 | Probably fine. |
| 4–6 | Inspect for drift. Each reference file should still fit on one screen and contain configuration only. |
| 7–10 | Require explicit grouping in the command table and a strong domain boundary. Document why it earned the count. |
| 10+ | Only allowed inside an object-centered orchestrator with extreme discipline (Impeccable territory). |
| 20+ | Almost certainly an object-centered workbench, not a skill. Acceptable only when the user mental model is "I am inside this one craft environment." |

### When to split instead

- A command requires a different setup spine (not just configuration).
- A command introduces a new risk class or authority profile.
- A command changes the user's promise (what they expect to happen).
- A reference file starts redeclaring spine logic.
- A reference file grows past ~80 lines and the bulk is workflow rather than configuration.
- The parent skill name stops predicting what happens.

## Sequential orchestrators

Some orchestrators run sub-steps in sequence rather than routing to one of N targets. A skill that cleans a transcript, then tags conceptual shifts, then drafts an evolution entry, then updates a research-state file is sequential. It has stages, not commands.

The sub-steps are internal until operational friction earns their separation into standalone pipeline-worker skills. When separated, each sub-step becomes its own skill declaring its own role. Earn-by-incident discipline applied to skill granularity.

The rule: ship the orchestrator first. Split when a sub-step needs to be called independently. Log the split as an incident.

A sequential orchestrator declares `role: orchestrator` in frontmatter and uses `references/` for overflow detail, not for per-stage routing.

## Skill density guidance

Prefer one skill per role per domain. Two skills with the same role serving the same domain are candidates for merging. One skill serving two domains with different instructions for each is a candidate for splitting.

At single-operator scale, fewer skills with broader scope are easier to maintain than many narrow skills. As the instance scales (more operators, more agents, more domains), narrow specialization earns its ship through incidents where the broad skill couldn't serve both use cases without internal routing logic.

The 16-role appendix in `rules/pipeline-roles.md` is the reference for naming splits. When a pipeline-worker skill splits, each piece adopts a finer role label (collector, extractor, transformer, etc.) as its description, while still declaring `role: pipeline-worker` in frontmatter per the four-group normative enum.

## Relationship to other contracts

- **`rules/pipeline-roles.md`** — declares the role enum. Every `role:` value in SKILL.md frontmatter must match one of the four normative groups.
- **`rules/instance-hard-rules.md`** — declares valid domains and any instance-specific frontmatter extensions.
- **`rules/capability-broker.md`** — when the broker ships, `capabilities:` declarations in SKILL.md become the scope declarations the broker validates.
- **`deferred/skill-manifest/`** — the full typed input/output declaration extension. Earns promotion when `workspace-input-schema` activates. Until then, this format is sufficient.
