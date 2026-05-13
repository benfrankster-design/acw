---
id: D-ACW-031
title: "`context/` canonical for operator/project context layer"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-031 — `context/` canonical for operator/project context layer

**Date:** 2026-05-02
**Decision:** `context/` ships as canonical instance_layer with four templated files: `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`. Lightweight pointers to operating reality. Read on demand by agents that need the context, not auto-loaded into every chat. Templates render at scaffold time; operator fills with workspace-specific content. Updates happen as operating reality shifts, not on a schedule.
**Rationale:** Substrate categories so far covered decisions (specific choices), rules (governance), skills (operations), glossary (vocabulary). Missing: lightweight context that helps agents calibrate ("what is this workspace for? who matters? how does the operator work?"). `context/` fills the gap. Especially load-bearing for cockpit-shaped instances where personal + business context blends; useful in any workspace type. The four canonical files match `_Command/context/` shape (which surfaced the absorption candidate).
**Source:** Operator design conversation during v0.5.0/v0.6.0 scoping; absorbed from `_Command`'s organic substrate.
