#!/usr/bin/env python3
# ---
# class: operational
# authority: canonical
# stability: experimental
# loaded_by_agent: yes
# ---
"""
scaffold-instance.py — Bootstrap a canonical ACW instance into a target directory.

Reads `acw-state.yaml::template_layer` and `instance_layer` to determine what
to copy. The manifest is the single source of truth — adding a new file to
ACW that should propagate to instances means editing acw-state.yaml, not this
script. See LAYERS.md for the explainer.

Closes the bootstrap gap surfaced by Incident D-02
(uuid 616d435b-ec6d-470a-9cdf-2935b739e4a1).

Usage:
    python tools/scaffold-instance.py <target_dir> --code <PROJECT_CODE>
        --domain <DOMAIN> [--name <PROJECT_NAME>] [--host claude-code|gpt|gemini|none]
        [--dry-run]

Behavior: refuses to clobber. Lists conflicts and exits 1. --dry-run lists what
would be written without writing.

Stdlib only. UTF-8. LF endings via newline='\\n'.
"""

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ACW_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ACW_ROOT / "acw-state.yaml"


def parse_state() -> dict:
    """Minimal YAML parse — stdlib only. Reads only the keys we need:
    template_layer (list of strings), instance_layer (list of dicts with
    path/template/instance_only), empty_dirs (list of strings).

    Bails on malformed input rather than guessing.
    """
    text = STATE_FILE.read_text(encoding="utf-8")
    state = {"template_layer": [], "instance_layer": [], "empty_dirs": []}

    section = None
    pending: dict | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            key = line[:-1]
            if key in state:
                section = key
                pending = None
            else:
                section = None
                pending = None
            continue
        if section is None:
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if section in ("template_layer", "empty_dirs"):
            if stripped.startswith("- ") and indent == 2:
                state[section].append(stripped[2:].strip().strip('"').strip("'"))
            else:
                # End of section
                section = None
                pending = None

        elif section == "instance_layer":
            if stripped.startswith("- ") and indent == 2:
                # Start a new entry
                if pending is not None:
                    state["instance_layer"].append(pending)
                pending = {"path": None, "template": None, "instance_only": False}
                rest = stripped[2:].strip()
                _consume_kv(pending, rest)
            elif indent >= 4 and ":" in stripped:
                _consume_kv(pending, stripped)
            else:
                if pending is not None:
                    state["instance_layer"].append(pending)
                    pending = None
                section = None

    if pending is not None:
        state["instance_layer"].append(pending)

    return state


def _consume_kv(target: dict, frag: str) -> None:
    """Parse a single 'key: value' fragment into target dict.
    Strips inline '#' comments outside quotes.
    """
    if ":" not in frag:
        return
    key, _, value = frag.partition(":")
    key = key.strip()
    value = value.strip()
    # Strip inline comment (only when not inside quotes)
    if value and value[0] not in ('"', "'"):
        hash_idx = value.find("#")
        if hash_idx != -1:
            value = value[:hash_idx].strip()
    value = value.strip('"').strip("'")
    if value == "null" or value == "":
        target[key] = None
    elif value == "true":
        target[key] = True
    elif value == "false":
        target[key] = False
    else:
        target[key] = value


