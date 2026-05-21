# codemap implementation plan

This skill's contract is authored (SKILL.md). The Graphify wrapper itself — the code that invokes Graphify and routes its output into `.acw/codemap/` — is deferred to a follow-up session because it needs the actual Graphify CLI surface probed first.

## What's deferred and why

The skill needs to:

1. Invoke Graphify via subprocess.
2. Parse Graphify's output structure (currently documented as `graphify-out/GRAPH_REPORT.md` + `graph.html`).
3. Route Graphify's nodes/edges into `.acw/codemap/nodes.json` + `edges.json` (Graphify's internal representation may differ from this schema; verify).
4. Add ACW-specific bridges: walk `.acw/decisions/entries/*.md`, find code references, emit `implements_decision` edges with confidence tags.

Each step depends on Graphify's actual CLI behavior:

- **Subprocess args.** What flags does `graphify` accept? What's the equivalent of `--ast-only` and `--semantic`?
- **Output format.** Does Graphify write a single JSON file, multiple files, a markdown report only?
- **Exit codes.** What does Graphify return on success vs partial failure vs full failure?
- **Incremental rebuild.** How does Graphify cache per-file extraction? Does its cache live at a path we can route?

Authoring the wrapper without probing these would ship a guess. Better to probe first.

## Investigation steps (next session)

1. **Install Graphify locally.** Per https://graphify.net install instructions.
2. **Run against a known repo.** Use cs-atlas as the dogfood target (post-upgrade to v0.10.0 with profile=coding-project).
3. **Document the actual CLI surface.** Subprocess args, output structure, exit code semantics, cache layout. Write this up at `references/graphify-cli-probe.md`.
4. **Author the wrapper.** Subprocess invocation, output routing, error handling.
5. **Author the ACW-specific bridge step.** Walk `.acw/decisions/`, match code symbols to decisions, emit `implements_decision` edges.
6. **Author `references/rebuild.md`, `references/status.md`, `references/audit.md`.** One reference file per verb.
7. **Dogfood against cs-atlas.** Verify `.acw/codemap/GRAPH_REPORT.md` lands correctly. Verify auto-load on next session start surfaces the report.

## Estimated effort

3-5 hours focused work assuming Graphify installs cleanly and its CLI is reasonable to wrap. The ACW-bridge step is the most LLM-cost-sensitive piece — implementation requires careful prompt engineering for the code-to-decision matching.

## What lands first

Even before the full wrapper, three things can ship:

1. **The SKILL.md contract** (this file's sibling). Already authored.
2. **The substrate location.** `.acw/codemap/` directory created during instance upgrade for coding-project / library profiles. Already in `migrations/0.9.9-to-0.10.0.yaml` and `migrations/pre-acw-to-0.10.0.yaml`.
3. **The auto-load entry.** Once `.acw/codemap/GRAPH_REPORT.md` exists, it gets added to `acw-state.yaml::auto_load_at_session_start` per the coding-project profile's defaults.

The wrapper itself is the last piece. Until it lands, `/codemap rebuild` errors with: *"codemap wrapper not yet implemented; see skills/codemap/references/implementation-plan.md."* This is intentional — better to fail loudly than ship a broken wrapper.
