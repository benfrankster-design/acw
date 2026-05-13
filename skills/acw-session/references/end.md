---
scope: end
---

# end

Session-end verb. Up to five phases: capture, distribute, metabolize, optional synapse log, optional research prompt. Mode-portable across `decision_tracking.mode` and `glossary.mode`.

## After the spine

The orchestrator's spine has resolved configuration, paths, buffer state, recent capture paths, and run the **pre-flight context-budget check** (Step 0). The end verb dispatches on profile.

## Profile dispatch (replaces flag soup)

Five named profiles. The first positional argument selects the profile. Unknown profile → error with the table.

| Invocation | Profile | Phases that run |
|---|---|---|
| `/acw-session end` | `quick` (default) | 1 + 2-append-only + 3-auto-sweep |
| `/acw-session end full` | `full` | 1 + 2-full + 3-full + 4 (if `synapse_log_path` set) + 5 (if non-empty) |
| `/acw-session end log-only` | `log-only` | 1 only — capture file, no distribution, no metabolize |
| `/acw-session end synapse-only` | `synapse-only` | 1 + 2-append-only + 3-auto-sweep + 4 |
| `/acw-session end research-only` | `research-only` | 1 + 2-append-only + 3-auto-sweep + 5 (gated on non-empty) |

**Run banner.** First line of skill output: `[acw-session end | profile=<name> | mode=<decision_tracking.mode>/<glossary.mode>]`. Final line of output: `[summary] phases=ran:N skipped:M failed:0 artifacts=<count>` followed by per-phase status (`RAN | SKIPPED(reason) | FAILED(error)`).

## Mode-portability gate

Before Phase 2, resolve substrate mode:
- `dm = acw-state.yaml::decision_tracking.mode` (default `single-file`)
- `gm = acw-state.yaml::glossary.mode` (default `single-file`)

All Phase 2 + Phase 3 writes branch on these. The skill is portable across both shapes — see `references/distribution-rules.md` and `references/metabolize-rules.md` for per-mode dispatch.

## Phase 1 — Capture (runs in every profile)

Resolve the active capture file via `<sessions_dir>/.current-session`. If the tracker exists with a `file:` field pointing to a real file (started by `/acw-session start` or self-bootstrapped by `update`), use it (Phase 1 may RENAME from `untitled` to topic-from-this-step). If tracker absent or empty, write fresh capture at the path computed from today's date + topic.

Steps:
1. Identify topic: 3–7 word noun phrase.
2. Identify decisions made (→ Phase 2 decisions candidates).
3. Identify conceptual shifts (→ `paths.evolution` candidates).
4. Identify terms that entered or shifted meaning (→ Phase 2 glossary candidates).
5. Identify tasks completed or newly started (→ `paths.tasks_status` candidates per v0.9.3+ Pending-only shape; completed → archive + remove from Pending; new → append to Pending). Deferred-but-keep ideas route to `inbox/ideas/`, not back into tasks-status.
6. Identify hard-rule changes (→ instance hard-rules file candidates, prefix `HR-{project.code}-NNN` if `project.code` set).
7. Identify external sources cited (→ `paths.sources` candidates).
8. Identify incidents. Each becomes one JSONL line in `paths.incidents`. Schema in `references/incidents-format.md` (read **only if** incidents identified — progressive disclosure).
9. Surface unresolved design questions (§5 of capture file).
10. Write the session capture per `references/session-capture-format.md`.
11. Clean transcript noise per `references/transcript-cleaning-rules.md`. Apply `voice` references if non-empty; else skip.

**Emit:** `[phase1] RAN — capture at <path>; <N> decisions, <M> incidents, <K> shifts, <T> task moves`.

**Resume token.** After Phase 1 completes, update `<sessions_dir>/.current-session`:
```yaml
file: <capture filename>
session_hash: <sha256 of capture contents>
last_completed_phase: 1
```

## Phase 2 — Distribute (profile-gated)

| Profile | Phase 2 scope |
|---|---|
| `quick` (default) | Append-only subset (see below) |
| `full` | All distribution operations per `distribution-rules.md` |
| `log-only` | **Skip Phase 2 entirely.** Emit `[phase2] SKIPPED(profile=log-only)`. |
| `synapse-only` / `research-only` | Append-only subset |

