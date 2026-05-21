# explain

Pass-through to `graphify explain`. Plain-language description of a node and its immediate neighborhood.

## Pre-flight

Profile + module checks. Graphify availability check. `.acw/codemap/graph.json` must exist.

## Invocation

```
/codemap explain "<node>"
```

The wrapper invokes:

```
subprocess.run(
    ["graphify", "explain", node],
    cwd=".acw/codemap",
    check=True,
)
```

`<node>` can be a Graphify normalized label, file path, or symbol name. Graphify resolves; the wrapper passes through.

## Output

Graphify writes a structured explanation: what the node is, what it calls, what calls it, what it contains, community membership, and any rationale-tagged content nearby. Streamed through unchanged.

## ACW augmentation (post-pass-through)

After Graphify's output, the wrapper appends bridge-edge context from `.acw/codemap/acw-edges.json`:

```
ACW substrate links:
  implements_decision → D-CATL-003 (Atlas catalog frontmatter convention)
    confidence: EXTRACTED (literal id match in docstring)
  implements_decision → D-CATL-007 (HC article id normalization)
    confidence: INFERRED 0.82
    rationale: <model's one-sentence justification>
```

If no bridge edges exist for the node, the section is omitted.

This is the only verb that merges Graphify's native view with ACW bridge edges. Other verbs read one or the other; `explain` joins.

## Use cases

- "What is `MailRouter.deliver`?" → `/codemap explain "MailRouter.deliver"`.
- Investigating a node before refactoring.
- Following bridge edges back to the decisions that govern a piece of code.

## Failure modes

- **Node not found.** Graphify reports; wrapper exits 1.
- **acw-edges.json missing or unreadable.** Wrapper completes Graphify output, prints one-line warning about the bridge view, exits 0 (Graphify's output is still useful).
