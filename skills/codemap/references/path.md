# path

Pass-through to `graphify path`. Shortest path between two nodes in the codemap.

## Pre-flight

Profile + module checks. Graphify availability check. `.acw/codemap/graph.json` must exist.

## Invocation

```
/codemap path "<node-a>" "<node-b>"
```

The wrapper invokes:

```
subprocess.run(
    ["graphify", "path", node_a, node_b],
    cwd=".acw/codemap",
    check=True,
)
```

Node identifiers can be Graphify's normalized labels (e.g., `auth_verify_token`), file paths (`auth/auth.py`), or class/function names. Graphify resolves; the wrapper passes through.

## Output

Graphify writes the shortest path (node-by-node, with edge relations) to stdout. The wrapper streams it through.

## Use cases

- "Why does `payment.refund` depend on `notification.email_template_3`?" → `/codemap path "payment.refund" "notification.email_template_3"`.
- Debugging unexpected coupling surfaced in `GRAPH_REPORT.md`'s Surprising Connections section.
- Onboarding: trace from a known entry point to an unfamiliar module.

## What path does NOT do

- Does not search `acw-edges.json` for bridge edges. If a path goes through `implements_decision`, use `/codemap explain` on the decision-side nodes instead.
- Does not return multiple paths or shortest-K paths — Graphify returns one.

## Failure modes

- **No path exists.** Graphify reports "no path"; wrapper exits 1.
- **Node not found.** Graphify reports the unresolvable label; wrapper exits 1.
