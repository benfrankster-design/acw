---
term: "broker"
status: active
updated: 2026-05-13
---

# broker

A sideband role that holds credentials and issues scope-bounded capability references to skills. The broker never exposes credential values to the calling skill. The broker tool is deferred in v0.1.0; the design ships in `rules/capability-broker.md`. Inspired by HashiCorp Vault's response-wrapping pattern but is not that product — do not conflate them.
