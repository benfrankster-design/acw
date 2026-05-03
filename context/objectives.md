# Objectives — ACW

Current near-term focus.

- **Lattice dogfood:** validate `/acw-instance audit` and `/acw-instance upgrade` against the operator's three downstream workspaces (`cs-copilot`, `gsg-copilot`, `_Command`). Each dogfood produces evidence; bugs found earn v0.N+1 fixes.
- **Operator-centric substrate cluster (v0.6.0, in flight):** `context/`, `inbox/`, tasks-status framing update, meta-layer maintenance harness.
- **Meta-layer harness:** close the staleness gap that produced v0.5.1's front-door cleanup. Substrate has Phase 2 distribution; meta-layer should too.

## Recently shifted away from

- The original v0.1.0 framing of ACW as "the template, period." ACW is also its own first instance, and the three-layer manifest formalizes that. (See D-ACW-006.)
- Permanent divergence as a third terminal flow alongside adopt/absorb. Operator pushback in the v0.4.0 turn made it temporary-pending-review only. Two terminal states, not three. (See `rules/multi-instance-topology.md`.)
