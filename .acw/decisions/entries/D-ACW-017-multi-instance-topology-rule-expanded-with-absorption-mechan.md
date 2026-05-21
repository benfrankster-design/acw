---
id: D-ACW-017
title: "Multi-instance topology rule expanded with absorption mechanics"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-017 — Multi-instance topology rule expanded with absorption mechanics

**Date:** 2026-05-02
**Decision:** `rules/multi-instance-topology.md` expanded with four sections: three-flow resolution model (adopt / absorb / instance-specific), absorption candidate format (`_inbox/` payload schema), divergence markers (`divergent_pending_review` for temporary, `instance_specific_substrate` for permanent with decision-log ref), and re-adoption flow. Plus cross-repo write governance for workspaces writing absorption candidates to ACW's `_inbox/`.
**Rationale:** The v0.3.0 ship named the lattice topology but didn't specify how absorption actually flows mechanically. The operator's question "how does ACW know about an absorption candidate?" exposed the gap. The mechanics now use the existing `_inbox/` cross-instance handoff seed. ACW's `/acw-session start` reads `_inbox/`; absorption candidates surface naturally in next session-start.
**Source:** Operator's question on absorption mechanics during the multi-instance lattice conversation.
