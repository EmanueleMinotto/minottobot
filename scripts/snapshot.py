#!/usr/bin/env python3
"""Deterministic helpers for minottobot audit snapshots.

Three commands, all stdlib-only so the script runs wherever `python3` does:

    snapshot.py parse    <snapshot.md>                 -> JSON on stdout
    snapshot.py delta    <previous.md> <current.md>    -> markdown delta section
    snapshot.py validate <report.md> [--cap AREA=N]    -> violations, exit 1 if any

The script never *writes* a report — judgement (scores, findings, wording) stays
with the model. It parses what the model wrote, computes what is pure
arithmetic (score deltas, action item IDs, status transitions), and refuses
output that breaks the fixed format contract in skills/audit/SKILL.md and
skills/strategy/references/snapshot-delta.md.

Exit codes: 0 = clean, 1 = violations found, 2 = usage or parse error.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

SUPPORTED_FORMAT_VERSIONS = {1}

#: The six area rows, in the exact order the output contract fixes them.
CANONICAL_AREAS = [
    "CI/CD",
    "Testing",
    "Code review",
    "Monitoring",
    "Developer Experience",
    "Ownership & culture",
]

#: Blockers are prose, so they are matched by similarity rather than equality.
#: Above this ratio two blockers are considered the same one across sessions.
BLOCKER_MATCH_RATIO = 0.6


class ParseError(Exception):
    """Raised when an input file does not match the documented format."""


# --------------------------------------------------------------------------
# Low-level parsing helpers
# --------------------------------------------------------------------------


def _split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_body, rest). Frontmatter is optional."""
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    raise ParseError("frontmatter opened with '---' but never closed")


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_frontmatter(body: str) -> dict:
    """Parse the flat subset of YAML the snapshot format actually uses.

    Supported shapes are `key: value` and the `repos:` list of `- name:` /
    `tech:` pairs. Anything richer is a format change, not something to guess
    at, so unknown indented keys are ignored rather than misread.
    """
    data: dict = {}
    repos: list[dict] = []
    in_repos = False

    for raw in body.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        stripped = raw.strip()

        if not raw.startswith((" ", "\t", "-")):
            in_repos = stripped == "repos:"
            if in_repos:
                continue
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                data[key.strip()] = _unquote(value)
            continue

        if not in_repos:
            continue

        if stripped.startswith("- "):
            entry = stripped[2:].strip()
            repos.append({})
            if ":" in entry:
                key, _, value = entry.partition(":")
                repos[-1][key.strip()] = _unquote(value)
        elif repos and ":" in stripped:
            key, _, value = stripped.partition(":")
            repos[-1][key.strip()] = _unquote(value)

    if repos:
        data["repos"] = repos
    return data


