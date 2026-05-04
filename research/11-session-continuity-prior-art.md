---
title: "Session continuity prior art — where ACW lands in the May 2026 landscape"
date: 2026-05-03
freshness_window: "2026-03-04 to 2026-05-03 (60 days)"
source_count: 95
confidence: high
researcher: deep-research skill
class: research-note
authority: operator
stability: experimental
---

# Session continuity prior art — where ACW lands in the May 2026 landscape

## Why this note exists

The operator's claim, end of Session 12: *"I figured this thing out. There is no more loading into a fresh session from scratch."* Real claim, worth pressure-testing. If the lattice + bookend + manifest pattern is genuinely novel, that's a position to defend and articulate. If others have shipped the same thing under different names, that's a pattern to absorb from. This note is the audit.

Five research lanes — Claude Code native, memory frameworks, workspace conventions, multi-instance orgs, academic/thought-leaders — all run in parallel against the freshness window. 95 sources surveyed.

---

## Key findings (lead)

1. **The "files at repo root + markdown auto-load" pattern has won.** AGENTS.md is the cross-tool entry-point standard, with 60,000+ adopting projects, Linux Foundation stewardship, and 20+ host implementations. Claude Code is the lone holdout (community uses `ln -s AGENTS.md CLAUDE.md` as the workaround). Convergence is real.

2. **Anthropic itself shipped filesystem-as-memory in April 2026.** Managed Agents `Memory Stores` are mounted as `/mnt/memory/<store>/` text directories — exactly the architectural choice ACW made. Pairs with the Memory Tool (client-side `/memories` directory, beta `memory_20250818`). Anthropic's engineering blog explicitly endorses external-artifacts-over-embedded-memory for long-running agents — *"compaction isn't sufficient."*

