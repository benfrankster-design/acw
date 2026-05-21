---
date: 2026-04-30
participants: [ben, claude]
topic: rc3 acw as instance of itself manifest rule extracted
decisions_made: [D-ACW-006, D-ACW-007]
conceptual_shifts: yes
linked_files:
  - acw-state.yaml
  - skills/capture-and-metabolize/SKILL.md
  - LAYERS.md
  - rules/manifest-discipline.md
duration_minutes: ~30
---

# Session — RC3: ACW as Instance of Itself; Manifest-Discipline Rule Extracted

## 1. Topic & Goal

Resolve the configuration gaps surfaced by the prior session's Phase 1 dogfood (captured in this same `research/sessions/` directory in the prior cycle, then wiped on re-clone). Specifically:

- OQ-001 from prior dogfood: ACW lacks a `project:` block. Resolution candidates were (a) adapt skill to fallback gracefully, (b) add minimal block, (c) document hand-maintenance for ACW.
- OQ-002 from prior dogfood: Manifest classification step not wired into Phase 2.
- Operator-surfaced framing question: split `LAYERS.md` so the generic three-layer pattern ships in `rules/` (template_layer) and ACW-specific narrative stays in meta_layer.

Goal: ship rc3 with all three resolutions, then fire all five phases against a fresh ACW clone (sandbox) as a real dogfood test.

## 2. What was decided

- **D-ACW-006 — ACW carries a `project:` block (`code: ACW`, `domain: meta-template`).** Reframes ACW as an instance of itself that also serves as a template, rather than "the template, period." Existing legacy ids `D-001` through `D-005` stay unprefixed; new entries use `D-ACW-NNN`. This makes ACW valid input to `capture-and-metabolize` and the rest of the skill suite.
- **D-ACW-007 — Generic three-layer pattern extracted into `rules/manifest-discipline.md` (template_layer); ACW-specific narrative trimmed in `LAYERS.md` (meta_layer).** Every derived workspace gets the rule. ACW's own narrative — the rc1/rc2/rc3 history, the specific files in each layer, why ACW landed here — stays meta. A consultancy workspace (Frank Context, hypothetically) writes its own `LAYERS.md` for its own narrative and reads the same `rules/manifest-discipline.md` for the underlying pattern.

Operator directive locking these: *"okay. fantastic. fresh clone at acw-sandbox. first Add project: block to ACW's acw-state.yaml (treats ACW as an instance of itself). Update capture-and-metabolize SKILL.md with the two conditional steps (project.code fallback, manifest classification step). Then split LAYERS.md — ship a generic rules/manifest-discipline.md in template_layer; keep ACW-specific narrative in LAYERS.md (meta_layer)."* (turn 39)

## 3. What changed in the conception

**Shift — ACW is an instance, not a template.**

Until rc3, the implicit framing was "ACW is the template; instances are downstream." During this session the operator pressed on the framing: ACW has its own decisions, tasks-status, build-log, incidents, evolution, glossary, threat-model. That IS the shape of an instance. ACW happens to ALSO serve as a template. Two roles in one repo, and the lack of a `project:` block was a gap, not a deliberate "ACW is the template" choice.

The shift formalizes:
- ACW = instance + template, both at once.
- Most workspaces will be one or the other; some (ACW today, Frank Context tomorrow) will be both.
- The three-layer manifest is the machinery that lets a workspace play both roles cleanly.
- The `project:` block makes ACW valid skill input. The skill suite now runs on ACW like any other instance.

Linked entry to add to `research/evolution.md`: `2026-04-30 — ACW reframed as instance of itself; project block added; skill suite valid on ACW.`

## 4. What was built / changed

- `acw-state.yaml` — bumped to `0.2.0-rc3`. Added `project:` block (`name: "ACW"`, `code: "ACW"`, `domain: "meta-template"`). Added `rules/manifest-discipline.md` to `template_layer`.
- `skills/capture-and-metabolize/SKILL.md` — Configuration section now documents `project.code` as optional with a fallback to unprefixed ids; `synapse_log_path` and `cross_repo_writes` and `voice` as optional with sensible defaults. Phase 2 gained the conditional manifest-classification step (fires only when `template_layer`/`instance_layer`/`meta_layer` blocks are present and non-empty; defaults to `instance_layer` per asymmetry of mistakes).
- `rules/manifest-discipline.md` — new file (template_layer). Generic pattern documentation: when this rule applies, the three-layer model, where the manifest lives, how the system uses it, why default-to-instance, operator quick-reference, the recurring-pattern naming, and the recursive-instances note for derived templates.
- `LAYERS.md` — trimmed to ACW-specific narrative. Points at `rules/manifest-discipline.md` for the generic pattern. Lists the exact files in each ACW layer and the changelog of how ACW landed here.