def _sections(text: str) -> dict[str, list[str]]:
    """Map `## Heading` -> its lines. Deeper headings stay inside their parent."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^##\s+(?!#)(.*)$", line)
        if match:
            current = match.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def _find_section(sections: dict[str, list[str]], prefix: str) -> list[str]:
    """Look a section up by heading prefix — headings carry trailing detail.

    "Area scores (1 = critical · 5 = excellent)" and "Area scores" are the same
    section in the audit and snapshot formats respectively.
    """
    lowered = prefix.lower()
    for heading, lines in sections.items():
        if heading.lower().startswith(lowered):
            return lines
    return []


def _table_rows(lines: list[str]) -> list[list[str]]:
    """Return data rows of the first markdown table in `lines`, header dropped."""
    rows: list[list[str]] = []
    seen_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if seen_table and rows:
                break
            continue
        seen_table = True
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells if cell):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def _normalize_area(label: str) -> str:
    """Strip decoration (emoji, bold) so an area cell matches a canonical name."""
    cleaned = re.sub(r"[*`]", "", label)
    cleaned = re.sub(r"[^\w/&\s]", " ", cleaned, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    for area in CANONICAL_AREAS:
        if cleaned.lower() == area.lower():
            return area
    return cleaned


def _score_value(cell: str) -> int | None:
    """Read `2`, `2/5` or `**2/5**` as 2. Return None if it is not a score."""
    match = re.fullmatch(r"\**\s*([1-5])\s*(?:/\s*5)?\s*\**", cell.strip())
    return int(match.group(1)) if match else None


def _numbered_items(lines: list[str]) -> list[str]:
    """Collect `1. ...` list items, with bold and trailing punctuation stripped."""
    items = []
    for line in lines:
        match = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if match:
            items.append(re.sub(r"\*\*", "", match.group(1)).strip())
    return items


def _bullet_items(lines: list[str]) -> list[str]:
    items = []
    for line in lines:
        match = re.match(r"^\s*[-*]\s+(.*)$", line)
        if match:
            items.append(match.group(1).strip())
    return items


# --------------------------------------------------------------------------
# Snapshot model
# --------------------------------------------------------------------------


def parse_snapshot(path: Path) -> dict:
    """Parse a `.minottobot/audit-YYYY-MM-DD.md` snapshot into plain data."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ParseError(f"cannot read {path}: {exc}") from exc

    front_body, body = _split_frontmatter(text)
    front = _parse_frontmatter(front_body)
    sections = _sections(body)

    warnings: list[str] = []
    raw_version = front.get("format_version")
    if raw_version is None:
        warnings.append("no format_version in frontmatter — assuming 1")
        version = 1
    else:
        try:
            version = int(raw_version)
        except ValueError:
            raise ParseError(f"format_version is not an integer: {raw_version!r}")
        if version not in SUPPORTED_FORMAT_VERSIONS:
            warnings.append(
                f"format_version {version} is newer than this script understands "
                f"(supported: {sorted(SUPPORTED_FORMAT_VERSIONS)}) — "
                "fields may be missing"
            )

    scores: dict[str, int] = {}
    for row in _table_rows(_find_section(sections, "Area scores")):
        if len(row) < 2:
            continue
        area = _normalize_area(row[0])
        score = _score_value(row[1])
        if score is not None:
            scores[area] = score

    repos = []
    for repo in front.get("repos", []) or []:
        repos.append({"name": repo.get("name", ""), "tech": repo.get("tech", "")})
    if not repos:
        for bullet in _bullet_items(_find_section(sections, "Repos in scope")):
            match = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", bullet)
            if match:
                repos.append({"name": match.group(1).strip(), "tech": match.group(2).strip()})
            else:
                repos.append({"name": bullet, "tech": ""})

    actions = []
    for row in _table_rows(_find_section(sections, "Action items")):
        if len(row) < 2 or not re.fullmatch(r"A\d+", row[0].strip()):
            continue
        actions.append(
            {
                "id": row[0].strip(),
                "description": row[1].strip(),
                "horizon": row[2].strip() if len(row) > 2 else "",
                "owner": row[3].strip() if len(row) > 3 else "",
                "status": (row[4].strip() if len(row) > 4 else "") or "open",
            }
        )

    highest = max((int(a["id"][1:]) for a in actions), default=0)

    return {
        "path": str(path),
        "format_version": version,
        "date": front.get("date", ""),
        "team": front.get("team", ""),
        "repos": repos,
        "scores": scores,
        "blockers": _numbered_items(_find_section(sections, "Top 3 blockers")),
        "action_items": actions,
        "next_action_id": f"A{highest + 1}",
        "warnings": warnings,
    }


# --------------------------------------------------------------------------
# delta
# --------------------------------------------------------------------------


def _score_emoji(score: int) -> str:
    if score <= 2:
        return "🔴"
    if score == 3:
        return "🟡"
    return "🟢"


def _match_blockers(previous: list[str], current: list[str]) -> list[tuple[int, int]]:
    """Pair previous/current blockers by best similarity, greedily and stably."""
    candidates = []
    for i, old in enumerate(previous):
        for j, new in enumerate(current):
            ratio = difflib.SequenceMatcher(None, old.lower(), new.lower()).ratio()
            if ratio >= BLOCKER_MATCH_RATIO:
                candidates.append((-ratio, i, j))
    candidates.sort()

    pairs: list[tuple[int, int]] = []
    used_old: set[int] = set()
    used_new: set[int] = set()
    for _, i, j in candidates:
        if i in used_old or j in used_new:
            continue
        used_old.add(i)
        used_new.add(j)
        pairs.append((i, j))
    return sorted(pairs)


