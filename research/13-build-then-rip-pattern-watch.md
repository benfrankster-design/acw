---
class: reference
authority: derived
stability: experimental
loaded_by_agent: no
---

# Build-then-rip pattern — watch list (incident #1 of N)

Pattern-accumulation note. Not canonical. Not load-bearing for any skill or rule. Exists so the next incident has something to be the second of.

## The pattern

A plan stages infrastructure across phases — Phase 0 uses scaffold X, Phase N+1 swaps in real Y. Mid-build, the operator or an agent surfaces a sharper read: building Y directly at Phase 0 would have cost less than X plus the eventual rip. The scaffold gets thrown away.

Net cost = scaffold build time + scaffold tear-down time + the eventual real build. Locking the staging in the plan locked the cost.

## Incident ledger

### Incident #1 — cx-dashboard-saas auth pivot (2026-05-05)

- **Plan:** `cx-dashboard-saas/plans/2026-05-04--phase-0-scaffold-and-tenant-0-dashboard.md` staged Cloudflare Access for Phase 0 (team auth) + Clerk for Phase 1+ (customer auth).
- **Built:** ~250 lines middleware, JWKS handling, 9-test suite, Microsoft Entra runbook. ~6 hours.
- **Pivot:** mid-runbook, operator surfaced "why am I adding GSG users to Cloudflare? When the app is built, anyone signing up should just create an account."
- **Outcome:** D-CXD-005 (drop Cloudflare entirely; Clerk Phase 0 day-1). Scaffold ripped. Two commits + one runbook deleted.
- **Source:** absorption note `_buffer/2026-05-05-cx-dashboard-saas-auth-pivot-build-then-rip.md`.

## Why this is research-only and not canonical

- ACW canonical doesn't ship a planner skill — there is no surface to hang "ask the scaffold-vs-real cost question" guidance on without inventing infrastructure.
- The auth-specific and connector-creds-specific recommendations from the absorption note are vendor-flavored SaaS-build wisdom, not workspace-template doctrine. ACW canonical stays vendor-neutral by design (same reason `AGENTS.md` exists instead of `CLAUDE.md`).
- Plans are user-driven artifacts. `plans/` is a scratchpad convention, not substrate that needs canonical format or discipline.
- Earn-by-incident threshold (count of three) genuinely applies. This is incident #1.

## What earns promotion

If a second consumer instance ships a plan that stages a temporary scaffold and pays the build-then-rip cost — and the cause is recognizably the same shape (plan-locked Phase 0 scaffold the planner should have questioned) — log it here as incident #2 with a link back to its source absorption note. At three incidents, the pattern earns a canonical home; until then, it stays in `research/`.

## What does NOT earn promotion

- Vendor-specific recommendations (Clerk vs Cloudflare, Stripe vs LemonSqueezy, Supabase vs Neon, etc.) — these belong in cx-dashboard-saas's instance-specific notes or in the operator-personal brain, never in ACW canonical.
- Plan-format or plan-discipline rules — `plans/` is whatever the operator wants it to be.
- Decision-log automated detection of "Phase N+1 will replace this" phrases — over-engineering; the pattern is rare enough that automated detection isn't worth the noise.

## Source

Operator session 2026-05-05. Operator quote on declining canonical promotion: "Plans could be anything. It's just the users' work, the operators working with Claude in the workspace for whatever project... I don't really see why a runbook or a rule is why we got to get all technical about the format and the discipline."
