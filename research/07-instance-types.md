---
class: reference
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# 07 — Instance Types

How to determine what kind of ACW instance a workspace needs and what primitives apply at each level. This file exists so that an agent can reason about "does this workspace need X?" for any future question, not just at bootstrap time.

## The classification question

Every folder, project, or system that an operator considers bringing under ACW discipline falls into one of four types. The type determines which ACW primitives apply.

## Type 1 — Full instance

**Definition:** A workspace that accumulates state across sessions. Knowledge is created, vocabulary is used, assets persist, skills produce output that other skills consume. The thing that was true last Tuesday might not be true today. Drift is a real risk.

**Signals:**
- Multiple skills that read and write to the same knowledge base
- Vocabulary used across multiple files or by multiple agents
- Assets that need to stay current (SOPs, glossaries, org charts, procedures)
- More than one author or agent contributing content
- A canon or glossary that could drift

**What applies:** Everything. Full ACW hygiene: glossary, incidents.jsonl, instance-hard-rules.md, decision-log, research scaffolding (research-state.yaml, evolution.md, sessions/), skill-format contract, frontmatter headers on all files. Canon governance and deferred library primitives activate per earn-by-incident when the instance's scale demands them.

**Examples:** An org brain (gsg-brain), a consultancy knowledge base (frank-context), a personal workspace with rules and skills and research (synapse).

## Type 2 — Cockpit

**Definition:** A session-scoped operator console that reads from and writes to other systems but accumulates minimal state of its own. It has pointers, controls (MCPs), and skills that operate on external surfaces. The cockpit itself produces nothing that persists between sessions — all knowledge goes to other instances, all logs go to other instances, all content goes to other instances.

**Signals:**
- Skills that read from MCPs and write to external systems, not to local files
- Context files that are pointers or cached summaries, not original content
- No vocabulary to drift because the cockpit borrows vocabulary from the instances it operates on
- Session-scoped work — what happens in the cockpit is logged elsewhere

**What applies:** Universal hygiene only.
- Role declarations on all skills (the one-role contract is universal)
- Frontmatter headers on all files (trust-drift prevention is universal)
- incidents.jsonl (incident tracking is universal — even cockpits can discover friction)
- instance-hard-rules.md (every workspace has boundaries)
- decision-log.md scaffold (decisions happen everywhere)

**What does NOT apply:**
- Canon governance (no vocabulary to drift)
- Research scaffolding (cockpit doesn't produce research — it consumes results from full instances)
- Deferred library (the primitives address problems that accumulating workspaces have, not cockpits)
- Glossary (borrow from the instances you operate on)

**Examples:** An operator command center (_Command), a morning-briefing console, a client-facing dashboard workspace.

## Type 3 — Project

**Definition:** A time-bounded effort with a start, a deliverable, and an end. It may accumulate state during its lifetime but it is not permanent infrastructure. When the project ships, it wraps and archives.

**Signals:**
- Has a clear deliverable (a tool, a document, a migration, a build)
- Has a tasks-status.md tracking progress toward completion
- Will eventually be wrapped (`/project-wrap`) and archived or absorbed into a full instance

**What applies:** Light hygiene during the project's lifetime.
- tasks-status.md (standard project tracking)
- decision-log.md if decisions are being made (scaffold — may stay empty for short projects)
- Frontmatter headers if the project has enough files to benefit
- incidents.jsonl if the project is long enough to accumulate friction

**What does NOT apply unless earned:**
- Full research scaffolding (unless the project IS research, like the ACW template itself)
- Canon governance (unless the project involves vocabulary that multiple people use)
- Skill-format contract (unless the project produces skills)

**Examples:** A help-center article revision project, a budget workbook build, a wiki decomposition project. These may get absorbed into a full instance when complete.

## Type 4 — Read-only reference

**Definition:** A workspace that is consumed but never written to. It exists as a source of truth maintained elsewhere. ACW instances may read from it but must never write to it.

**Signals:**
- Maintained by a different system (BookStack, a wiki, a shared drive)
- The operator reads and cites from it but does not contribute to it
- Any write would corrupt the source of truth

**What applies:** Nothing from ACW. The read-only boundary is declared as a hard rule in the instances that consume it.

**Examples:** A wiki (gsg-wiki), a shared reference library, a third-party documentation set.

## How types evolve

Types are not permanent. A cockpit can grow into a full instance if it starts accumulating state. A project can be absorbed into a full instance when it completes. A full instance can be archived when its purpose is served. The type classification is based on current behavior, not intended future state.

The signal that a type needs upgrading:
- **Cockpit → full instance:** The cockpit starts accumulating original content that isn't pointers. Vocabulary appears that needs governance. Research happens inside the cockpit instead of in another instance.
- **Project → full instance:** The project doesn't end. It becomes ongoing infrastructure. tasks-status.md stops tracking toward a deliverable and starts tracking ongoing maintenance.
- **Full instance → archive:** The instance's domain is served by another system. No new content is being produced. The knowledge has been metabolized elsewhere.

When a type upgrade happens, the additional ACW primitives are added incrementally — the same earn-by-incident discipline. Don't pre-install full instance scaffolding on a cockpit "just in case." Add it when the behavior change earns it.

## The one-ACW-per-concern principle

Regardless of type, every distinct concern (distinct hard rules, authority set, and vocabulary) gets its own instance. A business and a personal life are two concerns. Two businesses are two concerns. A cockpit that orchestrates across concerns is a third. Mixing concerns in one instance removes the folder boundary as a security boundary.

See `DEFERRED.md` for the contract registry primitive, which earns its ship when cross-instance vocabulary consistency becomes a problem — meaning you have two or more full instances that need to agree on terms.
