---
class: capture
authority: skill
stability: complete
date: 2026-05-21
topic: graphify-probe-and-codemap-audit
session_n: 23
carry_forward: true
---

# Session 23 — Graphify probe + canonical codemap audit + integration decision

## TL;DR for resumption

Three things this session produced that the NEXT session in acw/ should pick up and finish:

1. **Ground truth on Graphify.** `graphifyy 0.8.14` installed. AST-only `update` is free and works. Output structure documented. CLI surface mapped. Gemini (not Claude) is the Stage 2 LLM. The audit at `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md` is the reference document.

2. **Two integration decisions locked.** Codify as D-ACW-052 next session:
   - **ACW's auto-load wins.** Skip `graphify claude install`. CLAUDE.md stays a thin pointer. Codemap loads via `acw-state.yaml::auto_load_at_session_start` like every other substrate module.
   - **AST-only is the default.** Graphify's Stage 2 (Gemini) stays opt-in via `acw-state.yaml::env_secrets`. The ACW-specific `implements_decision` bridge runs via Claude (already in stack) — that becomes the semantic layer instead of Graphify's native Stage 2 for most instances.

3. **Patch plan ready.** ~90 minutes of canonical authoring across ten files to land the audit corrections + the two decisions + the wrapper authoring. Concrete file list below.

## What happened this session (chronology)

### Phase 1 — Reframe (operator pushback)

Operator pushed back on my earlier framing that the `/acw-instance upgrade` skill should encode v0.10.0 migration logic. Correct framing: skill is a thin portable executor; canonical IS the source of truth; migration knowledge lives in declarative `migrations/<from>-to-<to>.yaml` files. Reframed.

### Phase 2 — Phase 2 work landed

Committed `0f17108` (manifest schema, 0.9.9-to-0.10.0 manifest, /substrate-map skill, scaffolder updates, rules/ stays-at-root decision D-ACW-051 + C-004) and `aa61f65` (intermediate manifests for v0.9.2-to-0.9.3 task-tracking, pre-acw-to-0.10.0 bootstrap; /codemap skill stub; executor patch; skill audit pass with archives_dir → paths.archives_dir replacements in 4 files; five-instance audit report at `.acw/raw/2026-05-21-instance-audit-five-instances.md`).

### Phase 3 — Graphify reality check

Operator caught me out: I'd described Graphify's architecture from secondary-source articles (betterstack, pyshine, medium) without ever installing or running it. He said "you didn't install it? pip install graphifyy".

