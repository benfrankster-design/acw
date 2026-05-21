---
date: 2026-05-13
participants: [operator, agent]
topic: v0.9.9 drift short-circuit and buffer sweep
decisions_made: [D-ACW-049]
conceptual_shifts: yes
linked_files:
  - acw-state.yaml
  - rules/instance-current-manifest.md
  - skills/acw-session/references/start.md
  - skills/acw-session/references/end.md
  - skills/acw-instance/references/upgrade.md
duration_minutes: 30
---

# Session capture 2026-05-13 — v0.9.9 drift short-circuit and buffer sweep

## 1. Topic

Act on the cops `_buffer/` note flagging the redundant full-body read of `instance-current-manifest.md` in `/acw-session start` Step 5. Land three coupled changes as v0.9.9: (1) drift-walk short-circuit; (2) buffer-sweep convention so acted-on `_buffer/` notes auto-archive on session end; (3) hardening the short-circuit's correctness signal from file mtime to an explicit `synced_to:` frontmatter field on the manifest cache.

## 2. What was decided

- **D-ACW-049** — v0.9.9 ship: drift-walk short-circuit in `/acw-session start` Step 5 + buffer-sweep convention added to Step 4 / end Phase 2 + `synced_to:` frontmatter field on `rules/instance-current-manifest.md` (written by `/acw-instance upgrade`, read by start). Bump `acw-state.yaml::version`, `last_reconciled_version`, and manifest `synced_to:` to `0.9.9` together.

## 3. What changed in the conception

The drift check was treated as load-bearing; the cops note exposed it as structurally dead code in normal operation. `/acw-instance upgrade` writes the local manifest cache and bumps `last_reconciled_version` atomically, so under normal operation those two surfaces never disagree — the drift walk is guaranteed empty by construction, and the only meaningful failure modes are broken upgrade or manual edit of the cache. The conception shifts from "drift check is the safety net" to "drift check is a fallback for the broken-upgrade edge case; the common path is structurally `no-op` and should be free."

Companion shift: `_buffer/` notes were a one-way drop (system writes, operator manually archives). The new buffer-sweep convention closes the loop: capture file marks acted-on notes; end verb sweeps them to `_read/`. `_buffer/` is now a true queue with explicit lifecycle, not a notification graveyard.

## 4. What was built / changed

- `acw-state.yaml` — `version` 0.9.8 → 0.9.9; `last_reconciled_version` 0.9.8 → 0.9.9.
- `rules/instance-current-manifest.md` — added `synced_to: "0.9.9"` frontmatter field; added header paragraph documenting the field's contract; new registry entry `synced_to:` frontmatter on this file — v0.9.9.
- `skills/acw-session/references/start.md` — Step 5 short-circuit using `synced_to == last_reconciled_version`; Step 4 acted-on tracking convention (capture file `## Buffer notes acted on` section).
- `skills/acw-session/references/end.md` — Phase 2 append-only subset gains "Buffer sweep" line item: read capture's `## Buffer notes acted on`, move each listed file to `_buffer/_read/`.
- `skills/acw-instance/references/upgrade.md` — refresh-canonical-cache step now writes `synced_to:` after overwriting the manifest.
- `_buffer/2026-05-13--cops-acw-session-start-redundant-manifest-read.md` → moved to `_buffer/_read/` (acted on this session, dogfooding the new sweep convention manually since end-verb code lands in this same session).

## 5. Open questions left

*(None — session closed cleanly.)*

## 6. Operator directives (verbatim)

> "Operator said: 'when buffer items are read and moved to decisions the buffer note should move to _read.' (turn 4)"

> "Operator said: 'do that now' [in response to offered `synced_to:` follow-up] (turn 8)"

## 7. Cleaned transcript excerpt

Skipped — wording captured above is sufficient.
