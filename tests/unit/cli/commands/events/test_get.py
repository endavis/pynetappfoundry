"""Tests for events get command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cli.commands.events.get import (
    _get_cluster_events,
    _write_csv,
    clean_message,
)
from pynetappfoundry.models.ontap.support.ems.events import OntapEmsEventResponse
from pynetappfoundry.query import QuerySet

MODULE = "pynetappfoundry.cli.commands.events.get"


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
                "node": "node-01",
                "time": "2024-01-15T10:00:00",
                "name": "vsa.event",
                "severity": "error",
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
                "node": "node-01",
                "time": "2024-01-15T10:00:00",
                "name": "vsa.event",
                "severity": "error",
                "message": "Test message",
            }
        ]
        _write_csv(output_path, events)

        content = output_path.read_text()
        lines = content.strip().split("\n")
        header = lines[0]
        assert "cluster" in header
        assert "node" in header
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
                "node": "node-01",
                "time": "2024-01-15T10:00:00",
                "name": "vsa.event",
                "severity": "error",
                "message": "Test message 1",
            },
            {
                "cluster": "cluster2",
                "node": "node-02",
                "time": "2024-01-15T11:00:00",
                "name": "vsa.other",
                "severity": "warning",
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
    def ems_event(self) -> OntapEmsEventResponse:
        """Create an EMS event as the API returns it."""
        return OntapEmsEventResponse.model_validate(
            {
                "node": {"name": "node-01"},
                "time": "2024-01-15T10:00:00Z",
                "message": {"name": "vsa.mlx.nic.detach", "severity": "error"},
                "log_message": "vsa.mlx.nic.detach: NIC 0 has been detached",
            }
        )

    def _run(
        self,
        config: MagicMock,
        details: dict[str, Any],
        events: list[OntapEmsEventResponse],
        **kwargs: Any,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Run _get_cluster_events with the live fetch stubbed out.

        Returns:
            The events it returned, and the query params it sent to the API.
        """
        sent: dict[str, Any] = {}

        def fake_all(qs: QuerySet) -> list[OntapEmsEventResponse]:
            sent.update(qs._build_merged_filter_dict())
            return events

        args: dict[str, Any] = {"severity": None, "event_names": (), "sort": "time", "limit": 50}
        args.update(kwargs)
        with (
            patch(f"{MODULE}.ONTAPAPIClient"),
            patch.object(QuerySet, "_all_via_data_source", autospec=True, side_effect=fake_all),
        ):
            result = _get_cluster_events("cluster1", details, config, **args)
        return result, sent

    def test_returns_events_list_for_file_output(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        ems_event: OntapEmsEventResponse,
    ) -> None:
        """Test that file output returns events list."""
        result, _ = self._run(mock_config, sample_cluster_details, [ems_event])

        assert len(result) == 1
        assert result[0]["cluster"] == "cluster1"
        assert result[0]["node"] == "node-01"
        assert result[0]["severity"] == "error"
        assert result[0]["name"] == "vsa.mlx.nic.detach"

    def test_time_formatted_as_before_migration(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        ems_event: OntapEmsEventResponse,
    ) -> None:
        """Test that time keeps the format the netapp_ontap SDK's datetime produced."""
        result, _ = self._run(mock_config, sample_cluster_details, [ems_event])

        assert result[0]["time"] == "2024-01-15 10:00:00+00:00"

    def test_message_is_cleaned_for_file_output(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        ems_event: OntapEmsEventResponse,
    ) -> None:
        """Test that message is cleaned when outputting to file."""
        result, _ = self._run(mock_config, sample_cluster_details, [ems_event])

        assert "vsa.mlx.nic.detach:" not in result[0]["message"]
        assert "NIC 0 has been detached" in result[0]["message"]

    def test_severity_filter_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that severity filter is passed as message.severity to API."""
        _, sent = self._run(mock_config, sample_cluster_details, [], severity="error")

        assert sent["message.severity"] == "error"

    def test_default_severity_wildcard_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that message.severity defaults to '*' to include debug events."""
        _, sent = self._run(mock_config, sample_cluster_details, [])

        assert sent["message.severity"] == "*"

    def test_event_names_filter_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that event names filter is passed to API."""
        _, sent = self._run(
            mock_config,
            sample_cluster_details,
            [],
            event_names=("vsa.mlx.nic.detach", "vsa.mlx.nic.attach"),
        )

        assert sent["message.name"] == "vsa.mlx.nic.detach,vsa.mlx.nic.attach"

    def test_no_event_names_filter_by_default(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that message.name is not sent when no event names are given."""
        _, sent = self._run(mock_config, sample_cluster_details, [])

        assert "message.name" not in sent

    def test_sort_ascending_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that ascending sort is passed to API."""
        _, sent = self._run(mock_config, sample_cluster_details, [], sort="time")

        assert sent["order_by"] == "time asc"

    def test_sort_descending_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that descending sort is passed to API."""
        _, sent = self._run(mock_config, sample_cluster_details, [], sort="-time")

        assert sent["order_by"] == "time desc"

    def test_handles_connection_error(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that connection errors are handled gracefully."""
        with (
            patch(f"{MODULE}.ONTAPAPIClient", side_effect=Exception("Connection failed")),
            patch(f"{MODULE}.print_error") as mock_print,
        ):
            result = _get_cluster_events(
                "cluster1",
                sample_cluster_details,
                mock_config,
                severity=None,
                event_names=(),
                sort="time",
                limit=50,
            )

        # Should print error but not raise, and return an empty list
        mock_print.assert_called()
        assert result == []

    def test_limit_passed_to_api(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that limit is passed to API."""
        _, sent = self._run(mock_config, sample_cluster_details, [], limit=100)

        assert sent["max_records"] == "100"

    def test_requests_all_fields(self) -> None:
        """Test that the EMS event query asks the API for every field."""
        mapping = model_registry.get_mapping("OntapEmsEventResponse")

        assert mapping is not None
        assert mapping.api_endpoint.endswith("?fields=*")

    def test_node_included_in_csv_output(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        ems_event: OntapEmsEventResponse,
    ) -> None:
        """Test that node is included in CSV output."""
        result, _ = self._run(mock_config, sample_cluster_details, [ems_event])

        assert result[0]["node"] == "node-01"

    def test_message_uses_log_message(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        ems_event: OntapEmsEventResponse,
    ) -> None:
        """Test that message comes from log_message field."""
        result, _ = self._run(mock_config, sample_cluster_details, [ems_event])

        # Message should come from log_message (prefix stripped)
        assert "NIC 0 has been detached" in result[0]["message"]

    def test_severity_from_message_object(
        self,
        mock_config: MagicMock,
        sample_cluster_details: dict[str, Any],
        ems_event: OntapEmsEventResponse,
    ) -> None:
        """Test that severity comes from message.severity, not top-level."""
        result, _ = self._run(mock_config, sample_cluster_details, [ems_event])

        assert result[0]["severity"] == "error"
