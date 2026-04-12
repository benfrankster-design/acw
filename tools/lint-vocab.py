#!/usr/bin/env python3
# ---
# class: operational
# authority: canonical
# stability: experimental
# loaded_by_agent: yes
# ---
"""
lint-vocab.py — Vocabulary linter for ACW instances.

Parses a glossary.md for forbidden-synonym blocks, optionally merges hidden_labels
from canon.yaml approved entries, and scans a content directory for violations.

Stdlib only. UTF-8 everywhere. Regex with word boundaries, case-insensitive.

CLI:
    python lint-vocab.py <glossary.md> [--canon <canon.yaml>] [--content-dir <path>]

Exit codes:
    0 — clean
    1 — violations found
    2 — bad input (missing file, parse error)
"""

import argparse
import re
import sys
from pathlib import Path

FORBIDDEN_BLOCK = re.compile(
    r"\*\*forbidden synonyms:\*\*\s*(.+?)(?:\n\n|\n\*\*|\Z)",
    re.IGNORECASE | re.DOTALL,
)
TERM_HEADING = re.compile(r"^#{2,4}\s+(.+?)\s*$", re.MULTILINE)


def parse_glossary(path: Path) -> dict[str, str]:
    """Return {forbidden_term_lower: canonical_term}."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"lint-vocab: cannot read glossary {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    forbidden: dict[str, str] = {}
    # Walk sections: for each heading, look for a forbidden-synonyms block under it.
    headings = list(TERM_HEADING.finditer(text))
    for i, match in enumerate(headings):
        canonical = match.group(1).strip()
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[start:end]
        for block in FORBIDDEN_BLOCK.finditer(section):
            raw = block.group(1)
            for token in re.split(r"[,\n]", raw):
                tok = token.strip().strip("`*-").strip()
                if tok:
                    forbidden[tok.lower()] = canonical
    return forbidden


def parse_canon_hidden_labels(path: Path) -> dict[str, str]:
    """Extract hidden_labels from approved canon entries without requiring PyYAML."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"lint-vocab: cannot read canon {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    hidden: dict[str, str] = {}
    current_pref: str | None = None
    current_hidden: list[str] = []
    current_state: str | None = None

    def flush():
        if current_pref and current_state == "approved":
            for h in current_hidden:
                hidden[h.lower()] = current_pref

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- concept_id:") or stripped.startswith("- pref_label:"):
            flush()
            current_pref = None
            current_hidden = []
            current_state = None
        if stripped.startswith("pref_label:"):
            current_pref = stripped.split(":", 1)[1].strip().strip("\"'")
        elif stripped.startswith("state:"):
            current_state = stripped.split(":", 1)[1].strip().strip("\"'")
        elif stripped.startswith("hidden_labels:"):
            remainder = stripped.split(":", 1)[1].strip()
            if remainder.startswith("[") and remainder.endswith("]"):
                items = remainder[1:-1].split(",")
                current_hidden = [i.strip().strip("\"'") for i in items if i.strip()]
    flush()
    return hidden


def scan_file(path: Path, forbidden: dict[str, str]) -> list[tuple[Path, int, int, str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    violations = []
    for term, canonical in forbidden.items():
        pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE | re.MULTILINE)
        for m in pattern.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            line_start = text.rfind("\n", 0, m.start()) + 1
            col = m.start() - line_start + 1
            violations.append((path, line_no, col, m.group(0), canonical))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="ACW vocabulary linter")
    parser.add_argument("glossary", help="Path to glossary.md")
    parser.add_argument("--canon", help="Optional canon.yaml path")
    parser.add_argument("--content-dir", default=".", help="Directory to scan (default: cwd)")
    args = parser.parse_args()

    glossary_path = Path(args.glossary)
    if not glossary_path.is_file():
        print(f"lint-vocab: glossary not found: {glossary_path}", file=sys.stderr)
        return 2

    forbidden = parse_glossary(glossary_path)
    if args.canon:
        canon_path = Path(args.canon)
        if canon_path.is_file():
            forbidden.update(parse_canon_hidden_labels(canon_path))

    if not forbidden:
        return 0

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        print(f"lint-vocab: content dir not found: {content_dir}", file=sys.stderr)
        return 2

    all_violations = []
    for md_path in content_dir.rglob("*.md"):
        if md_path.resolve() == glossary_path.resolve():
            continue
        all_violations.extend(scan_file(md_path, forbidden))

    if not all_violations:
        return 0

    for path, line, col, found, canonical in all_violations:
        print(f"{path}:{line}:{col}: forbidden synonym '{found}' (canonical: '{canonical}')")
    return 1


if __name__ == "__main__":
    sys.exit(main())
