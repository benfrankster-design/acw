---
id: D-004
title: "Auto-load convention is vendor-agnostic"
date: 2026-04-30
status: accepted
kind: decision
updated: 2026-05-13
---

# D-004 — Auto-load convention is vendor-agnostic

**Date:** 2026-04-30
**Decision:** AGENTS.md directive 7 declares the auto-load convention as the cross-vendor contract. The canonical file list lives in `acw-state.yaml::auto_load_at_session_start`. Each agent host implements via its native mechanism (Claude Code: `@`-imports in `CLAUDE.md`; agents reading `acw-state.yaml` directly need no host-specific file).
**Rationale:** ACW is designed to outlive any single vendor. Coupling the convention to `@`-imports would couple ACW to Claude Code. Splitting the convention across three layers (prose contract, machine-readable list, host-specific implementation) preserves portability.
**Source:** `research/09-gsg-copilot-instance-extensions.md` C-06
