---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# Instance Hard Rules

Per-instance non-negotiable rules. Everything in this file is stop-work if violated. New rules added here MUST be recorded as a decision in `decisions/decision-log.md` first, then propagated here with a pointer to the decision entry.

## Declaring an authority set

Every instance declares the valid values for `approval_authority` in the canon. The single-operator default looks like this:

```yaml
authority_set:
  - operator
```

A two-tier instance:

```yaml
authority_set:
  - operator
  - leadership
```

A four-tier instance:

```yaml
authority_set:
  - operator
  - department-lead
  - director
  - sponsor
```

Any `approval_authority` value used in `rules/canon.yaml` that is not listed in this block MUST cause lint to fail.

## Declaring domains

Every instance declares its MECE domains. Domains are the top-level partition of work in this workspace. The canon `domain` field MUST resolve to one of these values.

```yaml
domains:
  - example-domain-a
  - example-domain-b
```

## Worked example (non-empty)

A minimal single-operator instance:

```yaml
authority_set:
  - operator

domains:
  - writing
  - research

hard_rules:
  - id: HR-001
    rule: "No writes to paths under `read-only/` by any skill."
    violation: stop-work
    rationale: "read-only/ holds source material that must not be mutated. Violations corrupt the source of truth."
    decision_ref: "decisions/decision-log.md § Decisions and Rationale, entry HR-001"
```

## How to add a new hard rule

1. Open `decisions/decision-log.md` and add an entry under "Decisions and Rationale" describing the rule, the triggering incident or concern, and the rationale.
2. Add the rule to the `hard_rules` block above with an `id`, `rule` text, `violation` level, `rationale`, and `decision_ref` pointing back to the decision-log entry.
3. Run `python tools/lint-vocab.py` and any other relevant checks to verify nothing breaks.
4. Commit with a message naming the new rule id.

Hard rules are not casual. If a rule does not warrant a decision-log entry, it does not belong here — put it in `rules/` as an operational guideline instead.
