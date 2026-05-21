---
id: D-ACW-014
title: "`/upgrade-instance` fetches canonical from GitHub as single source of truth; supports adopt mode"
date: 2026-05-02
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-014 — `/upgrade-instance` fetches canonical from GitHub as single source of truth; supports adopt mode

**Date:** 2026-05-02
**Decision:** `/upgrade-instance` fetches `rules/instance-current-manifest.md` from the ACW GitHub repo (`benfrankster-design/acw`, private) on every run via `gh` CLI or `urllib.request` with `GITHUB_TOKEN`. The instance's local copy is a write-once cache of "the last canonical I reconciled to," never used as comparison yardstick. Skill fails closed if GitHub is unreachable. Also adds an adopt mode: when `acw-state.yaml` and/or `rules/instance-current-manifest.md` are missing but ≥3 substrate signals are present, the skill offers to write the missing registration files using the GitHub canonical and proceed to reconciliation.
**Rationale:** Operator rejected a local-ACW fallback as introducing race conditions between local and remote canonical. Single source of truth via GitHub means one pointer; if the repo ever moves, only one place needs updating. The cs-copilot session that prompted this work surfaced a pre-existing substrate-shaped workspace that the original `/upgrade-instance` refused to act on; adopt mode closes that gap. Substance signals threshold (3 of 6) prevents false positives in random workspaces.
**Source:** Operator rejection of local-ACW fallback in the multi-instance topology conversation; cs-copilot adopt-mode requirement surfaced earlier in same arc.
