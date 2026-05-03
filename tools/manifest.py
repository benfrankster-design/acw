#!/usr/bin/env python3
# ---
# class: operational
# authority: canonical
# stability: experimental
# loaded_by_agent: yes
# ---
"""
manifest.py — reference implementation of the manifest-tooling spec.

See `rules/manifest-discipline.md` for the four-operation contract.

Operations:
    load(state_file, list_name)       → list or dict (with canonical defaults)
    append(state_file, list_name, v)  → True if changed, False if already present
    contains(state_file, list_name, v)→ bool
    validate(state_file, list_name)   → None; raises ManifestError on schema error

Stdlib only. UTF-8. LF line endings on write.

Limitations (v1):
- `instance_layer` (list of dicts with multi-field items) is not supported.
  Consumers needing it implement their own multi-line item construction.
- Comments between list items survive but inline comments on individual
  items may not be preserved when items near them are modified.
- Block ordering is preserved; appended entries land at the end of the block.
"""

import re
import sys
from pathlib import Path
from typing import Union

CANONICAL_DEFAULTS: dict[str, dict[str, str]] = {
    "paths": {
        "decisions_log": "decisions/decision-log.md",
        "tasks_status": "tasks-status.md",
        "build_log": "build-log.md",
        "glossary": "glossary.md",
        "threat_model": "threat-model.md",
        "incidents": "incidents.jsonl",
        "evolution": "research/evolution.md",
        "sources": "research/sources.md",
        "research_state": "research/research-state.yaml",
        "problem_framing": "research/01-problem-framing.md",
        "session_captures_dir": "research/sessions",
        "research_queries_dir": "research/queries",
        "research_queries_consumed_dir": "research/queries/_consumed",
        "buffer_dir": "_buffer",
        "runbooks_dir": "runbooks",
        "integrations_dir": "integrations",
        "briefings_dir": "briefings",
        "context_dir": "context",
        "inbox_dir": "inbox",
    },
}

KNOWN_LISTS: set[str] = {
    "template_layer",
    "meta_layer",
    "empty_dirs",
    "auto_load_at_session_start",
    "cross_repo_writes",
    "voice",
}

KNOWN_DICTS: set[str] = {"paths", "project"}

UNSUPPORTED: set[str] = {"instance_layer"}


class ManifestError(Exception):
    """Raised on unknown blocks, schema errors, or validation failures."""


def _read_lines(state_file: Path) -> list[str]:
    return state_file.read_text(encoding="utf-8").splitlines(keepends=True)


def _write_lines(state_file: Path, lines: list[str]) -> None:
    with state_file.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("".join(lines))


def _find_block(lines: list[str], name: str) -> Union[tuple[int, int], None]:
    """Return [start, end) for the named block, or None if absent.

    Block start: first line matching `^name:`.
    Block end: first line at indent 0 (and not blank or comment) after start.
    """
    pattern = re.compile(rf"^{re.escape(name)}:\s*(.*)$")
    start = None
    for i, line in enumerate(lines):
        if pattern.match(line):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        stripped_line = lines[j].rstrip("\n")
        if stripped_line == "" or stripped_line.lstrip().startswith("#"):
            continue
        if not stripped_line.startswith((" ", "\t")):
            end = j
            break
    return (start, end)


def _strip_inline_comment(value: str) -> str:
    """Strip an inline `#` comment outside of quoted strings."""
    if not value:
        return ""
    if value[0] in ('"', "'"):
        quote = value[0]
        end = value.find(quote, 1)
        if end == -1:
            return value
        return value[: end + 1]
    idx = value.find("#")
    if idx == -1:
        return value.strip()
    return value[:idx].strip()


def _parse_scalar(raw: str) -> Union[str, None]:
    """Parse a yaml scalar into a Python string (or None for null)."""
    raw = _strip_inline_comment(raw).strip()
    if raw == "" or raw == "null" or raw == "~":
        return None
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ('"', "'"):
        return raw[1:-1]
    return raw


def _parse_inline_list(inline: str) -> list[str]:
    """Parse an inline yaml list like `[a, b, c]`."""
    content = inline.strip()
    if content == "[]":
        return []
    if not (content.startswith("[") and content.endswith("]")):
        return []
    body = content[1:-1].strip()
    if not body:
        return []
    return [v.strip().strip('"').strip("'") for v in body.split(",") if v.strip()]


def _parse_list_block(lines: list[str], start: int, end: int) -> list[str]:
    header = lines[start].rstrip("\n")
    inline = header.split(":", 1)[1].strip() if ":" in header else ""
    if inline:
        return _parse_inline_list(inline)
    items: list[str] = []
    for j in range(start + 1, end):
        line = lines[j].rstrip("\n")
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            value = _parse_scalar(stripped[2:])
            if value is not None:
                items.append(value)
    return items


def _parse_dict_block(lines: list[str], start: int, end: int) -> dict[str, str]:
    header = lines[start].rstrip("\n")
    inline = header.split(":", 1)[1].strip() if ":" in header else ""
    if inline == "{}":
        return {}
    items: dict[str, str] = {}
    for j in range(start + 1, end):
        line = lines[j].rstrip("\n")
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            parsed = _parse_scalar(value)
            if parsed is not None:
                items[key] = parsed
    return items


def _check_known(list_name: str) -> None:
    if list_name in UNSUPPORTED:
        raise ManifestError(f"{list_name!r} is not supported by this implementation")
    if list_name not in KNOWN_LISTS and list_name not in KNOWN_DICTS:
        raise ManifestError(f"unknown manifest block: {list_name!r}")


