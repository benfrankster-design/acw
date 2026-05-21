---
class: buffer
date: 2026-05-14
source: _Command/sessions/2026-05-14--ai-infra-direction-with-robert.md
topic: rag-mcp-poc-and-substrate-tooling-overlap
---

# Buffer — Robert's RAG MCP POC + substrate-tooling relevance to ACW (from _Command huddle 2026-05-14)

## Why this lives in acw/_buffer

Robert built a working RAG + MCP server in roughly half a day on 2026-05-13:
- Qdrant vector DB in local Docker
- Indexes Nextcloud markdown + Confluence + Jira via OAuth
- Honors Nextcloud group permissions for access control
- MCP-exposed so Claude Desktop (and other clients) consume it natively
- Demonstrated live: cross-source query against indexed material, plus access-control honoring across two user accounts in different Nextcloud groups

This overlaps with ACW substrate tooling territory in three specific ways worth tracking:

## 1. Cross-instance retrieval is a substrate question

ACW currently treats each instance's substrate as locally consumed (auto-load at session start, on-demand reference loading). Robert's MCP server pattern hints at a different shape: **a vectorized, queryable view across all substrate surfaces in the home directory, exposed via MCP**.

Imagine: a single MCP server that indexes every ACW instance's `decisions/`, `glossary/`, `sessions/`, `tasks-status.md`, `runbooks/`. Claude Code (and Claude Desktop) consumes it. Cross-instance retrieval ("has any instance decided X?") becomes a single query instead of a manual grep across home-dir.

ACW already has the discipline that makes this viable: substrate is small, dense, atomized (wiki shape), and indexes well. The shape was chosen for human readability + Claude auto-load; it happens to be ideal for vector retrieval too.

## 2. Access-control honoring as a substrate primitive

Robert's POC honors Nextcloud group permissions at retrieval time. ACW substrate doesn't currently encode access control beyond filesystem permissions. For a single-operator instance topology that's fine. For multi-operator instances (or a future where some ACW substrate is consumed by team members other than the operator), an access-control primitive becomes load-bearing.

The cs-ops-spec instance just hit this — it explicitly assumes Nextcloud group permissions as the access-control primitive for downstream knowledge surfaces. ACW canonical could codify the pattern: when an instance is consumed by multiple readers with different scopes, the substrate inherits the host filesystem's group permissions, and any RAG-style query layer must honor them.

## 3. The MCP-server pattern as a canonical ACW capability

ACW's `capabilities` declarations in SKILL.md currently anticipate the broker-sideband shape (per `rules/pipeline-roles.md`). Robert's POC is a working example of what an MCP-server-shaped capability looks like in practice: a single MCP server that wraps multiple data sources, exposes a small set of tools, and is consumed by any MCP-capable client.

Worth considering whether ACW should declare a canonical pattern for "substrate-indexing MCP server" — what tools it exposes (`search`, `get_decision`, `get_glossary_entry`, etc.), what its capability surface looks like, how it interacts with the broker once that ships.

## Implications for ACW roadmap

- **Not urgent.** Single-operator instances are the current scale. The patterns above earn their ship when ACW grows beyond single-operator or when an instance genuinely outgrows in-context auto-load.
- **Worth a deferred/ entry.** Not a v0.x decision; a v1.x consideration.
- **Robert's POC code** would be a useful reference if/when this pattern earns its ship. Ask him for the Docker config + indexing scripts at that point.

## Action items

- [ ] When a future ACW upgrade considers cross-instance retrieval, reference this buffer note
- [ ] When the capability-broker spec firms up, evaluate whether substrate-indexing-MCP-server is a canonical capability shape worth declaring
- [ ] No action needed now
