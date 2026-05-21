---
class: archive
authority: derived
stability: stable
loaded_by_agent: no
---

# Build Log — ACW

Append-only, newest-first narrative of build progress per session.

## 2026-05-21 — Codemap canonical correction sweep + D-ACW-052/C-005 (Session 24)

Executed the 90-minute patch plan from Session 23's capture. All ten files corrected against the audit at `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md`.

**Decisions landed.** D-ACW-052 (codemap integration via ACW's auto-load, NOT `graphify claude install`; AST-only is default; Stage 2 Gemini opt-in via env_secrets; `implements_decision` bridge runs via Claude). C-005 (stop-work on writing Graphify content into any instance's CLAUDE.md). Both registered in `.acw/decisions/INDEX.md`.

**`rules/codemap.md` rewrite.** Substantial corrections: output structure shows Graphify native (`graphify-out/`) vs ACW relocated (`.acw/codemap/`) forms; node types match probe (`document`, `code`, `rationale`); edge types match probe (`calls`, `contains`, `rationale_for`, `inherits` confirmed AST-stage); confidence tagging documents the numeric `confidence_score` companion field; Stage 2 LLM is Gemini (not Claude, not local); `implements_decision` is ACW-specific bridge running via Claude (not Graphify-native); build triggers no longer reference pre-commit hooks (Graphify ships post-commit, ACW uses on-demand); skill contract gains pass-through verbs (query, path, explain).

**`rules/confidence-tagging.md` patch.** Added `confidence_score: 0.0–1.0` numeric companion field documentation. Convention: EXTRACTED → 1.0, INFERRED → explicit float required, AMBIGUOUS → not assigned.

**`rules/instance-current-manifest.md` patch.** New entry: `env_secrets` block (earned v0.10.1). Schema with `name`, `required_by`, `when`, `notes`. Documents `.env` (gitignored) or shell-env supply pattern. Authority: D-ACW-052.

**`skills/codemap/SKILL.md` rewrite.** Command table expanded with pass-through verbs (query, path, explain) plus the underlying Graphify call per row. Pre-flight gates expanded: CLAUDE.md integrity check (refuses if Graphify-managed block detected per C-005), env_secrets check (for `--semantic` runs). Output structure corrected to combined `graph.json` (no nodes/edges/communities split). New "What this skill MUST NOT do" section enforces C-005, no auto-rebuild hooks, no `graph.json` mutation, AST-only default.

**`skills/codemap/gotchas.md` rewrite.** Eleven gotchas covering: two-y package name, no `--output-dir` flag, `cache/` not `.cache/`, Gemini not Claude for Stage 2, `implements_decision` is ACW-specific, `graphify claude install` forbidden per C-005, profile gating, AMBIGUOUS triage, branch-switch cache staleness, single combined `graph.json`, and wrapper-authoring readiness.

**`skills/codemap/references/implementation-plan.md` rewrite.** Replaced "investigation deferred" framing. Now contains: probe findings (CLI verbs, output structure, edge schema), wrapper job (output relocation, `implements_decision` bridge via Claude, pass-through verbs), reference files to author, dogfood target (cs-atlas post-v0.10.0), estimated effort (1-2 hours).

**Migration manifests.** Both `migrations/0.9.9-to-0.10.0.yaml` and `migrations/pre-acw-to-0.10.0.yaml` had their `.acw/codemap/.cache` create_dir step replaced with a NOTE — Graphify creates `cache/` (no dot) on first run, so the migration doesn't need to pre-create it.

**`tools/templates/acw-state.yaml.tmpl` patch.** Added commented-out `env_secrets:` scaffold block with `GEMINI_API_KEY` example. Default value `[]`. Instances opting into Graphify Stage 2 uncomment and populate.

**What did NOT change in scaffolder.** `tools/scaffold-instance.py` doesn't directly create `.acw/codemap/cache/` — only references `codemap` as a module name (lines 201, 204) and prints a hint to run `/codemap rebuild` (line 358). All correct. No patch needed.

**Patch sweep complete.** Wrapper reference authoring landed in the same session — see below.

## 2026-05-21 — 0.9.7-to-0.9.8 migration manifest authored (Session 24, continued)

Closed the last canonical-side blocker for downstream upgrade dogfooding. With this manifest in place, every chain in the five-instance audit walks end-to-end against current canonical.

**`migrations/0.9.7-to-0.9.8.yaml`.** Authority D-ACW-048. Eight steps:

1. Create `decisions/entries/`, `decisions/open-questions/`, `decisions/constraints/` skeleton.
2. Run `tools/migrate_to_wiki.py` on live `decisions/decision-log.md` (gated by `has_single_file_decisions` operator prompt).
3. Glob and re-split every `decisions/decision-log-YYYY-Q*.md` rolling-window archive via a new hook (gated by `has_decision_archives` prompt).
4. Migrate `glossary.md` to wiki shape via a new hook (gated by `has_single_file_glossary` prompt); create `glossary/entries/` skeleton first.
5. Verify-before-delete legacy sources via a new hook.
6. Reshape `acw-state.yaml::decision_tracking` and `::glossary` blocks to wiki shape; flip `paths` keys; update `auto_load_at_session_start` entries from single-file to INDEX paths. Block-level replacement via dedicated hook (exceeds `update_acw_state` subop set).
7. Trim `meta_layer` of the now-deleted quarterly-archive entries.
8. Bump version to 0.9.8.

Five new hooks are declared in the manifest's trailing comment block (split-decision-archives, migrate-glossary-to-wiki, delete-legacy-sources, reshape-acw-state, trim-meta-layer). Per the v0.9.3 convention, they author on first execution against a real instance — the manifest is the spec, the hooks are the implementation.

**Path convention.** Pre-v0.10.0 substrate lives at workspace root (`decisions/`, `glossary/`), NOT under `.acw/`. This manifest uses root paths intentionally; the `.acw/` prefix flip happens later, in `0.9.9-to-0.10.0.yaml`.

**`migrations/README.md` updated.** Index table gains a row for the new manifest. The "Intermediate version gaps" section now correctly omits 0.9.7→0.9.8 from the gap list.

**Effect on downstream chains.**
- `_command` (v0.9.7) — chain is now complete end-to-end: `0.9.7-to-0.9.8.yaml` → (0.9.8-to-0.9.9 not needed, no file-shape change) → `0.9.9-to-0.10.0.yaml`.
- `cs-copilot`, `gsg-copilot` — if any are at single-file decision-log shape, the v0.9.8 manifest fires automatically as the audit detects legacy shape.
- All five instances from the Session 23 audit are now executor-unblocked. Hooks land on first run.

**Next.** Operator dogfoods from frank-context per their plan.

## 2026-05-21 — `/acw-instance upgrade` executor closure (Session 24, continued)

Closed the three executor gaps that blocked manifest-driven upgrades across the downstream instances.

**`upgrade.md` — new "Step kind execution detail" section.** Concrete behavior for the five step kinds that had open questions:

- `remove_gitignore_rule` — whitespace-tolerant exact-line removal; idempotent (no-op when rule absent or file missing); writes back through `git add .gitignore` on tracked workspaces; emits `[?]` row when the rule appears as part of a longer line (refuses partial-line matching).
- `only_if` conditional — predicate forms: `equals`, `in`, `not_equals`, `present`, `all` (conjunction), `any` (disjunction). Field resolution order: operator-prompt answers → existing `acw-state.yaml` keys → declared defaults. Audit-phase evaluation only; not re-evaluated at execution time. Unknown fields conservatively treat predicate as false.
- `git_mv` with `optional: true` — per-move flag (not per-step). Skip-if-source-missing tolerance for pre-acw bootstrap where workspaces have only a subset of substrate paths. Audit emits `[would-skip-if-absent]` plan rows for visibility. Non-optional moves retain hard-fail behavior on missing source.
- `update_acw_state` subops — full coverage of `path_prefix_substrate` (idempotent), `rename_keys` (idempotent), `add_fields` (only when key absent or null; operator prompts override), `set_fields` (unconditional, `<DATE>` token resolution). Uses `tools/manifest.py`, preserves comments and key ordering.
- `update_file` — refuse only on missing file; missing patterns produce warnings, not failures (operator-customized prose is expected); idempotent across re-runs.

**`upgrade.md` — "Executor verification status" table refreshed.** All step kinds required by `0.9.9-to-0.10.0.yaml` and `pre-acw-to-0.10.0.yaml` are marked ready. The three previously-blocking kinds (`remove_gitignore_rule`, `only_if`, `optional: true` on git_mv) carry "ready (Session 24)" markers.

**`audit.md` — new "Migration manifest pass (v0.10.0+)" section.** Documents how the audit reads manifests, evaluates prerequisites, collects operator-prompt entries as `[?]` rows, resolves `only_if` predicates against operator-prompt answers, generates plan rows per step, and prints a per-manifest summary block. Covers chain mode for multi-hop upgrades (e.g., 0.9.7 → 0.10.0 walks three manifests in order), conservative prerequisite evaluation against the state previous manifests would have produced, and fallback to version-specific upgrade.md sections when intermediate manifests are missing.

**Effect on downstream instances.** Per the five-instance audit:

- **frank-context** is now unblocked. `migrations/0.9.9-to-0.10.0.yaml` can run end-to-end against it.
- **cs-atlas** is now unblocked. `migrations/pre-acw-to-0.10.0.yaml` can run with `optional: true` skips for the substrate paths it doesn't have yet.
- **cs-copilot** is now unblocked on the pre-acw bootstrap path. Same mechanism as cs-atlas.
- **cs-ops-spec** was already at v0.10.0 shape; needs profile/modules verification (no executor work).
- **_command** still needs `0.9.7-to-0.9.8.yaml` authored (a separate task — the executor is now ready when it lands).

