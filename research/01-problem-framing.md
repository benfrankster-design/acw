---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# 01 — Problem Framing

## The question that started the research

Persistent agentic workspaces — systems where an LLM agent operates against a set of files, tools, and rules across many sessions — have a maturity problem. Individual skills work. Individual sessions work. But the thing that is supposed to hold across sessions, across agents, across weeks, is fragile in ways that are not obvious at session scale and become expensive at month scale.

The research project that produced ACW started with a simple framing: what would a persistent agentic workspace need in order to not drift? Not "what features would be nice to add" and not "what tools could we build if we had time," but specifically: what is the smallest set of things that must be true for a workspace to remain coherent across a meaningful span of time without human rescue?

## The five frontier problems

The research identified five problems that all persistent agentic workspaces face and that no existing tool or framework solves completely. They are named in the order they tend to surface rather than the order of difficulty.

### 1. Mechanical MECE enforcement

Skills collide. Two skills claim to handle the same input shape. Two routers disagree about which domain an asset belongs to. A new skill ships that overlaps an old skill by 70% and nobody notices for six weeks. The failure mode is not that any individual skill is wrong — it is that the workspace as a whole has no machine-readable notion of mutual exclusion. Every collision is caught by a human, in production, after the damage.

### 2. Cross-vendor controlled vocabulary

Different agents (different vendors, different models, different sessions) use different words for the same concept. "Ticket" means one thing to the answerbot skill and another to the triage skill. "Approved" passes through a state machine nobody wrote down. Every agent is locally consistent; the workspace is globally incoherent. Standard vocabulary frameworks (SKOS, KCS, domain-driven design's ubiquitous language) solve this at the design-time layer but have no commit-time enforcement story.

### 3. Self-correcting drift detection

Assets go stale. A claim that was true six weeks ago is no longer true. Nothing in the workspace notices. The next agent that reads the stale asset acts on it and the damage propagates. Truth Maintenance Systems (Doyle 1979, de Kleer 1986) and AGM belief revision (Alchourrón-Gärdenfors-Makinson 1985) describe the shape of the solution but require typed contracts the workspace does not have.

### 4. Credential and secret management

Skills accumulate authority. A skill that started with narrow read access gets a new tool. The new tool needs broader write access. Six months later the skill holds authority it no longer needs for its original job. No mechanism revokes the unused scope. Standard object-capability patterns (Miller canon, Vault response wrapping, SPIFFE/SPIRE) solve this at the infrastructure layer but require a broker — which agentic workspaces almost never have.

### 5. Pre-tool-call semantic validation

An agent is about to call a tool. The call is syntactically valid. The call is permitted by the current authority. The call will damage an asset because the call violates a semantic invariant that the tool's type signature does not capture. Nothing catches this. Kubernetes admission control (two-phase mutator + validator) describes the shape; multiparty session types and PDDL-style preconditions describe the typing; neither ships as a drop-in for agentic workspaces.

## Why these five collapse to one foundation

The research's central claim is that all five problems share a single missing piece: **a typed, machine-readable contract registry**. Not a documentation file. Not a config file. A registry that every skill, every asset, and every tool call can be validated against, and that every drift can be measured against.

- MECE enforcement needs the registry to know what "same input" means
- Vocabulary needs the registry as the lookup surface for canonical terms
- Drift detection needs the registry as the ground truth to measure against
- Credential management needs the registry as the declaration surface for scope
- Semantic validation needs the registry as the type system for preconditions

No registry, no solution to any of the five. A minimal registry addresses all five partially. A mature registry addresses all five fully.

## Why v0.1.0 does not ship the registry

The full contract registry is the primitive named `contract-registry` in `DEFERRED.md`. It is deferred because shipping it requires a second independent workspace to validate against. Until two ACW instances exist in the same hands, a contract registry cannot be tested for cross-workspace consistency — and testing cross-workspace consistency is the entire point. So v0.1.0 ships the governance-layer precursors (canon, roles, lint, promotion ritual) and holds the typed registry in deferred library with a clear activation trigger.

This is not a cop-out. It is the earn-by-incident discipline applied to the largest primitive in the system. The operator who ships the full registry without a second workspace is solving a problem they do not yet have.
