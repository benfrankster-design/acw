# status

Read-only verb. Reports the current state of `.acw/codemap/` without invoking Graphify or running any rebuild stages.

## Pre-flight

Profile check + module check only. No Graphify availability check (status is purely a reader of existing artifacts; if Graphify isn't installed, status can still report the current graph or report "no graph yet").

## Reads

1. `.acw/codemap/manifest.json` — Graphify's per-file mtime + ast_hash + semantic_hash registry.
2. `.acw/codemap/graph.json` — node and edge counts.
3. `.acw/codemap/acw-edges.json` — bridge edge counts (if present).
4. Source-tree mtimes — to detect files newer than the manifest's recorded mtime (cache staleness signal).
5. `.acw/decisions/entries/*.md` mtimes — to detect decision-log changes since last bridge run.

## Reports

```
[codemap] status
  Last AST rebuild:     <iso timestamp>  (<N hours ago>)
  Last Stage 2 rebuild: <iso timestamp | never>
  Last bridge run:      <iso timestamp | never>
  Graph: <nodes> nodes, <edges> edges
    by file_type:  document <a>, code <b>, rationale <c>
    by relation:   calls <a>, contains <b>, rationale_for <c>, inherits <d>, implements_decision <e>
    by confidence: EXTRACTED <a>, INFERRED <b> (avg <x.xx>), AMBIGUOUS <c>
  Cache:    <K> files cached
  Staleness:
    Source files newer than manifest: <N>  (rebuild recommended if > 0)
    Decision entries newer than last bridge: <N>  (bridge recommended if > 0)
  Cache dir: .acw/codemap/cache/  (<size>)
```

## Exit codes

- `0` — status reported cleanly.
- `2` — `.acw/codemap/` empty or `graph.json` absent. Print: *"no codemap built yet. Run `/codemap rebuild` to initialize."* Exit 2.
- `3` — `graph.json` present but unreadable (corrupt JSON). Print path and error. Exit 3.

## What status does NOT do

- Does not call Graphify.
- Does not modify any file.
- Does not invoke the bridge.
- Does not print a per-node breakdown (use `/codemap explain` or `/codemap query` for node-level detail).

Status is the cheap, always-safe verb. Operator runs it before deciding whether a rebuild is needed.
