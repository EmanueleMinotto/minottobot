"""Unit tests for scripts/snapshot.py.

These run without an LLM: everything under test is pure parsing, arithmetic,
or contract checking. The deepeval suites under evals/ still cover the parts
that are genuinely judgement calls.
"""

import json
import re
import textwrap

import pytest

import snapshot

PREVIOUS = """\
---
format_version: 1
date: 2026-01-15
team: "Acme Checkout squad"
repos:
  - name: "checkout-web"
    tech: "React"
  - name: "checkout-api"
    tech: "Node"
---

# minottobot audit snapshot — Acme Checkout squad — 2026-01-15

## Repos in scope
- checkout-web (React)
- checkout-api (Node)

## Area scores
| Area | Score |
|------|-------|
| CI/CD | 2 |
| Testing | 1 |
| Code review | 3 |
| Monitoring | 2 |
| Developer Experience | 2 |
| Ownership & culture | 3 |

## Top 3 blockers
1. Flaky suite: around 30% of tests fail intermittently and are ignored.
2. Jenkins full build takes 47 minutes, blocking every merge.
3. No named owner for checkout-api since the reorg.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Quarantine flaky tests | short | QA guild | open |
| A2 | Split the Jenkins pipeline | short | CI team | open |
| A3 | Assign an owner to checkout-api | medium | CTO | open |
"""

CURRENT = """\
---
format_version: 1
date: 2026-04-27
team: "Acme Checkout squad"
repos:
  - name: "checkout-web"
    tech: "React"
  - name: "checkout-infra"
    tech: "Terraform"
---

# minottobot audit snapshot — Acme Checkout squad — 2026-04-27

## Repos in scope
- checkout-web (React)
- checkout-infra (Terraform)

## Area scores
| Area | Score |
|------|-------|
| CI/CD | 4 |
| Testing | 1 |
| Code review | 3 |
| Monitoring | 1 |
| Developer Experience | 3 |
| Ownership & culture | 3 |

## Top 3 blockers
1. Flaky suite: roughly 30% of tests still fail intermittently and get ignored.
2. No named owner for checkout-api since the reorg.
3. Monitoring was switched off during the Terraform migration.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Quarantine flaky tests | short | QA guild | done |
| A2 | Split the Jenkins pipeline | short | CI team | open |
| A4 | Restore Sentry alert routing | short | SRE | open |
"""


@pytest.fixture
def previous(tmp_path):
    path = tmp_path / "audit-2026-01-15.md"
    path.write_text(PREVIOUS, encoding="utf-8")
    return path


