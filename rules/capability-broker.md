---
class: deferred
authority: canonical
stability: experimental
loaded_by_agent: no
---

# Capability Broker — Design Document

**Version:** 0.1.0
**Status:** Design document only. The tool implementation is deferred in v0.1.0. See `DEFERRED.md` row `capability-broker` for the activation trigger.

---

## Why this doc ships even though the tool does not

The capability broker is the one primitive every serious analysis of agentic workspace security converges on. Vault response wrapping, AWS STS AssumeRole, Google Workload Identity Federation, SPIFFE SVIDs, and object capabilities (Miller et al.) all independently arrive at the same structural answer across thirty years of security research: **the calling party never needs the secret; it needs a short-lived, scope-bounded, revocable reference that a trusted intermediary can cash in.**

ACW v0.1.0 does not ship the broker tool because a single-operator workspace on a single machine with OS-level credential storage (Windows Credential Manager, macOS Keychain, libsecret) already has 60% of the broker's value for free. The tool earns its ship when one of the activation triggers in `DEFERRED.md` fires.

This document preserves the design so that the day the trigger fires, there is no re-derivation. An operator can pick up this file, implement the tool, and ship.

---

## Design contract

### Invariants

1. **Credential value never enters the calling skill's context.** The broker reads and emits real credentials only during outbound tool calls that route through the broker itself. Calling skills handle references, never values.

2. **Every credential use is logged.** An append-only audit log records who requested what scope, when it was issued, when it was used, and when it expired or was revoked.

3. **Capability references are scope-bounded and time-bounded.** A reference names exactly one authority ("read from surface X") and has an expiration timestamp. Expired references are rejected at verify time.

4. **Declared scope must match requested scope.** The broker reads the calling skill's SKILL.md manifest, verifies the `capabilities:` field declares the scope being requested, and refuses requests for undeclared scopes.

5. **Revocation is immediate.** A revoked reference fails verification even before its TTL expires.

---

## CLI surface (proposed)

```
python cap-broker.py request <capability> <scope> <ttl-seconds> [--holder <id>]
python cap-broker.py verify <reference-id>
python cap-broker.py release <reference-id>
python cap-broker.py list [--status active|released|expired]
python cap-broker.py gc
```

### Commands

- **`request`** — issue a new capability reference. Returns the reference ID and expiration time on stdout. Exit 0 on success, 1 on denial (scope not declared in manifest), 2 on bad input.

- **`verify`** — check whether a reference is still valid. Returns the scope and holder on success. Exit 0 if valid, 1 if expired or revoked, 2 on bad input.

- **`release`** — mark a reference as released before its TTL expires.

- **`list`** — show all references, optionally filtered by status.

- **`gc`** — mark expired references as `expired` in the audit log without deleting history.

---

## Data layout

**Lease store:** `.acw/leases.jsonl`, append-only JSONL. Each line is one lease event.

**Lease event schema:**

```json
{
  "event": "issue|verify|release|expire",
  "id": "uuid4",
  "capability": "string",
  "scope": "string",
  "holder": "string",
  "issued_at": "ISO 8601 UTC",
  "expires_at": "ISO 8601 UTC",
  "status": "active|released|expired"
}
```

**Credential store:** OS-level (Windows Credential Manager, macOS Keychain, libsecret on Linux). The broker never persists credentials itself; it reads from the OS store at the moment of egress.

---

## Portability constraints (pinned for the v0.1.0 doc even though tool is deferred)

The tool implementation, when it ships, MUST:

1. **Use `datetime.now(timezone.utc)` for all timestamps.** Naive local-time strings break across DST and across machines.
2. **Open files in binary mode with explicit LF line endings** (`open(path, 'ab')` and write `b'\n'` explicitly). Windows auto-CRLF corrupts JSONL.
3. **Use `pathlib.PurePosixPath` for scope comparisons** so path-prefix matching works identically on Windows and POSIX.
4. **Declare single-process constraint explicitly** in tool README. No file locking across processes in v0.1; document the constraint so operators don't run concurrent invocations.
5. **Open all file reads with `encoding='utf-8'`** explicitly. Windows cp1252 default crashes on any non-ASCII content.
6. **Stdlib only.** No PyYAML, no click, no rich. Use `json`, `argparse`, `pathlib`, `datetime`, `uuid`, `sys`.