## 5. Open questions left — structured

#### OQ-ACW-004 — When does `manifest-discipline.md` graduate from "documented pattern" to "shape with tooling"?

**Question:** The pattern (single source of truth, additive maintenance by skill, removal by ritual, lint as safety net) now appears three times in ACW: `auto_load_at_session_start`, the three-layer manifest, the canon governance state machine. The rule documents the shape so future authors don't reinvent it. But there's no shared tooling — each consumer (scaffolder, capture-and-metabolize Phase 2, capture-and-metabolize auto-load maintenance, vocabulary lint) implements the pattern from scratch. At what point does shared tooling earn its build (e.g., a generic "manifest validator" or "manifest-aware skill base class")?

**Candidates considered:**
- **Wait for fourth case.** The pattern is named; the rule is shipped. Don't generalize tooling until the fourth concrete case is in the door. Earn-by-incident discipline.
- **Build a generic helper now.** A small `tools/manifest.py` module that loads/writes/validates manifest blocks, used by all consumers. Cheap, but premature DRY.
- **Defer to incident.** Track in `DEFERRED.md` with activation trigger "fourth manifest case ships and reimplements the same load/validate/append logic."

**Why unresolved:** Earn-by-incident discipline says wait. The rule itself is the shipped artifact for now. Tooling is a separate ship.

**Who needs to weigh in:** Operator + the fourth manifest case when it arrives.

#### OQ-ACW-005 — When ACW eventually publishes to GitHub, what does the README at root point readers toward first?

**Question:** Two consumer modes are now explicit (scaffold-only and template-evolving). ACW's root `README.md` is meta_layer (about ACW), but it doubles as the GitHub landing page for both consumer types. A scaffold-only user wants `tools/scaffold-instance.py` instructions front and center; a template-evolving user wants the architecture story and the layered model. The question is how to layer the README so neither gets lost.

**Candidates considered:**
- **Scaffold-first README.** Lead with "if you just want to spin up a workspace, run X." Architecture story below the fold.
- **Architecture-first README.** Lead with the three-layer model and the manifest-discipline pattern. Scaffold instructions in a "Quick start" subsection.
- **Two READMEs.** `README.md` for landing-page (links to the other), `ARCHITECTURE.md` for deep dive.

**Why unresolved:** Premature — ACW has not published to GitHub. Resolves when public ship is on the calendar.

**Who needs to weigh in:** Operator, when public ship is queued.

## 6. Operator directives (verbatim)

> "yes I approve the suggestions. just 1 thing to explain further please: scaffold-instance.py reads from acw-state.yaml::template_layer + instance_layer; the existing hardcoded lists go away." (turn 31) — locked the manifest design.

> "1. correct me if im wrong but doesnt not running phase 2 on the acw-sandbox defeat the purpose of the test fire? 2. correct me if im wrong, but you say acw itself does not have project: block because it's 'the template', but doesnt the face that it exists in 3 layers prove it is in fact an instance with a template layer and a meta layer?" (turn 37) — pressed on the test-rigor dodge and the ACW-as-template framing; corrected the agent on both points.

> "okay. fantastic. fresh clone at acw-sandbox. first Add project: block to ACW's acw-state.yaml (treats ACW as an instance of itself). Update capture-and-metabolize SKILL.md with the two conditional steps (project.code fallback, manifest classification step). Then split LAYERS.md — ship a generic rules/manifest-discipline.md in template_layer; keep ACW-specific narrative in LAYERS.md (meta_layer). Then run the full five-phase fire test against a fresh ACW clone. hurry. I want to wrap this up and fire it here too and wrap up and get back to gsg-copilot." (turn 39) — authorized rc3 batch and the full five-phase fire test.

## 7. Cleaned transcript excerpt

*(Skipped — operator directives in §6 carry the load-bearing wording.)*