@pytest.fixture
def current(tmp_path):
    path = tmp_path / "audit-2026-04-27.md"
    path.write_text(CURRENT, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# parse
# --------------------------------------------------------------------------


def test_parse_reads_frontmatter_scores_and_actions(previous):
    data = snapshot.parse_snapshot(previous)

    assert data["date"] == "2026-01-15"
    assert data["team"] == "Acme Checkout squad"
    assert data["repos"] == [
        {"name": "checkout-web", "tech": "React"},
        {"name": "checkout-api", "tech": "Node"},
    ]
    assert data["scores"] == {
        "CI/CD": 2,
        "Testing": 1,
        "Code review": 3,
        "Monitoring": 2,
        "Developer Experience": 2,
        "Ownership & culture": 3,
    }
    assert len(data["blockers"]) == 3
    assert [a["id"] for a in data["action_items"]] == ["A1", "A2", "A3"]
    assert data["warnings"] == []


def test_next_action_id_continues_past_the_highest_previous_id(previous):
    assert snapshot.parse_snapshot(previous)["next_action_id"] == "A4"


def test_next_action_id_is_a1_when_there_are_no_action_items(tmp_path):
    path = tmp_path / "audit-2026-01-01.md"
    path.write_text("---\nformat_version: 1\ndate: 2026-01-01\n---\n\n## Area scores\n", "utf-8")
    assert snapshot.parse_snapshot(path)["next_action_id"] == "A1"


def test_parse_accepts_n_slash_5_scores_as_well_as_bare_numbers(tmp_path):
    path = tmp_path / "audit-2026-02-01.md"
    path.write_text(
        "---\nformat_version: 1\ndate: 2026-02-01\n---\n\n"
        "## Area scores\n| Area | Score |\n|---|---|\n| CI/CD | 3/5 |\n",
        encoding="utf-8",
    )
    assert snapshot.parse_snapshot(path)["scores"] == {"CI/CD": 3}


def test_parse_falls_back_to_the_repos_section_without_frontmatter_repos(tmp_path):
    path = tmp_path / "audit-2026-02-01.md"
    path.write_text(
        "---\nformat_version: 1\ndate: 2026-02-01\n---\n\n"
        "## Repos in scope\n- checkout-web (React)\n- Laravel monolith\n",
        encoding="utf-8",
    )
    assert snapshot.parse_snapshot(path)["repos"] == [
        {"name": "checkout-web", "tech": "React"},
        {"name": "Laravel monolith", "tech": ""},
    ]


def test_parse_warns_on_a_newer_format_version_instead_of_guessing(tmp_path):
    path = tmp_path / "audit-2026-02-01.md"
    path.write_text("---\nformat_version: 99\ndate: 2026-02-01\n---\n", encoding="utf-8")
    warnings = snapshot.parse_snapshot(path)["warnings"]
    assert any("format_version 99" in w for w in warnings)


def test_parse_raises_on_unterminated_frontmatter(tmp_path):
    path = tmp_path / "broken.md"
    path.write_text("---\ndate: 2026-02-01\n", encoding="utf-8")
    with pytest.raises(snapshot.ParseError):
        snapshot.parse_snapshot(path)


def test_parse_raises_on_a_missing_file(tmp_path):
    with pytest.raises(snapshot.ParseError):
        snapshot.parse_snapshot(tmp_path / "nope.md")


def test_parse_covers_every_canonical_area(previous):
    """A snapshot always carries all six areas — a missing one is a format break."""
    assert set(snapshot.parse_snapshot(previous)["scores"]) == set(snapshot.CANONICAL_AREAS)


# --------------------------------------------------------------------------
# delta
# --------------------------------------------------------------------------


def test_delta_score_arrows_and_unchanged_dash(previous, current):
    out = snapshot.build_delta(
        snapshot.parse_snapshot(previous), snapshot.parse_snapshot(current)
    )
    assert "| 🟢 CI/CD | 2/5 | 4/5 | ↑ +2 |" in out
    assert "| 🔴 Testing | 1/5 | 1/5 | — |" in out
    assert "| 🔴 Monitoring | 2/5 | 1/5 | ↓ -1 |" in out
    assert "| 🟡 Ownership & culture | 3/5 | 3/5 | — |" in out


def test_delta_emoji_follows_the_current_score(previous, current):
    out = snapshot.build_delta(
        snapshot.parse_snapshot(previous), snapshot.parse_snapshot(current)
    )
    # Developer Experience went 2 -> 3, so it must be yellow, not red.
    assert "| 🟡 Developer Experience | 2/5 | 3/5 | ↑ +1 |" in out


def test_delta_matches_reworded_blockers_and_classifies_the_rest(previous, current):
    out = snapshot.build_delta(
        snapshot.parse_snapshot(previous), snapshot.parse_snapshot(current)
    )
    blockers = out.split("### Blockers")[1].split("### Action items")[0]
    # Reworded but the same problem.
    assert "Flaky suite" in blockers.split("**Still open:**")[1]
    assert "Jenkins full build" in blockers.split("**Resolved:**")[1].split("\n")[0]
    assert "Monitoring was switched off" in blockers.split("**New:**")[1]


def test_delta_action_items_track_status_transitions(previous, current):
    out = snapshot.build_delta(
        snapshot.parse_snapshot(previous), snapshot.parse_snapshot(current)
    )
    assert "| A1 | Quarantine flaky tests | ○ open → ✓ done |" in out
    assert "| A2 | Split the Jenkins pipeline | still open |" in out
    assert "| A3 | Assign an owner to checkout-api | dropped from plan |" in out
    assert "| A4 | Restore Sentry alert routing | new |" in out


def test_delta_action_items_are_ordered_numerically_not_lexically(previous, tmp_path):
    many = CURRENT.replace(
        "| A4 | Restore Sentry alert routing | short | SRE | open |",
        "| A10 | Ten | short | SRE | open |\n| A4 | Four | short | SRE | open |",
    )
    path = tmp_path / "audit-2026-05-01.md"
    path.write_text(many, encoding="utf-8")
    out = snapshot.build_delta(
        snapshot.parse_snapshot(previous), snapshot.parse_snapshot(path)
    )
    ids = [
        line.split("|")[1].strip()
        for line in out.splitlines()
        if re.match(r"^\| A\d+ \|", line)
    ]
    assert ids == ["A1", "A2", "A3", "A4", "A10"]


def test_delta_reports_repo_scope_changes(previous, current):
    out = snapshot.build_delta(
        snapshot.parse_snapshot(previous), snapshot.parse_snapshot(current)
    )
    assert "- Added: checkout-infra (Terraform) — no previous data to compare" in out
    assert "- Removed: checkout-api — dropped from scope" in out


def test_delta_omits_the_repo_scope_section_when_nothing_moved(previous):
    data = snapshot.parse_snapshot(previous)
    assert "### Repo scope" not in snapshot.build_delta(data, data)


def test_delta_of_a_snapshot_with_itself_is_all_unchanged(previous):
    data = snapshot.parse_snapshot(previous)
    out = snapshot.build_delta(data, data)
    assert out.count("| — |") == len(snapshot.CANONICAL_AREAS)
    assert "**Resolved:** none" in out
    assert "**New:** none" in out


# --------------------------------------------------------------------------
# validate
# --------------------------------------------------------------------------

VALID_AUDIT = textwrap.dedent(
    """\
    # Minottobot audit — Acme — 2026-04-27

    ## Repos in scope
    - checkout-web (React)

    ## Phase 0 baseline
    - Team size: 8

    ## Area scores (1 = critical · 5 = excellent)
    | Area | Score | One-line finding |
    |------|-------|------------------|
    | CI/CD | 2/5 | Jenkins and GitHub Actions in parallel |
    | Testing | 1/5 | No integration tests |
    | Code review | 3/5 | Required on main, skipped on hotfix |
    | Monitoring | 2/5 | Sentry added after the last incident |
    | Developer Experience | 2/5 | No staging environment |
    | Ownership & culture | 2/5 | No product owner, three VPs in 18 months |

    ## Evidence & red flags
    - 47-minute Jenkins build.

    ## Systems flagged for replacement evaluation
    - Jenkins — 47-minute build, dedicated CI team.
    """
)


def _write(tmp_path, text, name="report.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_validate_accepts_a_well_formed_audit(tmp_path):
    kind, violations = snapshot.validate(_write(tmp_path, VALID_AUDIT), {})
    assert kind == "audit"
    assert violations == []


def test_validate_detects_the_report_kind_from_the_executive_summary(tmp_path):
    report = VALID_AUDIT.replace(
        "## Phase 0 baseline\n- Team size: 8",
        "## Executive summary\n- CI is split.\n\n## Top 3 blockers\n1. **Flaky suite** — ignored."
        "\n\n## Improvement plan\n### Short term\n- Quarantine flaky tests."
        "\n\n## Action items\n| ID | Description | Horizon | Owner | Status |\n"
        "|----|---|---|---|---|\n| A1 | Quarantine | short | QA | open |",
    )
    kind, violations = snapshot.validate(_write(tmp_path, report), {})
    assert kind == "report"
    assert violations == []


def test_validate_rejects_a_bracketed_placeholder_score(tmp_path):
    bad = VALID_AUDIT.replace("| CI/CD | 2/5 |", "| CI/CD | [2]/5 |")
    _, violations = snapshot.validate(_write(tmp_path, bad), {})
    assert any("not a bare 1-5 value" in v for v in violations)


def test_validate_rejects_a_bare_score_without_the_slash_five(tmp_path):
    bad = VALID_AUDIT.replace("| CI/CD | 2/5 |", "| CI/CD | 2 |")
    _, violations = snapshot.validate(_write(tmp_path, bad), {})
    assert any("must be written as 'N/5'" in v for v in violations)


def test_validate_allows_bare_scores_in_a_snapshot(previous):
    kind, violations = snapshot.validate(previous, {})
    assert kind == "snapshot"
    assert violations == []


def test_validate_rejects_a_missing_area_row(tmp_path):
    bad = VALID_AUDIT.replace("| Monitoring | 2/5 | Sentry added after the last incident |\n", "")
    _, violations = snapshot.validate(_write(tmp_path, bad), {})
    assert any("exactly these six rows in order" in v for v in violations)


def test_validate_rejects_an_extra_area_row(tmp_path):
    bad = VALID_AUDIT.replace(
        "| Ownership & culture | 2/5 | No product owner, three VPs in 18 months |",
        "| Ownership & culture | 2/5 | No product owner |\n| Environments | 2/5 | No staging |",
    )
    _, violations = snapshot.validate(_write(tmp_path, bad), {})
    assert any("exactly these six rows in order" in v for v in violations)


def test_validate_rejects_reordered_area_rows(tmp_path):
    lines = VALID_AUDIT.splitlines()
    ci = lines.index("| CI/CD | 2/5 | Jenkins and GitHub Actions in parallel |")
    lines[ci], lines[ci + 1] = lines[ci + 1], lines[ci]
    _, violations = snapshot.validate(_write(tmp_path, "\n".join(lines)), {})
    assert any("exactly these six rows in order" in v for v in violations)


def test_validate_flags_a_missing_required_section(tmp_path):
    bad = VALID_AUDIT.replace(
        "## Systems flagged for replacement evaluation\n- Jenkins — 47-minute build, dedicated CI team.\n",
        "",
    )
    _, violations = snapshot.validate(_write(tmp_path, bad), {})
    assert any("Systems flagged for replacement evaluation" in v for v in violations)


def test_validate_enforces_a_mandatory_score_cap(tmp_path):
    over = VALID_AUDIT.replace(
        "| Ownership & culture | 2/5 |", "| Ownership & culture | 4/5 |"
    )
    _, violations = snapshot.validate(
        _write(tmp_path, over), {"Ownership & culture": 2}
    )
    assert any("exceeds the mandatory cap of 2/5" in v for v in violations)


def test_validate_accepts_a_score_at_the_cap(tmp_path):
    _, violations = snapshot.validate(
        _write(tmp_path, VALID_AUDIT), {"Ownership & culture": 2, "CI/CD": 2}
    )
    assert violations == []


def test_validate_rejects_a_cap_for_an_unknown_area(tmp_path):
    _, violations = snapshot.validate(_write(tmp_path, VALID_AUDIT), {"Deployments": 2})
    assert any("unknown area" in v for v in violations)


def test_validate_enforces_a_mandatory_score_floor(tmp_path):
    _, violations = snapshot.validate(
        _write(tmp_path, VALID_AUDIT), {}, floors={"Code review": 4}
    )
    assert any("falls below the mandatory floor of 4/5" in v for v in violations)


def test_validate_accepts_a_score_at_the_floor(tmp_path):
    _, violations = snapshot.validate(
        _write(tmp_path, VALID_AUDIT), {}, floors={"Code review": 3}
    )
    assert violations == []


def test_validate_rejects_an_area_declared_with_both_a_cap_and_a_floor(tmp_path):
    _, violations = snapshot.validate(
        _write(tmp_path, VALID_AUDIT), {"CI/CD": 2}, floors={"CI/CD": 4}
    )
    assert any("both a cap and a floor" in v for v in violations)


def test_validate_rejects_a_floor_for_an_unknown_area(tmp_path):
    _, violations = snapshot.validate(
        _write(tmp_path, VALID_AUDIT), {}, floors={"Deployments": 4}
    )
    assert any("unknown area" in v for v in violations)


def test_validate_flags_unreplaced_template_placeholders(tmp_path):
    bad = VALID_AUDIT.replace("- checkout-web (React)", "- {repo name} ({primary tech})")
    _, violations = snapshot.validate(_write(tmp_path, bad), {})
    assert any("unreplaced template placeholder" in v for v in violations)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def test_cli_parse_emits_json(previous, capsys):
    assert snapshot.main(["parse", str(previous)]) == 0
    assert json.loads(capsys.readouterr().out)["team"] == "Acme Checkout squad"


def test_cli_delta_writes_markdown(previous, current, capsys):
    assert snapshot.main(["delta", str(previous), str(current)]) == 0
    assert capsys.readouterr().out.startswith("## Delta since 2026-01-15")


def test_cli_validate_exits_1_on_violations(tmp_path, capsys):
    bad = _write(tmp_path, VALID_AUDIT.replace("| CI/CD | 2/5 |", "| CI/CD | [2]/5 |"))
    assert snapshot.main(["validate", str(bad)]) == 1
    assert "violation" in capsys.readouterr().err


def test_cli_validate_exits_0_when_clean(tmp_path, capsys):
    assert snapshot.main(["validate", str(_write(tmp_path, VALID_AUDIT))]) == 0


def test_cli_validate_accepts_floor_arguments(tmp_path, capsys):
    path = _write(tmp_path, VALID_AUDIT)
    assert snapshot.main(["validate", str(path), "--floor", "Code review=4"]) == 1
    assert "mandatory floor" in capsys.readouterr().err


def test_cli_exits_2_on_a_bad_floor_argument(tmp_path, capsys):
    path = _write(tmp_path, VALID_AUDIT)
    assert snapshot.main(["validate", str(path), "--floor", "Testing"]) == 2
    assert "--floor expects AREA=N" in capsys.readouterr().err


def test_cli_exits_2_on_a_bad_cap_argument(tmp_path, capsys):
    path = _write(tmp_path, VALID_AUDIT)
    assert snapshot.main(["validate", str(path), "--cap", "Testing"]) == 2
    assert "error:" in capsys.readouterr().err


def test_cli_exits_2_on_an_unreadable_file(tmp_path, capsys):
    assert snapshot.main(["parse", str(tmp_path / "missing.md")]) == 2
    assert "error:" in capsys.readouterr().err
