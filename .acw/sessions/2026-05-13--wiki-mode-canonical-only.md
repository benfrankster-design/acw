---
class: capture
authority: derived
stability: stable
loaded_by_agent: no
date: 2026-05-13
project: ACW
version: 0.9.8
---

# 2026-05-13 — wiki-mode canonical-only and contacts opt-in

## 1. Topic

Drop dual-mode support (`single-file` / `wiki`) for `decisions/` and `glossary/`. Wiki is the only sanctioned mode. Add `context/contacts/` as an earn-by-discipline opt-in pattern surfaced by `/acw-instance audit` and `/acw-instance upgrade`. Ship as v0.9.8.

## 2. Decisions made

- **D-ACW-048** — Wiki mode canonical-only for decisions and glossary; `context/contacts/` as earn-by-discipline opt-in. Entry written to `decisions/entries/D-ACW-048-wiki-mode-canonical-only-and-contacts-opt-in.md`. Status: accepted.

## 3. Conceptual shifts

- Dual-mode design retired. The v0.9.3 opt-in framing (D-ACW-043) was always a transition state; treating it as a permanent option blocked simplification across the rule, scaffolder, audit, and upgrade surfaces.
- "Earn-by-discipline" pattern formalized as a canonical scaffolder primitive: optional templates that ship in `tools/templates/` but are NOT propagated by default; audit emits opt-in plan rows; operator accepts at upgrade plan-review time. `context/contacts/` is the first instance of the pattern.

## 4. Tasks moved

- **New Pending:** Dogfood `/acw-instance upgrade` against cs-copilot / gsg-copilot / _Command for v0.9.8 wiki-mode canonical-only migration. (Subsumes earlier v0.9.3 dogfood row.)
- **Completed:** none — this session was a doctrine + tooling change.

## 5. Open questions

None surfaced this session. The migration tooling (`tools/migrate_to_wiki.py`) is already in place from v0.9.6; the v0.9.8 change is doctrine + skill-reference rewiring, not new tooling.

## 6. Hard-rule changes

None.

## 7. Sources

None external. Operator directive (in-session).

## 8. Incidents

None.

## 9. Files touched

- `acw-state.yaml` — version 0.9.7 → 0.9.8; `instance_layer` rows for decisions/glossary swapped to INDEX-based wiki templates; `empty_dirs` extended with wiki subdirectories; dual-purpose NOTE removed.
- `tools/templates/acw-state.yaml.tmpl` — wiki-mode `decision_tracking` + new `glossary` block + `paths` block; auto-load + canonical-runtime-files reference INDEX files.
- `tools/templates/decisions-INDEX.md.tmpl` (new)
- `tools/templates/glossary-INDEX.md.tmpl` (new)
- `tools/templates/context-contacts-INDEX.md.tmpl` (new)
- `rules/decision-tracking.md` — "The format" section rewritten for wiki-only; rolling-window section trimmed to one paragraph about INDEX sort order.
- `skills/acw-instance/SKILL.md` — Step 2 substance scan + Step 3 fetch stripped of mode branching.
- `skills/acw-instance/references/audit.md` — "Mode-dependent substrates" replaced with mandatory legacy → wiki migration; new "Optional patterns (earn-by-discipline)" section for contacts opt-in.
- `skills/acw-instance/references/upgrade.md` — single-file → wiki section reframed as mandatory v0.9.8 doctrine; new "Optional patterns" section for contacts execution; adopt-mode defaults clarified.
- `decisions/entries/D-ACW-048-wiki-mode-canonical-only-and-contacts-opt-in.md` (new)
- `decisions/INDEX.md` — D-ACW-048 prepended.
- `tasks-status.md` — v0.9.8 dogfood Pending row added.
