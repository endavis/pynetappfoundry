"""Tests for the top-level `nf` CLI group, focusing on -h / --help equivalence."""

from __future__ import annotations

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