`tools/manifest.py` is referenced as the write surface for `acw-state.yaml` mutations. The script already exists per earlier sessions; concrete coverage of the four subops (`path_prefix_substrate`, `rename_keys`, `add_fields`, `set_fields`) needs verification on first manifest run against a live downstream instance — this is the dry-run recommendation in the verification-status section.

## 2026-05-21 — Codemap wrapper reference authoring (Session 24, continued)

Authored all six `skills/codemap/references/` files immediately after the patch sweep. The reference files are the executable specification an agent or operator follows when invoking each verb.

**`rebuild.md`.** Three modes (default / `--ast-only` / `--semantic`). Pre-flight runs the SKILL.md gates in order: profile, module, Graphify availability (binary `graphify`, package `graphifyy`), CLAUDE.md integrity per C-005, env_secrets gate (only for Stage 2 paths), codemap dir. Stage 1 invokes `graphify update <project-root>` with Pattern A (`cwd=.acw/codemap/`) as the recommended relocation pattern. Stage 2 re-runs with Gemini env vars set. ACW bridge walks `.acw/decisions/entries/`, emits `implements_decision` edges to `acw-edges.json` sidecar (literal-id-match path always; LLM judgment path gated by `ANTHROPIC_API_KEY` env_secret), appends a "Code-to-decision bridges" section to `GRAPH_REPORT.md`. Failure modes documented (Graphify non-zero, Stage 2 quota, bridge LLM, acw-edges write).

**`status.md`.** Read-only. Reads `manifest.json`, `graph.json`, `acw-edges.json`, source mtimes, decision-entry mtimes. Reports last AST/Stage 2/bridge timestamps, node and edge counts by file_type/relation/confidence, staleness signals, cache size. Exit codes 0/2/3.

**`audit.md`.** Five walks: AMBIGUOUS edges, low-confidence INFERRED (threshold 0.5 default), stale bridge edges (deleted decision targets, deleted source symbols), orphan nodes, optional `graphify benchmark`. Reports a one-line clean/needs-attention summary. Exit codes 0/1/2.

**`query.md`, `path.md`, `explain.md`.** Pass-through verbs. `query` and `path` stream Graphify's stdout unchanged. `explain` is the one verb that joins Graphify's native output with ACW's `acw-edges.json` bridge view — appends a "ACW substrate links:" section with `implements_decision` edges for the queried node.

**Implementation status updated.** SKILL.md's status note now reflects "all six references authored; Python wrapper code is the remaining gap." References ARE the executable specification — an agent following them step by step can perform a manual rebuild today, which is the dogfood path against cs-atlas.

**Tasks-status updated.** Wrapper-authoring task is closed (collapsed into the dogfood task). NEXT is cs-atlas dogfood: finish its v0.10.0 upgrade, install graphifyy, follow `rebuild.md` manually, verify GRAPH_REPORT.md loads via SessionStart hook, run literal-match-only bridge over `.acw/decisions/entries/`, refine references if friction surfaces.

## 2026-05-21 — Graphify probe + canonical audit + integration decision (Session 23)

Same calendar day as Sessions 21 and 22. Continued the codemap track after the operator caught me citing Graphify's architecture from secondary-source articles without ever installing or running it.

**The catch.** I'd described Graphify's CLI surface, output format, and integration patterns from blog posts (betterstack, pyshine, medium) — confidently, as if I'd used it. Operator pushed back with one line: "you didn't install it? pip install graphifyy". Right.

