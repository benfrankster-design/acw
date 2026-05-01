---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Incident Tracking

Every ACW instance ships with `incidents.jsonl` at the repo root from day zero. The earn-by-incident discipline is the load-bearing mechanism behind the entire deferred library and the promotion ritual. Without an incident ledger present from the moment an instance is scaffolded, there is no way to *gather* the evidence that promotions require. `incidents.jsonl` does not earn its build; it IS the substrate that lets every other primitive earn its build.

## When to log an incident

- A bug surfaced and was fixed (any deferred primitive that would have prevented it gets N+1 evidence)
- A hard rule was violated (governance leak)
- An assumption proved false (wrong-assumption)
- A pattern was identified that won't survive scale (scale-vulnerability)
- A workflow gap surfaced (process-gap)
- A runtime-environment surprise caused a failure (environment-state)

If a session ended with the operator saying "we shouldn't have to do that next time," it is incident-worthy. Log it.

## Schema

Each line in `incidents.jsonl` is a JSON object:

```json
{
  "id": "uuid4",
  "timestamp": "ISO 8601 UTC",
  "primitive": "name-of-deferred-primitive-or-process",
  "severity": "low|med|high",
  "symptom": "what happened, in one sentence",
  "operator": "who logged it",
  "category": "implementation-bug|governance-leak|environment-state|process-gap|wrong-assumption|scale-vulnerability|earn-by-incident"
}
```

`category` is optional but strongly recommended — it sharpens triage and makes promotion-ritual evidence easier to count by category.

## Severity

- **low** — minor friction, no remediation required
- **med** — required a manual fix or workaround; surfaces evidence on the named primitive
- **high** — caused damage, data loss, or security exposure; one occurrence may justify emergency promotion (per `rules/promotion-ritual.md`)

Promotion review requires three med-or-higher incidents on the same primitive. See `rules/promotion-ritual.md`.

## Category vocabulary

| Category | Meaning |
|---|---|
| `implementation-bug` | Code or config error that surfaced and was fixed |
| `governance-leak` | Hard rule violation discovered post-hoc |
| `environment-state` | State of the runtime (venv, deps, OS) caused the failure |
| `process-gap` | Discipline or workflow gap surfaced |
| `wrong-assumption` | Agent or operator assumption proven false |
| `scale-vulnerability` | Single-operator pattern that won't survive scale |
| `earn-by-incident` | N+1 evidence on a deferred primitive |

`primitive` and `category` are orthogonal: `primitive` says *what this is evidence about*; `category` says *what kind of evidence*.

## Logging

Use `tools/log-incident.py`:

```bash
python tools/log-incident.py log <primitive> <severity> "<symptom>" --category <cat>
```

Example:

```bash
python tools/log-incident.py log capability-broker high \
  "skill committed credential to git" --category governance-leak
```

## Counting

```bash
python tools/log-incident.py count --primitive capability-broker
```

Returns the number of med-or-higher incidents for that primitive. Three or more triggers promotion review.

## Append-only

`incidents.jsonl` is append-only. Never edit past lines. If a past incident's symptom or category was wrong, append a new line correcting it (with `primitive: "correction"` and a pointer in `symptom`). The ledger is forensic; mutability would defeat its purpose.
