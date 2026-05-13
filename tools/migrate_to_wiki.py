#!/usr/bin/env python3
"""
migrate_to_wiki.py — Split a single-file decisions log and glossary into
Karpathy-wiki shape (atomic per-entry files + INDEX).

Usage:
    python tools/migrate_to_wiki.py [WORKSPACE_ROOT]

Defaults to current working directory. Idempotent: re-running regenerates
INDEX files from existing entries/.

Splits:
    decisions/decision-log.md   ->  decisions/INDEX.md
                                    decisions/entries/<id>-<slug>.md
                                    decisions/open-questions/<id>-<slug>.md
                                    decisions/constraints/<id>-<slug>.md
    glossary.md                 ->  glossary/INDEX.md
                                    glossary/entries/<slug>.md

Leaves the source files in place; operator removes them after verifying.
"""
from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


def slugify(text: str, maxlen: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:maxlen].rstrip("-")


@dataclass
class Entry:
    id: str
    title: str
    body: str
    kind: str          # decision | open-question | constraint
    status: str
    date_str: str


HEADING_RE = re.compile(r"^###\s+(?P<id>[A-Z][A-Z0-9-]+|D-[A-Z]+-\d+|Q-\d+|C-\d+|OQ-\d+|CG-\d+)\s*[—-]\s*(?P<title>.+?)\s*$")