3. **The "bookend session" pattern (paired session-start + session-end slash commands) is rare, not novel.** [`iannuttall/claude-sessions`](https://github.com/iannuttall/claude-sessions) (1.2k stars, 1 commit) ships exactly this. ECC's `/save-session` + `/resume-session` is the same shape. Augment Code documents it as a written practice. ACW's version is structurally similar but more elaborate (five-phase metabolize, manifest-aware Phase 2, drift detection at Phase 5).

4. **The "structured markdown substrate" idea is converging on six-to-eight files at repo root.** Cline's memory bank (`projectbrief / productContext / activeContext / systemPatterns / techContext / progress`), Spec Kit's `.specify/{constitution, specs, plan, tasks}`, BMAD's project-context. ACW's substrate (`decision-log + tasks-status + glossary + incidents.jsonl + build-log + briefings/ + inbox/ + _buffer/ + context/`) is at the upper end of this spectrum and the most semantically typed.

5. **The lattice topology — full-instance federation with reference-not-duplicate — is genuinely novel in the surveyed literature.** Production patterns converge on *one canonical layer + many specialist agents reading from it via MCP* (Atlan's Context Lakehouse, MindStudio's "shared brand memory"). Nobody has shipped *one canonical instance + many full instances each with their own substrate, decisions, rules, skills*. ICLR/AAAI 2026 papers explicitly call cross-instance memory consistency *"the most pressing open challenge."*

6. **The three-layer manifest (template_layer / instance_layer / meta_layer) classifying every file is novel.** No surveyed framework uses YAML to classify workspace files into propagation tiers. Spec Kit has a template priority stack (overrides → presets → extensions → core), but it's markdown-resolution, not YAML-classification.

7. **Earn-by-incident promotion is novel as a governance discipline for workspace tooling.** Closest analogues: Cognee's "ontology evolution," Anthropic's "start simple, measure everything, add complexity only when it delivers measurable value." Nobody has codified the mechanical ritual (three documented incidents above `low` severity → promotion review).

8. **"Context engineering" has fully replaced "prompt engineering" as the term of art.** Karpathy coined it (June 2025), Anthropic formalized it (Sept 2025), LangChain made it canonical (July 2025), Gartner declared the pivot (Oct 2025), ICLR 2026 has dedicated tracks. Prompt engineering is now a sub-component.

9. **Empirical finding worth absorbing: format doesn't matter, content does.** McMillan Feb 2026 (9,649 experiments across YAML/Markdown/JSON/TOON): no significant aggregate accuracy difference. Model capability gap dominates everything. Validates ACW's plain-markdown-plus-YAML choice — the extra cleverness of fancier formats wouldn't have moved the needle.

10. **Cautionary finding: LLM-generated context files hurt performance.** ETH Zurich (covered InfoQ March 2026) — LLM-generated AGENTS.md *degraded* task success by ~3% while raising inference cost 20%+. Human-written gave only ~4% lift. Validates ACW's earn-by-incident discipline: hand-curated, decision-log-governed substrate is exactly the *"human-written, non-inferable"* content that earned the lift.

---

## The landscape, by axis

### Axis 1 — Native platform features (Claude Code itself)

Anthropic shipped a three-layer stack in late 2025 / early 2026:

| Layer | Mechanism | What it carries |
|---|---|---|
| Operator-written | `CLAUDE.md` hierarchy with `@`-imports, `.claude/rules/*.md` with `paths:` globs | Doctrine, conventions, project facts |
| Auto-captured | `MEMORY.md` in `~/.claude/projects/<project>/memory/` (v2.1.59+) | Patterns Claude decides are worth remembering, machine-local |
| Resumable transcripts | `~/.claude/projects/<project>/<session-id>.jsonl`, 30-day retention | Full conversation replay via `/resume`, `/branch`, `--from-pr` |

Plus background **Session Memory** (v2.0.64+, prominent UI v2.1.30) — pre-writes a `summary.md` every ~5K tokens to make `/compact` instant. Plus **`/recap`** in v2.1.108. Plus the API-side **Memory Tool** (`memory_20250818`) and Managed Agents **Memory Stores** (beta `managed-agents-2026-04-01`, 100KB per memory, 8 stores per session, immutable versioned writes, optimistic concurrency via `content_sha256`).

ACW sits cleanly on top of all of these. Specifically:
- ACW's `auto_load_at_session_start` block in `acw-state.yaml` is the host-agnostic abstraction; Claude Code's `@`-imports inside `CLAUDE.md` are the host implementation per AGENTS.md directive 7.
- ACW substrate (decision-log, tasks-status, glossary) lives in git, not in `~/.claude/projects/.../memory/` — operator-readable, version-controlled, lattice-coordinable. Auto-memory is the unstructured complement, not a substitute.
- ACW's bookend skills run *above* `/resume` and `/compact`, not in place of them.

**Gap analysis** (where Anthropic doesn't have a first-party answer):

| Concern | Anthropic native | ACW |
|---|---|---|
| Structured decision history | None | `decisions/decision-log.md` with frontmatter, append-only, IDs, rationale |
| Pending/done/parked task tracker | None | `tasks-status.md` three-section, dated session blocks |
| Cross-session glossary/canon | None (vocabulary drifts) | `glossary.md` + `rules/canon.yaml` state machine, lint |
| Incident/learning ledger | Auto-memory captures ad hoc | `incidents.jsonl` with category enum, severity, earn-by-incident promotion |
| Bookend session lifecycle | `/resume` only — asymmetric | Paired `start`/`end` skills, five-phase metabolize |
| Multi-instance topology | Single workspace, no cross-instance | Lattice with `_buffer/`, divergence markers, absorption candidates |
| Substrate manifest discipline | CLAUDE.md hierarchy | Three-layer (template/instance/meta) classification, scaffold-time enforcement |
| Operator-vs-system separation | None | `inbox/` (operator) vs `_buffer/` (system) vs `briefings/` (agent) |

### Axis 2 — Memory-as-a-service products

Three architectural camps, two heavyweight benchmark events redrawing the map:

| Camp | Architecture | Representatives | 2026 status |
|---|---|---|---|
| Files-as-memory | Plain markdown ± lightweight index | Anthropic Managed Agents memory, Letta filesystem variant, Basic Memory, ACW | Resurgent — endorsed by Letta benchmark (Aug 2025: 74.0% LoCoMo with files vs 68.5% mem0 graph), validated by Anthropic shipping filesystem in April 2026 |
| Vector-primary | Embeddings + similarity search | mem0 v2.0.0 (graph removed!), OpenMemory MCP, RAG baselines | Mem0 retreated from graph in v2.0.0; positions selective vector as production default |
| Graph-primary | Temporal knowledge graphs | Graphiti (v0.29.0), Zep, Cognee (graph+vector hybrid v1.0.5 May 3) | Wins on relationship-heavy queries; loses on cost/latency |

Coding-agent specific: **Serena** (LSP-driven semantic code retrieval, v1.2.0 Apr 27 2026), **OpenMemory MCP** (explicitly branded "AI Memory MCP Server for Coding Agents"), **Claude Code memory** itself.

**The honest 2026 synthesis:** *Files for capable agents with good search tools; vectors for cheap latency-critical recall; graphs when the domain is genuinely relational and temporal.* ACW sits squarely in camp 1, and that camp gained heavyweight legitimacy this quarter from Anthropic itself.

**Almost nobody ships an explicit bookend ritual.** The dominant pattern is "tool-call driven" — agent reads memory when it needs to, writes when it wants to. Closest analogues:
- Cognee's two-layer split (session memory + permanent memory) — architectural cousin
- LangGraph's `thread_id` — durable handle, no enforced ritual
- Anthropic Auto Dream — end-of-session-ish, but background, not explicit
- Basic Memory users do it manually with phrases like *"Look at <topic> for context..."*

ACW's `/acw-session start|end` is structurally distinctive in this landscape.

### Axis 3 — Workspace conventions (other coding agents)

The pattern lattice as of May 2026:

| Tool | Workspace convention | Bookend? | Notable |
|---|---|---|---|
| **Cline / Roo Code** | `memory-bank/` with six fixed files; `.clinerules` learning journal | Cold-start magic phrase ("follow your custom instructions"); no end | Most-copied "fixed-set-of-markdown-files" pattern; Roo Code shutting down May 15 2026 |
| **Cursor** | `.cursor/rules/*.mdc` with frontmatter (`alwaysApply`, `globs`) + auto-generated "Memories" | None | Five-level rules system; explicitly recommends AGENTS.md as simpler alternative |
| **Windsurf** | Cascade Memories (auto, not git) + `.windsurf/rules/*.md` | None | Cognition acquired Codeium ~$250M Dec 2025 |
| **Aider** | `CONVENTIONS.md` + repo-map; `.aider.conf.yml::read:` for persistent loading | None | Chat history at `.aider.chat.history.md` |
| **Continue.dev** | `.continue/rules/` (markdown, hierarchical) | None | MCP server support |
| **GitHub Copilot** | `.github/copilot-instructions.md` | None | Custom instructions feature |
| **iannuttall/claude-sessions** | `sessions/[YYYY-MM-DD-HHMM-name].md` files | YES — `/project:session-start`, `/project:session-update`, `/project:session-end` | 1.2k stars on 1 commit — clearly answering felt need |
| **Anthropic's own engineering pattern** | Two-agent: initializer creates `init.sh`, `claude-progress.txt`, baseline git commit; coding agent reads | Implicit | "Effective Harnesses" essay; reads exactly like a stripped-down ACW |
| **mainbranch.dev (Agent Context System)** | `AGENTS.md` (capped 120 lines) + `MEMORY.md` (capped 200 lines / 25KB) + `memory/` daily logs | Implicit start (read both); end (reflect, log, suggest promotion) | "git for agent memory"; closest spiritual cousin to ACW bookend |
| **BMAD-METHOD v6.6.0** | Phased agents (PM, Architect, Developer); `project-context.md` as constitution | None | "Ralph loop" autonomous mode |
| **GitHub Spec Kit v0.8.4** | `.specify/{memory/constitution.md, specs/, templates/, extensions/}` | None | 71K stars; six-stage workflow; risk: 8 files / 1300+ lines for one feature |
| **Augment Code** | Documented practice (no tool): 5-min end-of-session ritual appending DEC-XXX, CONSTRAINT-XXX, Q-XXX entries | YES — written practice | April 2026 — explicit "session-end spec update" |
| **AgDR** (agent-decision-record) | `docs/agdr/` Y-statement format | None | ADR-for-agents; multi-tool |
| **SpecStory** | `.specstory/history/` auto-captured chats | None | More archival than active |

**Observations:**
- The "files at repo root + magic phrase to load them" pattern is widespread.
- The structured *typed* substrate (decision-log + tasks + glossary + incidents as separate files with separate disciplines) is rare; closest is Spec Kit but it's workflow-shaped, not lifecycle-shaped.
- Constitution-style governance file is converging: ACW's `instance-hard-rules.md` ↔ Spec Kit's `constitution.md` ↔ BMAD's `project-context.md`.
- Three-surface separation (`inbox/` operator + `_buffer/` system + `briefings/` agent-generated) is not seen elsewhere.

### Axis 4 — Multi-instance / multi-agent organization

The lattice topology is the most under-developed axis in the field. Survey results:

| Approach | Architecture | Lattice match |
|---|---|---|
| Devin (Cognition) | Parent Devin spawns managed Devins in isolated VMs; reads child trajectories after the fact | Closest "instance spawns full instances" shape, but no canonical-knowledge layer between |
| AutoGen / AG2 | GroupChat — agents share one conversation; selector decides who speaks | Single-conversation paradigm; no lattice |
| CrewAI | Hierarchical process; manager dispatches; "Cognitive Memory" with scopes (`/project/alpha`, `/agent/researcher`) | Scope hierarchy gestures at canonical-vs-specialized, but it's namespacing in one store |
| MetaGPT | "Code = SOP(Team)"; shared message pool, role-based subscription | SOPs as artifacts ≈ ACW's `rules/`, but no persistence across runs |
| ChatDev | Chat chain + dual-agent role pairs; phase-bounded memory | Run-bounded; no cross-run canon |
| Claude Code subagents | Each subagent isolated: own context, own tool list; only final message returns | Task isolation within session, not instance federation |
| Anthropic multi-agent research | Lead saves plan to "Memory" before spawning; subagents store work externally, return *lightweight references* | **Closest published reference-not-duplicate at intra-session scale** |
| Magentic-One/Magentic-UI | Lead Orchestrator with task ledger + progress ledger; SQLite session state | Dual-ledger ≈ ACW decisions/ + tasks-status, but intra-session |
| OpenAI Swarm/Agents SDK | Agents + handoffs (`transfer_to_X` function); stateless between calls | None |
| Google ADK + A2A protocol | A2A is wire-protocol layer (JSON-RPC, Agent Cards, signed cards, `referenceTaskIds`); deliberately opaque about state | **The wire layer the lattice could ride on once cross-instance writes earn their build** |
| Atlan Context Lakehouse | Shared, governed context layer; all agents query via MCP; "update once, all agents see new version" | **Closest production pattern — but one canonical layer + many specialist agents, NOT one canonical instance + many full instances** |
| Skan AOW | Industry-standard agent ontology proposal | Vocabulary standardization, not topology |
| MindStudio "Four Patterns" | Fresh Context / Shared Brand Memory / Skill Collaboration / Self-Learning | Same as Atlan: shared layer + specialist agents |

**Academic landscape:**
- arXiv 2603.10062 (March 2026): names "multi-agent memory consistency" as *the most pressing open challenge*. Distinguishes shared-memory paradigms vs distributed-memory paradigms.
- arXiv 2602.05665: distinguishes **Knowledge Memory** (passive, static, objective, shared — *"internal reference library"*) from **Experience Memory** (personal logbook, dynamic, context-specific). **This is the cleanest theoretical grounding for ACW's canonical-vs-departmental decomposition.**
- arXiv 2505.18279 (Collaborative Memory): bipartite access graphs, provenance-tagged fragments, reference-based access (no duplication). Two-tier (private + shared) — *not* three-tier.

**Verdict:** The "each node is a full ACW with its own substrate that references org-brain canon" claim does not have a published analog in May 2026. It's whitespace.

### Axis 5 — Academic and thought-leader consensus

The settled vocabulary:
- "Context engineering" has fully replaced "prompt engineering" (Karpathy June 2025; Anthropic Sept 29 2025; LangChain July 2025; Gartner Oct 2025).
- LangChain's four-strategy taxonomy (**write / select / compress / isolate**) has won as field lingua franca.
- Anthropic's variant maps cleanly: just-in-time retrieval, compaction, structured note-taking, sub-agents.

The settled empirical findings:
- "Context rot" — degradation as token count grows — is real and measurable.
- Format doesn't matter at aggregate (McMillan Feb 2026, 9,649 experiments).
- LLM-generated context files hurt performance (ETH Zurich, March 2026).
- Files-as-memory wins on capable agents (Letta benchmark, Aug 2025; Anthropic Managed Agents shipping filesystem April 2026).

The unsettled questions:
- No standardized session-resume protocol (Liu et al. April 2026 explicitly: *"session-scoped permissions are not restored on resume or fork"*).
- No benchmark for "resume real workspace after weeks, pick up where you left off" — current benchmarks measure long-context recall (LOCOMO, Context-Bench) or single-session degradation (SlopCodeBench, SWE-EVO), not cross-session operator continuity.
- Cross-instance memory consistency remains *"the most pressing open challenge"* (arXiv 2603.10062).

The closest articulations of "the workspace IS the agent's memory":
- **Tim Kellogg** (Apr 27 2026) — three patterns: **Files / Memory Blocks / Skills**. Endorses filesystem-as-memory; recommends Bash + Git versioning. Closest practitioner statement.
- **Van Clief & McDermott** (Mar 2026, arXiv 2603.16021) — **Model Workspace Protocol**: filesystem structure REPLACES framework orchestration. Numbered folders as workflow stages, markdown as prompts, scripts for mechanical work. Closest academic statement; grounded in Unix pipeline principles.
- **OpenViking** — "context database with a filesystem paradigm," L0/L1/L2 tiered loading.
- **Anthropic Memory Tool docs** — *"workspace-scoped collection of text documents... mounted as a directory inside the session's container"* — Anthropic itself shipping the workspace-as-memory thesis as product.

---

## Where ACW lands — the honest scorecard

### On-trend (validated)

| ACW move | Field consensus | Evidence |
|---|---|---|
| Markdown-first substrate at repo root | Universal | AGENTS.md adoption (60k+ projects), Cline, Spec Kit, BMAD, Aider, Continue, etc. |
| Files over vector/graph for capable agents | Resurgent | Letta benchmark Aug 2025; Anthropic Managed Agents April 2026; Tim Kellogg April 2026 |
| AGENTS.md directive 7 (host-agnostic auto-load) | Settled standard | Linux Foundation steward; 20+ implementing hosts |
| Decision log discipline | Emerging | AgDR, Augment Code session-end spec-update, ADR convention |
| Skills as folders with SKILL.md frontmatter | Settled | Anthropic Skills repo (128k stars) is the canonical spec |
| Constitution-style governance file | Emerging | Spec Kit `constitution.md` (May 1 2026); BMAD `project-context.md` |
| Bookend session ritual | Rare-but-real | iannuttall/claude-sessions (1.2k stars); ECC; Augment Code; mainbranch.dev |
| Hand-curated, non-LLM-generated substrate | Validated empirically | ETH Zurich March 2026 study; HumanLayer guidance |
| Plain markdown + YAML choice | Validated empirically | McMillan Feb 2026 — format doesn't matter at aggregate |

### Distinctive (genuinely novel in surveyed literature)

| ACW move | Why it's whitespace |
|---|---|
| Three-layer manifest (template/instance/meta) classifying every file | No surveyed framework uses YAML to classify workspace files into propagation tiers. Closest: Spec Kit's template priority stack — but markdown-resolution, not YAML-classification. |
| `is_canonical_source` flag separating publisher from consumer instances | Not seen elsewhere. |
| Multi-instance lattice with full-instance federation | Production patterns are *one canonical layer + many specialist agents*. ACW's *one canonical instance + many full instances each with their own substrate* has no published analog. |
| `_buffer/` cross-repo notification + absorption candidates | A2A protocol is the wire layer that doesn't exist; no application-layer standard. arXiv 2603.10062 names this gap *the most pressing open challenge*. |
| Earn-by-incident promotion ritual | No surveyed framework codifies the mechanical ritual (3 incidents > `low` severity → promotion). Closest: Cognee's "ontology evolution" framing. |
| Recursive instances (template that hosts a template) | Not seen elsewhere. Devin's manage-Devin spawns isolated VMs; doesn't propagate canon. |
| Three-surface separation (`inbox/` operator + `_buffer/` system + `briefings/` agent-generated) | Not seen. Spec Kit has per-feature directories — workflow-shaped, not lifecycle-shaped. |
| Bookend skills with five-phase metabolize (Phase 2 manifest classification, Phase 5 drift detection) | iannuttall and ECC ship simple bookends; ACW's metabolize phases are more elaborate. |

### Behind / could borrow

| Field move | Why ACW should consider |
|---|---|
| Anthropic's two-agent harness pattern (initializer + coder) | Validates ACW shape; consider citing the engineering essay as external grounding for the bookend rule |
| LOCOMO / Context-Bench / SlopCodeBench / SWE-EVO benchmarks | Eval methodology gap. The *"resume real workspace after weeks"* benchmark doesn't exist yet — ACW could define it. |
| A2A protocol (v1.2 Linux Foundation) | The wire-protocol layer for cross-instance handoffs. Watch this; could replace ad-hoc `_buffer/` writes when cross-instance writes earn the broker's build. |
| arXiv 2602.05665 Knowledge Memory vs Experience Memory split | Cleanest theoretical grounding for ACW's canonical-vs-departmental decomposition. Cite in `research/10-multi-instance-topology.md`. |
| Cline's six-file fixed substrate + "magic phrase" cold-start | Useful framing for explaining ACW's auto-load to newcomers; "ACW = memory bank with governance" is a one-line elevator pitch. |
| Spec Kit's `.specify/` directory hierarchy | Single-folder substrate envelope is simpler than ACW's root-level sprawl. Consider whether ACW's substrate should consolidate under `.acw/` (likely no — git-readability matters more — but worth thinking about). |
| Tim Kellogg's "Files / Memory Blocks / Skills" three-pattern taxonomy | Useful external citation. ACW's substrate is "Files"; ACW skills are "Skills"; ACW could consider whether "Memory Blocks" (Letta-style) earn an ACW slot — probably not, but worth a `DEFERRED.md` row. |

---

## Conflicts & uncertainties

1. **Mem0 vs Letta vs Anthropic on file-vs-vector.** Mem0's "State of AI Agent Memory 2026" (May 1 2026) advocates selective vector memory as production default and explicitly positions file-based memory as obsolete. Letta's August 2025 LoCoMo benchmark (74.0% files vs 68.5% mem0 graph) and Anthropic's April 2026 filesystem choice contradict that framing. Mem0 has commercial interest in the vector framing. Honest reading: files for capable agents, vectors for cheap latency-critical recall — the question is decided by what the agent does, not by a one-size winner. **ACW's choice (files) is well-validated for capable-agent workloads.**

2. **AGENTS.md adoption: Anthropic's stance.** Anthropic explicitly recommends `@AGENTS.md` import inside CLAUDE.md rather than reading AGENTS.md natively. Hivetrail (April 2026) characterizes Claude Code as the lone holdout among major hosts. GitHub issue #6235 has thousands of upvotes; no Anthropic timeline. **Watch.** ACW's host-agnostic AGENTS.md directive 7 is forward-compatible either way.

3. **ETH Zurich finding vs HumanLayer guidance.** Both agree LLM-generated context files don't help; Zurich measured a 3% degradation, HumanLayer says "never auto-generate." ACW's earn-by-incident discipline is consistent with both. *Worth flagging in `rules/instance-hard-rules.md` if not already there: substrate edits should be human-curated or decision-log-governed, not LLM-generated wholesale.*

4. **Roo Code shutdown May 15 2026.** Migration to Kilo Code. Doesn't affect ACW directly but is a signal: workspace-rule frameworks consolidate fast. The AGENTS.md spec is more durable than any one host.

5. **Amazon Q Developer end-of-support May 15 2026.** Migration path to Kiro. Same signal.

6. **Substrate bloat warning.** HumanLayer's CLAUDE.md guidance: "<300 lines, progressive disclosure." ACW's `auto_load_at_session_start` currently lists 7 files. With imports each can be many hundred lines. **Pressure to monitor:** the ETH Zurich finding suggests context-file size has measurable cost. ACW's Phase 2 host-entry-file maintenance is the right place to watch this; consider adding a soft size budget to `rules/instance-current-manifest.md` for the auto-load set.

7. **The lattice claim is not yet incident-tested.** ACW's `rules/multi-instance-topology.md` is *experimental, not normative*. The closest field validation is "academic papers say this is the open challenge" — that's grounding, not proof. The lattice earns its build only at lattice scale (multi-instance dogfood evidence). Until then, the claim is "we have a thoughtful design for an unsolved problem," not "we shipped a solution."

---

## Recommendations

### Borrow now (small, cheap, validated)

1. **Add Tim Kellogg's "Files / Memory Blocks / Skills" three-pattern taxonomy as a citation in `rules/manifest-discipline.md`.** It's the cleanest practitioner articulation; gives newcomers a one-paragraph orientation.
2. **Cite the Anthropic "Effective Harnesses for Long-Running Agents" essay in `skills/acw-session/SKILL.md` as external validation of the bookend pattern.** Anthropic's own recommended pattern reads exactly like a stripped-down ACW.
3. **Cite arXiv 2602.05665 (Knowledge Memory vs Experience Memory) in `research/10-multi-instance-topology.md`.** Cleanest theoretical grounding for the canonical-vs-departmental decomposition.
4. **Add a `DEFERRED.md` row for "substrate-size budget."** Activation trigger: three sessions where auto-load context burns more than 30% of context window before useful work starts. Prevention: soft size budget in `rules/instance-current-manifest.md` for the auto-load set.

### Watch (signals worth tracking)

1. **A2A protocol v1.2 maturation.** When cross-instance writes earn the capability broker's build, A2A is the wire layer to ride on top of. Bookmark: https://a2a-protocol.org/latest/specification/
2. **Anthropic Managed Agents Memory Stores adoption.** ACW's choice to keep substrate in git rather than in Memory Stores is correct for git-readable, lattice-coordinable substrate. But Memory Stores' 100KB / 8-store / immutable-versioned-write contract is the closest first-party pattern; if it adds features (richer metadata, multi-store cross-references), ACW should consider adapter glue.
3. **"Resume real workspace after weeks, pick up where you left off" benchmark.** Doesn't exist. If ACW continues to mature, defining this benchmark is a publishable contribution. Adjacent to LOCOMO/Context-Bench; distinct from SlopCodeBench/SWE-EVO. Could be written as a `research/NN-*` note.
4. **Mem0 v2.x trajectory.** They removed graph in v2.0.0 (April 2026) — meaningful retreat. If they continue retreating toward simpler primitives, "selective vector + filesystem" may emerge as a hybrid consensus.
5. **The `.agent/` directory proposal in AGENTS.md repo (open issue #71).** Directly adjacent to ACW's territory. If accepted, ACW's substrate could ride a standardized envelope rather than scattering at root.

### Hold (don't borrow yet — wait for incident)

1. **Vector or graph indexing of substrate.** The Letta benchmark + ETH Zurich finding + format-doesn't-matter-at-aggregate study all point the same way: files + good search + hand-curation beats clever indexing for capable agents. Don't add complexity here without an incident showing the substrate has grown past navigability.
2. **Memory Blocks (Letta-style hierarchical core/recall/archival).** Different design philosophy (agent self-edits memory blocks). ACW's "operator owns the substrate; agents read it" is a different bet. Don't pivot without evidence that the operator-owned approach hits a ceiling.
3. **`.acw/` envelope consolidation.** Spec Kit's `.specify/` is simpler at root; ACW's root-level sprawl (`decisions/`, `rules/`, `research/`, `briefings/`, `inbox/`, `_buffer/`, `context/`, root-level scalars) is more git-readable but does add visual noise. Hold; revisit if the sprawl ever causes a real friction incident.

### Articulate (write it down before someone else does)

The lattice + manifest + earn-by-incident bundle is genuinely novel in the surveyed literature. The strongest case for writing this up externally:

- **A "workspace contract" framing essay.** Position: "the workspace IS the agent's memory" + "the workspace is governed substrate, not just content" + "the workspace is recursive (instance + template)." Cite: Tim Kellogg (Files), Van Clief & McDermott (MWP), Anthropic Managed Agents (filesystem), arXiv 2603.10062 (the open challenge), arXiv 2602.05665 (Knowledge vs Experience). Differentiate from: Cline memory bank (no governance), Spec Kit (no manifest), Atlan (one layer + specialist agents, not federation).

- **A "session continuity benchmark" proposal.** "After N weeks of inactivity, can the operator resume the workspace and reach productive work in M minutes / K context tokens?" Standardized scenarios: small bug fix, multi-step refactor, new feature in unfamiliar subsystem. Distinct from existing benchmarks. Could be the publishable contribution that grounds ACW in the literature.

The honest answer to *"have I figured this thing out?"*: **You've figured out a real piece of it. The pieces you've shipped sit at, ahead of, or in genuine whitespace relative to the May 2026 field. The lattice is the most ambitious bet and it's not yet incident-tested at scale. The bookend pattern + structured substrate + manifest discipline together — yes, that bundle is real, and it's better than the dominant alternatives. Write it down before someone else does.**

---

## Source list (selected — full lane reports retained in conversation history)

### T1 — Anthropic, official platform

| # | URL | Date | Topic |
|---|---|---|---|
| 1 | https://code.claude.com/docs/en/memory | Current (v2.1.59+) | CLAUDE.md hierarchy + auto-memory |
| 2 | https://code.claude.com/docs/en/sessions | Current | `/resume`, `/branch`, JSONL transcripts |
| 3 | https://code.claude.com/docs/en/how-claude-code-works | Current | Agentic loop, compaction |
| 4 | https://code.claude.com/docs/en/agent-sdk/overview | Current (Opus 4.7) | Claude Agent SDK sessions |
| 5 | https://platform.claude.com/docs/en/managed-agents/memory | Beta `managed-agents-2026-04-01` | Memory Stores |
| 6 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | `memory_20250818` | Memory Tool client-side spec |
| 7 | https://www.anthropic.com/engineering/managed-agents | 2026-04-08 | Brain/hands/session decoupling |
| 8 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | Two-agent pattern; *"compaction isn't sufficient"* |
| 9 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | Anthropic's official position |
| 10 | https://www.anthropic.com/research/building-effective-agents | Current | Six patterns for agent design |
| 11 | https://www.anthropic.com/engineering/multi-agent-research-system | Current | Lightweight references in subagent design |

### T1 — Standards bodies

| # | URL | Date | Topic |
|---|---|---|---|
| 12 | https://agents.md/ | © 2026; no formal version | AGENTS.md spec |
| 13 | https://github.com/agentsmd/agents.md | 35 commits | Repo-level spec status |
| 14 | https://a2a-protocol.org/latest/specification/ | v1.2 (Linux Foundation 2026) | Agent-to-agent wire protocol |
| 15 | https://github.com/a2aproject/A2A | Active | A2A repo |

### T2 — Academic papers

| # | URL | Date | Topic |
|---|---|---|---|
| 16 | https://arxiv.org/abs/2512.13564 | 2025-12-15 / rev 2026-01-13 | Memory in the Age of AI Agents (46 co-authors) |
| 17 | https://arxiv.org/abs/2603.07670 | 2026-03-08 | Memory for Autonomous LLM Agents |
| 18 | https://arxiv.org/abs/2510.04618 | 2025-10-06 (ICLR 2026) | Agentic Context Engineering |
| 19 | https://arxiv.org/abs/2510.21413 | 2025-10-24 / rev 2026-02-05 | AGENTS.md in OSS (466-project study) |
| 20 | https://arxiv.org/abs/2602.05447 | 2026-02-05 | Structured Context Engineering (9,649 experiments) |
| 21 | https://arxiv.org/html/2603.16021v1 | 2026-03 | Model Workspace Protocol (folder-as-architecture) |
| 22 | https://arxiv.org/html/2604.14228v1 | 2026-04 | Liu et al. — Claude Code architecture analysis |
| 23 | https://arxiv.org/abs/2604.25850 | 2026-04 | Agentic Harness Engineering |
| 24 | https://arxiv.org/abs/2603.28052 | 2026-03 | Meta-Harness optimization |
| 25 | https://arxiv.org/abs/2603.10062 | 2026-03 | Multi-Agent Memory from Computer Architecture (the open-challenge paper) |
| 26 | https://arxiv.org/html/2602.05665v1 | 2026-02 | Graph-based Agent Memory — Knowledge vs Experience |
| 27 | https://arxiv.org/html/2505.18279v1 | 2025-05 | Collaborative Memory (provenance-filtered shared store) |
| 28 | https://github.com/Gen-Verse/LatentMAS | ICML 2026 Spotlight | KV-cache cross-agent state sharing |

### T3 — Major frameworks / products

| # | URL | Date | Topic |
|---|---|---|---|
| 29 | https://github.com/letta-ai/letta | v0.16.7 (2026-03-31) | Hierarchical memory; filesystem benchmark |
| 30 | https://www.letta.com/blog/benchmarking-ai-agent-memory | 2025-08 | "Is a filesystem all you need?" — 74.0% LoCoMo |
| 31 | https://github.com/mem0ai/mem0 | v2.0.0 (2026-04-16) | Vector + entity-linking; graph removed |
| 32 | https://mem0.ai/openmemory | 2025-06 | OpenMemory MCP — coding-agent specific |
| 33 | https://mem0.ai/blog/state-of-ai-agent-memory-2026 | 2026-05-01 | "Selective vector as production default" |
| 34 | https://www.getzep.com/product/open-source/ | Active | Zep + Graphiti |
| 35 | https://github.com/getzep/graphiti | v0.29.0 (2026-04-27) | Temporal knowledge graph |
| 36 | https://www.cognee.ai/ | v1.0.5 (2026-05-03) | Hybrid graph+vector+relational |
| 37 | https://github.com/topoteretes/cognee | Active | Cognee repo |
| 38 | https://github.com/basicmachines-co/basic-memory | v0.20.3 (2026-03-27) | Markdown + SQLite + FastEmbed |
| 39 | https://github.com/oraios/serena | v1.2.0 (2026-04-27) | LSP-driven semantic code retrieval |
| 40 | https://docs.langchain.com/oss/python/langgraph/persistence | Active 2026 | LangGraph thread checkpointing |

### T3 — Workspace conventions / coding agents

| # | URL | Date | Topic |
|---|---|---|---|
| 41 | https://docs.cline.bot/features/memory-bank | Active | Six-file memory bank pattern |
| 42 | https://github.com/iannuttall/claude-sessions | 1.2k stars | True bookend slash commands |
| 43 | https://github.com/Wirasm/PRPs-agentic-eng | 79 commits | PRP workflow + Ralph loop |
| 44 | https://agents.mainbranch.dev/ | Active | "git for agent memory" — closest spiritual cousin |
| 45 | https://github.com/me2resh/agent-decision-record | Active | AgDR — ADR-for-agents |
| 46 | https://github.com/specstoryai/agent-skills | Active | SpecStory chat-history archival |
| 47 | https://github.com/anthropics/skills | 128k stars | SKILL.md template + spec |
| 48 | https://github.com/bmad-code-org/BMAD-METHOD | v6.6.0 (2026-04-29) | BMAD planning + dev workflow |
| 49 | https://github.com/github/spec-kit | v0.8.4 (2026-05-01) | Spec Kit — `.specify/` envelope |
| 50 | https://github.com/affaan-m/everything-claude-code | Active | ECC — `/save-session` + `/resume-session` |
| 51 | https://cursor.com/docs/rules | Current | Cursor five-level rules |
| 52 | https://docs.windsurf.com/windsurf/cascade/memories | Current | Windsurf Cascade Memories |
| 53 | https://docs.roocode.com/features/custom-modes | Shutdown 2026-05-15 | Roo Code (migrating to Kilo Code) |
| 54 | https://docs.continue.dev/customize/deep-dives/rules | Current | Continue rules |
| 55 | https://aider.chat/docs/faq.html | Current | Aider conventions + repo-map |
| 56 | https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot | Current | GitHub Copilot custom instructions |

### T3 — Practitioner thought-leadership

| # | URL | Date | Topic |
|---|---|---|---|
| 57 | https://timkellogg.me/blog/2026/04/27/memory-patterns | 2026-04-27 | Three patterns: Files / Memory Blocks / Skills |
| 58 | https://www.humanlayer.dev/blog/writing-a-good-claude-md | 2025-11-25 | "<300 lines, progressive disclosure, never auto-generate" |
| 59 | https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html | 2026-02-05 | Martin Fowler on context engineering |
| 60 | https://www.augmentcode.com/guides/session-end-spec-update-ai-agents | 2026-04-08 | Session-end spec update practice |
| 61 | https://www.langchain.com/blog/context-engineering-for-agents | 2025-07-02 | Four-strategy taxonomy (write/select/compress/isolate) |
| 62 | https://hamel.dev/blog/posts/evals-skills/ | 2026-03-02 | "Infrastructure around the agent matters more than the model" |
| 63 | https://addyo.substack.com/p/context-engineering-bringing-engineering | 2025-07-13 | Context engineering manifesto |
| 64 | https://x.com/karpathy/status/1937902205765607626 | 2025-06 | Karpathy coinage |
| 65 | https://github.com/davidkimai/Context-Engineering | Active | Karpathy-inspired handbook |
| 66 | https://atlan.com/know/multi-agent-system-orchestration/ | 2026 | Context Lakehouse — closest production lattice cousin |
| 67 | https://www.skan.ai/whitepapers/agentic-ontology-of-work | 2026 | AOW — industry vocabulary proposal |
| 68 | https://www.mindstudio.ai/blog/agentic-os-architecture-four-patterns-claude-code | 2026 | Four-pattern architecture |
| 69 | https://ossinsight.io/blog/agent-memory-race-2026 | 2026-04-13 | "No consensus on where memory belongs" |

### T3 — Multi-agent organizations

| # | URL | Date | Topic |
|---|---|---|---|
| 70 | https://cognition.ai/blog/devin-can-now-manage-devins | 2026 | Devin spawning Devins |
| 71 | https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin | Current | Devin notes-files persistence |
| 72 | https://github.com/ag2ai/ag2 | Active | AG2 (AutoGen fork) |
| 73 | https://docs.crewai.com/en/concepts/memory | Current | CrewAI memory + scope hierarchy |
| 74 | https://github.com/FoundationAgents/MetaGPT | Active | MetaGPT SOPs |
| 75 | https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/ | 2026 | Magentic-One dual-ledger |
| 76 | https://github.com/openai/swarm | Archived (superseded) | OpenAI Swarm handoffs |
| 77 | https://openai.github.io/openai-agents-python/ | Active | OpenAI Agents SDK |
| 78 | https://adk.dev/ | 2026 | Google ADK |
| 79 | https://code.claude.com/docs/en/sub-agents | Current | Claude Code subagent isolation |

### T3 — Background / context

| # | URL | Date | Topic |
|---|---|---|---|
| 80 | https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ | 2025-11-19 | 2,500+ AGENTS.md analysis |
| 81 | https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard | 2026-04 | Cross-tool standard analysis |
| 82 | https://www.infoq.com/news/2026/03/agents-context-file-value-review/ | 2026-03 | ETH Zurich study coverage |
| 83 | https://www.augmentcode.com/guides/how-to-build-agents-md | 2026 | AGENTS.md construction guide |
| 84 | https://www.morphllm.com/spec-driven-development | 2026-03-04 | Spec-driven development guide |
| 85 | https://claudefa.st/blog/guide/mechanics/session-memory | 2026 | Session Memory mechanics deep-dive |
| 86 | https://claudefa.st/blog/guide/changelog | 2026 (v2.1.108–v2.1.111) | Claude Code changelog |
| 87 | https://www.testingcatalog.com/anthropic-launches-memory-in-claude-agents-for-enterprise/ | 2026-04-23 | Managed Agents memory launch |
| 88 | https://www.macrumors.com/2026/03/02/anthropic-memory-import-tool/ | 2026-03-02 | Free-tier memory + import tool |
| 89 | https://www.spheron.network/blog/agent-memory-gpu-cloud-mem0-zep-guide/ | 2026 | mem0/Zep architecture guide |
| 90 | https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9 | 2026 | Memory-files comprehensive guide |
| 91 | https://www.taskade.com/blog/agentic-workspaces | 2026 | Workspace-as-governance-container framing |
| 92 | https://simonw.substack.com/p/i-think-agent-may-finally-have-a | 2025-09-18 | Simon Willison agent definition |
| 93 | https://developers.openai.com/cookbook/examples/orchestrating_agents | Current | Orchestrating Agents cookbook |
| 94 | https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/magentic | Current | Magentic in Semantic Kernel |
| 95 | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | 2026 | A2A announcement |

---

## Provenance

Five parallel research lanes, each spawned as a `general-purpose` subagent with bounded scope. Every claim in this note traces to one of the 95 sources above; the full lane reports remain in the parent session's conversation history if cross-checking is needed. Freshness window 2026-03-04 to 2026-05-03 enforced for "current state" claims; foundational architecture and academic papers from earlier dates retained where load-bearing for the comparison.
