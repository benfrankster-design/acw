---
id: D-ACW-008
title: "Paths block + manifest-tooling spec"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-008 — Paths block + manifest-tooling spec

**Date:** 2026-05-02
**Decision:** `acw-state.yaml::paths` declares every substrate file path. The bookend skills read paths from this block at runtime; canonical defaults documented in `rules/manifest-discipline.md`. The manifest-tooling spec (four operations: load, append, contains, validate) ships in `rules/manifest-discipline.md` with a stdlib-only Python reference implementation in `tools/manifest.py`.
**Rationale:** Decouples bookend skills from hardcoded paths. Future template evolution (moving a substrate file) requires editing one yaml block per instance instead of grepping skills. Manifest-tooling spec is the fourth application of the manifest-discipline pattern (after auto_load_at_session_start, three-layer manifest, vocabulary canon) — the operator chose to ship the shared tooling now rather than wait for a fifth case. Section heading conventions also moved to per-file frontmatter (`section_conventions` key).
**Source:** Operator scoping conversation, turns 67–73. Reference implementation is 33-test TDD; subagent verified spec/impl alignment before commit.
