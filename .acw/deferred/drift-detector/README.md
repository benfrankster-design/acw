---
class: deferred
authority: derived
stability: experimental
loaded_by_agent: no
---

# drift-detector

## What it is

A tool that walks the workspace, computes content hashes (Merkle-style), runs natural language inference (NLI) to detect contradictions between assets, and maintains an ATMS-style assumption graph so that contradictions can be traced to their originating claims.

## What problem it addresses

Frontier problem #3: self-correcting drift detection. Assets go stale, claims contradict each other, and the workspace has no mechanism to notice. The drift detector is the mechanism.

## Prior art

Truth Maintenance Systems (Doyle 1979, de Kleer 1986), AGM belief revision (Alchourrón-Gärdenfors-Makinson 1985), Merkle trees, NLI models from the NLP literature. See `research/02-literature-survey.md`.

## Activation trigger

One contradiction the operator could not date. "Could not date" means the operator noticed the contradiction but could not determine which of the conflicting claims was older, newer, or still valid. Severity `high` counts as a single triggering incident.

## Shippable form factor

A stdlib Python script for Merkle hashing (`tools/drift-hash.py`, not shipped) and a separate script that invokes an NLI model (`tools/drift-nli.py`, not shipped — requires model selection). The ATMS-style assumption graph is a YAML file derived from the contract registry.

## What it is NOT

- Not a replacement for bitemporal asset frontmatter — it consumes that primitive
- Not a runtime detector — it walks the workspace on demand
- Not designed to automatically repair contradictions — it detects and reports
- Not sufficient without the typed self-correcting-contract primitive for mechanical remediation