def build_delta(previous: dict, current: dict) -> str:
    """Render the `## Delta since {date}` section from two parsed snapshots."""
    out: list[str] = [f"## Delta since {previous['date'] or 'previous audit'}", ""]

    out.append("### Score changes")
    out.append("| Area | Previous | Current | Change |")
    out.append("|------|----------|---------|--------|")
    for area in CANONICAL_AREAS:
        old = previous["scores"].get(area)
        new = current["scores"].get(area)
        if new is None:
            continue
        if old is None:
            change = "new"
            old_cell = "—"
        else:
            diff = new - old
            change = "—" if diff == 0 else f"{'↑ +' if diff > 0 else '↓ -'}{abs(diff)}"
            old_cell = f"{old}/5"
        out.append(f"| {_score_emoji(new)} {area} | {old_cell} | {new}/5 | {change} |")
    out.append("")
    out.append("> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5")
    out.append("")

    pairs = _match_blockers(previous["blockers"], current["blockers"])
    still_open_old = {i for i, _ in pairs}
    still_open_new = {j for _, j in pairs}
    resolved = [b for i, b in enumerate(previous["blockers"]) if i not in still_open_old]
    still_open = [current["blockers"][j] for _, j in pairs]
    new_blockers = [b for j, b in enumerate(current["blockers"]) if j not in still_open_new]

    out.append("### Blockers")
    out.append(f"- **Resolved:** {'; '.join(resolved) if resolved else 'none'}")
    out.append(f"- **Still open:** {'; '.join(still_open) if still_open else 'none'}")
    out.append(f"- **New:** {'; '.join(new_blockers) if new_blockers else 'none'}")
    out.append("")

    old_actions = {a["id"]: a for a in previous["action_items"]}
    new_actions = {a["id"]: a for a in current["action_items"]}

    out.append("### Action items")
    out.append("| ID | Description | Status change |")
    out.append("|----|-------------|---------------|")
    for action_id in sorted(set(old_actions) | set(new_actions), key=lambda i: int(i[1:])):
        old = old_actions.get(action_id)
        new = new_actions.get(action_id)
        if old and new:
            if old["status"] == new["status"]:
                change = f"still {new['status']}"
            else:
                mark = "✓" if new["status"] == "done" else "○"
                change = f"○ {old['status']} → {mark} {new['status']}"
            description = new["description"]
        elif new:
            change = "new"
            description = new["description"]
        else:
            change = "dropped from plan"
            description = old["description"]
        out.append(f"| {action_id} | {description} | {change} |")
    out.append("")

    old_repos = {r["name"]: r for r in previous["repos"]}
    new_repos = {r["name"]: r for r in current["repos"]}
    scope: list[str] = []
    for name, repo in new_repos.items():
        if name not in old_repos:
            tech = f" ({repo['tech']})" if repo["tech"] else ""
            scope.append(f"- Added: {name}{tech} — no previous data to compare")
    for name in old_repos:
        if name not in new_repos:
            scope.append(f"- Removed: {name} — dropped from scope")
    if scope:
        out.append("### Repo scope")
        out.extend(scope)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------
# validate
# --------------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{(team|date|repo name|primary tech|score)\}")

REQUIRED_SECTIONS = {
    "audit": [
        "Repos in scope",
        "Phase 0 baseline",
        "Area scores",
        "Evidence & red flags",
        "Systems flagged for replacement evaluation",
    ],
    "report": [
        "Repos in scope",
        "Executive summary",
        "Area scores",
        "Top 3 blockers",
        "Improvement plan",
        "Action items",
    ],
    "snapshot": ["Repos in scope", "Area scores", "Top 3 blockers", "Action items"],
}


def _detect_kind(sections: dict[str, list[str]]) -> str:
    headings = " | ".join(sections).lower()
    if "executive summary" in headings:
        return "report"
    if "phase 0" in headings:
        return "audit"
    return "snapshot"


