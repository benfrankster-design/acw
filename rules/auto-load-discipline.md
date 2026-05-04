---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: no
---

# Auto-Load Discipline

Earn-by-incident applied to the auto-load list. Every entry in `acw-state.yaml::auto_load_at_session_start` declares a claim — *what fails if this isn't loaded every session?* If the answer is "the skill that needs it loads it itself" or "agents can grep when relevant," the entry didn't earn its slot.

This rule is normative. The audit verb (`/acw-instance audit`) walks the instance's `auto_load_at_session_start` block, compares each entry against the canonical recommendations below, and proposes demotions for entries that don't carry a justified claim.

## Why this rule exists

The auto-load list is the most expensive substrate surface in the workspace. Every entry is loaded into context at every session start, every chat, every agent invocation. A 17k-line decision log loaded by default costs the operator real money on every chat with no agent memory recall — across thousands of invocations per week, the cost compounds.

Earned by `incidents.jsonl` entry `a8e771f0-7686-484d-b89e-cc25e96f8c93` (cost-friction, severity med, 2026-05-04) and follow-on incident `<v0.9.0-incident-uuid>` (auto-load bloat, severity med, 2026-05-04). The v0.8.0 ship attacked the bookend's per-invocation cost (Haiku default, quick mode); v0.9.0 attacks the structural per-session-load cost.

The principle is the same earn-by-incident discipline that governs the deferred library and the recommended-blocks registry: nothing ships without a named, dated claim justifying it. Auto-load entries are no different.

## The discipline gate

Every entry in `auto_load_at_session_start` MUST satisfy one of:

1. **Carry a structured `claim` field** declaring what fails without auto-load (and an `earned_by` field naming the activation evidence).
2. **Match a path in the canonical recommendations below** (in which case the canonical claim applies).
3. **Be marked `earned_by: legacy-pending-review`** (transitional; the audit verb flags these for operator review on next pass).

A bare-path entry in a v0.9.0+ instance is treated as `legacy-pending-review`. The audit verb proposes structuring or demoting it.

## Structured entry shape

```yaml
auto_load_at_session_start:
  - path: tasks-status.md
    claim: "Pending work surface must be visible at session start; without it agents propose duplicate work."
    earned_by: structural
  # Backward-compat — bare paths are treated as legacy-pending-review.
  - decisions/decision-log.md
```

Fields:

| Field | Required | Values |
|---|---|---|
| `path` | yes | path relative to workspace root |
| `claim` | required for structured form | one-sentence statement of what fails without auto-load |
| `earned_by` | required for structured form | `structural` (claim is doctrine), `legacy-pending-review` (transitional, surfaces in next audit), or an `incidents.jsonl` uuid (claim earned by named incident) |

Bare-path entries (legacy form) remain valid in v0.9.0 — `tools/manifest.py::load` accepts both shapes. The discipline gate fires at audit time, not at load time. This keeps every existing instance valid on day-one of v0.9.0; the discipline tightens via operator audit, not forced migration.

## Canonical recommendations

The four files ACW canonical recommends for auto-load. Each carries a stated claim and is `earned_by: structural`. Instances inherit these recommendations; instances may override (drop a recommended entry, add an instance-specific entry) but each override needs its own structured claim.

### `decisions/decision-log.md`

**Claim:** Recently decided history must be visible to agents at session start; without it, agents re-litigate settled choices and propose alternatives that have already been considered and rejected.

**Earned by:** structural.

**Caveat:** the value is concentrated in the most recent ~10–20 entries. Older history is reference material, not load-bearing for current decisions. If the file grows past ~15k tokens, archive older entries via the promotion ritual in `rules/decision-tracking.md`.

### `rules/instance-hard-rules.md`

**Claim:** Stop-work rules must be visible to every agent at every session start. Loading them on-demand is too late — by the time the agent realizes a hard rule applies, it may already be acting against one.

**Earned by:** structural. The whole point of the file is universal pre-load.

### `tasks-status.md`

**Claim:** Pending work surface must be visible at session start; without it agents propose duplicate work, miss the operator's queued items, and lose continuity across sessions.

