---
from_project: cx-dashboard-saas
from_session_capture: ~/projects/cx-dashboard-saas/sessions/2026-05-05--week-1-clerk-pivot-and-first-deploy.md
date: 2026-05-05
topic: Build-then-rip pattern in plan-driven instances; should ACW canonical have a "earn auth at correct layer" check
read: true
absorbed_in: research-only (pattern-accumulation; no canonical promotion this incident)
---

# Notification — Build-then-rip auth scaffolding pattern surfaced

**What happened.** `cx-dashboard-saas`'s approved Phase 0 plan (`plans/2026-05-04--phase-0-scaffold-and-tenant-0-dashboard.md`) staged Cloudflare Access for Phase 0 (team auth) and Clerk for Phase 1+ (customer auth). Phase 0 Week 1 spent ~6 hours building Cloudflare Access scaffolding (~250 lines middleware + JWKS + 9-test suite + a Microsoft Entra-flavored runbook) before the operator's mid-runbook question — "why am I adding GSG users to Cloudflare? When the app is built, anyone signing up should just create an account" — collapsed the architecture and triggered D-CXD-005 (drop Cloudflare entirely; Clerk Phase 0 day-1).

The ~250 lines were thrown away. Net cost: ~6 hours, two commits, one deleted runbook.

**Why this matters for ACW canonical.** This is the second consumer-instance friction this week (the first was the runtime-code-location ambiguity already absorbed as D-ACW-039). Both share a pattern: **the plan locked a Phase 0 / Phase 1 staging decision that didn't earn its weight at Phase 0 scale**. In both cases, mid-build the operator surfaced a sharper architectural read that the planning agent didn't bring up earlier.

The structural question for ACW: when an instance's plan stages infrastructure for Phase N+1 with a temporary scaffold for Phase N, ACW canonical doesn't have a "is this scaffold load-bearing or is it build-then-rip?" check.

**Absorption candidate options:**

1. **Add a planning-phase check to ACW's plan template / planner agent guidance.** Before locking a "Phase 0 uses scaffold X, Phase N uses real Y" staging, surface the question: *would building Y directly at Phase 0 cost less than scaffold X plus the eventual rip?* For auth specifically: Clerk's free tier is ~30 minutes to set up; Cloudflare Access scaffolding is ~6 hours. The "Phase 0 simpler" argument was wrong by an order of magnitude.

2. **Add a "build-then-rip risk" check to existing decision-log discipline.** When a decision contains the phrase "Phase N+1 will [replace/rewrite/migrate] this," flag the staging for adversarial review. Most build-then-rip pivots are recognizable from the decision text alone.

3. **Document the pattern in `rules/` or research/** as observed friction. Lighter touch — surfaces the pattern for future planner agents to consider, no schema or check change.

**Recommendation.** Option 3 (document the pattern) at minimum; option 1 (planner-agent guidance) if ACW's planner is part of the canonical scaffold. Option 2 (decision-log discipline) is over-engineering — the pattern is rare enough that automated detection isn't worth the noise.

**Two specific patterns worth canonical mention:**

- **Auth specifically:** B2B SaaS auth almost always wants Clerk / WorkOS / Auth0 from day 1, not edge-level gating. Edge-level gating (Cloudflare Access, IP allowlists) is for *internal* tools or *enterprise SSO overlay on existing customer auth* — not the only auth.
- **Connector creds specifically:** Phase 0 env-var-stored connector creds are a known acceptable hack but should be explicitly tagged "this disappears in Phase N." `cx-dashboard-saas`'s D-CXD-001 mentioned this implicitly; the operator surfaced it explicitly mid-session ("shouldn't this be in a database?"). Worth a glossary or rules entry: *connector-creds-as-env-vars is Phase 0 scaffolding; Week 2 of Phase 0 ships per-tenant DB rows.*

**No action required from ACW** unless the pattern recurs in other consumer instances. Logging here so it's visible.