**Append-only subset** (quick + synapse-only + research-only):
- New decisions → write per `distribution-rules.md::Decisions` for `dm`
- Tasks completed → write dated session block to `archives/tasks-status/YYYY-MM.md` (current month) AND remove from Pending. Tasks newly started → append to Pending. New deferred-but-keep idea → write to `inbox/ideas/`, NOT to tasks-status. Per `distribution-rules.md::paths.tasks_status`.
- New incidents → append JSONL lines to `paths.incidents`
- Build-log entry → prepend to `paths.build_log`
- New sources → append to `paths.sources` (only if file already exists)
- New conceptual shifts → prepend to `paths.evolution` (only if file already exists)
- Hard-rule changes → append to instance hard-rules file (only if changes are unambiguous)
- **Skip in append-only subset:** glossary edits, manifest classification prompt, host-entry-file maintenance, canonical-edit detection branch, meta-layer trigger walk, cross-repo writes, cross-project notifications, research-state updates.

**Full profile additionally runs:**

Glossary writes per `distribution-rules.md::Glossary` for `gm`.

**Distribution scope rule (always applies).** Distribute only project-specific findings into this project's substrate. Findings about another project, cross-cutting framework, or operator-personal infrastructure do NOT enter this project's substrate.

`paths.research_state` updates only when a Phase 1 finding actually changes conception (architectural shift, scope change, abstraction-layer change, tool-surface change). Routine work does NOT update research-state.

**Auto-load list maintenance.** If Phase 2 creates a new top-level substrate file that meets the substrate-worthy test, append its path to `acw-state.yaml::auto_load_at_session_start` via `manifest.append`. Additive only.

**Symmetric archive registration.** Detect new archive files and propose `acw-state.yaml::meta_layer` append. Scope is mode-aware:
- **tasks-status archive** (`archives/tasks-status/YYYY-MM.md`) — applies always.
- **decision-log archive** — applies only when `dm == 'single-file'` (file matching `decision_tracking.archive_pattern`). In wiki mode this is structurally moot (no rolling-window archive); skip silently.

Operator confirms before append.

**Manifest classification (conditional).** If three-layer manifest blocks present and non-empty, surface a classification prompt per new file at a tracked path. Default `instance_layer`. Skip silently if blocks absent.

**Host entry file maintenance.** Surface proposed edits to host entry files when substrate shifts that the entry file should reflect. Operator approves before the edit lands. Skip silently if no host entry files.

