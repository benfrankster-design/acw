---
class: archive
authority: derived
stability: stable
loaded_by_agent: no
---

# Build Log — ACW

Append-only, newest-first narrative of build progress per session.

## 2026-04-30 — RC3: ACW as instance of itself; manifest-discipline rule extracted

Resolved two configuration gaps surfaced in the prior dogfood (OQ-001 missing `project:` block, OQ-002 manifest-classification step not wired into Phase 2). Operator pressed on the framing — "doesn't the fact that ACW exists in 3 layers prove it is in fact an instance with a template layer and a meta layer?" — and that reframe locked D-ACW-006.

Shipped:

- **`project:` block** in `acw-state.yaml` (`name: ACW`, `code: ACW`, `domain: meta-template`). D-ACW-006. Reframes ACW as an instance of itself. Existing legacy ids `D-001..D-005` stay unprefixed; new entries use `D-ACW-NNN`. The skill suite now runs on ACW.
- **`rules/manifest-discipline.md`** (template_layer) — generic pattern documentation extracted from LAYERS.md. D-ACW-007. Covers when the rule applies, the three-layer model, manifest mechanics, why-default-to-instance, operator quick-reference, recurring-pattern naming, recursive-instances note.
- **`LAYERS.md`** trimmed to ACW-specific narrative (meta_layer): exact files in each ACW layer, why ACW landed here, rcN changelog. Points at the new generic rule.
- **`skills/capture-and-metabolize/SKILL.md`** — Configuration section documents all fields as optional with defaults; Phase 2 gained the conditional manifest-classification step.
- **Version bumped** to `0.2.0-rc3`.

First real dogfood of `capture-and-metabolize` ran cleanly on the sandbox: Phase 1 produced this session's capture file, Phase 2 wrote D-ACW-006/007 plus this build-log entry plus a tasks-status Session 3 block plus an evolution entry, Phase 3 metabolize swept the empty queries directory and reported nothing else stale, Phase 4 correctly skipped (`synapse_log_path: null`), Phase 5 prompted for research-prompt build and exited cleanly when no operator was present. Then operator instructed to fire the same skill in ACW directly — this entry is the result.

## 2026-04-30 — Three-layer manifest

Followed the v0.2.0-rc1 absorption pass with the manifest discipline that makes the template-vs-instance split explicit. Without a manifest, the classification lived as five hardcoded lists inside `tools/scaffold-instance.py`; every new propagatable file required a paired script edit, and a forgotten edit silently broke instances scaffolded thereafter.

Shipped:

- **Three blocks in `acw-state.yaml`** — `template_layer` (verbatim copies), `instance_layer` (templated initial form, per-file `path` + `template` declaration), `meta_layer` (about-ACW only, never propagated). Plus `empty_dirs` for `.gitkeep` initialization.
- **Refactored `tools/scaffold-instance.py`** — reads the manifest, stdlib-only mini-yaml parser. The hardcoded `VERBATIM_FILES` / `VERBATIM_RULES` / `TEMPLATED_FILES` constants are gone. Skips `__pycache__/` and `.pyc` files when copying directories.
- **`tools/templates/README.md.tmpl`** — instances now ship with an operator-facing README explaining what the workspace is and the first-session checklist.
- **`LAYERS.md`** (meta_layer) — explainer document with the three-bucket table, the why, the how, and the operator quick-reference. Names manifest-discipline as a recurring pattern (third application in ACW after `auto_load_at_session_start` and the canon governance state machine).
- **D-005 in the decision log** — records the architectural choice and the default-to-instance discipline.
- **Release gate added** — every file at root, `rules/`, `tools/`, `skills/` must be classified in one of the three layers.

Verification: scaffolded a fresh instance to `/tmp/acw-scaffold-v2`, confirmed it renders correctly, passes its own lint and test suite, and excludes meta_layer files (no `LINEAGE.md`, `AUTHOR.md`, `LAYERS.md`, etc. in the scaffolded output).

## 2026-04-30 — v0.2.0-rc1: gsg-copilot extensions absorbed

First absorption pass from the first ACW instance (`gsg-copilot`). Three weeks of single-operator lived experience surfaced nine candidate primitives (C-01 through C-09) and two staleness incidents (D-01 synapse-rule-sync, D-02 instance-bootstrap).

Shipped this session:

- **`tools/scaffold-instance.py`** — closes the bootstrap gap. Stdlib-only, ~200 lines, refuses to clobber, supports `--dry-run`. Templates live in `tools/templates/`.
- **`rules/task-tracking.md`** — codifies the three-section `tasks-status.md` model (Pending / Done / Parked) with dated session blocks under Done and pinned-marker convention at the top of Pending. Promoted from C-01.
- **`rules/incident-tracking.md`** — codifies the incident schema, severity ladder, and category vocabulary. Documents `incidents.jsonl` as default-on substrate that does not earn its build.
- **`tools/log-incident.py`** — gained `--category` flag with the seven-value enum from C-09.
- **`tasks-status.md` and `build-log.md`** — added at repo root and to `canonical_runtime_files` per C-01/C-02.
- **`acw-state.yaml::auto_load_at_session_start`** — new array per C-06. Names the canonical file list any agent host should pull at session start.
- **`AGENTS.md` directive 7** — declares the auto-load convention as the cross-vendor contract. Host-specific entry files implement via native syntax.
- **`skills/capture-and-metabolize/` and `skills/resume-session/`** — bookend skill pair ported from gsg-copilot. Adapted to read project code, synapse log path, voice references, and cross-repo writes from `acw-state.yaml`. Replaces `skills/capture-session/`.

Deferred:

- C-04 synthesis-cycle (only one cycle of evidence). Will revisit after second instance or third cycle.
- C-05 runbooks layer, C-07 vault-boundary as hard rule, C-08 backlog triple-tag — operator-preference-flavored. Documented as recommendations, not normative.

Version bumped: `0.1.0` → `0.2.0-rc1`. Tag earns promotion to `0.2.0` after release-gate verification.
