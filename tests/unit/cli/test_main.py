"""Tests for the top-level `nf` CLI group, focusing on -h / --help equivalence."""

from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


class TestHelpShortAlias:
    """Verify that -h is accepted everywhere --help is accepted."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    # ------------------------------------------------------------------
    # Top-level group
    # ------------------------------------------------------------------

    def test_top_level_help_short_option_exit_code_zero(self, runner: CliRunner) -> None:
        """`nf -h` exits with code 0."""
        result = runner.invoke(nf, ["-h"])
        assert result.exit_code == 0

    def test_top_level_help_short_option_matches_long(self, runner: CliRunner) -> None:
        """`nf -h` produces the same output as `nf --help`."""
        short = runner.invoke(nf, ["-h"])
        long = runner.invoke(nf, ["--help"])
        assert short.exit_code == long.exit_code
        assert short.output == long.output

    # ------------------------------------------------------------------
    # Subcommand: cache
    # ------------------------------------------------------------------

    def test_subcommand_cache_help_short_option_exit_code_zero(self, runner: CliRunner) -> None:
        """`nf cache -h` exits with code 0."""
        result = runner.invoke(nf, ["cache", "-h"])
        assert result.exit_code == 0

    def test_subcommand_cache_help_short_option_matches_long(self, runner: CliRunner) -> None:
        """`nf cache -h` produces the same output as `nf cache --help`."""
        short = runner.invoke(nf, ["cache", "-h"])
        long = runner.invoke(nf, ["cache", "--help"])
        assert short.exit_code == long.exit_code
        assert short.output == long.output

    # ------------------------------------------------------------------
    # Subcommand: events
    # ------------------------------------------------------------------

    def test_subcommand_events_help_short_option_exit_code_zero(self, runner: CliRunner) -> None:
        """`nf events -h` exits with code 0."""
        result = runner.invoke(nf, ["events", "-h"])
        assert result.exit_code == 0

    def test_subcommand_events_help_short_option_matches_long(self, runner: CliRunner) -> None:
        """`nf events -h` produces the same output as `nf events --help`."""
        short = runner.invoke(nf, ["events", "-h"])
        long = runner.invoke(nf, ["events", "--help"])
        assert short.exit_code == long.exit_code
        assert short.output == long.output

    # ------------------------------------------------------------------
    # Nested subcommand: cache show
    # ------------------------------------------------------------------

    def test_nested_subcommand_cache_show_help_short_option_exit_code_zero(
        self, runner: CliRunner
    ) -> None:
        """`nf cache show -h` exits with code 0."""
        result = runner.invoke(nf, ["cache", "show", "-h"])
        assert result.exit_code == 0

    def test_nested_subcommand_cache_show_help_short_option_matches_long(
        self, runner: CliRunner
    ) -> None:
        """`nf cache show -h` produces the same output as `nf cache show --help`."""
        short = runner.invoke(nf, ["cache", "show", "-h"])
        long = runner.invoke(nf, ["cache", "show", "--help"])
        assert short.exit_code == long.exit_code
        assert short.output == long.output


class TestTopLevelHandler:
    """The `nf` group turns unexpected exceptions into a clean exit code 1."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @staticmethod
    def _register(monkeypatch: pytest.MonkeyPatch, name: str, func: Callable[[], None]) -> None:
        monkeypatch.setitem(nf.commands, name, click.Command(name, callback=func))

    def test_unexpected_error_exits_one_with_hint(
        self,
        runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        def boom() -> None:
            raise RuntimeError("kaboom [/x]")

        self._register(monkeypatch, "boom", boom)
        with caplog.at_level(logging.ERROR):
            result = runner.invoke(nf, ["boom"])

        assert result.exit_code == 1
        assert "Unexpected error: kaboom [/x]" in result.output
        assert "Re-run with --debug" in result.output
        assert "Traceback" not in result.output
        assert any(r.exc_info for r in caplog.records)

    def test_debug_prints_traceback_without_hint(
        self, runner: CliRunner, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def boom() -> None:
            raise RuntimeError("kaboom")

        self._register(monkeypatch, "boom", boom)
        result = runner.invoke(nf, ["--debug", "boom"])

        assert result.exit_code == 1
        assert "Traceback" in result.output
        assert "Re-run with --debug" not in result.output

    def test_click_exception_unchanged(
        self, runner: CliRunner, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def nope() -> None:
            raise click.ClickException("nope")

        self._register(monkeypatch, "nope", nope)
        result = runner.invoke(nf, ["nope"])

        assert result.exit_code == 1
        assert "Error: nope" in result.output
        assert "Unexpected error" not in result.output

    def test_ctx_exit_code_preserved(
        self, runner: CliRunner, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def two() -> None:
            click.get_current_context().exit(2)

        self._register(monkeypatch, "two", two)
        assert runner.invoke(nf, ["two"]).exit_code == 2

    def test_abort_unchanged(self, runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
        def abort() -> None:
            raise click.Abort

        self._register(monkeypatch, "abort", abort)
        result = runner.invoke(nf, ["abort"])

        assert result.exit_code == 1
        assert "Aborted!" in result.output
        assert "Unexpected error" not in result.output

    def test_usage_error_exits_two(self, runner: CliRunner) -> None:
        result = runner.invoke(nf, ["--no-such-option"])
        assert result.exit_code == 2
        assert "Unexpected error" not in result.output


class TestGroupOutputDirShortOption:
    """The `nf` group keeps `-o` for `--output-dir`; subcommands dropped it (#943)."""

    def test_group_accepts_short_o(self, tmp_path: Path) -> None:
        """`nf -o DIR --help` parses `-o` as the group's `--output-dir`."""
        result = CliRunner().invoke(nf, ["-o", str(tmp_path), "--help"])
        assert result.exit_code == 0, result.output

    def test_group_declares_short_o(self) -> None:
        """`-o` is an alias of `--output-dir` on the group."""
        opt = next(p for p in nf.params if p.name == "output_dir")
        assert "-o" in opt.opts
