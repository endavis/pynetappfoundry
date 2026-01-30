"""Tests for events get command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.events.get import (
    _get_cluster_events,
    _write_csv,
    clean_message,
)


class TestCleanMessage:
    """Tests for clean_message function."""

    def test_removes_event_name_prefix(self) -> None:
        """Test that event name prefix is removed."""
        result = clean_message("vsa.mlx.nic.detach: NIC detached", "vsa.mlx.nic.detach")
        assert result == "NIC detached"

    def test_replaces_commas_with_semicolons(self) -> None:
        """Test that commas are replaced with semicolons."""
        result = clean_message("Error: field1, field2, field3", "Error")
        assert ";" in result
        assert "," not in result

    def test_removes_newlines(self) -> None:
        """Test that newlines are replaced with spaces."""
        result = clean_message("Line1\nLine2\nLine3", "Event")
        assert "\n" not in result
        assert "Line1 Line2 Line3" in result

    def test_strips_whitespace(self) -> None:
        """Test that leading/trailing whitespace is stripped."""
        result = clean_message("  message with spaces  ", "Event")
        assert result == "message with spaces"

    def test_empty_message(self) -> None:
        """Test handling of empty message."""
        result = clean_message("", "Event")
        assert result == ""

    def test_message_without_prefix(self) -> None:
        """Test message that doesn't contain the event name prefix."""
        result = clean_message("Some other message", "vsa.event")
        assert result == "Some other message"


class TestWriteCsv:
    """Tests for _write_csv function."""

    def test_creates_csv_file(self, tmp_path: Path) -> None:
        """Test that CSV file is created."""
        output_path = tmp_path / "events.csv"
        events = [
            {
                "cluster": "cluster1",
                "time": "2024-01-15T10:00:00",
                "severity": "error",
                "name": "vsa.event",
                "message": "Test message",
            }
        ]
        _write_csv(output_path, events)
        assert output_path.exists()

    def test_csv_has_header(self, tmp_path: Path) -> None:
        """Test that CSV has correct headers."""
        output_path = tmp_path / "events.csv"
        events = [
            {
                "cluster": "cluster1",
                "time": "2024-01-15T10:00:00",
                "severity": "error",
                "name": "vsa.event",
                "message": "Test message",
            }
        ]
        _write_csv(output_path, events)

        content = output_path.read_text()
        lines = content.strip().split("\n")
        header = lines[0]
        assert "cluster" in header
        assert "time" in header
        assert "severity" in header
        assert "name" in header
        assert "message" in header

    def test_csv_has_data_rows(self, tmp_path: Path) -> None:
        """Test that CSV contains data rows."""
        output_path = tmp_path / "events.csv"
        events = [
            {
                "cluster": "cluster1",
                "time": "2024-01-15T10:00:00",
                "severity": "error",
                "name": "vsa.event",
                "message": "Test message 1",
            },
            {
                "cluster": "cluster2",
                "time": "2024-01-15T11:00:00",
                "severity": "warning",
                "name": "vsa.other",
                "message": "Test message 2",
            },
        ]
        _write_csv(output_path, events)

        content = output_path.read_text()
        lines = content.strip().split("\n")
        # Header + 2 data rows
        assert len(lines) == 3

    def test_csv_empty_events(self, tmp_path: Path) -> None:
        """Test CSV creation with empty events list."""
        output_path = tmp_path / "events.csv"
        events: list[dict[str, Any]] = []
        _write_csv(output_path, events)

        content = output_path.read_text()
        lines = content.strip().split("\n")
        # Only header
        assert len(lines) == 1


