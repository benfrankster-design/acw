---
kind: bug
source_instance: cs-ops-spec (COPS)
date: 2026-05-21
status: triaged
disposition: fixed-in-canonical
fixed_in_session: 25
fix_summary: "rules/instance-current-manifest.md frontmatter bumped to synced_to: '0.10.1'; Maintenance section gained a normative bump-discipline paragraph requiring synced_to bump on the same commit as any new earned-in entry."
---

# Bug: `rules/instance-current-manifest.md` `synced_to` field is stale

## What

The canonical `rules/instance-current-manifest.md` at GitHub has `synced_to: "0.9.9"` in its frontmatter, but the file body contains recommended-blocks entries earned in `0.10.0` and `0.10.1`:

- `profile` field — earned `0.10.0`
- `modules` field — earned `0.10.0`
- `env_secrets` block — earned `0.10.1`

## Why it matters

`/acw-session start` Step 5 reads `synced_to` from the local manifest cache and compares it against `acw-state.yaml::last_reconciled_version` to decide whether to short-circuit the drift walk. An instance that has just upgraded to `0.10.1` and written `synced_to: "0.10.1"` locally is using a value that doesn't match what canonical shipped — the drift walk may misbehave on next session start in edge cases.

More practically: any instance that pulls the canonical manifest and checks `synced_to` to infer "what ACW version does this file represent" gets a wrong answer.

## Expected fix

On ACW's canonical repo, the manifest frontmatter should read `synced_to: "0.10.1"` (or whatever the highest earned-in version in the file is). This field should be bumped as part of shipping any new recommended-block entry.

## Workaround applied

COPS instance manually set `synced_to: "0.10.1"` in its local cache after pulling canonical.
