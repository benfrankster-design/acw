---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Threat Model — ACW v0.1.0

What ACW defends against, what it doesn't, and where the known gaps are. This is not a comprehensive security audit. It is the set of named threats the primitives in this template were designed to mitigate, with honest labeling of what remains unsolved.

## Scope

**In scope:** threats that arise inside a single ACW instance from normal operator and agent behavior. Vocabulary drift, stale claims, credential overexposure, role ambiguity, governance escalation failures.

**Out of scope for v0.1.0:** network attackers, supply-chain compromise of dependencies, physical access to the operator's machine, reflexive prompt injection from external content consumed by an LLM agent, insider abuse of legitimate authority. These are real threats and ACW does not address them.

## Threat 1 — Hidden label drift after approval

**Description.** A term enters the canon as `approved`, but content committed days or weeks later uses a synonym that was not yet in the `hidden_labels` list. The drift accumulates silently until two skills disagree about what the term means.

**Attack surface.** Any content write path that is not lint-gated.

**Defense.** `tools/lint-vocab.py` runs at commit time and blocks commits containing known hidden labels. The canonicalization gate in `rules/canon-governance.md` describes the escalation path when a novel synonym appears: add it to hidden_labels, log an incident, update content.

**Known gap.** The lint only catches synonyms that have already been added to hidden_labels. Novel drift is caught by human review, not by the tool. This is a lint-assisted governance, not a fully automated guarantee.

**Activation trigger.** One contradiction the operator could not date — promotes `deferred/drift-detector/`.

## Threat 2 — Capability lease forgery

**Description.** A skill obtains a capability reference it should not hold and calls a tool outside its declared scope.

**Attack surface.** Any credential read path.

**Defense.** Not mitigated in v0.1.0. The broker (`rules/capability-broker.md`) is a design doc; the tool is deferred. Until a real credential-exposure incident is logged, v0.1.0 operates under the assumption that credential access is operator-managed and skills do not hold credentials directly.

**Known gap.** This is the largest deliberate gap in v0.1.0. The operator reframing explicitly accepts this risk under the training-ground framing.

**Activation trigger.** First real credential-exposure incident — promotes `rules/capability-broker.md` to shipped tool.

## Threat 3 — Glossary bypass via non-markdown content

**Description.** `lint-vocab.py` only scans `.md` files. Forbidden terms embedded in YAML, JSON, or other text formats are not caught.

**Attack surface.** Any non-markdown content that agents read.

**Defense.** Partial. The lint's file-extension scope is documented. Operators who commit non-markdown content must extend the lint scope or accept the gap.

**Known gap.** Explicit. Extension is a one-line change in `tools/lint-vocab.py` but requires operator decision.

## Threat 4 — Role enum extension without evidence

**Description.** An operator adds a seventeenth role to the pipeline-roles appendix without a documented incident justifying the addition. The enum bloats, MECE breaks.

**Attack surface.** `rules/pipeline-roles.md` edit path.

**Defense.** The extension protocol in `rules/pipeline-roles.md` requires incident evidence, a MECE check, a version bump, and a skill migration pass. Enforcement is human, not mechanical.

**Known gap.** No tool currently blocks edits to the role enum. An auditor skill could be added in a future version.

## Threat 5 — canon.yaml merge conflict in git

**Description.** Two operators edit `canon.yaml` simultaneously. Git merge conflict resolves incorrectly and one operator's term addition is lost.

**Attack surface.** Multi-operator instances only.

**Defense.** Partial. The schema is line-oriented and merge-friendly by design. `approval_authority` is a free-form string that can carry multi-operator attribution.

**Known gap.** No machine-readable merge resolver. Multi-operator instances should coordinate canon edits via the decision log rather than concurrent commits.

## Threat 6 — Secret leakage into glossary terms

**Description.** An operator pastes a secret-bearing example into a term definition. The secret is committed.

**Attack surface.** Glossary and canon edit paths.

**Defense.** Out of scope for ACW's tools. Use standard pre-commit secret scanners (gitleaks, trufflehog) alongside ACW.

**Known gap.** Explicit. ACW is not a secret scanner.

## Threat 7 — Symlink escape from lint scope

**Description.** `lint-vocab.py` walks the content directory. If a symlink points outside the intended scope, the lint reads files the operator did not mean to include.

**Attack surface.** Any workspace with symlinks.

**Defense.** The lint uses `rglob` which does follow symlinks on some platforms. Operators who use symlinks should verify scope behavior.

**Known gap.** Documented, not mitigated.

## Threat 8 — TOCTOU on lease verification

**Description.** Time-of-check-to-time-of-use race between the broker verifying a capability scope and the actual tool call.

**Attack surface.** Broker tool (not shipped in v0.1.0).

**Defense.** N/A — the broker tool is deferred. Design notes in `rules/capability-broker.md` describe the intended mitigation (short-lived leases, single-use tokens) but no code ships.

**Known gap.** Fully deferred to future activation.
