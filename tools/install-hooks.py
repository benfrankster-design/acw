#!/usr/bin/env python3
# ---
# class: operational
# authority: canonical
# stability: experimental
# loaded_by_agent: no
# ---
"""
install-hooks.py — Install ACW git hooks into .git/hooks/.

Installs:
  post-commit — runs codemap-update.py --ast-only in background after each commit

.git/hooks/ is not tracked by git. Run this after cloning or when setting up
a new working environment. If a post-commit hook already exists, ACW's entry
is appended rather than overwriting (unless --force is passed).

CLI:
    python tools/install-hooks.py [--force]

Flags:
    --force   Overwrite any existing post-commit hook

Exit codes:
    0   success
    1   not in a git repo, or write error
"""

import argparse
import os
import sys
from pathlib import Path

ACW_HOOK_MARKER = "# ACW: codemap-update (added by tools/install-hooks.py)"

POST_COMMIT_ENTRY = """\
{marker}
_acw_root="$(git rev-parse --show-toplevel)"
python "$_acw_root/tools/codemap-update.py" --ast-only > /dev/null 2>&1 &
"""


def find_git_dir(start: Path) -> Path | None:
    current = start.resolve()
    while True:
        candidate = current / ".git"
        if candidate.is_dir():
            return candidate
        parent = current.parent
        if parent == current:
            return None
        current = parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Install ACW git hooks")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing post-commit hook",
    )
    args = parser.parse_args()

    git_dir = find_git_dir(Path.cwd())
    if not git_dir:
        print("install-hooks: not in a git repository", file=sys.stderr)
        return 1

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    hook_path = hooks_dir / "post-commit"

    entry = POST_COMMIT_ENTRY.format(marker=ACW_HOOK_MARKER)

    if hook_path.exists() and not args.force:
        existing = hook_path.read_text(encoding="utf-8")
        if ACW_HOOK_MARKER in existing:
            print("install-hooks: ACW post-commit entry already present — nothing to do")
            return 0
        new_content = existing.rstrip("\n") + "\n\n" + entry
        hook_path.write_text(new_content, encoding="utf-8")
        print(f"install-hooks: appended ACW entry to existing {hook_path}")
    else:
        verb = "overwrote" if hook_path.exists() else "wrote"
        hook_path.write_text("#!/bin/sh\n\n" + entry, encoding="utf-8")
        print(f"install-hooks: {verb} {hook_path}")

    os.chmod(hook_path, os.stat(hook_path).st_mode | 0o111)
    print(
        "install-hooks: done. Re-run after each fresh clone to restore the hook."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