**Earned by:** structural.

**Caveat:** the value is concentrated in the Pending and Parked sections. The Done section is historical narrative, redundant with `build-log.md`, and earns archival per the rolling-window discipline in `rules/task-tracking.md` once it exceeds ~3 sessions inline.

### `glossary.md`

**Claim:** Vocabulary canon prevents drift to colloquial English in agent output. Without it, agents use "campaign" instead of "fundraiser," "donor" instead of "giver," etc., which propagates into customer-facing artifacts before review catches it.

**Earned by:** structural.

## Demotion candidates (declared not auto-load-justified)

The following paths appear in some instances' auto-load lists but are NOT recommended for auto-load by ACW canonical. Each has a stated reason. Audit will propose demotion when found in an instance's `auto_load_at_session_start`.

### `rules/manifest-discipline.md`

**Reason for demotion:** consumed only by skills that perform manifest classification (the bookend's Phase 2 step). Those skills load the rule directly when needed. Auto-loading it for every chat costs context the consumer-skill model can pay on its own.

### `rules/instance-current-manifest.md`

**Reason for demotion:** consumed only by `/acw-session start` Step 5 (drift check) and `/acw-instance audit|upgrade`. These skills read it directly. Operators reading it for reference do so on demand.

### `rules/multi-instance-topology.md`

**Reason for demotion:** the rule's own opening section declares it "applies when multi-domain." Single-operator workspaces don't qualify. Multi-instance lattices that genuinely need it can declare an instance-specific structured entry with a claim.

### `incidents.jsonl`

**Reason for demotion:** consumed by `/acw-instance audit` and the promotion-ritual review. Neither needs it auto-loaded into every chat. The forensic record is exactly the kind of file that benefits from on-demand reading scoped to the relevant primitive.

## Instance-specific overrides

An instance may add entries not on the canonical recommendations list, or drop entries that are. Each override requires:

1. A structured entry in `auto_load_at_session_start` with `path`, `claim`, `earned_by`.
2. If the entry is dropping a canonical recommendation, a decision-log entry naming the rationale.

The audit verb respects structured entries with declared claims even when they don't match canonical recommendations. The claim is the contract.

## Discipline application

`/acw-instance audit` reads the workspace's `auto_load_at_session_start` block and produces a report:

```
Auto-load entries (N declared):
  <path>   form: <structured | bare-legacy>   verdict: <KEEP | DEMOTE | REVIEW>   reason: <one-line>
```

`/acw-instance upgrade` applies the verdicts under the existing single approval gate. KEEP entries stay as-is (with structured-form migration proposed if currently bare). DEMOTE entries are removed from `auto_load_at_session_start`; the file itself stays in the workspace. REVIEW entries surface for operator confirmation.

The verb never silently mutates the auto-load list; demotions only fire after operator approval of the migration plan.

## Drift detection

The drift check in `/acw-session start` Step 5 is unaffected by this rule. Drift compares `last_reconciled_version` against earned-in versions in `rules/instance-current-manifest.md`. Auto-load discipline is checked at audit time, not session-start time.

## When to add a new entry to canonical recommendations

If an incident demonstrates a path that materially earns auto-load (skill X failed because file Y was not in context, consistently, across N sessions), the canonical recommendations list grows by:

1. Logging the incident in `incidents.jsonl` per `rules/incident-tracking.md`.
2. Adding the path to the "Canonical recommendations" section above with a stated claim and incident reference.
3. Bumping ACW version per the promotion ritual.
4. New entry's `earned_by` cites the incident uuid.

Until evidence accumulates, the four-file recommendation is the floor.

## When to retire a canonical recommendation

If the load-bearing claim for a recommended path no longer holds (e.g., the file's content moves elsewhere, the consumer-skill loads it directly, the incident class is closed by another fix), retire it via:

1. Decision-log entry naming the change and the incidents that justified the original ship.
2. Removing the entry from "Canonical recommendations."
3. Audit verb flags the retirement as a DEMOTE recommendation for instances still carrying it.
