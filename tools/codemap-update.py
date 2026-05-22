#!/usr/bin/env python3
# ---
# class: operational
# authority: canonical
# stability: experimental
# loaded_by_agent: no
# ---
"""
codemap-update.py — ACW-managed incremental codemap rebuild.

Wraps graphify update and promotes output to .acw/codemap/ (Pattern A).
Designed for post-commit hook invocation and direct operator use.
Stdlib only. UTF-8 everywhere.

CLI:
    python tools/codemap-update.py [--ast-only] [--project-root PATH]

Flags:
    --ast-only       AST stage only; skip bridge and Stage 2.
                     Always pass this flag from the post-commit hook.
    --project-root   Workspace root (default: git toplevel, then cwd).

Run-in-place vs temp-dir rationale:
    Graphify caches incremental state in graphify-out/cache/. Running from
    a temp dir destroys the cache on every run, defeating incremental rebuilds.
    Instead, the wrapper runs graphify from .acw/codemap/ so graphify-out/
    lands there and the cache persists across runs. Canonical files
    (GRAPH_REPORT.md, graph.json, etc.) are promoted to .acw/codemap/ only
    after a successful run — the canonical surface is never mutated on failure.

Exit codes:
    0   success (or codemap not adopted — silent skip)
    1   graphify build failed (canonical surface preserved)
    2   pre-flight error
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CODEMAP_PROFILES = {"coding-project", "library"}

# Files promoted from graphify-out/ to .acw/codemap/ after a successful run.
# cache/ stays inside graphify-out/ to preserve incremental rebuild state.
PROMOTE_FILES = [
    "GRAPH_REPORT.md",
    "graph.json",
    "graph.html",
    "manifest.json",
    ".graphify_labels.json",
    ".graphify_root",
]


def find_project_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return Path.cwd()


def parse_acw_state(state_file: Path) -> dict:
    """Extract profile and modules from acw-state.yaml without PyYAML."""
    data: dict = {"profile": None, "modules": []}
    if not state_file.is_file():
        return data

    in_modules = False
    for line in state_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("profile:"):
            data["profile"] = stripped.split(":", 1)[1].strip().strip("\"'")
            in_modules = False
        elif stripped == "modules:":
            in_modules = True
        elif in_modules and stripped.startswith("- "):
            data["modules"].append(stripped[2:].strip().strip("\"'"))
        elif ":" in stripped and not stripped.startswith("-"):
            in_modules = False

    return data


def codemap_adopted(state: dict) -> bool:
    if state.get("profile") in CODEMAP_PROFILES:
        return True
    return "codemap" in state.get("modules", [])


def graphify_available() -> bool:
    return subprocess.run(["graphify", "--version"], capture_output=True).returncode == 0


def promote_output(graphify_out: Path, codemap_dir: Path) -> None:
    """Copy canonical files from graphify-out/ up to .acw/codemap/ level."""
    for name in PROMOTE_FILES:
        src = graphify_out / name
        if src.exists():
            shutil.copy2(str(src), str(codemap_dir / name))


def main() -> int:
    parser = argparse.ArgumentParser(description="ACW codemap incremental rebuild")
    parser.add_argument(
        "--ast-only",
        action="store_true",
        help="AST stage only; skip bridge and Stage 2 (always use for hooks)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Workspace root (default: git toplevel)",
    )
    args = parser.parse_args()

    project_root = args.project_root or find_project_root()
    state_file = project_root / ".acw" / "acw-state.yaml"
    codemap_dir = project_root / ".acw" / "codemap"

    state = parse_acw_state(state_file)
    if not codemap_adopted(state):
        print(
            f"[codemap-update] codemap not adopted by profile "
            f"'{state.get('profile', 'unknown')}' — skipping"
        )
        return 0

    if not graphify_available():
        print(
            "[codemap-update] graphify not found — install with: pip install graphifyy",
            file=sys.stderr,
        )
        return 2

    codemap_dir.mkdir(parents=True, exist_ok=True)

    print(f"[codemap-update] rebuilding AST graph — {project_root}")
    result = subprocess.run(
        ["graphify", "update", str(project_root)],
        cwd=str(codemap_dir),
    )
    if result.returncode != 0:
        print(
            "[codemap-update] graphify exited non-zero — canonical surface unchanged",
            file=sys.stderr,
        )
        return 1

    graphify_out = codemap_dir / "graphify-out"
    if not graphify_out.is_dir():
        print(
            "[codemap-update] graphify produced no graphify-out/ directory",
            file=sys.stderr,
        )
        return 1

    promote_output(graphify_out, codemap_dir)
    print(f"[codemap-update] done — {codemap_dir / 'GRAPH_REPORT.md'}")

    if not args.ast_only:
        print(
            "[codemap-update] bridge step requires /codemap rebuild — "
            "run that for full implements_decision edges"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
