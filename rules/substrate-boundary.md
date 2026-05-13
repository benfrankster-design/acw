---
class: reference
authority: canonical
stability: stable
loaded_by_agent: no
---

# Substrate boundary

Defines what the `/acw-instance audit|upgrade` verbs treat as **substrate** (in-scope) versus **project content** (out-of-scope; never read for classification, never written to).

This file is the authoritative source for the project-content exclusion list. The skill `skills/acw-instance/` references this rule; do not duplicate the lists into skill prose.

## Substrate (in-scope)

Authoritative source: canonical `acw-state.yaml` blocks `template_layer`, `instance_layer[].path`, `paths.*`, `empty_dirs`, `meta_layer`. Every path declared in those blocks is in-scope by definition.

Substrate-shaped patterns at non-canonical locations are also in-scope:

- Markdown files with `class/authority/stability/loaded_by_agent` frontmatter.
- Dated capture files (`YYYY-MM-DD-*.md`).
- `.jsonl` event logs.
- Directories whose name matches a canonical `paths.*_dir` key but at the wrong location (candidate for `move`).
- Workspace-named substrate directories the operator created (`notes/`, `journal/`, `kb/`, etc.) — substrate-shaped patterns, candidate for `move`/`reshape`/`instance-specific`/`absorption-candidate`.

## Project content (out-of-scope)

Never read for classification, never written to.

**Directories.**

```
src/  lib/  test/  tests/  spec/  app/  pkg/  cmd/  internal/
dist/  build/  out/  target/  bin/  obj/  .next/
node_modules/  __pycache__/  .venv/  venv/  env/  vendor/  deps/
coverage/  .git/  .github/  .vscode/  .idea/
.mypy_cache/  .pytest_cache/  .ruff_cache/  .tox/
```

**Build / package manifest files.**

```
package.json  package-lock.json  pnpm-lock.yaml  yarn.lock
pyproject.toml  setup.py  setup.cfg  Pipfile  Pipfile.lock  requirements.txt
Cargo.toml  Cargo.lock  go.mod  go.sum  pom.xml  build.gradle  tsconfig.json
.eslintrc*  .prettierrc*  .editorconfig  .gitignore  .gitattributes
Makefile  Dockerfile  docker-compose.yml  *.lock  .env*
```

**Source file extensions.**

```
.py .js .ts .tsx .jsx .rs .go .java .kt .swift
.cpp .c .h .rb .php .cs .scala .clj .ex .exs
.elm .hs .ml .html .css .scss .sql
```

**Exception:** files inside `tools/` are in-scope when the workspace is ACW-style stdlib substrate tooling (per the canonical `template_layer` declaration for `tools/`).

## Adding new exclusions

When a new ecosystem (language, build tool, framework) starts shipping its config or output into workspaces, extend this file. Skill prose stays unchanged. Reconciliation discipline:

1. Add the path or extension to the appropriate group above.
2. Log the change as a decision-log entry referencing this rule.
3. Bump `acw-state.yaml::version` per the standard discipline.

The skill picks up the new exclusion on its next canonical fetch.
