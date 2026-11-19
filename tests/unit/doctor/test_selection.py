"""Tests for the ``--api`` row selection of ``nf doctor`` (#1122)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pynetappfoundry.core.config import Config
from pynetappfoundry.core.config_checks import (
    CheckResult,
    CheckSection,
    CheckStatus,
    run_static_checks,
)
from pynetappfoundry.doctor.selection import apis_for_subject, select_sections

ALL_USERS = {"ontap", "aiqum", "dii", "console"}


@pytest.mark.parametrize(
    ("subject", "expected"),
    [
        ("clusters", {"ontap"}),
        ("clusters.c1.credentials", {"ontap"}),
        ("users", ALL_USERS),
        ("users.clusters", {"ontap"}),
        ("users.console", {"console"}),
        ("users.connectors", {"console"}),
        ("users.azure", set()),
        ("aiqums.a1.credentials", {"aiqum"}),
        ("aiqumapi.general", {"aiqum"}),
        ("cloudinsights.t.credentials", {"dii"}),
        ("diiapi.general", {"dii"}),
        ("consoleapi.general", {"console"}),
        ("connectors.x", {"console"}),
        ("ontapapi.general", {"ontap"}),
        ("digitaladvisorapi.general", {"digitaladvisor"}),
        ("spec.dii", {"dii"}),
        ("spec.unknown", set()),
        ("settings.SMTP", set()),
        ("licensing", set()),
        ("monitoring", set()),
        ("brand_new", None),
    ],
)
def test_apis_for_subject(subject: str, expected: set[str] | None) -> None:
    result = apis_for_subject(subject)
    assert result == (None if expected is None else frozenset(expected))


def _section(title: str, *subjects: str) -> CheckSection:
    return CheckSection(title, tuple(CheckResult(s, CheckStatus.OK, s) for s in subjects))


def test_select_sections_none_returns_input_unchanged() -> None:
    sections = [_section("A", "clusters", "licensing"), _section("B")]
    assert select_sections(sections, None) is sections


def test_select_sections_filters_orders_and_drops_empty() -> None:
    sections = [
        _section("Clusters", "clusters.c1.credentials"),
        _section("Settings", "licensing", "diiapi.general", "brand_new"),
        _section("Other", "licensing"),
    ]
    selected = select_sections(sections, ("dii",))

    assert [s.title for s in selected] == ["Settings"]
    assert [r.subject for r in selected[0].results] == ["diiapi.general", "brand_new"]
    both = select_sections(sections, ("dii", "ontap"))
    assert [s.title for s in both] == ["Clusters", "Settings"]


def test_every_static_subject_is_classified(tmp_path: Path) -> None:
    files = {
        "inv.toml": '[settings]\ntype = "data"\n\n[clusters.c1]\nip = "192.0.2.1"\n'
        '\n[aiqums.a1]\nip = "192.0.2.2"\n'
        '\n[cloudinsights.t1]\nurl = "https://example.invalid"\n'
        '\n[connectors.k1]\nip = "192.0.2.3"\n',
        "users.toml": '[clusters]\nuser = "u"\nenc = "placeholder"\n'
        '\n[aiqums]\nuser = "u"\nenc = "placeholder"\n'
        '\n[console]\nuser = "u"\nenc = "placeholder"\n'
        '\n[azure]\nuser = "u"\n',
        "ontapapi.toml": '[general]\nbase_api_path = "/api"\n',
        "aiqumapi.toml": '[general]\nbase_api_path = "/api"\n',
        "diiapi.toml": '[general]\nbase_api_path = "/api"\n',
        "consoleapi.toml": '[general]\nbase_api_path = "/api"\n',
        "digitaladvisorapi.toml": '[general]\nbase_api_path = "/api"\n',
        "settings.toml": '[SMTP]\nserver = "smtp.invalid"\n',
        "licensing.toml": "",
        "apis/ontap/all.json": "{}",
        "Org1/scope.toml": "",
        "Org1/monitoring.toml": "",
        "Org1/consoleapi.toml": '[general]\nbase_api_path = "/api"\n',
    }
    config_dir = tmp_path / "cfg"
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    config = Config(config_dir=str(config_dir), script_name="test")

    subjects = {
        r.subject
        for scope in (None, "Org1")
        for section in run_static_checks(config, scope)
        for r in section.results
    }
    assert subjects
    assert {s for s in subjects if apis_for_subject(s) is None} == set()
