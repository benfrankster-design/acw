---
from_project: cx-dashboard-saas
from_session_capture: ~/projects/cx-dashboard-saas/sessions/2026-05-04--phase-0-week-1-kickoff.md
date: 2026-05-04
topic: ACW scaffold leaves "where does app code live?" implicit; consumers may need explicit guidance
read: true
absorbed_in: D-ACW-039
---

# Notification — App-code location convention is unclear in canonical scaffold

When `cx-dashboard-saas` (a consumer instance) reached the point of running `create-next-app`, the operator and I had to make an unguided structural decision: does the Next.js app go at the project root (alongside `decisions/`, `rules/`, `sessions/`, `acw-state.yaml`, `CLAUDE.md`) or in a subdirectory (e.g. `web/`)?

**What we picked.** Subdirectory: `web/`. ACW substrate stays clean at root; runtime code lives under `web/`. Vercel project root = `web/`.

**Why this matters for ACW canonical.** The plan that drove this instance (`plans/2026-05-04--phase-0-scaffold-and-tenant-0-dashboard.md`) said "Next.js at project root" without addressing the conflict with ACW substrate at root. Consumer instances that ship runtime code (web apps, services, agents) will keep hitting this. ACW's current canonical scaffold treats every instance as if it's a pure-substrate workspace, but several active instances (cs-copilot, cx-dashboard-saas, likely others) ship real code too.

**Absorption candidate options for ACW canonical:**

1. **Add a `runtime_code_location` field to `acw-state.yaml`** — declared per-instance: `root` | `subdir:<name>` | `none`. Consumer instances declare upfront where runtime code lives so agents have a deterministic answer to "where do I `cd` to run the app?"

2. **Add a section to `AGENTS.md` (or new `rules/runtime-code-location.md`)** — recommend `subdir/` for any instance shipping runtime code, root only for pure-substrate workspaces. Rationale: substrate is governance (slow-moving, decision-driven); runtime is operational (fast-moving, build-driven). Mixing them at one path level conflates two clocks.

3. **Leave it implicit; document the pattern as observed convention.** Lighter touch — just a note in `rules/multi-instance-topology.md` that "instances shipping runtime code typically locate it under `web/`, `server/`, or `agents/` subdir." No schema change.

**Recommendation:** option 2 or 3, not 1. The schema field is over-engineering for a convention that's stable once chosen. A rules file that says "if your instance ships runtime code, put it in a subdir, here's why" is enough.

**No action required from ACW** unless this trips other consumer instances. Logging here so the pattern is visible the next time it does.