---

## Threat model (scoped to broker)

### T1. Reference leakage via session log
A capability reference leaks into a session transcript the model provider retains. If the reference is still valid, replay could use it.
**Mitigation:** short TTLs (default 15 minutes), explicit revocation on session end, scope so narrow that a leaked reference is low-value.
**Known gap:** prompt caching on the model provider side can retain a reference past its logical revocation. This is noted in the deferred library's `self-correcting-contract` primitive as an unresolved research direction.

### T2. Compromised skill requesting undeclared scope
A prompt-injected skill attempts to request a broader scope than its manifest declares.
**Mitigation:** broker verifies against SKILL.md manifest at request time; refuses undeclared scopes. The skill manifest is not LLM-writable at request time; it was committed to git before the session.

### T3. Broker process compromise
An attacker with local filesystem access reads `.acw/leases.jsonl` and replays active references.
**Mitigation:** `.acw/` is in `.gitignore`. Reference IDs are uuid4 (unguessable) but do not protect against local-filesystem read. Threat is out of scope for v0.1.0; documented here so the operator knows.

### T4. Scope-match bypass via path manipulation
A scope like `surface/read` matches `surface/read/secret` if string prefix is used naively. An attacker requests `surface/read/` and then uses the returned reference to access a child path.
**Mitigation:** use `pathlib.PurePosixPath.is_relative_to()` or equivalent, not string prefix. Document this in the implementation.

### T5. Concurrent request race
Two concurrent `request` invocations write to the JSONL and collide.
**Mitigation:** single-process constraint documented; no file locking in v0.1. When concurrent access becomes a real requirement, this is a promotion trigger.

### T6. Clock skew
Two machines with different clocks disagree about expiration.
**Mitigation:** all timestamps UTC; document that multi-machine operation requires NTP sync. Single-machine operator is fine.

### T7. Audit-log tampering
An attacker with write access to `.acw/leases.jsonl` forges or deletes lease events.
**Mitigation:** out of scope for v0.1.0. Append-only discipline is file-system convention, not cryptographic guarantee. When this matters, the audit log becomes a ledger with hash-chained entries, documented in `DEFERRED.md` as a future extension.

### T8. Reflexive injection of the broker itself
An attacker tricks the broker into issuing a reference it would not otherwise issue, by manipulating the SKILL.md manifest or the request payload.
**Mitigation:** the broker reads SKILL.md from the filesystem as committed at session start, not from the LLM's session context. The request payload is a CLI invocation, not LLM output, unless the calling skill is itself LLM-directed. In that case the broker's guarantees degrade to whatever integrity the manifest carries.

---

## Integration with the four-role enum

The broker is the canonical `broker-sideband` role. When the tool ships, its SKILL.md (or tool-level equivalent) declares:

```yaml
name: Capability Broker
description: Holds credentials and issues scope-bounded capability references to pipeline skills.
role: broker-sideband
capabilities:
  - broker.admin
```

No pipeline skill declares `broker.admin`; only the broker itself does. Pipeline skills declare narrower scopes like `source.read` or `target.write` and request references for those scopes at runtime.

---

## Why this is not in v0.1.0

Three reasons:

1. **Single-operator, single-machine operator already has OS-level credential storage.** Windows Credential Manager, macOS Keychain, and libsecret all provide 60% of the broker's value for free. The remaining 40% (scope declaration, audit log, revocation semantics) is earned once the operator runs agents unsupervised or moves to a second machine.

2. **The earn-by-incident rule.** Nothing ships without a named, dated, documented incident justifying it. The broker waits for one of the activation triggers in `DEFERRED.md`.

3. **The skeptic warned against building admission controllers and brokers before brokers.** The broker is a foundation; the admission controller sits above it. Both are deferred. Shipping the broker alone, before any pipeline skill declares a capability, would be infrastructure without a customer.

---

## Changelog

- **v0.1.0 — 2026-04-11** — Initial design document. Tool implementation deferred.
