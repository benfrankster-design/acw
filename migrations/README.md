---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Migrations

Declarative migration manifests for `/acw-instance upgrade`. Each file describes the steps to upgrade an instance from one canonical version to the next.

The skill `/acw-instance upgrade` is a thin executor. The manifests in this directory are the source of truth for migration steps. New canonical version → new manifest here → instances pick it up on next upgrade. Skill code does not change per version bump.

Schema: `rules/migration-manifest.md`.

## Index

| File | From | To | Breaking | Authority |
|---|---|---|---|---|
| `0.9.9-to-0.10.0.yaml` | 0.9.9 | 0.10.0 | yes | D-ACW-050 |

## Conventions

- Naming: `<from_version>-to-<to_version>.yaml`. Consecutive-version pairs only.
- An instance two versions behind runs two manifests in order (e.g., 0.9.8 → 0.9.9 → 0.10.0).
- Breaking migrations must declare `breaking: true` in the manifest header. Audit surfaces this to the operator before upgrade.

## Adding a new migration

1. Author the manifest at `migrations/<from>-to-<to>.yaml`.
2. Verify each step kind is supported by the executor (see `rules/migration-manifest.md` § Step kinds).
3. Test by running `/acw-instance audit` against a copy of an instance at the `from_version`. The audit emits the plan; verify the plan matches intent.
4. Land the decision-log entry that authorizes the migration.
5. Bump canonical `acw-state.yaml::version` to the `to_version`.
6. Update this README's index table.