def validate(path: Path, caps: dict[str, int], kind: str = "auto") -> tuple[str, list[str]]:
    """Check a report or snapshot against the fixed output contract."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ParseError(f"cannot read {path}: {exc}") from exc

    _, body = _split_frontmatter(text)
    sections = _sections(body)
    if kind == "auto":
        kind = _detect_kind(sections)
    if kind not in REQUIRED_SECTIONS:
        raise ParseError(f"unknown kind {kind!r}")

    violations: list[str] = []

    for required in REQUIRED_SECTIONS[kind]:
        if not _find_section(sections, required):
            violations.append(f"missing or empty section: '## {required}'")

    score_lines = _find_section(sections, "Area scores")
    rows = _table_rows(score_lines)
    if not rows:
        violations.append("area scores table not found")
    else:
        found = [_normalize_area(row[0]) for row in rows if row]
        if found != CANONICAL_AREAS:
            violations.append(
                "area scores table must have exactly these six rows in order "
                f"{CANONICAL_AREAS} — found {found}"
            )
        for row in rows:
            if len(row) < 2:
                violations.append(f"area row has no score cell: {row}")
                continue
            area, cell = _normalize_area(row[0]), row[1].strip()
            if _score_value(cell) is None:
                violations.append(f"{area}: score cell {cell!r} is not a bare 1-5 value")
                continue
            if kind != "snapshot" and not re.fullmatch(r"\**\s*[1-5]\s*/\s*5\s*\**", cell):
                violations.append(f"{area}: score must be written as 'N/5', found {cell!r}")

    scores = {}
    for row in rows:
        if len(row) >= 2:
            value = _score_value(row[1])
            if value is not None:
                scores[_normalize_area(row[0])] = value

    for area, cap in caps.items():
        canonical = _normalize_area(area)
        if canonical not in CANONICAL_AREAS:
            violations.append(f"--cap names an unknown area: {area!r}")
            continue
        actual = scores.get(canonical)
        if actual is not None and actual > cap:
            violations.append(
                f"{canonical}: score {actual}/5 exceeds the mandatory cap of {cap}/5 "
                "triggered by the Phase 0 data"
            )

    for match in PLACEHOLDER_PATTERN.finditer(body):
        violations.append(f"unreplaced template placeholder: {match.group(0)}")
    if re.search(r"\[\s*score\s*\]", body):
        violations.append("score written as '[score]/5' — the brackets are a placeholder")

    return kind, violations


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _parse_caps(raw: list[str]) -> dict[str, int]:
    caps: dict[str, int] = {}
    for item in raw or []:
        if "=" not in item:
            raise ParseError(f"--cap expects AREA=N, got {item!r}")
        area, _, value = item.rpartition("=")
        try:
            caps[area.strip()] = int(value)
        except ValueError:
            raise ParseError(f"--cap value is not an integer: {item!r}") from None
    return caps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="snapshot.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="parse a snapshot into JSON")
    p_parse.add_argument("snapshot", type=Path)

    p_delta = sub.add_parser("delta", help="render the delta between two snapshots")
    p_delta.add_argument("previous", type=Path)
    p_delta.add_argument("current", type=Path)

    p_validate = sub.add_parser("validate", help="check a report against the output contract")
    p_validate.add_argument("report", type=Path)
    p_validate.add_argument(
        "--cap",
        action="append",
        default=[],
        metavar="AREA=N",
        help="mandatory score cap triggered by Phase 0 data, e.g. 'Ownership & culture=2'",
    )
    p_validate.add_argument(
        "--kind", choices=["auto", "audit", "report", "snapshot"], default="auto"
    )

    args = parser.parse_args(argv)

    try:
        if args.command == "parse":
            data = parse_snapshot(args.snapshot)
            for warning in data["warnings"]:
                print(f"warning: {warning}", file=sys.stderr)
            json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
            print()
            return 0

        if args.command == "delta":
            previous = parse_snapshot(args.previous)
            current = parse_snapshot(args.current)
            for source, data in (("previous", previous), ("current", current)):
                for warning in data["warnings"]:
                    print(f"warning ({source}): {warning}", file=sys.stderr)
            sys.stdout.write(build_delta(previous, current))
            return 0

        kind, violations = validate(args.report, _parse_caps(args.cap), args.kind)
        if not violations:
            print(f"OK — {args.report} is a valid '{kind}' output")
            return 0
        print(f"{len(violations)} violation(s) in {args.report} (kind: {kind}):", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        return 1

    except ParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
