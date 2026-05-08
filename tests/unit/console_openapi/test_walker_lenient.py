"""Tests for ``parse_service`` lenient/strict modes."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tools.console_openapi.parser.endpoint import EndpointParseError
from tools.console_openapi.walker import parse_service

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "console_openapi"


def _make_service(tmp_path: Path, fixtures: list[str]) -> Path:
    """Stage a synthetic service folder under ``tmp_path/service``."""
    service_dir = tmp_path / "demo_service"
    service_dir.mkdir()
    for name in fixtures:
        shutil.copy(FIXTURES / name, service_dir / name)
    return tmp_path


def test_strict_propagates_parse_error(tmp_path: Path) -> None:
    repo = _make_service(tmp_path, ["happy_post_with_definitions.adoc", "malformed_table.adoc"])
    with pytest.raises(EndpointParseError) as excinfo:
        parse_service(repo, "demo_service", strict=True)
    assert "malformed_table.adoc" in str(excinfo.value)


def test_lenient_records_error_and_continues(tmp_path: Path) -> None:
    repo = _make_service(tmp_path, ["happy_post_with_definitions.adoc", "malformed_table.adoc"])
    report = parse_service(repo, "demo_service", strict=False)

    # Healthy endpoint still parsed
    assert len(report.endpoints) == 1
    assert report.endpoints[0].method == "POST"

    # Malformed file recorded
    assert len(report.errors) == 1
    err = report.errors[0]
    assert err.source_file.endswith("malformed_table.adoc")
    assert err.section == "endpoint"
    assert err.message  # non-empty
