# query

Pass-through to `graphify query`. BFS traversal over the codemap from a natural-language question, returning context capped at a token budget.

## Pre-flight

Profile + module checks. Graphify availability check. `.acw/codemap/graph.json` must exist (else exit 2 with "no codemap built yet").

## Invocation

```
/codemap query "<question>" [--budget N]
```

The wrapper invokes:

```
subprocess.run(
    ["graphify", "query", question, "--budget", str(budget)],
    cwd=".acw/codemap",
    check=True,
)
```

`cwd` is set to `.acw/codemap/` so Graphify finds the relocated `graph.json` and cache.

`--budget` defaults to 4000 tokens if not supplied; the wrapper passes through whatever the operator provides.

## Output

Graphify writes the traversal result to stdout. The wrapper streams it through unchanged.

## What query does NOT do

- Does not run AST or Stage 2.
- Does not modify the graph.
- Does not consult `acw-edges.json` (Graphify's query is over its native `graph.json`). For substrate-aware queries that include `implements_decision` edges, use `/codemap explain` on a specific symbol and follow the bridge edges manually, or wait for a future verb that merges the views.

## Failure modes

- **Graphify exits non-zero.** Forward stderr; exit with same code.
- **Question is empty.** Refuse with the syntax hint.