**The install.** Package on PyPI is `graphifyy` (two y's); CLI binary is `graphify`. Version 0.8.14. Installed cleanly with full Tree-sitter language pack. `graphify update <path>` ran against three files in skills/codemap/ — 19 nodes, 16 edges, 4 communities, zero LLM cost. AST-only Stage 1 confirmed free.

**The probe.** Ran against Python code from tools/ to see edge types beyond `contains`. Confirmed `calls`, `inherits`, `rationale_for` as native AST-stage edges. Confidence tags as documented (EXTRACTED on AST-only). Also discovered the `confidence_score` numeric field (0.0-1.0) I hadn't documented.

**The audit.** Wrote `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md`. Three breaking errors, four moderate, three minor across `rules/codemap.md`, `skills/codemap/*`, both migration manifests, `tools/scaffold-instance.py`, and the template. Most consequential: output location is `graphify-out/` at cwd (no `--output-dir` flag); LLM is Gemini not Claude; the ACW-decision bridge is NOT native to Graphify.

**The integration decision.** Graphify ships `graphify claude install` which writes a section into CLAUDE.md plus a PreToolUse hook. This conflicts with ACW's "CLAUDE.md is a thin pointer" convention (D-ACW-047). Operator chose ACW's auto-load: `.acw/codemap/GRAPH_REPORT.md` lands in `acw-state.yaml::auto_load_at_session_start` per the coding-project / library profile defaults; SessionStart hook loads it like every other substrate module; CLAUDE.md stays thin. Graphify is now treated as an internal AST engine we delegate to, not a co-equal integration partner.

**The Stage 2 question.** Graphify's semantic extraction uses Gemini API. ACW's recommended pattern: AST-only as the default (free, deterministic, sufficient for most navigation); ACW-specific `implements_decision` bridge via Claude becomes the semantic layer (linkage between code and decision entries); Graphify's native Stage 2 stays opt-in via `acw-state.yaml::env_secrets` declaration of `GEMINI_API_KEY`.

**Decisions ready to codify (Session 24):** D-ACW-052 (ACW's auto-load wins over graphify claude install; AST-only default; env_secrets pattern). C-005 (no Graphify content in any instance's CLAUDE.md).

**The 90-minute patch plan landed in Session 23 capture.** Ten files to patch in order to fix the audit findings. Session capture at `.acw/sessions/2026-05-21--graphify-probe-and-codemap-audit.md` carries the full plan forward.

**Honest framing.** Earlier ACW codemap work (rules/codemap.md, skills/codemap/SKILL.md) was authored confidently in a domain I hadn't touched. The architecture survives the audit; the specifics need correction. Single focused commit fixes it.

## 2026-05-21 — Phase 2: migration manifests, substrate-map, scaffolder, rules/ closure (Session 22)

Same calendar day as Session 21 (the v0.10.0 ship); continued work focused on landing the foundation pieces v0.10.0 deferred.

**Architectural correction first.** Mid-session the operator pushed back on the v0.10.1 framing I'd queued. I had Phase 2 work as "encode the v0.10.0 migration steps into the `/acw-instance` skill itself." Operator pointed out this inverts the source-of-truth: skill carries version-specific knowledge, must be redistributed every version bump. Right shape: skill is a thin portable executor; canonical IS the SoT. Migration knowledge lives in canonical as declarative data files. New version means a new manifest file in `migrations/`, never a skill change.

Reframed and re-executed.

**`rules/migration-manifest.md`.** Schema for the new `migrations/` directory. Documents the YAML shape (`from_version`, `to_version`, `breaking`, `prerequisites`, `operator_prompts`, `steps[]`) and the step-kind enum (`create_dir`, `git_mv`, `update_acw_state` with `path_prefix_substrate` / `rename_keys` / `add_fields` / `set_fields`, `update_file`, `rebuild_index`, `add_file`, `remove_gitignore_rule`, `run_hook`). Reserved future step kinds for forward-compat (`delete_file`, `delete_dir`, `validate_invariant`, `archive_to`).

**`migrations/0.9.9-to-0.10.0.yaml`.** The v0.10.0 migration expressed as declarative data, not skill code. Seven steps: retire the `.acw/` gitignore rule, create `.acw/`, batch `git mv` substrate (with the `_buffer → raw` rename folded in), patch `acw-state.yaml` (substrate path prefix + key rename + new profile/modules fields), patch entry-point doc text references, rebuild INDEX files, conditional `.acw/codemap/` init for coding-project/library profiles. Operator prompt for `profile:` selection at execution time.

**`migrations/README.md`.** Operator-facing index of available migrations.

**`rules/` migration question resolved.** Closed OQ-COPS-019 (from cs-ops-spec, deferred to canonical) as "stays at workspace root." Rationale in D-ACW-051: rules are closer in shape to project configuration than to operator working memory; load-bearing convention; different mental model; discoverability for new agents. C-004 codifies as constraint.

**`/substrate-map` skill.** New thin skill that renders the implicit cross-reference graph across ACW substrate as an on-demand markdown view. Walks frontmatter cross-refs and prose ID mentions, emits `.acw/substrate-map.md` with confidence tagging applied per `rules/confidence-tagging.md`. Read-only on source substrate. Operator-invoked. Sibling to `/codemap` (which covers code structure); both compose, neither replaces the other. Skill at `skills/substrate-map/SKILL.md` + `gotchas.md`.

**Scaffolder updated for v0.10.0.** `tools/scaffold-instance.py` gained `--profile` and `--modules` arguments. Profile choices: org-brain, spec-project, coding-project, library, custom. Default modules per profile codified at the top of the script (mirrors `rules/instance-types.md`). `--profile=custom` requires `--modules`. Template tokens `{{PROFILE}}` and `{{MODULES_YAML}}` added. `tools/templates/acw-state.yaml.tmpl` updated to v0.10.0 shape — paths block `.acw/`-prefixed, `profile:` and `modules:` fields added, `raw_dir:` replaces `buffer_dir:`, `decision_tracking` and `glossary` sub-blocks point at `.acw/` paths.

**Deferred to follow-up sessions.** `/codemap` skill (needs Graphify CLI investigation — the wrapper's only valuable if it correctly handles the actual CLI surface, and I haven't probed it yet). `/acw-instance upgrade` executor verification (needs reading the current skill prose to identify which step kinds from the manifest schema are already supported vs. need to be added). Skill audit pass for hardcoded paths (mechanical sweep, real time, dedicated session).

**Net effect.** v0.10.0 foundation is complete. Multi-instance upgrades (the five downstream instances) are unblocked once the executor verification lands — and that's a small follow-up because most of the step kinds are already what `/acw-instance upgrade` does.

## 2026-05-21 — v0.10.0 .acw/ dotfolder, instance types, codemap, confidence tagging (Session 21)

Four cross-cutting changes landed together as v0.10.0. The catalyst was substrate hygiene work in two downstream instances on the same day; the framing crystallized into a single coherent release.

**The catalyst.** cs-ops-spec hit a moment where the operator wanted the spec's deliverable folder (`research/spec/`) and the ACW operator-metadata substrate (`decisions/`, `sessions/`, `glossary/`, `_buffer/`, etc.) to stop competing for attention at the project root. Independently, cs-atlas was being prepped for first push to `bitbucket.org/GiveSendGoG1/gsg-cs-atlas` and the operator pushed back on shipping ACW substrate to a code repo where consumers cloning the library would see a journal of how it was built. Both instances independently arrived at the same answer: substrate goes under a `.acw/` dotfolder; the public-facing repo shows only the artifact and entry-point docs.

**The dotfolder convention.** `.acw/` follows the same shape as `.git/`, `.github/`, `.vscode/`, `.claude/` — a hidden-by-default folder for "tooling state, not artifact." Editors open dotfolder files transparently; the hidden-by-default behavior is for file browsers. The convention removes a category of mental friction for anyone cloning an instance.

**The `_buffer → raw` rename.** Coupled with the dotfolder move. "Buffer" suggested transient holding; "raw" matches the actual semantic — unmetabolized inputs awaiting routing through the enrichment principle (raw → metabolize → enriched).

**Instance types.** Same session surfaced the broader framing: ACW is becoming the substrate convention for any directory-based work where humans and AI both read and write. Org brains, spec projects, coding projects, libraries. Each has different substrate needs. Codified `profile: org-brain | spec-project | coding-project | library | custom` plus optional `modules:` override. Profile defaults documented in new `rules/instance-types.md`.

**Codemap + confidence tagging.** Operator asked about Graphify, the codebase knowledge graph approach. Two principles fit cleanly: codemap substrate module for coding instances (Graphify wrapper, two-stage AST + LLM extraction, stored under `.acw/codemap/`); confidence-tagged edges (EXTRACTED / INFERRED / AMBIGUOUS) generalized across all substrate. Codified in new `rules/codemap.md` and `rules/confidence-tagging.md`.

**Authoring sequence.** Wrote four new rule files. Updated three existing rule files. Migrated ACW's own substrate to `.acw/` via `git mv` as the reference implementation. Bumped 0.9.9 → 0.10.0. D-ACW-050 captures the decision; C-003 codifies the constraint.

**Deferred to v0.10.1.** `/acw-instance upgrade` skill mechanics to execute the migration on downstream instances. `/codemap` skill (Graphify wrapper). `/substrate-map` skill (rendered cross-ref view). Skill audit pass to verify all existing skills read paths from config rather than hardcoding.

**Originating evidence.** cs-ops-spec D-COPS-035 / C-COPS-001 / OQ-COPS-019 and cs-atlas D-CATL-001, both 2026-05-21. Two absorption candidates retained as provenance under `.acw/raw/`.

## 2026-05-13 — v0.9.9 drift short-circuit + buffer sweep + synced_to: hardening (Session 20)

Three coupled fixes shipped together as v0.9.9 (D-ACW-049), all triggered by a single `_buffer/` note from cops.

**Cops's note (turn 0).** `/acw-session start` Step 5 was reading the full body of `rules/instance-current-manifest.md` (~390 lines, ~10–12k tokens) on every session start. With `last_reconciled_version == ACW current version` the walk is structurally guaranteed to surface zero gaps. The full read was wasted context for the 99% case.

**Drift short-circuit.** Step 5 now reads only the manifest's frontmatter (cheap, ~10 lines). When `synced_to == acw-state.yaml::last_reconciled_version`, skip the walk and emit "no drift" silently. Falls through to the full walk when `synced_to` absent or mismatches (broken upgrade, manual edit, never-upgraded instance).

**Buffer sweep.** Operator pulled the buffer-lifecycle gap into scope mid-session: "when buffer items are read and moved to decisions the buffer note should move to `_read`." Capture file gains `## Buffer notes acted on` section; `/acw-session end` Phase 2 append-only subset reads it and moves each listed file to `_buffer/_read/`. Closes the cross-instance handoff lifecycle.

**`synced_to:` hardening.** First short-circuit attempt used file mtime as the "has the cache been touched?" signal. Operator asked for the bulletproof version. Added `synced_to: "<version>"` string field to the manifest's frontmatter, written by `/acw-instance upgrade` whenever it overwrites the file. Survives `git pull`, sync clients, workspace copies. start.md updated to use exact equality.

**Self-demonstrating.** When asked "is there anything you loaded up to this point that was redundant?", the agent identified the exact failure cops had flagged — the manifest read — by looking at its own context-loading from this very session. The cops note moved to `_buffer/_read/` manually since the new sweep logic landed in the same session.

Net: `/acw-session start` ~10k tokens cheaper per invocation across all reconciled instances, `_buffer/` lifecycle closed, version-stamp primitive added that other surfaces can adopt later.

## 2026-05-13 — v0.9.8 wiki mode canonical-only + context/contacts/ opt-in (Session 19)

Doctrine simplification + new optional pattern.

**v0.9.8 ship** (D-ACW-048): wiki mode is now the only sanctioned mode for `decisions/` and `glossary/`. Single-file mode is retired — not just deprecated, removed from canon. The v0.9.3 dual-mode opt-in framing (D-ACW-043) was always transitional; treating it as permanent forced rule, scaffolder, audit, and upgrade to carry parallel code paths. Scaffolder template (`tools/templates/acw-state.yaml.tmpl`) now ships wiki-mode `decision_tracking` block + new `glossary` block + wiki `paths` + INDEX-based `auto_load_at_session_start`. New templates: `decisions-INDEX.md.tmpl`, `glossary-INDEX.md.tmpl`. Main `acw-state.yaml` `instance_layer` rows for `glossary.md` / `decisions/decision-log.md` replaced with `glossary/INDEX.md` / `decisions/INDEX.md`; `empty_dirs` extended with `decisions/entries`, `decisions/open-questions`, `decisions/constraints`, `glossary/entries`. Dual-purpose NOTE comment removed.

**`rules/decision-tracking.md`** — "The format" section rewritten: wiki shape only, atomic per-entry files, canonical frontmatter from `acw-state.yaml::decision_tracking.{entry_frontmatter_required, status_values, kind_values}`. Rolling-window discipline section trimmed from ~14 bullets to one paragraph (wiki uses INDEX sort order, no archive ceremony).

**`skills/acw-instance/`** — SKILL.md Step 2 substance scan + Step 3 canonical fetch stripped of mode branching. `references/audit.md` "Mode-dependent substrates" branching replaced with mandatory legacy → wiki migration plan row (not `[?]`, not optional). `references/upgrade.md` single-file → wiki section reframed as mandatory v0.9.8 doctrine.

**`context/contacts/` opt-in** — new canonical optional pattern. Wiki-shaped (`context/contacts/INDEX.md` + `entries/<slug>.md`). NOT propagated by the scaffolder; surfaced by audit as an opt-in plan row when absent; upgrade scaffolds it on operator acceptance. First instance of "earn-by-discipline scaffolder primitive" pattern. Template at `tools/templates/context-contacts-INDEX.md.tmpl`.

Net: dual-mode complexity retired, one new canonical optional pattern, downstream instances (cs-copilot, gsg-copilot, _Command) queued for mandatory wiki migration on next `/acw-instance upgrade`.

## 2026-05-13 — v0.9.6 wiki migration + /acw-session model-pin fix (Session 17)

Two coupled ships and one diagnostic landing.

**v0.9.6 ship** (D-ACW-045): wiki migration doctrine flipped — ALL decisions live in `decisions/entries/` in wiki mode, including pre-migration history. Retired the "archives stay archived" expedient from D-ACW-043. ACW's own Q2 archive (34 entries: D-001..D-005, D-ACW-006..D-ACW-034) re-split into per-entry wiki files; `decisions/decision-log-2026-Q2.md` deleted; `acw-state.yaml::meta_layer` reference removed; INDEX regenerated (now 49 entries date-descending). `tools/migrate_to_wiki.py` gained `--archive=<path>` flag for flat-`###` archive parsing. `/acw-instance upgrade` reference extended with v0.9.6 single-file → wiki migration section (8 steps under one approval gate). `/acw-session` redundancy refactor: 7 sites collapsed to rule + state-file pointers, mirroring D-ACW-044's `/acw-instance` work.

**Model-pin fix** (D-ACW-046): post-ship, `/acw-session` failed "Prompt is too long" on the same Opus 1M session at ~300k context. Diagnosis: SKILL.md frontmatter pinned `model: claude-sonnet-4-6`, which capped inherited context to Sonnet's 200k window. `/compact` confirmed the diagnosis by restoring functionality. Root fix: drop `model:` from orchestrator SKILL.md — inherit parent session model. Sonnet escalation for Phase 3/5 judgment subagent retained (those run with bounded context). New rule (deferred until second incident): orchestrator skills that run inline MUST NOT pin `model:`.

Net: 49 decision entries (was 48), one new earned-by-incident structural fix, `/acw-session` usable on long Opus sessions again.

## 2026-05-05 — v0.9.1: bi-weekly rolling-window for decision-log + global synapse trim (Session 15)

Operator opened with a screenshot of context-usage: 128k / 1M with Memory files at 79.2k. The bloat traced to two structural sources: (a) `~/synapse/Rules/instance-current-manifest.md` (35.8k) plus five other ACW-canonical duplicates auto-loading globally via the `~/.claude/rules` → `~/synapse/Rules/` junction, and (b) ACW's own `decisions/decision-log.md` at 24k, past the v0.9.0 ~15k canonical-recommendation threshold without a documented archive mechanism.

The conversation arc:

1. **Context audit.** Memory-files breakdown surfaced the synapse junction as the structural attack surface — every workspace, every session was paying for ACW-canonical content that only belongs in ACW workspaces.
2. **Trim move proposed and approved.** Six ACW-canonical duplicates moved from `~/synapse/Rules/` → `~/synapse/Reference/acw-canonical/` (sibling, not under junction). Five citation references in `cs-copilot/` flagged as fix-on-touch. ~85k off global load every workspace, every session.
3. **Doctrine gap surfaced.** v0.9.0's `rules/auto-load-discipline.md` named the ~15k threshold for `decisions/decision-log.md` and pointed at `rules/decision-tracking.md` for the mechanism — but the rolling-window mechanism analogous to v0.9.0's tasks-status pattern was missing. Operator overrode the v0.9.0 "nothing before 1.0.0" directive: "lets do this bi-weekly actually (every two weeks) rolling window with the decision logs. and we were supposed to split tasks status. lets just do it now."
4. **Bi-weekly as unifying cadence.** Decision-log and tasks-status both adopt bi-weekly rolling-window discipline under one rule shape. v0.9.0's "Sessions ≥ N-2" placeholder for tasks-status aligns to bi-weekly; cadence is now consistent across both surfaces.
5. **ACW substrate split applied.** D-ACW-034 down through D-004 (30 entries dated 2026-04-30 to 2026-05-02) archived to `decisions/decision-log-2026-Q2.md`. Live decision-log retains D-ACW-035 onward (8 entries inline including D-ACW-042 recording this ship).
6. **Doctrine-completion patch framing.** v0.9.1 ships as patch — closes a v0.9.0 specification gap, does not extend scope. Distinct from a v0.10.0 that would add new content. Establishes a pattern: future v0.9.x patches may follow the same shape if other v0.9.0 gaps surface during soak.

Files touched: `decisions/decision-log.md`, `decisions/decision-log-2026-Q2.md` (new), `rules/decision-tracking.md`, `rules/task-tracking.md`, `rules/auto-load-discipline.md`, `rules/instance-current-manifest.md`, `acw-state.yaml`, `tools/templates/acw-state.yaml.tmpl`, `tasks-status.md`, `~/synapse/Rules/` → `~/synapse/Reference/acw-canonical/` (six files moved), `~/.claude/CLAUDE.md`. Incident `f7994d0d-b85a-41c1-b944-b4f55050c771` logged for the memory-bloat that earned the synapse trim. 54/54 unit tests pass; vocab lint clean. Bumped version 0.9.0 → 0.9.1; bumped `last_reconciled_version` to 0.9.1; updated template baseline to 0.9.1.

Net: ~30k off ACW workspace memory load + ~85k off every workspace globally + doctrine internally consistent across decision-log and tasks-status.

## 2026-05-04 — v0.9.0: auto-load discipline + tasks-status rolling-window archive (Session 14)

Operator opened the session with a screenshot of the context-usage panel: 113.2k tokens / 1M, with `Memory files` consuming 83.1k. After v0.8.0's per-invocation cost cut shipped earlier the same day (Haiku default + quick mode), this session attacks the structural per-session-load cost. The lever was the auto-load list — 8 entries pulling ~50k of substrate into context every chat.

The conversation arc:

1. **Context audit.** Operator surfaced the bloat. I proposed three trim moves (demote, archive Done, split decision-log) with risk callouts. Operator focused on the auto-load list as the cheapest highest-impact lever.
2. **Earn-its-ship reframe.** Operator pointed at the `## Project substrate (auto-loaded every session)` heading in `CLAUDE.md` and asked it to "earn its ship." The right move was applying ACW's existing earn-by-incident discipline (which governs the deferred library and the recommended-blocks registry) to auto-load entries themselves.
3. **Schema design.** Two options surfaced: (a) inline structured entries in `acw-state.yaml`, or (b) parallel rule-file registry. Inline structured won — instances can declare per-entry claims without editing canonical doctrine; the rule file owns the gate but not the data.
4. **Audit-as-active-discipline.** Operator pushed: "instances doing acw instance audit should be audited for demotions." This sharpened the audit verb's role from passive drift detection (additions) to active migration planning (additions AND removals AND form migration).
5. **Ship directive.** "Get it all done. there should be nothing for 1.0.0." — committing v0.9.0 as the final pre-promotion substantive ship; v1.0.0 becomes a clean soak/promotion.

**Core ship:**

- `rules/auto-load-discipline.md` — new template_layer rule. Earn-by-incident applied to auto-load. Canonical recommendations name the four files ACW recommends (decision-log, instance-hard-rules, tasks-status, glossary). Declared demotion candidates name what fails the gate and why (manifest-discipline, instance-current-manifest, multi-instance-topology, incidents.jsonl).
- `tools/manifest.py` — extended with `STRUCTURED_LISTS = {"auto_load_at_session_start"}`. Parser handles both bare and dict-shaped entries (backward compat). New `load_structured()` returns full dicts; `load()` continues returning paths only (existing consumers unchanged). `validate()` enforces no-duplicate-paths and required `path` field.
- `tests/test_manifest.py` — 8 new tests covering structured-list parse, mixed-form, validate, and the rejection contract for non-structured lists. All 54 tests pass.

**Substrate moves:**

- `acw-state.yaml::auto_load_at_session_start` migrated to structured form; 4 demotions applied (4 entries kept, each with structured claim).
- `tools/templates/acw-state.yaml.tmpl` migrated to structured form; new instances scaffold with the lean 4-entry default. Baseline `last_reconciled_version` bumped to `0.9.0`.
- `CLAUDE.md` `@`-imports synced to the lean 4-entry list; "Other substrate is read on demand" section names the demoted files and their consumer-skills.
- `acw-state.yaml::template_layer` extended with `rules/auto-load-discipline.md`; `meta_layer` extended with `tasks-status-2026-Q2.md`.

**Skill extensions:**

- `skills/acw-instance/references/audit.md` gained "Auto-load discipline" section: walks `auto_load_at_session_start`, classifies each entry against canonical recommendations and demotion candidates, produces consolidated `reshape` plan row with per-entry verdicts (KEEP / KEEP-migrate-to-structured / KEEP-instance-specific / DEMOTE / REVIEW).
- `skills/acw-instance/references/upgrade.md` gained "v0.9.0 migration: auto-load discipline" section: applies the audit's verdicts under the existing single approval gate; converts bare entries to structured form using canonical claims; removes demotion entries; resolves REVIEW interactively; updates host entry files to mirror.

**Tasks-status rolling-window:**

- `tasks-status-2026-Q2.md` created (meta_layer): Sessions 1–11 archived. Pointer line in `tasks-status.md`. Sessions 12–14 stay inline.
- `rules/task-tracking.md` extended with rolling-window discipline section declaring the inline ≤ 2–3 sessions convention and quarterly archive shape.
- New earned-in-0.9.0 entry in `rules/instance-current-manifest.md` documents the archive convention (paired with the `auto_load_at_session_start` v0.9.0 restructure entry).

**Discipline writes:**

- D-ACW-038 records the bundle (8-item change list, 4 open follow-ups, 3 risk callouts).
- Auto-load-bloat incident `e58b923d-5bfe-4c67-92b1-7ac981aade00` logged as activation evidence (severity med, category process-gap).
- Two new earned-in-0.9.0 entries in `rules/instance-current-manifest.md`: `rules/auto-load-discipline.md` (the rule itself) and `tasks-status-YYYY-Q.md archive` (the rolling-window discipline). Existing `auto_load_at_session_start` entry rewritten to declare the structured form and reference the discipline rule.

**Version bump:**

- `acw-state.yaml::version` 0.8.0 → 0.9.0. `last_reconciled_version` bumped to 0.9.0. Template baseline `last_reconciled_version` bumped to 0.9.0.

**Auto-load context impact:** ~30k off session-load when fully applied (5.2k manifest-discipline + 11.5k instance-current-manifest + 5.2k multi-instance-topology + ~3k incidents.jsonl + ~7k tasks-status Done section). Doctrine propagates to instances via `/acw-instance upgrade`; per-instance demotions stay operator-driven per audit.

**v0.9.0 framing:** per operator directive, this is the final pre-promotion substantive ship. v1.0.0 will be a clean soak/promotion of what's currently shipped — no new substrate, no new rules, no new skills. Pending items for v1.0.0 are dogfood validation runs against cs-copilot and gsg-copilot under v0.7.0+ plan-based audit/upgrade and the v0.9.0 auto-load discipline check.

## 2026-05-04 — v0.8.0: bookend efficiency cluster + plans/ + Kashef research (Session 13)

Operator surfaced acute cost pressure: `/acw-session end` running 7-10 minutes per invocation on Opus 4.7 1M context, halfway through Max-plan weekly budget after 2 days. Translated into six-change ship plus `plans/` folder folded in mid-execution as the seventh.

**Bookend efficiency:**

- `skills/acw-session/SKILL.md` declares `model: claude-haiku-4-5` in frontmatter. Three-verb command table (start/update/end). Tracker convention documented.
- `references/end.md` adds Mode dispatch + Quick mode (default) + Full mode sections. Each phase tagged with mode behavior. Sonnet escalation notes for Phase 3 operator-confirm and Phase 5 research-prompt. Tracker cleanup section.
- `references/start.md` adds Step 0 — creates active capture file + writes `.current-session` tracker.
- `references/update.md` ships as new file — mid-session checkpoint with self-bootstrap. Reads tracker, appends timestamped note under `## Updates`. Haiku-grade end-to-end.

**Substrate moves:**

- `git mv research/sessions sessions` — 8 capture files migrated. `paths.session_captures_dir` updated. `empty_dirs` swap.
- `mkdir plans && touch plans/.gitkeep` — new directory at root for plan artifacts. `paths.plans_dir: plans` added. Convention only in v0.8.0; no automatic writer skill yet.

**Cleanup:**

- Deleted four superseded skill directories: `capture-session/`, `capture-and-metabolize/`, `resume-session/`, `upgrade-instance/`. Removed entries from `acw-state.yaml::meta_layer`. Closes v0.4.0 Pending item the careful guardrail blocked from automated removal.

**Discipline writes:**

- D-ACW-037 records the bundle (7-item change list, 5 open follow-ups, 5 risk callouts).
- Cost-friction incident `a8e771f0-7686-484d-b89e-cc25e96f8c93` logged as activation evidence.
- Four new earned-in-0.8.0 entries in `rules/instance-current-manifest.md`: `sessions/` at root, `.current-session` tracker, `plans/` directory, `model:` frontmatter for bookend skills.

**Research:**

- `research/12-kashef-hive-mind-comparison.md` shipped (25 sources). Filtered Kashef's Hive Mind setup through earn-by-incident lens. Zero patterns original to Kashef; ACW positioned in substrate layer of agentic-OS stack uniquely. Three earn-ship candidates surfaced (`/acw-session standup` verb, briefing skill, suggestions/drift surfacer) — none ship in v0.8.0; held for incident-driven activation.

**Version bump:**

- `acw-state.yaml::version` 0.7.0 → 0.8.0. `last_reconciled_version` bumped to 0.8.0. Template baseline `last_reconciled_version` bumped to 0.8.0.

**Release gates:** vocab lint exit 0, drift check clean, 46/46 tests pass.

## 2026-05-03 — `/acw-session end` post-v0.6.1 (harness's second run; quiet)

Session-end run after the v0.6.1 meta-layer backfill commit landed. Capture file at `research/sessions/2026-05-03--v061-meta-layer-backfill.md`.

This is the **second invocation** of the v0.6.0 meta-layer maintenance harness. Walks the same trigger table the first run walked. Results:

| Meta file | Trigger fired this session? | Status |
|---|---|---|
| `README.md` | Substrate-shape: no new categories (v0.6.1 was a patch). Version bump 0.6.0→0.6.1 fired but no hardcoded version refs in README to update. | Current. |
| `CHANGELOG.md` | Version bump → already updated this session. | Current. |
| `LINEAGE.md` | New primitive: no (v0.2.0+ section was documentation, not new primitive). | Current — just-updated. |
| `ORCHESTRATION.md` | New methodology pattern: no (v0.2.0+ section was documentation). | Current — just-updated. |
| `SKEPTIC.md` | New med+ incident this session: no (no new incidents). | Current — just-updated. |

The harness's second run is quiet. Validates that trigger detection correctly identifies "no triggers fired" after a session that updated all the meta-files. The harness doesn't false-fire on freshly-updated files.

Phase 4 skipped (synapse_log_path null). Phase 5 skipped (no design questions surfaced this session; the carry-over open questions are operator-decision-shaped, not research-shaped).

### Metabolize report

**Auto-updated** (executed):
- `research/sessions/2026-05-03--v061-meta-layer-backfill.md` — session capture for v0.6.1 ship.
- This build-log entry.

**Proposed for operator review** (carry-over from prior sessions; no new proposals):
- Re-dogfood `/acw-instance audit` against `_Command`, `cs-copilot`, `gsg-copilot`.
- Cross-instance write trigger entry in `DEFERRED.md` for capability broker.
- Lint gate for command-routed skills.
- OQ-ACW-010 (now positive on two runs); OQ-ACW-011 (still open).

## 2026-05-03 — v0.6.1: meta-layer backfill from harness's first run

Single-word ship request after the v0.6.0 meta-layer harness's first invocation surfaced four staleness proposals. Operator accepted all four; v0.6.1 lands the meta-file updates that close the v0.2.0+ backfill gap.

The four proposals and what shipped:

1. **README.md directory map** extended with `context/` (and its four canonical files: `goals.md`, `objectives.md`, `how-i-work.md`, `key-people.md`) and `inbox/`. Previously listed only the v0.5.0 surfaces (`runbooks/`, `integrations/`, `briefings/`, `_buffer/`).

2. **LINEAGE.md** gained a major new section ("v0.2.0+ primitives") with primitive-trace entries covering the full v0.2.0–v0.6.0 cluster. The entries categorize as substrate categories (7), architectural primitives (5), skills (2), tooling (2), discipline primitives (3). Each names its triggering evidence (incident, decision-log entry, operator pushback) and any prior-art ancestor. The previous LINEAGE only traced v0.1.0 primitives to the formal seven-phase research project; v0.2.0+ traces predominantly to dogfood incidents.

3. **ORCHESTRATION.md** gained a "v0.2.0+ evolution methodology" section that documents the recurring dogfood-driven loop in operator-translation form. Names the loop's shape (operator runs ACW → friction surfaces → operator pushes back → session designs the fix → ship in next minor or patch with maintenance harness if pattern repeats), the three disciplines that keep it from becoming ad-hoc patching (earn-by-incident applies recursively; maintenance harnesses ship alongside structural fixes; append-only history is sacred), and the boundary (v0.2.0+ loop runs after v0.1.0-style structured research produces a coherent foundation; both methodologies are needed).

4. **SKEPTIC.md** gained Warning 4 ("Substrate is not static") earned 2026-05-03 via incident `e167b922`. Names the asymmetric-build anti-pattern: every "this won't drift, it's just reference" claim has been wrong on a long enough timeline. Existing Warning 4 (Reflexive injection) renumbered to Warning 5; file title updated from "Four Warnings" to "Five Warnings."

This validates the meta-layer harness's first-test correctness (OQ-ACW-010 earn-by-incident path appears clean for now). The harness produced clean proposals on first run; no spec bugs surfaced. Distinct from v0.4.0's audit verb which produced five bugs on first dogfood — the meta-layer harness's spec was tighter going in, partly because it inherited the lessons of the audit-verb experience.

### Metabolize report

**Auto-updated** (executed):
- `README.md` — directory map extended.
- `LINEAGE.md` — v0.2.0+ section added (~70 lines of primitive-trace entries).
- `ORCHESTRATION.md` — v0.2.0+ evolution methodology section added (~50 lines).
- `SKEPTIC.md` — Warning 4 added; renumbering applied; file title updated.
- `acw-state.yaml` — `version` and `last_reconciled_version` 0.6.0 → 0.6.1.
- `tools/templates/acw-state.yaml.tmpl` — baseline `last_reconciled_version` → 0.6.1.
- `decisions/decision-log.md` — D-ACW-035 (operator-approved acceptance of all four harness proposals).
- `CHANGELOG.md` — v0.6.1 entry per Keep a Changelog format.
- `tasks-status.md::Done` — Session 11 dated block.

**Proposed for operator review** (carry-over; no new proposals this session):
- Re-dogfood `/acw-instance audit` against `_Command`, `cs-copilot`, `gsg-copilot`.
- Cross-instance write trigger entry in `DEFERRED.md` for capability broker.
- Lint gate for command-routed skills.
- OQ-ACW-010 (resolved-positively-on-first-test); OQ-ACW-011 (still open; defer until evidence).

## 2026-05-02 — v0.6.0: operator-centric substrate + meta-layer harness

Continuation session immediately after v0.5.1's front-door cleanup. Operator approved the v0.6.0 scope queued at end of v0.5.1 and said simply: "ship." Four commits, one push.

The v0.6.0 cluster has two coherent halves:

**Operator-centric substrate.** `context/` fills the lightweight-context-layer gap that decisions/rules/skills/glossary didn't address — the "what is this workspace for, who matters, how does the operator work" layer that helps agents calibrate. Four canonical files (goals, objectives, how-i-work, key-people) ship as instance_layer with templates. ACW's own context/ files were populated with current operating reality (lightweight; ACW's deeper lineage lives in LINEAGE/ORCHESTRATION/research). `inbox/` fills the operator-capture surface — distinct from `_buffer/` (system handoffs) and `briefings/` (agent-generated snapshots). Three different surfaces, three different lifecycles. Items in inbox get triaged into tasks-status, parked, the operator's external task app, or deleted.

`rules/task-tracking.md` framing update made the workspace-purpose-vs-operator-personal split explicit. Tasks-status adapts per workspace type (cockpit = config + chief-of-staff ops; project = deliverables; full = org coordination). Operator-personal life tasks live in external task apps. Calendar lives in Google/iCloud/Nextcloud. Email lives in Gmail/Outlook. Same general rule applied consistently: don't duplicate operator-accessible-on-phone surfaces in workspace substrate. Lean on MCP integrations for live data; lean on briefings for moment-in-time aggregations.

**Meta-layer maintenance harness.** Closes the gap that produced v0.5.1's front-door cleanup. Substrate had Phase 2 distribution since v0.4.0; meta-layer had nothing, which let README go stale across four versions before someone noticed. The harness adds:

- `/acw-session end` Phase 2: walks a per-file trigger table (README on substrate-shape change, CHANGELOG on version bump, LINEAGE on new primitive, ORCHESTRATION on new methodology, SKEPTIC on med+ incident). For each trigger that fires, surfaces a proposed edit; operator confirms.
- `/acw-instance audit` Mode A extension: meta-layer staleness check using the same trigger table; flags stale files in the report.
- `/acw-instance upgrade`: walks audit-flagged meta-layer entries with operator-per-file confirmation prompts.

All three gated on `acw-state.yaml::meta_layer` block presence — consumer instances without the block see no meta-layer pass and pay no cost. Triggers are hardcoded sensible defaults; per-instance trigger overrides are earn-by-incident if needed.

The harness should prevent recurrence of the v0.5.1-style staleness incident: future ACW evolutions will surface meta-layer maintenance proposals automatically. README/CHANGELOG/LINEAGE/etc. won't drift across multiple versions before someone notices.

### Metabolize report

**Auto-updated** (executed):
- `acw-state.yaml` — `version` and `last_reconciled_version` → `0.6.0`. `instance_layer` extended with four `context/*.md` entries. `empty_dirs` extended with `inbox`. `paths` gained `context_dir` and `inbox_dir` (canonical defaults; instance overrides via paths block).
- `tools/templates/acw-state.yaml.tmpl` — baseline `last_reconciled_version` bumped to `0.6.0`.
- `tools/manifest.py` and `rules/manifest-discipline.md` — canonical default paths added for `context_dir` and `inbox_dir`.
- `tools/templates/context-{goals,objectives,how-i-work,key-people}.md.tmpl` — four new templates.
- `context/{goals,objectives,how-i-work,key-people}.md` — ACW's own context files populated.
- `inbox/.gitkeep` — directory marker for ACW's empty operator inbox.
- `rules/instance-current-manifest.md` — two new registry entries (`context/`, `inbox/`).
- `rules/task-tracking.md` — framing section added.
- `skills/acw-session/references/end.md` — Phase 2 meta-layer maintenance step added.
- `skills/acw-instance/references/audit.md` — Mode A meta-layer staleness check added; report format extended.
- `skills/acw-instance/references/upgrade.md` — meta-layer staleness resolution step added.
- `decisions/decision-log.md` — D-ACW-031 through D-ACW-034 (four entries).
- `tasks-status.md::Done` — Session 10 dated block. Pending now empty for the moment.
- `CHANGELOG.md` — v0.6.0 entry per Keep a Changelog format.
- `CLAUDE.md` — "Where things live" extended with `context/` and `inbox/` entries.

**Proposed for operator review** (deferred):
- Re-dogfood `/acw-instance audit` against `_Command` after v0.6.0 lands. Should now surface meta-layer staleness if `_Command` declares its own meta_layer block; otherwise skip the meta-layer pass silently.
- Cross-instance write trigger entry in `DEFERRED.md` for capability broker (carried over from v0.5.0 metabolize report; still pending).
- Lint gate for command-routed skills (carried over).

## 2026-05-03 — `/acw-session end` post-v0.6.0 capture + first meta-layer harness test

Continuation session-end run after the v0.5.1 + v0.6.0 ships. Capture file written at `research/sessions/2026-05-03--v051-frontdoor-and-v060-operator-centric.md`. Incident logged: `e167b922` (meta-layer-maintenance, med, process-gap) — README went stale across four versions before someone noticed; harness shipped same release closed the gap.

This is the **first invocation** of the v0.6.0 meta-layer maintenance harness. ACW has `meta_layer` block populated, so the trigger walk fires. Results:

| Meta file | Triggers fired | Status | Proposed action |
|---|---|---|---|
| `README.md` | substrate-shape changes (`context/`, `inbox/` added in v0.6.0); version bumps to 0.5.1 and 0.6.0 | Partially updated (full rewrite in v0.5.1; v0.6.0 substrate not reflected in directory map) | **Surface proposal** — extend directory map with `context/` and `inbox/`. Update version reference in any hardcoded text. |
| `CHANGELOG.md` | version bumps | Updated in both ships | **No action** — current. |
| `LINEAGE.md` | new primitives this session: `context/` canonical, `inbox/` canonical, meta-layer maintenance harness | Stale — no entries for v0.2.0+ primitives | **Surface proposal** — add primitive-trace entries for the v0.2.0–v0.6.0 cluster. |
| `ORCHESTRATION.md` | new methodology pattern earned (substrate-vs-meta-layer symmetry; earn-by-incident applied to spec evolution, not just primitives) | Stale — documents only the v0.1.0 build process | **Surface proposal** — add a "v0.2.0+ evolution methodology" section documenting the recurring pattern. |
| `SKEPTIC.md` | new incident logged this session: `e167b922` (severity med, process-gap) | Stale — no warnings absorbed from recent incidents | **Surface proposal** — should this incident (asymmetric build between substrate and meta-layer) earn a new warning about treating any substrate class as static reference? |

Three proposals for operator review. The harness ran end-to-end without bugs on this first test (OQ-ACW-010's earn-by-incident path appears clean for now), though it has not been stress-tested against `_Command` or other instances yet. Operator can either accept the proposals (which would land in a v0.6.1 follow-up commit) or defer them.

**Auto-updated** (executed):
- `research/sessions/2026-05-03--v051-frontdoor-and-v060-operator-centric.md` — full session capture for the v0.5.1 + v0.6.0 arc.
- `incidents.jsonl` — `e167b922` appended.
- This metabolize report.

**Proposed for operator review** (this session):
- Three meta-layer staleness proposals above (README, LINEAGE, ORCHESTRATION, SKEPTIC).
- OQ-ACW-010: meta-layer harness first-test bugs — accept earn-by-incident, or pre-emptive subagent stress test?
- OQ-ACW-011: meta-layer trigger table — keep hardcoded, declare per-instance, or move into meta-file frontmatter?

## 2026-05-02 — v0.5.0: audit verb fixes from `_Command` dogfood + new canonical substrate

Operator opened by pasting the first real `/acw-instance audit` output from `_Command`. Audit ran cleanly at the surface — produced a routing table, identified 5 canonical-shape OK files, 1 enrichment-incomplete, 1 divergent (sessions/ at root), 6 organic findings (briefings, context, notes, runbooks, integrations, etc.). But the agent in `_Command` produced the report with PROPOSED routings ("Likely [s]", "Possibly [b]") rather than walking each finding interactively with the four-option prompt. Result: nothing landed in ACW's `_buffer/`. Five v0.4.0 bugs fell out of the analysis.

Conversation arc:

1. Operator surfaced the bugs by reading the audit output critically. *"It sent nothing to your inbox."* Pointed at exactly the right thing.
2. Hard-stop scan was too narrow — counted only `decisions/` and `rules/`, missed `_Command`'s organic substrate at root. Fix: widen scope.
3. Mode B walk wasn't actually interactive. Spec was ambiguous; agent reading produced static report. Fix: tighten spec, prompt-per-finding, write-on-routing.
4. Default Mode B classification was `[s] instance-specific` — too conservative. Fix: "ask, don't guess" with canonical comparison surfaced in prompt.
5. Skills audit wasn't part of the verb spine. The audit found 6 skills under `_Command/skills/` but didn't validate frontmatter. Fix: bring SKILL.md frontmatter validation into the spine.
6. Absorption flow was gated on workspace registration. `_Command` is unregistered; even if Mode B had been interactive, absorption candidates couldn't have flowed because the workspace had no `acw-state.yaml::cross_repo_writes` block. Fix: candidates flow during audit pre-adoption; pending entries queue for upgrade verb to materialize when it writes the new acw-state.yaml.

Then the substrate-categorization conversation. Initial audit verdict had flagged `briefings/`, `runbooks/`, `integrations/` all as "Likely [s] instance-specific." Operator pushed back: most of these are universal patterns. Briefings is universal because cockpit + project + full all benefit from agent-generated snapshots, just with different aggregation content. Runbooks is universal because every workspace accumulates operator-facing how-to docs. Integrations is universal because most workspaces touching external systems via MCP/API/webhook accumulate docs about them. Verdict reversed; three new canonical surfaces shipped.

Sub-decisions during the substrate conversation:
- `notes/` deferred — needs lived experience for per-workspace-type subfolder defaults.
- `my-tasks.yaml` rejected — same logic as calendar; operator uses external task app, accessible on phone.
- Calendar mirror rejected — lean on MCP for live data; briefings handle aggregation when wanted.
- `inbox/` (operator-facing) and `_inbox/` (system) need to be distinct surfaces. Different generators, different lifecycles. Rename `_inbox/` → `_buffer/` per DIP vocabulary canon to avoid the collision when v0.6.0 ships operator inbox.

Operator's framing correction: leadership is cockpit; cockpit isn't role-gated. Anyone with a personal command center crossing personal+business surfaces is a cockpit operator. Per `research/07-instance-types.md` the canonical types are Full/Cockpit/Project/Read-Only — leadership doesn't appear because it's not a separate type. Updated examples accordingly.

Three commits in v0.5.0:
1. `fix(skills): audit/upgrade verb fixes + _inbox/ -> _buffer/ rename` — five bug fixes plus the system surface rename, all touching the same skill files.
2. `feat: runbooks/, integrations/, briefings/ as canonical substrate` — three registry entries, ACW declarations, scaffolder verified.
3. This housekeeping commit — version bump, decision log entries D-ACW-023 through D-ACW-029, this build-log entry, tasks-status update.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 8 dated block. Pending updated to remove the v0.5.0 dogfood-audit line item (it ran; the bugs are fixed; next dogfood comes after v0.5.0 lands) and add v0.6.0 scope note + re-dogfood task.
- `decisions/decision-log.md` — added D-ACW-023 through D-ACW-029 (seven entries) in chronological order.
- `acw-state.yaml` — bumped `version` and `last_reconciled_version` to `0.5.0`; updated `empty_dirs` (added `runbooks`, `briefings`; renamed `_inbox` → `_buffer`); added `integrations/README.md` to `instance_layer`; renamed `paths.inbox_dir` → `paths.buffer_dir`.
- `tools/templates/acw-state.yaml.tmpl` — bumped baseline `last_reconciled_version` to `0.5.0`.
- `_inbox/` → `_buffer/` directory rename via `git mv` (preserves history).
- `tools/manifest.py` and `tests/test_manifest.py` — updated canonical defaults and corresponding test assertions.
- `rules/manifest-discipline.md` — canonical default paths added for new dirs.
- `rules/instance-current-manifest.md` — three new registry entries earned in v0.5.0; `_buffer` entry rewritten with rename history.
- `rules/multi-instance-topology.md`, `rules/skill-format.md`, `CLAUDE.md`, all skill files — `_inbox` references updated to `_buffer`.
- `incidents.jsonl` — appended `73cf90d2` (v0.4.0 audit verb bugs from `_Command` dogfood, severity med, category implementation-bug; resolution shipped same release) and `64689988` (substrate-classification conservatism, severity low, category process-gap).
- `research/sessions/2026-05-02--v050-audit-fixes-and-substrate-absorption.md` — full session capture written by `/acw-session end`.

**Proposed for operator review** (deferred):
- v0.6.0 ship: `context/`, operator `inbox/`, tasks-status framing update, doc note about external systems.
- Re-dogfood `_Command` audit after v0.5.0 ships to validate the interactive Mode B walk works end-to-end.
- Cross-instance write trigger entry in `DEFERRED.md` for capability broker.
- Lint gate for command-routed skills.
- OQ-ACW-008: how does operator-facing `inbox/` (v0.6.0) relate to `tasks-status.md` and `briefings/`? Three candidate models in the session capture; needs lived experience to resolve.
- OQ-ACW-009: should briefings be configured per workspace type, per workspace, or per domain? Defer until first briefing skill ships.

## 2026-05-02 — v0.4.0: command-routed skills, full audit verb, absorption mechanics

Operator opened the session with a session capture from cs-copilot where they had tried to run `/upgrade-instance` and the agent there bailed because cs-copilot is substantively an ACW instance but lacks formal registration. This was already addressed in v0.3.0 via adopt mode, but the operator's question went deeper: what about workspaces with **organic substrate** that's evolved its own conventions (like `_Command`)? Steamrolling those into canonical shape would destroy institutional learning.

The conversation refined the three-flow model: adopt (canonical-shaped, just unregistered), absorb (workspace's pattern is better than canonical; flow upstream via `_inbox/`), and instance-specific (uniquely the workspace's, won't generalize). Operator pressed on permanent divergence as a smell: the gradient should always be toward canonical-shaped. Right answer — `divergent_pending_review` is temporary, pending ACW resolution; `instance_specific_substrate` is permanent but requires a decision-log reference.

Then a structural insight: rename `/upgrade-instance` → `/acw-instance` with verbs `audit` and `upgrade`, fitting the command-routed orchestrator pattern. Operator pushed further: `/resume-session` and `/capture-and-metabolize` should follow the same shape as `/acw-session start|end`. I initially pushed back — the four-test rule reading "same invariant workflow" seemed to prohibit sibling specialist operations. Operator pointed at Impeccable as the precedent: 23+ commands across genuinely different specialist workflows, unified by shared setup. Re-reading the skill-format with that lens, the strict-voice contradicted the permissive-voice (command-count ladder explicitly carves out object-centered workbenches at 10+ commands). The format itself was self-contradictory; that's why I false-flagged the pattern.

Then the synthesis question: is every problem named in this session shippable? It surfaced loose items — absorption candidate format wasn't specified, divergence marker schemas weren't documented, hard-stop threshold had no value, re-adoption flow had no mechanics. Six commits revised: tighten skill-format, expand multi-instance-topology with absorption mechanics, register four new recommended blocks, restructure skills as command-routed, housekeeping.

Two operator pushbacks during execution that produced better answers:
- Mode A doesn't need a new schema artifact; ACW rules + templates ARE the schema in prose form. Audit verb fetches them from GitHub canonical and compares inline.
- Mode B doesn't need sophisticated heuristics; it needs the operator in the loop. Walk for substrate-like patterns; surface to operator with four-option routing.

Both ship in v0.4.0 instead of being deferred.

The skill-format port was bigger than expected. ACW canonical's `rules/skill-format.md` had been shorter than the operator's synapse global rules — the command-routed orchestrator material had only existed in the personal layer. Ported the full content into ACW canonical with the three corrections applied.

User-level junctions swapped at the end. Old skill directories marked superseded in frontmatter (`status: superseded`, `superseded_by`, `superseded_in: 0.4.0`); moved to `meta_layer` awaiting manual delete (careful guardrail blocks automated `rm -rf`).

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 7 dated block. `tasks-status.md::Pending` rebuilt with v0.4.0-shaped tasks (dogfood `/acw-instance audit` against cs-copilot, `_Command`, gsg-copilot; deletion task for four superseded skill directories).
- `decisions/decision-log.md` — added D-ACW-016 through D-ACW-022 (seven entries) in chronological order.
- `acw-state.yaml` — bumped `version` and `last_reconciled_version` to `0.4.0`; added `_inbox` to `empty_dirs`; added `divergent_pending_review`, `instance_specific_substrate`, `adopt_mode_organic_threshold` blocks; updated `template_layer` to list new skills; added superseded skills to `meta_layer`; added `research/10-multi-instance-topology.md` to `meta_layer`.
- `tools/templates/acw-state.yaml.tmpl` — same shape as parent for the four new blocks.
- `incidents.jsonl` — appended `0e4dcc21` (skill-format false-flag, severity low, category process-gap). Resolution shipped in same release via D-ACW-016.
- `research/sessions/2026-05-02--v040-command-routed-skills-and-audit-verb.md` — session capture written by `/acw-session end` at session close.

**Proposed for operator review** (deferred to next session):
- Manual deletion of four superseded skill directories after dogfood validates v0.4.0 against cs-copilot.
- Cross-instance write trigger entry in `DEFERRED.md` for the capability broker.
- Lint gate for command-routed skills.
- OQ-ACW-007: how does ACW notify a workspace when an absorption candidate is rejected? (Three candidates in the session capture; needs lattice-scale evidence.)

## 2026-05-02 — RC4 → v0.3.0: multi-instance topology, GitHub-first canonical, adopt mode

Operator opened the session by feeding back a cs-copilot session where `/upgrade-instance` correctly identified missing registration files and bailed. They pushed back on the "not an ACW instance" verdict, asking what an ACW instance fundamentally **is**. The conversation surfaced the substance-vs-registration distinction: cs-copilot has every load-bearing piece of an ACW instance (decisions, rules, glossary, evolution, research, incidents, bookend skills) but lacks the registration metadata. Verdict: cs-copilot is substantively an ACW instance; the agent ran a registration check rather than a substance check.

That conversation escalated into the larger architectural question: can a full business run from ACW, and if so, what's the structure? Sketched the lattice model (org-brain instance + departmental instances), the knowledge-placement discriminator (who queries it; does the answer need to be the same), the reference-not-duplicate principle, the three coordination primitives needed (handoff protocol, capability broker, admission controller — the broker now has the lattice as its architectural target), the authority model across the lattice, the bootstrapping order (departmental first, org-brain refactored from extraction).

Wrote `research/10-multi-instance-topology.md` formalizing the lattice and naming Phase 1 ship: fix `/upgrade-instance` to support adopt mode for substrate-shaped pre-ACW workspaces.

Operator then asked four sharp follow-up questions that exposed real seams:

1. How do we conceptualize the lattice into the template so a business is informed when ready? **Answer:** promote canonical statement to `rules/multi-instance-topology.md` (template_layer). Research note stays meta_layer as provenance. Add as recommended block earned in v0.3.0.
2. When ACW's canonical registration updates, how do other instances stay current? **Answer:** GitHub as single source of truth. `/upgrade-instance` fetches canonical from `benfrankster-design/acw` on every run via `gh` CLI (private repo). Local copy is write-once cache. Operator rejected local-ACW fallback; one pointer means one place to update if repo ever moves.
3. How do edits inside ACW get captured and metabolized properly? **Answer:** add canonical-edit detection to `capture-and-metabolize` Phase 2. Detect edits to files in the intersection of `auto_load_at_session_start` and `template_layer`; branch on `is_canonical_source`.
4. What happens when child instances inherit the propagation behavior? **Operator caught the bug:** if Phase 2 ships a "version bump + push to GitHub" prompt to every instance, child instances will start trying to push to ACW's GitHub. Solution: add `is_canonical_source` flag to `acw-state.yaml`. ACW sets true; children default false. Phase 2 branches on the flag — publishers get the push prompt; consumers get a "local edits won't propagate" warning.

Shipped six pieces: new rule file, manifest registry entries, flag in state file + template, upgrade-instance rewrite, capture-and-metabolize Phase 2 update, version bump to 0.3.0. Logged D-ACW-012 through D-ACW-015. Updated tasks-status with two adopt-mode dogfood targets (cs-copilot and gsg-copilot) and a note to add the cross-instance write trigger to DEFERRED.md.

Push to `origin/master` retires the 8-commits-ahead parked task by landing rc1-rc4 plus v0.3.0 in a single batch — GitHub goes from 3 weeks stale to current in one move, and the new `/upgrade-instance` works against the live canonical from first run on any instance.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 6 dated block. Pruned the resolved 8-commits-ahead push task from Pending; added two adopt-mode dogfood tasks (cs-copilot, gsg-copilot) and the cross-instance broker trigger task.
- `decisions/decision-log.md` — added D-ACW-012, D-ACW-013, D-ACW-014, D-ACW-015 in chronological order.
- `acw-state.yaml` — bumped `version` and `last_reconciled_version` to `0.3.0`; added `is_canonical_source: true`; added `rules/multi-instance-topology.md` to `template_layer` and `auto_load_at_session_start`.
- `tools/templates/acw-state.yaml.tmpl` — set baseline `last_reconciled_version: "0.3.0"`; added `is_canonical_source: false` default.

**Proposed for operator review** (not executed):
- Whether `CLAUDE.md` needs an edit to reflect v0.3.0 substrate (new `rules/multi-instance-topology.md` in auto-load list); the auto-load list in CLAUDE.md is import-driven via `@`, so adding the file may want a manual import line.
- Whether `research/10-multi-instance-topology.md` should also live in cross-vendor-readable form somewhere downstream (e.g., as a starter template snippet) or whether the rule file is sufficient.

## 2026-05-02 — Skill registration via user-level junctions

Operator surfaced that `/resume-session` wasn't firing — the skills shipped at `acw/skills/<name>/` weren't being discovered by Claude Code, which reads from `.claude/skills/` and `~/.claude/skills/`. Discussed two registration patterns (project-level per workspace vs. user-level single canonical source) and the multi-instance pollution concern when child workspaces also ship the same skills via template_layer. Operator chose the user-level / single-canonical-source pattern: ACW is the registered source for every workspace; child copies stay passive on disk for self-contained distribution. Created three directory junctions in `~/.claude/skills/` pointing at ACW's `skills/<name>/` directories.

D-ACW-011 records the architectural choice. OQ-ACW-006 captures the open question of whether `tools/scaffold-instance.py` should optionally create skill junctions at scaffold time — deferred for second-instance evidence.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Done` — added Session 5 dated block.
- `decisions/decision-log.md` — added D-ACW-011.
- `incidents.jsonl` — appended one process-gap incident: skills ship in template_layer but registration is manual, future operators will hit the same friction.

**Proposed for operator review** (not executed):
- *(none)* — session was small and unambiguous.

**Skipped** (intentionally not touched):
- All append-only history (build-log past entries, evolution past entries, incidents prior lines, capture-session past files, decision-log past decisions).
- `paths.research_queries_dir` is empty; nothing to consume.

**Prompts consumed this session:** *(none — `paths.research_queries_dir` is empty.)*

## 2026-05-02 — RC4: portable bookend skills, drift detection, upgrade skill

The bookend skills (`capture-and-metabolize`, `resume-session`) were tightly coupled to ACW's specific directory layout — paths to `decisions/decision-log.md`, `tasks-status.md`, `research/sessions/`, etc. were hardcoded throughout. That worked for ACW but broke portability: instances that wanted to restructure substrate, or future template evolution that moved a file, would force grep-and-replace across every skill. RC4 decouples the skills from paths via a manifest-driven approach, then adds drift detection so existing instances can learn they're behind and reconcile through a guided skill.

Shipped in seven atomic phases with verification at each boundary:

**Phase 1 — Foundations.** Added `paths:` block to `acw-state.yaml` listing 14 substrate file paths. Documented canonical defaults and four-operation manifest-tooling spec (load / append / contains / validate) in `rules/manifest-discipline.md`. Version bumped `0.2.0-rc3 → 0.2.0-rc4`. Commit `62ba6be`.

**Phase 2 — Python tooling (TDD).** Wrote `tests/test_manifest.py` first (33 tests covering existing-list reads, canonical-default fallback, append additivity, dict/list round-trip, comment preservation, error semantics). Implemented `tools/manifest.py` until tests passed first run. Subagent confirmed spec/impl alignment. Commit `dd8c8da`.

**Phase 3 — Skill refactor + references audit.** Refactored both bookend skills to use `paths.X` shorthand throughout. Audited 11 reference files in `capture-and-metabolize/references/`, plus `resume-session/`'s SKILL.md and gotchas. Replaced hardcoded paths with prose-level references resolved at runtime. Generalized project-specific references (gsg-copilot, synapse, Cortex, HR-CP-NNN) to be portable. Added `section_conventions` frontmatter to `decisions/decision-log.md`, `tasks-status.md`, `research/evolution.md` and their templates. Subagent verified zero hardcoded substrate paths remain. Commit `3c1cac8`.

**Phase 4 — Drift detection.** Created `rules/instance-current-manifest.md`, the declarative registry of recommended blocks (project, paths, auto-load list, three-layer manifest, empty_dirs, cross_repo_writes, synapse_log_path, voice). Each entry documents what / why / required / how-to-add / earned-in. Added Step 5 drift check to `resume-session` SKILL.md. Subagent caught a version-vs-date conflation: `last_reconciled` was a date but the comparison needed semantic versions. Fixed by adding `last_reconciled_version` field alongside the date field. Also clarified present-but-empty semantics: a block declared empty is deliberate opt-out, not drift. Commit `9374ccb`.

**Phase 5 — `/upgrade-instance` skill.** Built the reconciliation skill that walks operators through gap closure. Subagent stress test caught two more edge cases: partial blocks (some-but-not-all canonical keys) and malformed blocks (wrong shape). Resolved: partial blocks are honored as deliberate operator choice (runtime defaults fill the rest); malformed blocks halt the pass and ask for hand-edit (skill is reconciliation, not validation cleanup). Commit `0070938`.

**Phase 6 — Substrate updates** (this entry). Decision-log entries D-ACW-008, D-ACW-009, D-ACW-010 record the architectural choices. Tasks-status Session 4 block. CLAUDE.md updated with the new auto-load entry (`rules/instance-current-manifest.md`). Evolution entry recording the framework-agnostic shift.

**Phase 7 — Final dogfood.** Scaffold a fresh instance from rc4. Run release gates inside it. Simulate outdated instance (remove a recommended block); confirm drift alert fires. Run upgrade skill; confirm reconciliation. Final cold-read subagent reviews the rc4 changeset for inconsistencies, hardcoded paths, circular dependencies, backwards-compatibility gaps.

The shape that fell out: ACW now treats every "what files matter" list the same way — single source of truth in `acw-state.yaml`, additive maintenance by the bookend skill, removal by ritual, lint as the safety net. The bookend skills are portable; instances upgrade themselves with a one-line alert and a one-skill walkthrough.

### Metabolize report

**Auto-updated** (executed):
- `tasks-status.md::Pending` — removed "Framework-agnostic bookend skills..." item; satisfied by Session 4 Done block.
- `tasks-status.md::Pending` — removed "Decide: ship tools/scaffold-instance.py under emergency clause..." item; decided in rc1 as D-003.
- `tasks-status.md::Pending` — reworded the "Promote v0.2.0-rc1 to v0.2.0" item to reflect the actual current state (multiple rcN have shipped; promotion is now to v0.2.0 final after a clean-soak window).
- `tasks-status.md::Pending` — added "Dogfood /upgrade-instance against an actually-outdated downstream instance" so the upgrade loop earns its build through real friction, not just simulated friction.
- `tasks-status.md::Pending` — added "Push branch to origin/master" since the rc4 work is committed locally only.

**Proposed for operator review** (not executed):
- *(none)* — no items needed operator confirmation this pass. The cleanups above were all unambiguous.

**Skipped** (intentionally not touched):
- `build-log.md` past entries — append-only history.
- `incidents.jsonl` — append-only ledger; rc4 had no new incidents (subagent verification protocol caught issues before commit, which is the protocol working as designed).
- `research/sessions/` past captures — frozen once written.
- `decisions/decision-log.md::section_conventions.decisions` past entries — append-only spirit.
- `tasks-status.md::Done` past dated entries — history.
- `paths.research_queries_dir` — empty; nothing to consume.

**Prompts consumed this session:** *(none — `paths.research_queries_dir` is empty.)*

The session was clean. No drift surfaced beyond the satisfied/stale Pending items above. No new incidents. Subagent verifications at four phase boundaries plus a final cold-read all surfaced fixable issues that landed before commit, exactly as the protocol intends.

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
