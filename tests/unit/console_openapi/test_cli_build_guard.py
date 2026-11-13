"""The ``build`` command refuses services with no declared base path (#1015)."""

from __future__ import annotations

from typing import Any

import pytest
from click.testing import CliRunner

from tools.console_openapi import cli as cli_module


def test_build_rejects_service_without_base_path(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("fetch must not be called")

    monkeypatch.setattr(cli_module, "fetch", _fail)

    result = CliRunner().invoke(cli_module.cli, ["build", "--service", "bogus"])

    assert result.exit_code != 0
    assert "bogus" in result.output
    assert "_SERVICE_BASE_PATHS" in result.output