def substitute(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def collect_planned_paths(target: Path, state: dict) -> list[Path]:
    """Return target paths the scaffold would create."""
    paths: list[Path] = []

    for entry in state["template_layer"]:
        src = ACW_ROOT / entry
        dst_root = target / entry
        if src.is_dir():
            for f in src.rglob("*"):
                if f.is_file() and not _should_skip(f):
                    paths.append(dst_root / f.relative_to(src))
        elif src.is_file():
            paths.append(dst_root)

    for entry in state["instance_layer"]:
        if entry.get("path"):
            paths.append(target / entry["path"])

    for d in state["empty_dirs"]:
        paths.append(target / d / ".gitkeep")

    return paths


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  would write: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def copy_verbatim(src: Path, dst: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"  would copy:  {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


SKIP_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def _should_skip(path: Path) -> bool:
    if any(part in SKIP_DIR_NAMES for part in path.parts):
        return True
    if path.suffix in SKIP_SUFFIXES:
        return True
    return False


def copy_tree(src: Path, dst: Path, dry_run: bool) -> None:
    for f in src.rglob("*"):
        if f.is_file() and not _should_skip(f):
            copy_verbatim(f, dst / f.relative_to(src), dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold an ACW instance.")
    parser.add_argument("target_dir")
    parser.add_argument("--code", required=True, help="Project code, e.g. NP")
    parser.add_argument("--domain", required=True, help="Primary domain")
    parser.add_argument("--name", default=None, help="Project name (defaults to code)")
    parser.add_argument("--host", default="claude-code",
        choices=["claude-code", "gpt", "gemini", "none"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = Path(args.target_dir).resolve()
    project_name = args.name or args.code
    today = datetime.now(timezone.utc).date().isoformat()

    tokens = {
        "PROJECT_NAME": project_name,
        "PROJECT_CODE": args.code,
        "DOMAIN": args.domain,
        "DATE": today,
    }

    if not STATE_FILE.is_file():
        print(f"scaffold: acw-state.yaml missing at {STATE_FILE}", file=sys.stderr)
        return 2

    state = parse_state()

    if not state["template_layer"] or not state["instance_layer"]:
        print("scaffold: manifest empty — refusing to scaffold", file=sys.stderr)
        return 2

    planned = collect_planned_paths(target, state)
    if target.exists():
        conflicts = [p for p in planned if p.exists()]
        if conflicts:
            print("scaffold: refusing to clobber. Existing files:", file=sys.stderr)
            for p in conflicts:
                print(f"  {p}", file=sys.stderr)
            return 1

    print(f"Scaffolding ACW instance at: {target}")
    if args.dry_run:
        print("(dry-run mode — no files will be written)")

    # template_layer: copy verbatim (files and directories)
    for entry in state["template_layer"]:
        src = ACW_ROOT / entry
        dst = target / entry
        if not src.exists():
            print(f"scaffold: template_layer source missing {src}", file=sys.stderr)
            return 2
        if src.is_dir():
            copy_tree(src, dst, args.dry_run)
        else:
            copy_verbatim(src, dst, args.dry_run)

    # instance_layer: render template, or write empty if template is null
    for entry in state["instance_layer"]:
        path = entry.get("path")
        if not path:
            continue
        dst = target / path
        tmpl = entry.get("template")
        if tmpl is None:
            write_text(dst, "", args.dry_run)
        else:
            tmpl_path = ACW_ROOT / tmpl
            if not tmpl_path.is_file():
                print(f"scaffold: template missing {tmpl_path}", file=sys.stderr)
                return 2
            content = tmpl_path.read_text(encoding="utf-8")
            write_text(dst, substitute(content, tokens), args.dry_run)

    # empty_dirs: .gitkeep markers
    for d in state["empty_dirs"]:
        write_text(target / d / ".gitkeep", "", args.dry_run)

    # Host-specific entry file (not in manifest because it's host-conditional).
    # Per D-ACW-047 (v0.9.7): CLAUDE.md is a thin pointer; auto-load runs via
    # SessionStart hook at .claude/hooks/load-context.py. The hook reads
    # acw-state.yaml::auto_load_at_session_start at runtime, so the manifest
    # is the single source of truth and CLAUDE.md never drifts.
    if args.host == "claude-code":
        write_text(target / "CLAUDE.md", "See AGENTS.md.\n", args.dry_run)
        # SessionStart hook + settings.json. Templates live in tools/templates/.
        hook_src = ACW_ROOT / "tools" / "templates" / "load-context.py.tmpl"
        settings_src = ACW_ROOT / "tools" / "templates" / "settings.json.tmpl"
        if hook_src.exists():
            write_text(
                target / ".claude" / "hooks" / "load-context.py",
                hook_src.read_text(encoding="utf-8"),
                args.dry_run,
            )
        if settings_src.exists():
            write_text(
                target / ".claude" / "settings.json",
                settings_src.read_text(encoding="utf-8"),
                args.dry_run,
            )

    print()
    print(f"Scaffolded ACW instance at {target}:")
    print(f"  Project name: {project_name}")
    print(f"  Project code: {args.code}")
    print(f"  Domain: {args.domain}")
    print(f"  Host: {args.host}")
    print()
    print("Placeholders to fill before first commit:")
    print("  research/01-problem-framing.md (operator-fill sections)")
    print("  glossary.md (no terms yet)")
    print("  threat-model.md (asset inventory + threat actors)")
    print()
    print("First-session checklist:")
    print("  1. Edit research/01-problem-framing.md")
    print("  2. Add domain-specific hard rules to rules/instance-hard-rules.md")
    print("  3. cd <target> && python tools/lint-vocab.py glossary.md --content-dir .")
    print("  4. cd <target> && python -m unittest discover tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
