"""Tests for CLI utility functions."""

from __future__ import annotations

import logging
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.utils import (
    is_debug_mode,
    print_debug,
    print_error,
    print_exception,
    print_info,
    print_success,
    print_warning,
)


class TestIsDebugMode:
    """Tests for is_debug_mode function."""

    def test_debug_mode_enabled(self) -> None:
        """Test when debug mode is enabled in context."""
        with patch("pynetappfoundry.cli.utils.click.get_current_context") as mock_ctx:
            mock_ctx.return_value = MagicMock(obj={"debug": True})
            assert is_debug_mode() is True

    def test_debug_mode_disabled(self) -> None:
        """Test when debug mode is disabled in context."""
        with patch("pynetappfoundry.cli.utils.click.get_current_context") as mock_ctx:
            mock_ctx.return_value = MagicMock(obj={"debug": False})
            assert is_debug_mode() is False

    def test_debug_mode_no_context(self) -> None:
        """Test when no context is available."""
        with patch("pynetappfoundry.cli.utils.click.get_current_context") as mock_ctx:
            mock_ctx.return_value = None
            assert is_debug_mode() is False

    def test_debug_mode_empty_obj(self) -> None:
        """Test when context obj is None."""
        with patch("pynetappfoundry.cli.utils.click.get_current_context") as mock_ctx:
            mock_ctx.return_value = MagicMock(obj=None)
            assert is_debug_mode() is False


class TestPrintSuccess:
    """Tests for print_success function."""

    def test_prints_to_console_and_logs(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_success prints to console and logs at INFO level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            caplog.at_level(logging.INFO),
        ):
            print_success("Test message")

            mock_console.print.assert_called_once_with("[green]Test message[/green]")
            assert "Test message" in caplog.text
            assert caplog.records[0].levelno == logging.INFO


class TestPrintError:
    """Tests for print_error function."""

    def test_prints_to_console_and_logs(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_error prints to console and logs at ERROR level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            caplog.at_level(logging.ERROR),
        ):
            print_error("Error message")

            mock_console.print.assert_called_once_with("[red]Error message[/red]")
            assert "Error message" in caplog.text
            assert caplog.records[0].levelno == logging.ERROR


class TestPrintWarning:
    """Tests for print_warning function."""

    def test_prints_to_console_and_logs(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_warning prints to console and logs at WARNING level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            caplog.at_level(logging.WARNING),
        ):
            print_warning("Warning message")

            mock_console.print.assert_called_once_with("[yellow]Warning message[/yellow]")
            assert "Warning message" in caplog.text
            assert caplog.records[0].levelno == logging.WARNING


class TestPrintInfo:
    """Tests for print_info function."""

    def test_prints_to_console_and_logs(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_info prints to console and logs at INFO level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            caplog.at_level(logging.INFO),
        ):
            print_info("Info message")

            mock_console.print.assert_called_once_with("[blue]Info message[/blue]")
            assert "Info message" in caplog.text
            assert caplog.records[0].levelno == logging.INFO


class TestPrintException:
    """Tests for print_exception function."""

    def test_with_exception_logs_exception(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_exception with exception logs at exception level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            patch("pynetappfoundry.cli.utils.is_debug_mode", return_value=False),
            caplog.at_level(logging.ERROR),
        ):
            exc = ValueError("Test error")
            print_exception("Exception message", exc)

            mock_console.print.assert_called_once_with("[red]Exception message[/red]")
            assert "Exception message" in caplog.text

    def test_without_exception_logs_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_exception without exception logs at error level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            caplog.at_level(logging.ERROR),
        ):
            print_exception("Error only message")

            mock_console.print.assert_called_once_with("[red]Error only message[/red]")
            assert "Error only message" in caplog.text
            assert caplog.records[0].levelno == logging.ERROR

    def test_with_exception_in_debug_mode_shows_traceback(self) -> None:
        """Test that traceback is shown on console in debug mode."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            patch("pynetappfoundry.cli.utils.is_debug_mode", return_value=True),
        ):
            exc = ValueError("Test error")
            print_exception("Exception message", exc)

            # Should have two console.print calls: error message and traceback
            assert mock_console.print.call_count == 2


class TestPrintDebug:
    """Tests for print_debug function."""

    def test_always_logs_to_file(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that print_debug always logs at DEBUG level."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            patch("pynetappfoundry.cli.utils.is_debug_mode", return_value=False),
            caplog.at_level(logging.DEBUG),
        ):
            print_debug("Debug message")

            # Should NOT print to console when debug mode is off
            mock_console.print.assert_not_called()
            # Should log to file
            assert "Debug message" in caplog.text
            assert caplog.records[0].levelno == logging.DEBUG

    def test_prints_to_console_in_debug_mode(self) -> None:
        """Test that print_debug prints to console when debug mode is enabled."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            patch("pynetappfoundry.cli.utils.is_debug_mode", return_value=True),
        ):
            print_debug("Debug message")

            mock_console.print.assert_called_once_with("[dim]Debug message[/dim]")

    def test_no_console_output_when_not_in_debug_mode(self) -> None:
        """Test that print_debug does not print to console when debug mode is off."""
        with (
            patch("pynetappfoundry.cli.utils.console") as mock_console,
            patch("pynetappfoundry.cli.utils.is_debug_mode", return_value=False),
        ):
            print_debug("Debug message")

            mock_console.print.assert_not_called()