I installed (`pip install graphifyy`; package name has two y's; CLI binary is `graphify`). Probed against three files in skills/codemap/, then against Python code from tools/. Got real ground truth.

### Phase 4 — Audit canonical against reality

Wrote `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md`. Found three breaking errors, four moderate, three minor. Most consequential:
- Output location: Graphify writes to `graphify-out/` at cwd; no `--output-dir` flag. Wrapper must cd-or-move.
- LLM provider: Gemini, not Claude, not local.
- ACW-decision bridging is NOT native to Graphify — it's an ACW-specific bridge we build on top.

### Phase 5 — Integration decision

Operator chose ACW's auto-load over Graphify's `claude install`. Reasoning:
- One mechanism for everything (decisions INDEX, glossary, tasks, rules, codemap report — all load the same way via SessionStart hook)
- CLAUDE.md stays thin pointer per D-ACW-047
- Codebase shape changes slowly; session-start loading is fresh enough
- Operator framing: "this is ACW, not Graphify. We're using Graphify concepts and making it our own."

### Phase 6 — Stage 2 env-var pattern designed

For instances that DO want Graphify's semantic extraction: declarative dependency in `acw-state.yaml::env_secrets`, value supplied via per-instance `.env` (gitignored) OR operator shell env. Skill reads from `os.environ`, refuses cleanly if missing. Default behavior is AST-only.

## Decisions locked, pending codification

### D-ACW-052 — Codemap integration: ACW's auto-load, not Graphify's claude install

To author next session. Key points:
- Graphify is treated as an internal AST engine, not a co-equal integration partner
- User-facing surface is `/codemap` (ACW skill), not `graphify` (CLI delegated to)
- Output lives at `.acw/codemap/` (relocated from `graphify-out/` by wrapper)
- Auto-load entry for `.acw/codemap/GRAPH_REPORT.md` lives in `acw-state.yaml::auto_load_at_session_start` per coding-project / library profile defaults
- `CLAUDE.md` stays a thin pointer; `graphify claude install` is NOT used
- Stage 2 (Gemini) is opt-in via `acw-state.yaml::env_secrets`; default is AST-only
- The `implements_decision` bridge (ACW-specific) runs via Claude when authored; this is where semantic linkage to decisions lands, not Graphify's Stage 2

### C-005 — Companion constraint

Stop-work on writing Graphify-specific content into any instance's CLAUDE.md. Codemap integration is via auto-load only. Authority: D-ACW-052.

## The 90-minute patch plan (concrete file list)

Order matters: rules first (sets contracts), then skill files (consumes contracts), then migrations (apply contracts to new instances), then scaffolder.

**1. Author D-ACW-052** at `.acw/decisions/entries/D-ACW-052-codemap-integration-acw-auto-load.md` (~15 min)

**2. Author C-005** at `.acw/decisions/constraints/C-005-no-graphify-content-in-claude-md.md` (~5 min)

**3. Patch `rules/codemap.md`** (~20 min):
- Output relocation pattern (`graphify-out/` → `.acw/codemap/`; no `--output-dir` flag)
- Gemini-not-Claude for Stage 2; opt-in via env_secrets
- Node-type enum from probe: `document`, `code`, `rationale` (drop "decision" — that's ACW-bridge-added, not Graphify-native)
- Edge-type enum from probe (AST-only): `calls`, `contains`, `rationale_for`, `inherits`. Note INFERRED additions come from Stage 2.
- `implements_decision` is ACW-specific (bridge), not native
- Build trigger direction: POST-commit hook native to Graphify; ACW codemap uses on-demand + auto-load. Skip Graphify's hook install.
- Add the `confidence_score: 0.0-1.0` numeric field

**4. Patch `rules/confidence-tagging.md`** (~5 min):
- Add `confidence_score` numeric field alongside the tag (EXTRACTED → 1.0, INFERRED → variable, AMBIGUOUS → not assigned)

**5. Patch `rules/instance-current-manifest.md`** (~10 min):
- Add `env_secrets:` block to the recommended-blocks registry, with schema (`name`, `required_by`, `when`, `notes`)

**6. Patch `skills/codemap/SKILL.md`** (~15 min):
- Verb names: keep `rebuild`, `status`, `audit` (ACW surface) but document that they delegate to `graphify update`, `graphify cluster-only`, etc.
- Pre-flight: add env_secrets check for `--semantic` runs
- Output structure: single `graph.json` (NetworkX), not separate files; `cache/` (no dot)
- Delegation pattern: pass-through for `query`, `path`, `explain`

**7. Patch `skills/codemap/gotchas.md`** (~5 min):
- Gemini-not-Claude correction
- `cache/` not `.cache/`
- "Wrapper authoring ready" status update

**8. Patch `skills/codemap/references/implementation-plan.md`** (~15 min):
- Replace "investigation deferred" framing
- Add the probe findings inline
- Concrete wrapper-authoring steps (cd-or-move output relocation; `implements_decision` bridge via Claude API)

**9. Fix `migrations/0.9.9-to-0.10.0.yaml` + `migrations/pre-acw-to-0.10.0.yaml`** (~5 min):
- `.cache` → `cache` (or drop the cache create_dir step entirely; Graphify creates it)

**10. Fix `tools/scaffold-instance.py` + `tools/templates/acw-state.yaml.tmpl`** (~10 min):
- Drop `.cache/` creation
- Add `env_secrets:` template scaffold (commented-out by default)

**11. Update INDEX + build-log + tasks-status** (~10 min):
- Decisions INDEX gains D-ACW-052 + C-005
- Build-log Session 24 entry (the patch session)
- Tasks-status: mark codemap audit-correction items as done, leave wrapper-authoring as the next concrete task

**Then commit + push.**

## What comes after the patch session

Once the canonical is corrected, the wrapper authoring is the next discrete piece. Estimated 1-2 hours:

- Author `skills/codemap/references/rebuild.md`, `status.md`, `audit.md`
- Author the wrapper subprocess invocation (`graphify update` from project root, move output to `.acw/codemap/`)
- Author the `implements_decision` bridge step (walk `.acw/decisions/entries/`, find code links via literal-ID match + LLM semantic judgment, append to graph or sidecar `.acw/codemap/acw-edges.json`)
- Dogfood against cs-atlas

## What's deferred but not lost

Five-instance upgrade execution. Per the audit at `.acw/raw/2026-05-21-instance-audit-five-instances.md`:
- frank-context (cleanest) — runs `0.9.9-to-0.10.0.yaml` direct
- cs-ops-spec — already at v0.10.0 shape (commit `f89ec44`); verify profile/modules
- cs-atlas — partial bootstrap (substrate already relocated; needs acw-state.yaml)
- _command — chain (0.9.7 → 0.9.8 → 0.9.9 → 0.10.0); needs `0.9.7-to-0.9.8.yaml` manifest authored (lift v0.9.8 wiki migration from existing skill prose)
- cs-copilot — full pre-acw bootstrap

Blocked on: `/acw-instance upgrade` executor verification (manifest step kinds the current executor handles vs needs added). Per upgrade.md's "Executor verification status" section: `remove_gitignore_rule`, `only_if` conditional, `optional: true` on git_mv all need executor implementation.

## Repo state at session end

Three commits on `master` of `acw/`, all pushed to github.com/benfrankster-design/acw:
- `fbddf2b` — v0.10.0 initial (partial — recovered by next commit)
- `fcf22a5` — recovery (removed obsolete .acw/ gitignore rule; recovered v0.10.0 content)
- `0f17108` — phase 2 (manifests + substrate-map + scaffolder + rules/ closure)
- `aa61f65` — phase 2 sweep (codemap stub + skill audit + audit reports)

cs-ops-spec: commit `f89ec44` local (no remote). Working tree clean.
cs-atlas: commit `099e57a` local (Bitbucket invite pending from Robert).

Untracked in acw/: `.acw/raw/2026-05-21-graphify-audit-canonical-vs-reality.md`, this session capture, plus any build-log/tasks-status edits from session-end commit.

## How the next session should start

1. Open Claude Code with cwd = `~/projects/acw/`
2. Run `/acw-session start` — the SessionStart hook will load auto-loaded substrate; this capture is discoverable in `.acw/sessions/`
3. Open this file and the audit doc as the first reads
4. Execute the 90-minute patch plan above, in order
5. Commit + push the canonical corrections
6. Optionally proceed to wrapper authoring in same session if time permits
7. `/acw-session end full` to bookend properly

## Probe environment for re-creation

If a new session needs to re-verify Graphify behavior:

```bash
pip install graphifyy        # graphifyy 0.8.14 confirmed
graphify --version           # → graphify 0.8.14
mkdir /tmp/probe && cd /tmp/probe
cp <some-python-files> .
graphify update .            # AST-only, free
cat graphify-out/GRAPH_REPORT.md
python -c "import json; d=json.load(open('graphify-out/graph.json')); print(d['nodes'][:3])"
```

Sample probe results documented in audit doc.

## One open call for the operator

cs-ops-spec has no remote configured. Local-only commit. Operator decision pending: push to GitHub (private?) or Bitbucket, or keep local. Not blocking anything; flagging.
