---
from_project: cs-copilot
from_session_capture: ~/projects/cs-copilot/decisions/decision-log.md::D-015
date: 2026-05-01
topic: source instance gsg-copilot renamed to cs-copilot
read: true
absorbed_in: informational (sibling-instance rename FYI; no canonical promotion needed)
---

# Notification — gsg-copilot renamed to cs-copilot 2026-05-01

The project that was the source-instance for the v0.2 promotion proposal in `research/09-gsg-copilot-instance-extensions.md` has been renamed from `gsg-copilot` to `cs-copilot`. The proposal title and body retain the original name as historical record, with a top-of-file note pointing to D-015 in the source project.

**What changed in the source project:**
- Folder: `c:\Users\benja\projects\gsg-copilot\` → `cs-copilot\`
- Slug: `gsg-copilot` → `cs-copilot` (also `GSG Copilot`, `GSG copilot`, `gsg_copilot` variants)
- Git: project gained git substrate during the rename (baseline + rename commit on `main`)

**Why:** Project is CS-specific (CS agents working tickets in the CS panel), not a broader GSG product. Renaming the slug aligns the surface name with the actual scope.

**No action required from ACW** unless future iterations of the v0.2 promotion proposal want to update the `source_instance:` frontmatter and inline references. The recommendation is to leave both as historical record — the rename happened after the proposal was authored and shouldn't rewrite its provenance.

**Future proposals from this instance** should reference `cs-copilot` as the source-instance, not `gsg-copilot`.