def parse_decision_log(text: str) -> list[Entry]:
    sections = re.split(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
    # sections = [preface, name1, body1, name2, body2, ...]
    entries: list[Entry] = []
    for i in range(1, len(sections), 2):
        section_name = sections[i].strip()
        section_body = sections[i + 1]
        kind = section_kind(section_name)
        if kind is None:
            continue
        entries.extend(parse_section(section_body, kind))
    return entries


def section_kind(name: str) -> str | None:
    n = name.lower()
    if "open question" in n:
        return "open-question"
    if "decision" in n and "rationale" in n:
        return "decision"
    if "constraint" in n:
        return "constraint"
    if "resolved" in n:
        return "decision"  # resolved questions become decisions
    return None


def parse_section(body: str, kind: str) -> list[Entry]:
    chunks = re.split(r"^###\s+", body, flags=re.MULTILINE)
    entries = []
    for chunk in chunks[1:]:
        # chunk starts with "<id> — <title>\n<rest>"
        first_line, _, rest = chunk.partition("\n")
        m = re.match(r"(?P<id>\S+)\s*[—-]\s*(?P<title>.+?)\s*$", first_line)
        if not m:
            continue
        eid = m.group("id").strip()
        title = m.group("title").strip()
        body_text = rest.strip()
        # Strip trailing horizontal rules and orphan separators
        body_text = re.sub(r"\n+---\s*$", "", body_text).rstrip()
        date_str = extract_date(body_text) or date.today().isoformat()
        status = derive_status(kind, body_text)
        entries.append(Entry(id=eid, title=title, body=body_text, kind=kind,
                             status=status, date_str=date_str))
    return entries


DATE_RE = re.compile(r"\*\*Date(?: raised)?:\*\*\s*(\d{4}-\d{2}-\d{2})")


def extract_date(body: str) -> str | None:
    m = DATE_RE.search(body)
    return m.group(1) if m else None


def derive_status(kind: str, body: str) -> str:
    if kind == "decision":
        return "accepted"
    if kind == "open-question":
        if re.search(r"\*\*Status:\*\*.*resolved", body, re.IGNORECASE):
            return "resolved"
        return "open"
    if kind == "constraint":
        return "active"
    return "accepted"


def write_entry(root: Path, entry: Entry) -> Path:
    subdir = {"decision": "entries",
              "open-question": "open-questions",
              "constraint": "constraints"}[entry.kind]
    out_dir = root / "decisions" / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(entry.title)
    fname = f"{entry.id}-{slug}.md"
    path = out_dir / fname
    fm = (
        "---\n"
        f"id: {entry.id}\n"
        f"title: \"{entry.title.replace('\"', '\\\"')}\"\n"
        f"date: {entry.date_str}\n"
        f"status: {entry.status}\n"
        f"kind: {entry.kind}\n"
        f"updated: {date.today().isoformat()}\n"
        "---\n\n"
        f"# {entry.id} — {entry.title}\n\n"
        f"{entry.body}\n"
    )
    path.write_text(fm, encoding="utf-8")
    return path


def write_decisions_index(root: Path, entries: list[Entry]) -> None:
    decisions = sorted([e for e in entries if e.kind == "decision"],
                       key=lambda e: e.date_str, reverse=True)
    open_qs = sorted([e for e in entries if e.kind == "open-question"],
                     key=lambda e: e.date_str, reverse=True)
    constraints = sorted([e for e in entries if e.kind == "constraint"],
                         key=lambda e: e.id)
    lines = [
        "---",
        "class: operational",
        "authority: canonical",
        "stability: experimental",
        "loaded_by_agent: yes",
        "---",
        "",
        "# Decisions Index",
        "",
        "Auto-loaded thin index. Bodies live in `entries/`, `open-questions/`, `constraints/`.",
        "Regenerate with `python tools/migrate_to_wiki.py`.",
        "",
        "Archived entries: see `decision-log-YYYY-Q*.md` files in this directory.",
        "",
        "## Open Questions",
        "",
    ]
    if not open_qs:
        lines.append("_(none)_")
    for e in open_qs:
        slug = slugify(e.title)
        lines.append(f"- [{e.id}](open-questions/{e.id}-{slug}.md) — {e.title} _(status: {e.status})_")
    lines += ["", "## Decisions", ""]
    for e in decisions:
        slug = slugify(e.title)
        lines.append(f"- [{e.id}](entries/{e.id}-{slug}.md) — {e.title} _({e.date_str})_")
    lines += ["", "## Constraints and Gotchas", ""]
    if not constraints:
        lines.append("_(none)_")
    for e in constraints:
        slug = slugify(e.title)
        lines.append(f"- [{e.id}](constraints/{e.id}-{slug}.md) — {e.title}")
    lines.append("")
    (root / "decisions" / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def parse_glossary(text: str) -> list[tuple[str, str]]:
    chunks = re.split(r"^##\s+", text, flags=re.MULTILINE)
    terms = []
    for chunk in chunks[1:]:
        first_line, _, rest = chunk.partition("\n")
        term = first_line.strip()
        body = rest.strip().rstrip("-").rstrip()
        # strip trailing horizontal rules
        body = re.sub(r"\n+---\s*$", "", body).rstrip()
        if term:
            terms.append((term, body))
    return terms


def write_glossary(root: Path, terms: list[tuple[str, str]]) -> None:
    entries_dir = root / "glossary" / "entries"
    entries_dir.mkdir(parents=True, exist_ok=True)
    for term, body in terms:
        slug = slugify(term)
        fm = (
            "---\n"
            f"term: \"{term}\"\n"
            "status: active\n"
            f"updated: {date.today().isoformat()}\n"
            "---\n\n"
            f"# {term}\n\n"
            f"{body}\n"
        )
        (entries_dir / f"{slug}.md").write_text(fm, encoding="utf-8")
    # INDEX
    lines = [
        "---",
        "class: reference",
        "authority: canonical",
        "stability: experimental",
        "loaded_by_agent: yes",
        "---",
        "",
        "# Glossary Index",
        "",
        "Auto-loaded. Bodies live in `entries/`. Regenerate with `python tools/migrate_to_wiki.py`.",
        "",
        "## Terms",
        "",
    ]
    for term, _ in sorted(terms, key=lambda t: t[0].lower()):
        slug = slugify(term)
        lines.append(f"- [{term}](entries/{slug}.md)")
    lines.append("")
    (root / "glossary" / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    if not root.exists():
        print(f"workspace root not found: {root}", file=sys.stderr)
        return 2

    decisions_src = root / "decisions" / "decision-log.md"
    glossary_src = root / "glossary.md"

    if decisions_src.exists():
        text = decisions_src.read_text(encoding="utf-8")
        entries = parse_decision_log(text)
        for e in entries:
            write_entry(root, e)
        write_decisions_index(root, entries)
        print(f"decisions: {len(entries)} entries written; INDEX regenerated")
    else:
        print(f"skip: {decisions_src} not found")

    if glossary_src.exists():
        text = glossary_src.read_text(encoding="utf-8")
        terms = parse_glossary(text)
        write_glossary(root, terms)
        print(f"glossary: {len(terms)} terms written; INDEX regenerated")
    else:
        print(f"skip: {glossary_src} not found")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