def load(state_file: Path, list_name: str):
    """Read a manifest block. Returns list or dict with defaults applied."""
    _check_known(list_name)
    lines = _read_lines(state_file)
    block = _find_block(lines, list_name)

    if list_name in KNOWN_DICTS:
        defaults = CANONICAL_DEFAULTS.get(list_name, {})
        if block is None:
            return dict(defaults)
        parsed = _parse_dict_block(lines, block[0], block[1])
        return {**defaults, **parsed}

    if block is None:
        return []
    return _parse_list_block(lines, block[0], block[1])


def append(state_file: Path, list_name: str, value) -> bool:
    """Add value to the named block. Returns True if file changed, False if no-op."""
    _check_known(list_name)

    if list_name in KNOWN_DICTS:
        if not (isinstance(value, tuple) and len(value) == 2):
            raise ManifestError(
                f"dict block {list_name!r} requires (key, value) tuple"
            )
        key, val = value
        return _append_to_dict(state_file, list_name, key, val)

    return _append_to_list(state_file, list_name, value)


def _append_to_list(state_file: Path, list_name: str, value: str) -> bool:
    lines = _read_lines(state_file)
    block = _find_block(lines, list_name)

    if block is None:
        # Block absent — create it at end of file
        if lines and not lines[-1].endswith("\n"):
            lines[-1] = lines[-1] + "\n"
        lines.append(f"\n{list_name}:\n")
        lines.append(f"  - {value}\n")
        _write_lines(state_file, lines)
        return True

    start, end = block
    parsed = _parse_list_block(lines, start, end)
    if value in parsed:
        return False

    # Inline empty list `name: []` → convert to multi-line
    header = lines[start].rstrip("\n")
    inline = header.split(":", 1)[1].strip() if ":" in header else ""
    if inline == "[]":
        lines[start] = f"{list_name}:\n"
        lines.insert(start + 1, f"  - {value}\n")
        _write_lines(state_file, lines)
        return True

    # Find insertion point: after last non-blank, non-comment line in block
    insert_idx = end
    for j in range(end - 1, start, -1):
        stripped = lines[j].rstrip("\n").rstrip()
        if stripped and not stripped.lstrip().startswith("#"):
            insert_idx = j + 1
            break

    lines.insert(insert_idx, f"  - {value}\n")
    _write_lines(state_file, lines)
    return True


def _append_to_dict(state_file: Path, list_name: str, key: str, val: str) -> bool:
    lines = _read_lines(state_file)
    block = _find_block(lines, list_name)

    if block is None:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] = lines[-1] + "\n"
        lines.append(f"\n{list_name}:\n")
        lines.append(f"  {key}: {val}\n")
        _write_lines(state_file, lines)
        return True

    start, end = block
    parsed = _parse_dict_block(lines, start, end)
    if parsed.get(key) == val:
        return False

    # Inline empty dict `name: {}` → convert to multi-line
    header = lines[start].rstrip("\n")
    inline = header.split(":", 1)[1].strip() if ":" in header else ""
    if inline == "{}":
        lines[start] = f"{list_name}:\n"
        lines.insert(start + 1, f"  {key}: {val}\n")
        _write_lines(state_file, lines)
        return True

    # Update existing key in place if present
    key_pattern = re.compile(rf"^(\s+){re.escape(key)}\s*:")
    for j in range(start + 1, end):
        m = key_pattern.match(lines[j])
        if m:
            indent = m.group(1)
            lines[j] = f"{indent}{key}: {val}\n"
            _write_lines(state_file, lines)
            return True

    # Insert new key at end of block
    insert_idx = end
    for j in range(end - 1, start, -1):
        stripped = lines[j].rstrip("\n").rstrip()
        if stripped and not stripped.lstrip().startswith("#"):
            insert_idx = j + 1
            break
    lines.insert(insert_idx, f"  {key}: {val}\n")
    _write_lines(state_file, lines)
    return True


def contains(state_file: Path, list_name: str, value) -> bool:
    """Check membership. For dict blocks, checks key presence."""
    _check_known(list_name)
    loaded = load(state_file, list_name)
    return value in loaded


def validate(state_file: Path, list_name: str) -> None:
    """Validate the named block. Raises ManifestError on schema failure."""
    _check_known(list_name)
    lines = _read_lines(state_file)
    block = _find_block(lines, list_name)
    if block is None:
        return

    if list_name in KNOWN_DICTS:
        parsed = _parse_dict_block(lines, block[0], block[1])
        for key, val in parsed.items():
            if not isinstance(val, str):
                raise ManifestError(f"{list_name}.{key} is not a string")
        return

    parsed_list = _parse_list_block(lines, block[0], block[1])
    seen: set[str] = set()
    for item in parsed_list:
        if item in seen:
            raise ManifestError(f"duplicate entry in {list_name}: {item!r}")
        seen.add(item)


def main(argv: list[str]) -> int:
    """Minimal CLI: `manifest.py load STATE_FILE LIST_NAME` etc."""
    if len(argv) < 3:
        print("usage: manifest.py {load|contains|validate} STATE_FILE LIST_NAME [VALUE]", file=sys.stderr)
        return 2
    op = argv[0]
    state_file = Path(argv[1])
    list_name = argv[2]
    try:
        if op == "load":
            print(load(state_file, list_name))
            return 0
        if op == "contains":
            if len(argv) < 4:
                print("contains requires a value", file=sys.stderr)
                return 2
            print(contains(state_file, list_name, argv[3]))
            return 0
        if op == "validate":
            validate(state_file, list_name)
            print("ok")
            return 0
    except ManifestError as exc:
        print(f"manifest: {exc}", file=sys.stderr)
        return 1
    print(f"unknown op: {op}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