class TestGetClusterEvents:
    """Tests for _get_cluster_events function."""

    @pytest.fixture
    def mock_config(self) -> MagicMock:
        """Create a mock Config object."""
        config = MagicMock()
        config.get_user.return_value = ("admin", "password123")
        return config

    @pytest.fixture
    def sample_cluster_details(self) -> dict[str, Any]:
        """Sample cluster details."""
        return {
            "ip": "10.0.0.1",
            "div": "Engineering",
            "bu": "Platform",
        }

    @pytest.fixture
    def mock_ems_event(self) -> MagicMock:
        """Create a mock EMS event."""
        event = MagicMock()
        event.to_dict.return_value = {
            "time": "2024-01-15T10:00:00Z",
            "severity": "error",
            "message": {
                "name": "vsa.mlx.nic.detach",
                "text": "vsa.mlx.nic.detach: NIC 0 has been detached",
            },
        }
        return event

    def test_returns_empty_list_for_console_output(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        mock_ems_event: MagicMock,
    ) -> None:
        """Test that console output returns empty list."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = [mock_ems_event]

                with patch("pynetappfoundry.cli.commands.events.get.console"):
                    result = _get_cluster_events(
                        "cluster1",
                        sample_cluster_details,
                        mock_config,
                        severity=None,
                        event_names=(),
                        sort="time",
                        limit=50,
                        output_to_file=False,
                    )

        # Console output returns empty list
        assert result == []

    def test_returns_events_list_for_file_output(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        mock_ems_event: MagicMock,
    ) -> None:
        """Test that file output returns events list."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = [mock_ems_event]

                result = _get_cluster_events(
                    "cluster1",
                    sample_cluster_details,
                    mock_config,
                    severity=None,
                    event_names=(),
                    sort="time",
                    limit=50,
                    output_to_file=True,
                )

        assert len(result) == 1
        assert result[0]["cluster"] == "cluster1"
        assert result[0]["severity"] == "error"
        assert result[0]["name"] == "vsa.mlx.nic.detach"

    def test_message_is_cleaned_for_file_output(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        mock_ems_event: MagicMock,
    ) -> None:
        """Test that message is cleaned when outputting to file."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = [mock_ems_event]

                result = _get_cluster_events(
                    "cluster1",
                    sample_cluster_details,
                    mock_config,
                    severity=None,
                    event_names=(),
                    sort="time",
                    limit=50,
                    output_to_file=True,
                )

        # Message should have event name prefix removed
        assert "vsa.mlx.nic.detach:" not in result[0]["message"]
        assert "NIC 0 has been detached" in result[0]["message"]

    def test_severity_filter_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that severity filter is passed to API."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = []

                with patch("pynetappfoundry.cli.commands.events.get.console"):
                    _get_cluster_events(
                        "cluster1",
                        sample_cluster_details,
                        mock_config,
                        severity="error",
                        event_names=(),
                        sort="time",
                        limit=50,
                        output_to_file=False,
                    )

                # Check that severity was passed
                call_kwargs = mock_event_class.get_collection.call_args[1]
                assert call_kwargs["severity"] == "error"

    def test_event_names_filter_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that event names filter is passed to API."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = []

                with patch("pynetappfoundry.cli.commands.events.get.console"):
                    _get_cluster_events(
                        "cluster1",
                        sample_cluster_details,
                        mock_config,
                        severity=None,
                        event_names=("vsa.mlx.nic.detach", "vsa.mlx.nic.attach"),
                        sort="time",
                        limit=50,
                        output_to_file=False,
                    )

                # Check that event names were passed
                call_kwargs = mock_event_class.get_collection.call_args[1]
                assert call_kwargs["message.name"] == "vsa.mlx.nic.detach,vsa.mlx.nic.attach"

    def test_sort_ascending_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that ascending sort is passed to API."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = []

                with patch("pynetappfoundry.cli.commands.events.get.console"):
                    _get_cluster_events(
                        "cluster1",
                        sample_cluster_details,
                        mock_config,
                        severity=None,
                        event_names=(),
                        sort="time",
                        limit=50,
                        output_to_file=False,
                    )

                call_kwargs = mock_event_class.get_collection.call_args[1]
                assert call_kwargs["order_by"] == "time asc"

    def test_sort_descending_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that descending sort is passed to API."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = []

                with patch("pynetappfoundry.cli.commands.events.get.console"):
                    _get_cluster_events(
                        "cluster1",
                        sample_cluster_details,
                        mock_config,
                        severity=None,
                        event_names=(),
                        sort="-time",
                        limit=50,
                        output_to_file=False,
                    )

                call_kwargs = mock_event_class.get_collection.call_args[1]
                assert call_kwargs["order_by"] == "time desc"

    def test_handles_connection_error(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that connection errors are handled gracefully."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(side_effect=Exception("Connection failed"))

            with patch("pynetappfoundry.cli.commands.events.get.print_error") as mock_print:
                result = _get_cluster_events(
                    "cluster1",
                    sample_cluster_details,
                    mock_config,
                    severity=None,
                    event_names=(),
                    sort="time",
                    limit=50,
                    output_to_file=True,
                )

                # Should print error but not raise
                mock_print.assert_called()

        # Should return empty list
        assert result == []

    def test_limit_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that limit is passed to API."""
        with patch("pynetappfoundry.cli.commands.events.get.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("pynetappfoundry.cli.commands.events.get.EmsEvent") as mock_event_class:
                mock_event_class.get_collection.return_value = []

                with patch("pynetappfoundry.cli.commands.events.get.console"):
                    _get_cluster_events(
                        "cluster1",
                        sample_cluster_details,
                        mock_config,
                        severity=None,
                        event_names=(),
                        sort="time",
                        limit=100,
                        output_to_file=False,
                    )

                call_kwargs = mock_event_class.get_collection.call_args[1]
                assert call_kwargs["max_records"] == 100
