---
name: acw-session
description: >
  ACW session lifecycle orchestrator. Three verbs: `start` (init capture + drift),
  `update` (mid-session note), `end` (distribute + metabolize + optional synapse/research).
  Mode-portable across single-file and wiki substrate. Operator-invoked only.
role: orchestrator
capabilities: []
model: claude-sonnet-4-6
---

| Domain | 6C Primary | Governance |
|--------|-----------|------------|
| (per instance) | Coordination | High |

# acw-session

Object-centered orchestrator. Object: this ACW instance's session lifecycle.

## Command table

| Command | What it does | Reference |
|---|---|---|
| `start` | Init capture + tracker; run drift check; surface buffer. | `references/start.md` |
| `update` | Mid-session checkpoint — append timestamped note to active capture. | `references/update.md` |
| `end` | Profile-dispatched: `quick` (default) / `full` / `log-only` / `synapse-only` / `research-only`. | `references/end.md` |

Routing: argument required. No-arg invocation prints this table. Unknown command errors with the table.

Every verb loads `references/spine.md` first (shared spine: pre-flight, config, paths, buffer, recent captures, safety, idempotency). Then its own reference.
