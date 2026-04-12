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

## Relationship to other contracts

- **`rules/pipeline-roles.md`** — declares the role enum. Every `role:` value in SKILL.md frontmatter must match one of the four normative groups.
- **`rules/instance-hard-rules.md`** — declares valid domains and any instance-specific frontmatter extensions.
- **`rules/capability-broker.md`** — when the broker ships, `capabilities:` declarations in SKILL.md become the scope declarations the broker validates.
- **`deferred/skill-manifest/`** — the full typed input/output declaration extension. Earns promotion when `workspace-input-schema` activates. Until then, this format is sufficient.
