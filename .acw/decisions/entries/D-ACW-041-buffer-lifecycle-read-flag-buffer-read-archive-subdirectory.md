---
id: D-ACW-041
title: "Buffer lifecycle: `read:` flag + `_buffer/_read/` archive subdirectory"
date: 2026-05-05
status: accepted
kind: decision
updated: 2026-05-13
---

# D-ACW-041 — Buffer lifecycle: `read:` flag + `_buffer/_read/` archive subdirectory

**Date:** 2026-05-05

**Decision:** After an absorption candidate is processed, the operator flips `read: false` → `read: true` in the file's frontmatter, adds an `absorbed_in:` pointer naming where it landed, and moves the file from `_buffer/` to `_buffer/_read/`. The session-start spine already excludes `_read/` from its walk (per spine convention), so processed notifications stop surfacing as drift. History preserved via git. Documented in `rules/multi-instance-topology.md` § "Buffer lifecycle." Applied retroactively — five existing files moved this session (3 backfilled with `read: true` + `absorbed_in:` pointers; 2 already flipped earlier today).

**Rationale:** Convention gap surfaced when operator asked "what happens to files in the buffer once they've been consumed?" The honest answer was: nothing, today. Three older absorbed-but-never-flipped files (D-001 source, cs-copilot rename FYI, Kashef YT note) would still surface as unread notifications on every `/acw-session start` if the spine took the read flag seriously — noise that defeats the buffer's purpose. The session-start spine already documents "do not descend into a `_read/` subdirectory," implying the convention was envisioned but never operationalized. This decision operationalizes it. Cheap form factor (one paragraph in the topology rule + one mkdir + git mv); structural prevention (every absorbed candidate stops surfacing as drift, every session, forever).

**Why subdirectory and not deletion:** the absorbed candidate is mirrored into the consuming surface (decision-log entry, research note, etc.), so the buffer file IS technically redundant after absorption. But: the buffer file carries source attribution (the `from_session_capture` pointer back to the originating instance's session) that the consuming surface may not preserve. Keeping the buffer file in `_read/` preserves the chain of evidence at zero cost.

**Why not just trust git history:** operator legibility. `git log _buffer/` requires intent; `ls _buffer/_read/` is the natural read. Archive subdirectory is the cheaper UX for "what's been processed?"

**Source:** Operator session 2026-05-05, immediately after the buffer-state inspection that revealed three older files still showing `read: false`. Operator approved option 2 (archive subdirectory) over option 1 (accept accumulation) and option 3 (delete on flip).

**Open follow-ups:**
- `/acw-session end` could optionally surface a "any unprocessed buffer notifications?" prompt during the bookend, prompting the operator to flip-and-move at session-end. Earn-by-incident: surfaces only if buffer accumulates faster than the operator processes manually.
- Cross-instance: downstream instances (cs-copilot, _Command, etc.) inherit the convention via the topology rule (template_layer propagation). Their own `_buffer/` directories follow the same lifecycle.
- `_read/` archive is not pruned. If it grows large enough to bother `git status` or directory listings, an annual archive (e.g., `_buffer/_read/2026/`) would earn its build. Not now.
