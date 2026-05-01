---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Conception Evolution Log

Dated record of how this instance's understanding has changed over time. Each entry captures a genuine conceptual shift — not every decision, not every session, but every moment where a prior belief was replaced by a new one.

**Updated by:** `/capture-session` proposes entries after processing session transcripts. Operator approves before append.

**Relationship to research-state.yaml:** This file records *how you got here*. research-state.yaml records *where you are now*. When capture-session identifies a shift, it proposes both an evolution.md entry and a research-state.yaml update. The evolution entry is the provenance; the state update is the truth.

## Entry format

```markdown
### YYYY-MM-DD — [one-line description of what shifted]

**Changed:** [the new belief]
**Replaced:** [the old belief]
**Justified by:** [the source — a session transcript, a research file, a conversation, a real-world incident]
**Stale in template:** [which files in the ACW instance are now inconsistent with this shift, if any]
```

## Entries

### 2026-04-30 — ACW reframed as instance of itself; project block added

**Changed:** ACW is an instance of itself that also serves as a template. Most workspaces will be one or the other; ACW (and Frank Context tomorrow) is both at once. The skill suite now runs on ACW like any other instance.
**Replaced:** "ACW is the template, period." Earlier framing treated ACW's lack of a `project:` block as deliberate.
**Justified by:** Operator framing question, turn 37 of the v0.2.0 absorption arc. The accumulated substrate (decisions, tasks-status, build-log, incidents, evolution, glossary, threat-model) gave the prior framing the lie — ACW had been operating as its own instance from session zero.
**Stale in template:** `acw-state.yaml` was missing a `project:` block; added in rc3 with `code: ACW`. `LAYERS.md` mixed generic pattern with ACW-specific narrative; split in rc3.

### 2026-04-30 — Manifest-discipline named as a recurring pattern

**Changed:** Single source of truth, additive maintenance by skill, removal by ritual, lint as safety net — this shape now appears three times in ACW (auto_load_at_session_start, three-layer manifest, canon governance state machine). Three applications is when a pattern becomes a primitive worth naming. Codified as `rules/manifest-discipline.md`.
**Replaced:** Treating each list as bespoke. Reinventing the load/validate/append logic per consumer.
**Justified by:** Direct operator questioning during the LAYERS.md split — "is the three-layer model something that ships or specific only to the author's meta template instance?"
**Stale in template:** None. The new rule ships in `rules/manifest-discipline.md` (template_layer); every derived workspace gets it.
