---
class: operational
authority: canonical
stability: stable
loaded_by_agent: yes
---

# Promotion Ritual — How Deferred Primitives Earn v0.2

**Version:** 0.1.0
**Status:** Normative. No deferred primitive ships without this ritual.

---

## The rule

A primitive listed in `DEFERRED.md` promotes to a shipped state only when:

1. **Three or more incidents above low severity** are logged in `incidents.jsonl` naming the same primitive as their `primitive` field.
2. **A decision entry** appended to `decisions/decision-log.md` under the "Decisions and Rationale" section, approving the promotion, with the incident IDs cited in the `Rationale` field.
3. **The promotion is executed atomically** (one commit) following the mechanical steps below.

No shortcuts. No exceptions for primitives the operator feels strongly about. The discipline is the point.

---

## Why this ritual exists

The deferred library is a restraint device, not a roadmap. Without a mechanical ritual, the restraint collapses into "I'll do it when I feel like it," and every deferred primitive becomes a procrastination target or a builder-mode tunnel-vision trigger. The ritual forces the operator to prove, in countable incident evidence, that the primitive has earned its ship.

Three incidents is the threshold because:
- One incident is noise
- Two incidents could be a coincidence
- Three incidents is a pattern worth infrastructure investment

The threshold is not science; it is convention. If an incident is catastrophically severe (severity `high`), one occurrence may justify promotion via an emergency decision record. The operator uses judgment, and the decision record names the emergency.

---

## The mechanical steps

### Step 1. Check the incident log.

```
python tools/log-incident.py count --primitive <name>
```

The tool reports how many incidents above low severity reference the named primitive. If the count is fewer than three, the primitive does not yet qualify. Log more real incidents; do not fabricate.

### Step 2. Write a decision record.

Append a new entry to `decisions/decision-log.md` under the "Decisions and Rationale" section. Use the entry frontmatter format from `rules/decision-tracking.md` with `id: YYYY-MM-DD-promote-<primitive>`. In the `Rationale` section, cite each incident ID (uuid from `incidents.jsonl`) and one-line summaries. Separate the new entry from the previous entry with a horizontal rule.

### Step 3. Read the DEFERRED.md row.

Open `DEFERRED.md`, find the row for the primitive, read the "Shippable form factor" description. That description is the design the original research prescribed. Honor it unless the incident evidence specifically contradicts it.

### Step 4. Ship the primitive.

Create the file or files named in the DEFERRED.md row's form-factor description. Examples:
- `workspace-input-schema` becomes `rules/workspace-schema.yaml`
- `asset-frontmatter` becomes an addition to the existing schema files
- `admission-controller` becomes `rules/admission-controller.md` plus `tools/admission-check.py`

Follow the rules/pipeline-roles.md declaration discipline if the primitive is a skill or tool.

### Step 5. Update DEFERRED.md.

Move the primitive's row from the active deferred table to a "Promoted" section at the bottom of DEFERRED.md. Record the decision ID and the promotion date.

### Step 6. Update CHANGELOG.md.

Add an entry under a new version heading (v0.2.0, v0.3.0, etc.) naming the promoted primitive and linking to the decision record.

### Step 7. Bump the version.

Update `CHANGELOG.md` heading and tag the commit `v0.X.0` where X is incremented per semver. Non-breaking promotions are minor bumps; breaking changes require a major bump and a migration note in the decision record.

### Step 8. Commit atomically.

One commit containing: the decision record, the new primitive files, the DEFERRED.md update, the CHANGELOG update, and the version tag. Commit message format:

```
promote(<primitive>): v0.X.0

Earned by incidents <id1>, <id2>, <id3>.
See decisions/decision-log.md entry YYYY-MM-DD-promote-<primitive>.
```

---

## What promotion does NOT mean

- It does not mean the primitive is now mandatory for other instances of ACW.
- It does not mean the design in `DEFERRED.md` was the only possible design.
- It does not mean the primitive is production-hardened. New primitives earn hardening through use, just as the v0.1.0 primitives did.
- It does not mean the deferred library shrinks by one. The library shrinks only when the primitive actually ships in this instance's rules or tools directory.

---

## Failure modes this ritual is designed to prevent

1. **Builder-mode tunnel vision.** An operator excited by a new design ships a primitive the system does not need. The three-incident threshold is the tripwire.
2. **Procrastination vehicle.** An operator avoids real work by continually refining the deferred library instead of closing current commitments. The ritual requires real incidents from real work, not synthetic ones.
3. **Silent accretion.** Primitives land in `rules/` without a paper trail. The decision record is the paper trail.
4. **Version drift.** A promoted primitive ships in one branch, the deferred table still lists it, the CHANGELOG never updates. The atomic commit requirement prevents this.

---

## What to do if the incident evidence is ambiguous

- **Not enough incidents.** Keep working. Log future incidents faithfully. The primitive stays deferred.
- **Incidents are low severity.** Reconsider whether the primitive is actually needed at all. Low-severity incidents are the operator absorbing the cost rather than the system needing infrastructure.
- **Incidents are conflated across primitives.** Split the incidents. An incident that argues for two primitives probably names the wrong one. Use `log-incident.py edit` to correct the primitive field, and document the correction in a decision record.
- **Incidents are old.** An incident from six months ago that never recurred is stale evidence. Give weight to recency. The operator's judgment call.

---

## Demotion

A promoted primitive that turns out to be wrong can be demoted back to `DEFERRED.md` via the same ritual in reverse. The decision record names the failure, the files are moved back to stubs (or deleted if the stub is still correct), and the CHANGELOG records the demotion under a new version. Demotion is rare. It is not forbidden.

---

## Changelog

- **v0.1.0 — 2026-04-11** — Initial release. Three-incident threshold. Eight mechanical steps. Decision record required.
