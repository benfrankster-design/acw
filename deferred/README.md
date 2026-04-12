---
class: deferred
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Deferred Library — Overview

This folder is the deferred library. It holds design documents for eleven primitives that ACW has deliberately not shipped in v0.1.0. Each primitive has its own subfolder with a README covering what it is, the prior art it draws from, its activation trigger, its shippable form factor, and what it is explicitly not.

## Canonical vs derived

The authoritative list of deferred primitives is `DEFERRED.md` at the repository root. This folder is the derived view: one subfolder per primitive, each with its own README, humans can navigate it spatially. If you are asking "what's in the library," read `DEFERRED.md` first — that file is `authority: canonical`. The subfolder READMEs here are `authority: derived` and may drift.

**Drift detection.** `tools/log-incident.py check-drift` walks this folder and compares each subfolder README against the canonical row in `DEFERRED.md`. Run it manually, recommended monthly. When drift is detected, log an incident via `tools/log-incident.py log`.

## The activation trigger rule

No primitive in this library ships until its activation trigger fires. The rule is mechanical: a primitive earns promotion review when three incidents at severity `med` or higher, on that primitive, are logged in `incidents.jsonl`. Some primitives have stricter triggers (a single specific high-severity incident, or an external condition). Subfolder READMEs elaborate per-primitive.

Promotion review opens a decision-log entry. It does not guarantee ship. The promotion ritual in `rules/promotion-ritual.md` runs eight mechanical steps before a deferred primitive becomes a shipped primitive.

## The library is a restraint device

This folder exists to preserve design work without shipping it prematurely. The author's known failure mode is builder-mode tunnel vision: enthusiasm for a primitive, followed by ship, followed by maintenance cost for something the workspace did not yet need. The deferred library is the mechanical restraint against that pattern.

If you are tempted to build one of these primitives without an activation trigger firing, stop and read `SKEPTIC.md`. The skeptic is the voice of this restraint in prose form.

## Pointer

See `SKEPTIC.md` before proposing a promotion from this library.
