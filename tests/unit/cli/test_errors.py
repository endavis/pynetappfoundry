"""Tests for CliError, the single command error-exit convention (ADR-0022)."""

from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock, patch

import click
import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.commands.cache.refresh import _failure_summary_lines, _report_summary
from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.main import nf


def _register(monkeypatch: pytest.MonkeyPatch, name: str, func: Callable[[], None]) -> None:
    monkeypatch.setitem(nf.commands, name, click.Command(name, callback=func))


class TestCliErrorAttributes:
    """Constructor behaviour."""

    def test_default_exit_code_is_one(self) -> None:
        assert CliError("x").exit_code == 1

    def test_exit_code_is_honoured(self) -> None:
        assert CliError("x", exit_code=2).exit_code == 2

    def test_hints_and_exc_stored(self) -> None:
        exc = ValueError("v")
        err = CliError("x", hints=["a", "b"], exc=exc)
        assert err.hints == ("a", "b")
        assert err.exc is exc

    def test_debug_is_captured_at_construction(self) -> None:
        """click shows the error after the context is gone, so debug is recorded early."""
        with click.Context(click.Command("c"), obj={"debug": True}):
            err = CliError("x")
        assert err.debug is True
        assert CliError("x").debug is False


class TestCliErrorOutput:
    """Rendering through the nf group and through a plain click command."""

    def test_exit_one_with_escaped_message(
        self, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        def bad() -> None:
            raise CliError("bad [/x]")

        _register(monkeypatch, "bad", bad)
        with caplog.at_level(logging.ERROR):
            result = CliRunner().invoke(nf, ["bad"])

        assert result.exit_code == 1
        assert "bad [/x]" in result.output
        assert "Error:" not in result.output
        assert "Unexpected error" not in result.output
        assert "Re-run with --debug" not in result.output
        assert any(r.getMessage() == "bad [/x]" for r in caplog.records)

    def test_exit_code_two(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def bad() -> None:
            raise CliError("bad", exit_code=2)

        _register(monkeypatch, "bad", bad)
        assert CliRunner().invoke(nf, ["bad"]).exit_code == 2

    def test_hints_follow_message_in_order(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def bad() -> None:
            raise CliError("the message", hints=["first hint", "second hint"])

        _register(monkeypatch, "bad", bad)
        out = CliRunner().invoke(nf, ["bad"]).output
        assert out.index("the message") < out.index("first hint") < out.index("second hint")

    def test_plain_click_command(self) -> None:
        @click.command()
        def cmd() -> None:
            raise CliError("plain failure", exit_code=2, hints=["a hint"])

        result = CliRunner().invoke(cmd, [])
        assert result.exit_code == 2
        assert "plain failure" in result.output
        assert "a hint" in result.output

    def test_message_goes_to_stdout_not_stderr(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def bad() -> None:
            raise CliError("on stdout")

        _register(monkeypatch, "bad", bad)
        result = CliRunner().invoke(nf, ["bad"])
        assert "on stdout" in result.stdout
        assert "on stdout" not in result.stderr

    def test_exc_without_debug_hides_traceback_but_logs_it(
        self, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        def bad() -> None:
            try:
                raise ValueError("inner")
            except ValueError as e:
                raise CliError("outer", exc=e) from e

        _register(monkeypatch, "bad", bad)
        with caplog.at_level(logging.ERROR):
            result = CliRunner().invoke(nf, ["bad"])

        assert result.exit_code == 1
        assert "Traceback" not in result.output
        records = [r for r in caplog.records if r.getMessage() == "outer"]
        assert records
        assert records[0].exc_info is not None
        assert records[0].exc_info[0] is ValueError

    def test_exc_with_debug_prints_traceback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def bad() -> None:
            try:
                raise ValueError("inner")
            except ValueError as e:
                raise CliError("outer", exc=e) from e

        _register(monkeypatch, "bad", bad)
        result = CliRunner().invoke(nf, ["--debug", "bad"])

        assert result.exit_code == 1
        assert "Traceback" in result.output
        assert "outer" in result.output


class TestRefreshFailureSummary:
    """The failure summary follows the failure line as hints."""

    def test_lines_empty_without_failures(self) -> None:
        assert _failure_summary_lines({}) == []

    def test_summary_after_failure_line(self, monkeypatch: pytest.MonkeyPatch) -> None:
        summary = MagicMock()
        summary.succeeded = 1
        summary.failed = 2
        summary.failures = {"c2": ["boom [/x]"]}

        def run() -> None:
            _report_summary(summary)

        _register(monkeypatch, "rs", run)
        result = CliRunner().invoke(nf, ["rs"])

        assert result.exit_code == 1
        out = result.output
        assert out.index("Failed to refresh 2 cluster(s)") < out.index("Failure Summary:")
        assert out.index("Failure Summary:") < out.index("c2:") < out.index("boom [/x]")


class TestHistoryRestoreIncompatibleSchema:
    """An incompatible snapshot exits 1 with the schema message only once."""

    @patch("pynetappfoundry.cli.commands.cache.history.CacheHistoryDB")
    def test_no_bogus_restore_failure_line(self, mock_db_class: MagicMock, tmp_path: Path) -> None:
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            '[ontapapi]\n[ontapapi.general]\nbase_api_path = "/api"\n'
        )
        mock_db_class.return_value.get_snapshot_at_date.return_value = {
            "id": 1,
            "after_json": '{"cache_version": 0}',
        }

        with patch(
            "pynetappfoundry.cli.commands.cache.history.is_schema_compatible", return_value=False
        ):
            result = CliRunner().invoke(
                nf,
                [
                    "-c",
                    str(config_dir),
                    "cache",
                    "history",
                    "snapshot",
                    "c1",
                    "--date",
                    "2025-01-01",
                    "--restore",
                ],
                catch_exceptions=False,
            )

        assert result.exit_code == 1
        assert result.output.count("incompatible schema version") == 1
        assert "Failed to restore snapshot" not in result.output
