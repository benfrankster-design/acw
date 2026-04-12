---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Gotchas

- **Multi-source creep**: This skill reads from exactly one source. If you need to read from two sources, create two collector skills and let an orchestrator call both — do not expand this skill's scope to read from multiple surfaces.
