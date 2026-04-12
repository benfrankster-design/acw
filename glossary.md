---
class: operational
authority: canonical
stability: experimental
loaded_by_agent: yes
---

# Glossary

**Status:** Seed glossary. Bootstrap vocabulary for ACW itself.
**Purpose:** Canonical terms ACW uses to describe its own machinery. An operator instantiating ACW adds their own domain vocabulary to `rules/canon.yaml` (the governed canon), not here.

The vocabulary lint tool (`tools/lint-vocab.py`) uses this file as its authoritative term list. The seed ships zero `**forbidden synonyms:**` blocks. This is deliberate: regex-based linting cannot distinguish a citation ("HashiCorp Vault") from a substitution ("our vault"), and a seed template forbidding ordinary English words (file, input, document) fails its own dogfood loop. Enforcement earns its ship when an instance populates `rules/canon.yaml` with `hidden_labels` that reflect real drift encountered in practice. See Incident #1 in `incidents.jsonl` for the earned finding that justified this design.

---

## authority set

The declared list of valid `approval_authority` values for a given instance. Declared in `rules/instance-hard-rules.md`. A canon entry whose `approval_authority` is not in the authority set causes lint to fail. See `rules/canon-governance.md` for the N-authority model.

---

## broker

A sideband role that holds credentials and issues scope-bounded capability references to skills. The broker never exposes credential values to the calling skill. The broker tool is deferred in v0.1.0; the design ships in `rules/capability-broker.md`. Inspired by HashiCorp Vault's response-wrapping pattern but is not that product — do not conflate them.

---

## canon

The workspace's controlled vocabulary declared in `rules/canon.yaml`, governed by `rules/canon-governance.md`. A canon entry has a stable `concept_id`, a `pref_label`, optional synonyms, a state (`draft`/`proposed`/`approved`/`deprecated`/`retired`), and a declared `approval_authority`. Distinct from this glossary, which is ACW's own bootstrap vocabulary and not subject to the canon's state machine.

---

## decision log

The single file at `decisions/decision-log.md` that records all open questions, decisions and rationale, constraints and gotchas, and resolved questions for an instance. Four top-level sections in one file. Splits into four separate files only after the file has grown large enough that a promotion ritual earns the split. See `rules/decision-tracking.md`.

---

## deferred library

The set of primitives whose design is ready but whose implementation is held until a named, dated, documented incident justifies shipping. Canonical listing in `DEFERRED.md`; derived subfolder READMEs in `deferred/`. Governed by the promotion ritual in `rules/promotion-ritual.md`. Deliberately not a roadmap — framing it as one invites the exact premature-ship failure mode the library exists to prevent.

---

## guardian

A role that blocks unsafe actions preventively. Accept-or-reject only; does not mutate state. One of the four normative role groups in `rules/pipeline-roles.md`.

---

## hard rule

A stop-work rule declared in `rules/instance-hard-rules.md`. Violation halts work until the rule is satisfied or the rule itself is changed via a decision-log entry. Hard rules are per-instance; ACW's template ships zero hard rules because it has no instance state.

---

## incident

A dated, documented moment where a deferred primitive would have prevented friction, damage, or ambiguity. Recorded in `incidents.jsonl` via `tools/log-incident.py log`. Three incidents above `low` severity on the same deferred primitive earn promotion review per `rules/promotion-ritual.md`.

---

## instance

A concrete workspace derived from the ACW template. An operator clones ACW, fills in `rules/instance-hard-rules.md`, seeds `rules/canon.yaml`, and the result is an instance. ACW itself is the template, not an instance.

---

## orchestrator

A role that coordinates other skills in sequence but does no leaf work. One of the four normative role groups in `rules/pipeline-roles.md`.

---

## pipeline-worker

A role that performs exactly one data-flow operation (the finer sixteen-role appendix in `rules/pipeline-roles.md` names variants: collector, extractor, classifier, router, enricher, transformer, composer, committer, auditor, sanitizer, worker, researcher). Every non-orchestrator, non-guardian, non-broker skill declares this role in v0.1.0.

---

## primitive

A named, shippable component of ACW — either a rule file, a tool, a schema, or a governance process. Every primitive has a class (operational, reference, deferred, archive) and a state (shipped or deferred). The deferred library lists 11 primitives; the shipped library is everything else in the template.

---

## promotion

The act of moving a primitive from `DEFERRED.md` into a shipped state (a new file under `rules/` or `tools/`). Governed by `rules/promotion-ritual.md`. Requires at least three incidents above `low` severity on the primitive, plus the eight mechanical steps of the ritual.

---

## role

The data-flow position a skill occupies. Exactly one per skill. Four normative groups in v0.1.0: `orchestrator`, `pipeline-worker`, `guardian`, `broker-sideband`. Declared in SKILL.md frontmatter as `role:`. A finer sixteen-role taxonomy exists as an informative appendix in `rules/pipeline-roles.md`. See that file for the full contract.

---

## scope

The narrow permission a skill requests from the broker. A scope names exactly one authority ("read from surface X") bounded by a short-lived lease. See `rules/capability-broker.md`.

---

## skill

An executable unit of work that declares its role, capabilities, and preconditions in a `SKILL.md` file. A skill occupies exactly one role. ACW v0.1.0 ships zero skills other than the worked reference in `skills/example-skill/`.

---

## trigger

An incident pattern that earns a deferred primitive its promotion. Every row in `DEFERRED.md` has an explicit activation trigger stated in countable, falsifiable terms. See the activation trigger rule in `DEFERRED.md`.