**Canonical-edit detection.** Compute intersection of `auto_load_at_session_start` and `template_layer`. For each canonical file edited this session (detect via `git diff --name-only HEAD` against the file's path), branch on `is_canonical_source`:
- **true:** surface version-bump prompt with push reminder
- **false/absent:** warn that local edits won't propagate

Skip silently if no canonical files edited.

**Meta-layer maintenance (conditional).** If `meta_layer` present and non-empty, walk triggers table per the canonical `instance-current-manifest.md` rules. Surface proposed edits; operator confirms.

**Cross-repo writes.** Path MUST be in `cross_repo_writes`. If not, refuse and surface the path.

**Cross-project notifications.** Drop notification at the other project's `paths.buffer_dir / YYYY-MM-DD-<source-project>-<topic-slug>.md` with `read: false`. Append-only.

**Idempotency.** Every Phase 2 write checks `<sessions_dir>/.current-session::session_hash`. If the hash matches a recent run AND `last_completed_phase >= 2`, skip writes already applied. Use content-hash dedup per substrate file (don't double-append the same decision id).

**Emit:** `[phase2] RAN — N decisions, M glossary edits, K archive registrations` or `[phase2] SKIPPED(<reason>)`.

After completion, update `.current-session::last_completed_phase: 2`.

## Phase 3 — Metabolize (profile-gated)

| Profile | Phase 3 scope |
|---|---|
| `quick`, `synapse-only`, `research-only` | Auto-update sweep only |
| `full` | Auto-update + operator-confirm proposals + consumed-prompt sweep + metabolize-report write |
| `log-only` | Skip |

**Auto-update sweep (always safe):**
- Move completed tasks `Pending` → today's `Done` block
- Mark resolved Open Questions per `metabolize-rules.md::open questions` for `dm` mode
- Consumed-prompt sweep: for each file at top level of `paths.research_queries_dir`, check for `## Findings` / `## Key Findings` heading; if present, move to `paths.research_queries_consumed_dir`

**Operator-confirm proposals (full profile only).** Collect ALL proposals into a single batch shown once at end of phase 3 — never N inline prompts:

```
[phase3] Operator review — N proposals collected:
  1. Mark idea X in inbox/ideas/ as superseded (now covered by D-CMD-NNN)
  2. Mark glossary term "Y" deprecated (no project references in 90d)
  3. Mark constraint C-003 resolved (underlying bug fixed in commit abc123)
Approve all / Approve specific (comma list) / Reject all / Edit each: ___
```

**Sonnet escalation for judgment.** Phase 3 operator-confirm proposal generation requires judgment about what's stale. The parent skill is bound to Haiku at frontmatter level; per-step model switching is not available in Claude Code. Dispatch this step to a Sonnet subagent via Task tool:

```
Agent({
  subagent_type: "session-end-judgment",
  prompt: "<bounded proposal input: list of candidates with surrounding context>. Return at most 800 tokens. Format: numbered list of proposals each with: candidate id, recommended action, rationale, confidence (high/med/low)."
})
```

Subagent definition lives at `.claude/agents/session-end-judgment.md` (`model: sonnet`). Returns bounded summary; parent renders the operator-batch.

Write the metabolize report to `paths.build_log` under the new entry per `metabolize-report-format.md`.

**Emit:** `[phase3] RAN — auto-moves: N; proposals: M (X approved); consumed prompts: K` or `[phase3] SKIPPED(profile=<name>)`.

Update `.current-session::last_completed_phase: 3`.

## Phase 4 & Phase 5 — Parallel (when both fire)

Phases 4 and 5 are DAG-parallelizable: neither depends on the other's output. When both fire (full profile, or `synapse-only`+`research-only` combination via two separate runs), invoke them in parallel via two Task tool calls in one message:

```
[Agent(synapse-log), Agent(research-prompt-builder)]  # parallel dispatch
```

If only one fires, run it directly.

### Phase 4 — Synapse session log (conditional)

| Profile | Phase 4 |
|---|---|
| `full` | Runs if `synapse_log_path` set; with `--no-synapse` flag, skip |
| `synapse-only` | Runs if `synapse_log_path` set |
| Others | Skip |

Append a session block to `<synapse_log_path>/YYYY-MM-DD.md` per `references/synapse-log-format.md`. Read that reference **only if Phase 4 actually fires** (progressive disclosure).

If `synapse_log_path` is null/absent, skip silently. **Emit:** `[phase4] RAN — appended to <path>` or `[phase4] SKIPPED(<reason>)`.

### Phase 5 — Research-prompt builder (conditional)

| Profile | Phase 5 |
|---|---|
| `full` | Asks operator: "Build research prompt now? [y/N]" — only if Track A or Track B non-empty |
| `research-only` | Runs without confirmation if Track A or Track B non-empty |
| Others | Skip |

**Emptiness gate (F-3 fix).** Before any prompt or write: check Phase 1 §5 (unresolved questions) and Phase 2-3 gap detection. If both Track A AND Track B are empty (Track C alone doesn't justify firing), emit `[phase5] SKIPPED(empty-tracks)` and exit. Do not surface the operator prompt.

**Sonnet escalation for synthesis.** Research-prompt synthesis is judgment-heavy. Dispatch to subagent:

```
Agent({
  subagent_type: "session-end-judgment",
  prompt: "<Track A inputs from Phase 1 §5> + <Track B inputs from substrate gaps>. Synthesize into a research prompt per references/research-prompt-format.md. Return at most 1500 tokens — just the artifact body with frontmatter; parent will write to file."
})
```

When fired:
1. Verify recent-session context (read last 2-3 captures if not already in context).
2. Build the artifact at `paths.research_queries_dir / YYYY-MM-DD-<topic-slug>.md`. Read `research-prompt-format.md` **only if Phase 5 fires**.
3. Pin fire-task at top of `paths.tasks_status` `section_conventions.pending` with `🔬 [FIRE AT NEXT SESSION START]`.
4. Append one-line entry to `paths.build_log` under the current session's metabolize report.

**Emit:** `[phase5] RAN — artifact at <path>` or `[phase5] SKIPPED(<reason>)`.

## Tracker cleanup (always, all profiles)

At the end of the verb, clear `<sessions_dir>/.current-session`. Write empty content; preserve the file as marker that no session is currently active. `/acw-session start` repopulates it next time.

## Output

Up to five artifacts per invocation:

1. **Session capture** — `paths.session_captures_dir / YYYY-MM-DD--<topic-slug>.md`
2. **Scaffolding edits** — targeted updates per Phase 2 rules (mode-portable)
3. **Metabolize report** — section appended to `paths.build_log`
4. **Synapse session log** *(conditional)*
5. **Research-prompt artifact** *(conditional)*

Chat reply: run banner (first line) + per-phase status lines + artifact summary in <300 words.

## When NOT to fire (verb-specific)

- Mid-session before substantive work has accumulated.
- Conversation only (no decisions, no shifts, no completions).
- Operator explicitly says "don't capture this session."
