#!/usr/bin/env python3
# ---
# class: operational
# authority: canonical
# stability: experimental
# loaded_by_agent: yes
# ---
"""
log-incident.py — Incident ledger + deferred-library drift detector.

Subcommands:
    log <primitive> <severity> <symptom> [--operator NAME] [--category CAT]
        Append a JSON line to incidents.jsonl. Severity: low|med|high.
        Category (optional): implementation-bug|governance-leak|environment-state|
        process-gap|wrong-assumption|scale-vulnerability|earn-by-incident.
    count --primitive NAME
        Count med+high incidents for a primitive.
    check-drift
        Walk deferred/ subfolders, compare each README against DEFERRED.md.
        Exit 1 if drift found.

Stdlib only. UTC timestamps. LF line endings. Binary-mode writes.

Exit codes:
    0 — success / no drift
    1 — soft failure / drift found / primitive count exceeded threshold (check-drift only)
    2 — bad input
"""

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

LEDGER = Path("incidents.jsonl")
SEVERITIES = {"low", "med", "high"}
CATEGORIES = {
    "implementation-bug",
    "governance-leak",
    "environment-state",
    "process-gap",
    "wrong-assumption",
    "scale-vulnerability",
    "earn-by-incident",
}


def cmd_log(args: argparse.Namespace) -> int:
    if args.severity not in SEVERITIES:
        print(f"log-incident: severity must be one of {sorted(SEVERITIES)}", file=sys.stderr)
        return 2
    if args.category and args.category not in CATEGORIES:
        print(f"log-incident: category must be one of {sorted(CATEGORIES)}", file=sys.stderr)
        return 2
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "primitive": args.primitive,
        "severity": args.severity,
        "symptom": args.symptom,
        "operator": args.operator or os.environ.get("ACW_OPERATOR", "operator"),
    }
    if args.category:
        entry["category"] = args.category
    line = (json.dumps(entry, ensure_ascii=False) + "\n").encode("utf-8")
    with LEDGER.open("ab") as fh:
        fh.write(line)
    print(f"logged: {entry['id']}")
    return 0


def cmd_count(args: argparse.Namespace) -> int:
    if not LEDGER.is_file():
        print(0)
        return 0
    count = 0
    with LEDGER.open("rb") as fh:
        for raw in fh:
            try:
                obj = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if obj.get("primitive") == args.primitive and obj.get("severity") in {"med", "high"}:
                count += 1
    print(count)
    return 0


DEFERRED_ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*([a-z0-9-]+)\s*\|\s*[^|]+\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|\s*$"
)


def parse_deferred_md(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        m = DEFERRED_ROW.match(line)
        if m:
            name, summary, trigger, pointer = m.groups()
            rows[name.strip()] = {
                "summary": summary.strip(),
                "trigger": trigger.strip(),
                "pointer": pointer.strip(),
            }
    return rows


def parse_subfolder_readme(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    result: dict[str, str] = {}
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        result["heading"] = m.group(1).strip()
    # Capture the full Activation trigger section — from its heading to the next
    # heading or end of file. Short intro paragraphs followed by numbered lists
    # would otherwise be truncated at the first blank line.
    m = re.search(
        r"(?im)^#{1,6}\s*activation trigger\b[^\n]*\n(.+?)(?=\n#{1,6}\s|\Z)",
        text,
        re.DOTALL,
    )
    if m:
        result["trigger"] = " ".join(m.group(1).split())
    return result


def cmd_check_drift(args: argparse.Namespace) -> int:
    deferred_md = Path("DEFERRED.md")
    deferred_dir = Path("deferred")
    if not deferred_md.is_file() or not deferred_dir.is_dir():
        print("check-drift: DEFERRED.md or deferred/ not found", file=sys.stderr)
        return 2

    canonical = parse_deferred_md(deferred_md)
    if not canonical:
        print("check-drift: no canonical rows parsed from DEFERRED.md", file=sys.stderr)
        return 2

    drift_found = False
    canonical_names = set(canonical.keys())
    subfolder_names = {p.name for p in deferred_dir.iterdir() if p.is_dir()}

    missing_subfolders = canonical_names - subfolder_names
    extra_subfolders = subfolder_names - canonical_names

    for name in sorted(missing_subfolders):
        print(f"drift: DEFERRED.md lists '{name}' but deferred/{name}/ does not exist")
        drift_found = True
    for name in sorted(extra_subfolders):
        if name == "README.md":
            continue
        print(f"drift: deferred/{name}/ exists but not in DEFERRED.md")
        drift_found = True

    for name in sorted(canonical_names & subfolder_names):
        readme = deferred_dir / name / "README.md"
        parsed = parse_subfolder_readme(readme)
        if not parsed:
            print(f"drift: deferred/{name}/README.md unreadable or missing")
            drift_found = True
            continue
        canon_trigger = canonical[name]["trigger"].lower()
        sub_trigger = parsed.get("trigger", "").lower()
        if sub_trigger and canon_trigger and not _trigger_match(canon_trigger, sub_trigger):
            print(f"drift: deferred/{name}/README.md trigger does not match DEFERRED.md row")
            drift_found = True

    return 1 if drift_found else 0


def _trigger_match(a: str, b: str) -> bool:
    """Coarse match — look for significant token overlap."""
    tokens_a = {t for t in re.findall(r"\w+", a) if len(t) > 3}
    tokens_b = {t for t in re.findall(r"\w+", b) if len(t) > 3}
    if not tokens_a or not tokens_b:
        return True
    overlap = tokens_a & tokens_b
    return len(overlap) >= max(2, len(tokens_a) // 3)


def main() -> int:
    parser = argparse.ArgumentParser(description="ACW incident ledger")
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_log = sub.add_parser("log", help="Append an incident")
    p_log.add_argument("primitive")
    p_log.add_argument("severity")
    p_log.add_argument("symptom")
    p_log.add_argument("--operator", default=None)
    p_log.add_argument("--category", default=None,
        help=f"Optional category. One of: {', '.join(sorted(CATEGORIES))}")
    p_log.set_defaults(func=cmd_log)

    p_count = sub.add_parser("count", help="Count med+high incidents for a primitive")
    p_count.add_argument("--primitive", required=True)
    p_count.set_defaults(func=cmd_count)

    p_drift = sub.add_parser("check-drift", help="Check DEFERRED.md vs deferred/ subfolders")
    p_drift.set_defaults(func=cmd_check_drift)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
