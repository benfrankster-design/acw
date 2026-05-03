# How I Work — ACW

Working conventions for ACW development specifically. The operator's broader working preferences live in `~/.claude/CLAUDE.md` and `~/synapse/Rules/Identity/about-me.md`; this file captures only the ACW-specific layer.

## Schedule and rhythm

- ACW work is bursty, not scheduled. Sessions happen when an architectural question or downstream-instance dogfood surfaces.
- Each session aims for a coherent ship — a numbered version, not a half-finished branch.

## Build-discipline preferences

- **Earn-by-incident before tooling.** No primitive ships without a documented incident or activation trigger. See `DEFERRED.md` and `rules/promotion-ritual.md`.
- **One session, one ship.** Substantive sessions end with a version bump, decision-log entries, build-log narrative, push to `origin/master`. Half-shipped state goes in `tasks-status.md::Pending`, not in committed-but-undocumented limbo.
- **Append-only history is sacred.** Past entries in `decisions/decision-log.md`, `incidents.jsonl`, `build-log.md`, `research/sessions/`, and `Done` blocks of `tasks-status.md` never get edited. Corrections append.

## Tooling preferences

- Plain-text, stdlib-only, Windows-native. No SQLite, no daemons, no external services. See `rules/instance-hard-rules.md` HR-002.
- Single source of truth: GitHub for canonical content; local copies are caches. `/acw-instance upgrade` fetches; never reads local cache as comparison yardstick.

## What I want agents to do differently

- Don't assume "tighten the spec to claim the bug was an interpretation issue" is a fix. The right fix is to rewrite the spec so future agents can't drift the same way; document the bug as the incident that earned the rewrite.
- Don't bypass the careful guardrail with `--no-verify` or force-pushes. Pre-commit hooks fail loudly for a reason; investigate the root cause.
- Don't propose extensions before reading `SKEPTIC.md`.
