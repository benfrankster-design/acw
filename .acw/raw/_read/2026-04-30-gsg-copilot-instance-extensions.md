---
from_project: gsg-copilot
from_session_capture: ~/projects/gsg-copilot/research/sessions/2026-04-30--acw-substrate-scaffolding-and-bookend-skills.md
date: 2026-04-30
topic: v0.2 promotion proposal + 2 incidents logged + ACW canonical work ready for next session
read: true
absorbed_in: D-001 (v0.2.0-rc1 absorbed C-01/C-02/C-03/C-06/C-09)
---

# Notification — gsg-copilot 2026-04-30 session touched ACW

A gsg-copilot session today did substantive ACW work that needs ACW's attention. Summary:

**New artifact in ACW:**
- `research/09-gsg-copilot-instance-extensions.md` — full v0.2 promotion proposal. 9 candidates (C-01 through C-09) covering substrate items (tasks-status.md, build-log.md, incident category vocabulary), the bookend-skill pattern that supersedes `capture-session`, single-file synthesis cycle (no separate synthesis/ subdir), runbooks layer, auto-load convention, vault-boundary hard rule, backlog triple-tag. Includes full `tools/scaffold-instance.py` specification ready to build, plus a three-layer auto-load convention design (AGENTS.md prose contract + `acw-state.yaml::auto_load_at_session_start` + host-specific entry file).

**Incidents logged in `/Projects/acw/incidents.jsonl`:**
- `e748da25-8996-41e7-9ec0-4142ffde9348` — synapse-rule-sync drift (med). Synapse copies of ACW rules at `~/synapse/Rules/Procedures/` are stale; missing canon-governance.md, canon.yaml, canon-schema.yaml, vocabulary-lint.md, promotion-ritual.md.
- `616d435b-ec6d-470a-9cdf-2935b739e4a1` — instance-bootstrap missing (med). gsg-copilot did not bootstrap from `bootstrap/` (which has only a README); grew its substrate parallel-evolution-style; multiple decisions diverged from canonical without justification.

**Recommended action for ACW's next session:**
1. Read `research/09-gsg-copilot-instance-extensions.md` end-to-end.
2. Decide which of C-01 through C-09 are immediately promotable, which need more incident evidence, which are operator-preference-only.
3. Build `tools/scaffold-instance.py` (full spec in 09 §"`tools/scaffold-instance.py` — full specification") — the load-bearing v0.2 ship that closes Incident D-02 (instance-bootstrap missing).
4. Port and adapt the bookend skills from gsg-copilot:
   - `~/projects/gsg-copilot/skills/capture-and-metabolize/SKILL.md`
   - `~/projects/gsg-copilot/skills/resume-build/SKILL.md`
   - `~/projects/gsg-copilot/skills/resume-build/gotchas.md`
   - 7 specific generalizations enumerated in 09 §C-03.
5. Retire `skills/capture-session/` (superseded; not just extended).
6. Update `acw-state.yaml` and `AGENTS.md` per the proposal.
7. Bump version, write decision-log entry, commit atomically per `rules/promotion-ritual.md`.

**Why this notification exists rather than direct edits to ACW substrate:**
gsg-copilot's `capture-and-metabolize` Phase 2 distribution-scope rule (added this session) keeps each project's substrate clean by routing cross-project work into notifications rather than the originating project's substrate. ACW work belongs in ACW; this notification points at it.

**Action when read:** archive to `_inbox/_read/` after addressing.
