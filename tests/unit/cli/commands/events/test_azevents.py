"""Tests for events save-azure command."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.events.azevents import ClusterData


class TestClusterDataInit:
    """Tests for ClusterData initialization."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> MagicMock:
        """Create a mock Config object."""
        config = MagicMock()
        config.get_user.return_value = ("admin", "password123")
        config.db_dir = tmp_path
        return config

    @pytest.fixture
    def mock_db(self) -> MagicMock:
        """Create a mock AzEventsDB."""
        return MagicMock()

    @pytest.fixture
    def sample_cluster_details(self) -> dict[str, Any]:
        """Sample cluster details for Azure cluster."""
        return {
            "ip": "10.0.0.1",
            "div": "Engineering",
            "bu": "Platform",
            "cloud": "azure",
        }

    def test_initializes_with_correct_name(
        self,
        mock_config: MagicMock,
        mock_db: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that ClusterData initializes with correct name."""
        cluster = ClusterData(
            "test-cluster", sample_cluster_details, mock_config, mock_db, datetime.now()
        )
        assert cluster.name == "test-cluster"

    def test_initializes_with_empty_state(
        self,
        mock_config: MagicMock,
        mock_db: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that ClusterData initializes with empty state."""
        cluster = ClusterData(
            "test-cluster", sample_cluster_details, mock_config, mock_db, datetime.now()
        )
        assert cluster.cluster_type == ""
        assert cluster.current_azevent == ""
        assert cluster.azmaints == {}
        assert cluster.ems_events == []


class TestClusterDataEmptyAzevent:
    """Tests for _empty_azevent method."""

    @pytest.fixture
    def cluster_data(self, tmp_path: Path) -> ClusterData:
        """Create a ClusterData instance for testing."""
        config = MagicMock()
        config.db_dir = tmp_path
        return ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            config,
            MagicMock(),
            datetime.now(),
        )

    def test_returns_dict_with_unknown_event_id(self, cluster_data: ClusterData) -> None:
        """Test that _empty_azevent returns dict with Unknown event_id."""
        result = cluster_data._empty_azevent()
        assert result == {"event_id": "Unknown"}

    def test_resets_current_azevent(self, cluster_data: ClusterData) -> None:
        """Test that _empty_azevent resets current_azevent."""
        cluster_data.current_azevent = "some-event-id"
        cluster_data._empty_azevent()
        assert cluster_data.current_azevent == ""


class TestClusterDataAddEmsevent:
    """Tests for _add_emsevent method."""

    @pytest.fixture
    def cluster_data(self, tmp_path: Path) -> ClusterData:
        """Create a ClusterData instance for testing."""
        config = MagicMock()
        config.db_dir = tmp_path
        return ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            config,
            MagicMock(),
            datetime.now(),
        )

    def test_adds_event_to_list(self, cluster_data: ClusterData) -> None:
        """Test that _add_emsevent adds event to ems_events list."""
        cluster_data.current_azevent = "event-123"
        emsevent = {
            "log_message": "vsa.scheduledEvent.scheduled: Maintenance scheduled",
            "message": {"name": "vsa.scheduledEvent.scheduled", "severity": "notice"},
            "node": {"name": "node-01"},
            "time": "2024-01-15T10:00:00Z",
        }
        cluster_data._add_emsevent(emsevent)
        assert len(cluster_data.ems_events) == 1
        assert cluster_data.ems_events[0]["event_id"] == "event-123"
        assert cluster_data.ems_events[0]["cluster"] == "test-cluster"

    def test_cleans_message(self, cluster_data: ClusterData) -> None:
        """Test that message is cleaned properly."""
        cluster_data.current_azevent = "event-123"
        emsevent = {
            "log_message": "vsa.scheduledEvent.scheduled: Maintenance, with commas\nand newlines",
            "message": {"name": "vsa.scheduledEvent.scheduled", "severity": "notice"},
            "node": {"name": "node-01"},
            "time": "2024-01-15T10:00:00Z",
        }
        cluster_data._add_emsevent(emsevent)
        message = cluster_data.ems_events[0]["message"]
        # Event name prefix removed
        assert "vsa.scheduledEvent.scheduled:" not in message
        # Commas replaced with semicolons
        assert "," not in message
        # Newlines removed
        assert "\n" not in message


class TestClusterDataAddAzmaint:
    """Tests for _add_azmaint method."""

    @pytest.fixture
    def cluster_data(self, tmp_path: Path) -> ClusterData:
        """Create a ClusterData instance for testing."""
        config = MagicMock()
        config.db_dir = tmp_path
        return ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            config,
            MagicMock(),
            datetime.now(),
        )

    def test_adds_new_event(self, cluster_data: ClusterData) -> None:
        """Test that new event is added to azmaints."""
        azmaint = {"event_id": "event-123", "cluster": "test-cluster"}
        cluster_data._add_azmaint(azmaint)
        assert "event-123" in cluster_data.azmaints
        assert cluster_data.azmaints["event-123"]["cluster"] == "test-cluster"

    def test_updates_existing_event(self, cluster_data: ClusterData) -> None:
        """Test that existing event is updated."""
        cluster_data.azmaints["event-123"] = {"event_id": "event-123", "field1": "value1"}
        azmaint = {"event_id": "event-123", "field2": "value2"}
        cluster_data._add_azmaint(azmaint)
        assert cluster_data.azmaints["event-123"]["field1"] == "value1"
        assert cluster_data.azmaints["event-123"]["field2"] == "value2"

    def test_resets_current_azevent(self, cluster_data: ClusterData) -> None:
        """Test that current_azevent is reset."""
        cluster_data.current_azevent = "event-123"
        cluster_data._add_azmaint({"event_id": "event-123"})
        assert cluster_data.current_azevent == ""


class TestClusterDataGetParamValue:
    """Tests for _get_param_value method."""

    @pytest.fixture
    def cluster_data(self, tmp_path: Path) -> ClusterData:
        """Create a ClusterData instance for testing."""
        config = MagicMock()
        config.db_dir = tmp_path
        return ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            config,
            MagicMock(),
            datetime.now(),
        )

    def test_returns_value_when_found(self, cluster_data: ClusterData) -> None:
        """Test that value is returned when parameter exists."""
        parameters = [
            {"name": "event_id", "value": "abc-123"},
            {"name": "event_type", "value": "Freeze"},
        ]
        result = cluster_data._get_param_value(parameters, "event_id")
        assert result == "abc-123"

    def test_returns_none_when_not_found(self, cluster_data: ClusterData) -> None:
        """Test that None is returned when parameter doesn't exist."""
        parameters = [{"name": "event_id", "value": "abc-123"}]
        result = cluster_data._get_param_value(parameters, "nonexistent")
        assert result is None

    def test_handles_empty_list(self, cluster_data: ClusterData) -> None:
        """Test that empty list is handled."""
        result = cluster_data._get_param_value([], "event_id")
        assert result is None


class TestClusterDataGatherData:
    """Tests for gather_data method."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> MagicMock:
        """Create a mock Config object."""
        config = MagicMock()
        config.get_user.return_value = ("admin", "password123")
        config.db_dir = tmp_path
        return config

    @pytest.fixture
    def mock_db(self) -> MagicMock:
        """Create a mock AzEventsDB."""
        return MagicMock()

    @pytest.fixture
    def sample_cluster_details(self) -> dict[str, Any]:
        """Sample cluster details."""
        return {"ip": "10.0.0.1", "cloud": "azure"}

    def test_detects_cvo_single_node(
        self,
        mock_config: MagicMock,
        mock_db: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that single node cluster is detected as CVO."""
        cluster = ClusterData(
            "test-cluster",
            sample_cluster_details,
            mock_config,
            mock_db,
            datetime.now(),
        )

        mock_node = MagicMock()
        mock_node.to_dict.return_value = {"ha": {"enabled": False}}

        with patch("netapp_ontap.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node]

                with patch("netapp_ontap.resources.EmsEvent") as mock_ems:
                    mock_ems.get_collection.return_value = []

                    cluster.gather_data()

        assert cluster.cluster_type == "CVO"

    def test_detects_cvo_ha_multiple_nodes(
        self,
        mock_config: MagicMock,
        mock_db: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that multi-node HA cluster is detected as CVO HA."""
        cluster = ClusterData(
            "test-cluster",
            sample_cluster_details,
            mock_config,
            mock_db,
            datetime.now(),
        )

        mock_node1 = MagicMock()
        mock_node1.to_dict.return_value = {"ha": {"enabled": True}}
        mock_node2 = MagicMock()
        mock_node2.to_dict.return_value = {"ha": {"enabled": True}}

        with patch("netapp_ontap.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node1, mock_node2]

                with patch("netapp_ontap.resources.EmsEvent") as mock_ems:
                    mock_ems.get_collection.return_value = []

                    cluster.gather_data()

        assert cluster.cluster_type == "CVO HA"

    def test_parses_scheduled_event(
        self,
        mock_config: MagicMock,
        mock_db: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that vsa.scheduledEvent.scheduled is parsed correctly."""
        cluster = ClusterData(
            "test-cluster",
            sample_cluster_details,
            mock_config,
            mock_db,
            datetime.now(),
        )

        mock_node = MagicMock()
        mock_node.to_dict.return_value = {"ha": {"enabled": False}}

        mock_scheduled_event = MagicMock()
        mock_scheduled_event.to_dict.return_value = {
            "message": {"name": "vsa.scheduledEvent.scheduled", "severity": "notice"},
            "log_message": "vsa.scheduledEvent.scheduled: Maintenance scheduled",
            "node": {"name": "node-01"},
            "time": "2024-01-15T10:00:00Z",
            "parameters": [
                {"name": "event_id", "value": "event-123"},
                {"name": "event_type", "value": "Freeze"},
                {"name": "node", "value": "node-01"},
                {"name": "status", "value": "scheduled"},
                {"name": "not_before_time", "value": "01/15/2024 12:00:00"},
            ],
        }

        mock_update_event = MagicMock()
        mock_update_event.to_dict.return_value = {
            "message": {"name": "vsa.scheduledEvent.update", "severity": "notice"},
            "log_message": "vsa.scheduledEvent.update: Maintenance complete",
            "node": {"name": "node-01"},
            "time": "2024-01-15T14:00:00Z",
            "parameters": [
                {"name": "event_id", "value": "event-123"},
                {"name": "event_type", "value": "Freeze"},
                {"name": "node", "value": "node-01"},
                {"name": "status", "value": "complete"},
                {"name": "not_before_time", "value": "01/15/2024 12:00:00"},
            ],
        }

        with patch("netapp_ontap.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node]

                with patch("netapp_ontap.resources.EmsEvent") as mock_ems:
                    # First call returns scheduled events (check), second returns all events
                    mock_ems.get_collection.side_effect = [
                        [mock_scheduled_event],
                        [mock_scheduled_event, mock_update_event],
                    ]

                    cluster.gather_data()

        # For CVO, should complete on az_maint_complete
        assert "event-123" in cluster.azmaints
        assert cluster.azmaints["event-123"]["event_id"] == "event-123"
        assert cluster.azmaints["event-123"]["type"] == "Freeze"

    def test_handles_connection_error(
        self,
        mock_config: MagicMock,
        mock_db: MagicMock,
        sample_cluster_details: dict[str, Any],
    ) -> None:
        """Test that connection errors are handled gracefully."""
        import netapp_ontap.error

        cluster = ClusterData(
            "test-cluster",
            sample_cluster_details,
            mock_config,
            mock_db,
            datetime.now(),
        )

        with patch("netapp_ontap.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(
                side_effect=netapp_ontap.error.NetAppRestError("Connection failed")
            )

            with patch("pynetappfoundry.cli.commands.events.azevents.print_error") as mock_print:
                cluster.gather_data()
                mock_print.assert_called()

        # Should not raise, azmaints should be empty
        assert cluster.azmaints == {}


class TestClusterDataProcessData:
    """Tests for process_data method."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> MagicMock:
        """Create a mock Config object."""
        config = MagicMock()
        config.db_dir = tmp_path
        return config

    @pytest.fixture
    def mock_db(self) -> MagicMock:
        """Create a mock AzEventsDB."""
        db = MagicMock()
        db.get_event_by_id.return_value = {
            "event_id": "event-123",
            "cluster": "test-cluster",
            "node": "node-01",
            "type": "Freeze",
            "az_maint_not_before": "2024-01-15T12:00:00",
            "az_maint_scheduled": "2024-01-15T10:00:00",
            "az_maint_started": "2024-01-15T12:00:00",
            "az_maint_complete": "2024-01-15T14:00:00",
            "node_takeover_complete": "",
            "node_reboot_starts": "",
            "node_reboot_complete": "",
            "node_ready_for_giveback": "",
            "node_giveback_starts": "",
            "node_giveback_complete": "",
        }
        return db

    def test_upserts_events_to_database(self, mock_config: MagicMock, mock_db: MagicMock) -> None:
        """Test that events are upserted to database."""
        cluster = ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            mock_config,
            mock_db,
            datetime.now(),
        )
        cluster.cluster_type = "CVO"
        cluster.azmaints = {"event-123": {"event_id": "event-123", "cluster": "test-cluster"}}

        cluster.process_data()

        mock_db.upsert_event.assert_called_once()

    def test_creates_error_db_for_unknown_event_id(
        self, mock_config: MagicMock, mock_db: MagicMock
    ) -> None:
        """Test that error database is created for events without ID."""
        cluster = ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            mock_config,
            mock_db,
            datetime.now(),
        )
        cluster.cluster_type = "CVO"
        cluster.azmaints = {"Unknown": {"event_id": "Unknown", "cluster": "test-cluster"}}
        cluster.ems_events = [{"event_id": "Unknown", "cluster": "test-cluster"}]

        with patch("pynetappfoundry.cli.commands.events.azevents.EmsEventsDB") as mock_ems_db:
            mock_ems_db.return_value.exists = False

            with patch("pynetappfoundry.cli.commands.events.azevents.print_error") as mock_print:
                cluster.process_data()
                # Should print error about event without id
                assert any("Event without id" in str(call) for call in mock_print.call_args_list)

    def test_creates_error_db_for_missing_maint_fields(self, mock_config: MagicMock) -> None:
        """Test that error database is created for events missing maintenance fields."""
        mock_db = MagicMock()
        mock_db.get_event_by_id.return_value = {
            "event_id": "event-123",
            "node": "node-01",
            "az_maint_not_before": "",  # Missing
            "az_maint_scheduled": "",
            "az_maint_started": "",
            "az_maint_complete": "",
        }

        cluster = ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            mock_config,
            mock_db,
            datetime.now(),
        )
        cluster.cluster_type = "CVO"
        cluster.azmaints = {"event-123": {"event_id": "event-123"}}
        cluster.ems_events = [{"event_id": "event-123"}]

        with patch("pynetappfoundry.cli.commands.events.azevents.EmsEventsDB") as mock_ems_db:
            mock_ems_db.return_value.exists = False

            with patch("pynetappfoundry.cli.commands.events.azevents.print_error") as mock_print:
                cluster.process_data()
                # Should print error about missing fields with field names
                assert any("missing fields:" in str(call) for call in mock_print.call_args_list)
                assert any("az_maint_not_before" in str(call) for call in mock_print.call_args_list)

    def test_creates_error_db_for_cvo_ha_missing_failover_fields(
        self, mock_config: MagicMock
    ) -> None:
        """Test that error database is created for CVO HA events missing failover fields."""
        mock_db = MagicMock()
        mock_db.get_event_by_id.return_value = {
            "event_id": "event-123",
            "node": "node-01",
            "az_maint_not_before": "2024-01-15T12:00:00",
            "az_maint_scheduled": "2024-01-15T10:00:00",
            "az_maint_started": "2024-01-15T12:00:00",
            "az_maint_complete": "2024-01-15T14:00:00",
            "node_takeover_complete": "",  # Missing for HA
            "node_reboot_starts": "",
            "node_reboot_complete": "",
            "node_ready_for_giveback": "",
            "node_giveback_starts": "",
            "node_giveback_complete": "",
        }

        cluster = ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            mock_config,
            mock_db,
            datetime.now(),
        )
        cluster.cluster_type = "CVO HA"
        cluster.azmaints = {"event-123": {"event_id": "event-123"}}
        cluster.ems_events = [{"event_id": "event-123"}]

        with patch("pynetappfoundry.cli.commands.events.azevents.EmsEventsDB") as mock_ems_db:
            mock_ems_db.return_value.exists = False

            with patch("pynetappfoundry.cli.commands.events.azevents.print_error") as mock_print:
                cluster.process_data()
                # Should print error about missing fields with field names
                assert any("missing fields:" in str(call) for call in mock_print.call_args_list)
                assert any(
                    "node_takeover_complete" in str(call) for call in mock_print.call_args_list
                )


class TestTimingFieldExtraction:
    """Tests for extracting all 10 timing fields."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> MagicMock:
        """Create a mock Config object."""
        config = MagicMock()
        config.get_user.return_value = ("admin", "password123")
        config.db_dir = tmp_path
        return config

    @pytest.fixture
    def mock_db(self) -> MagicMock:
        """Create a mock AzEventsDB."""
        return MagicMock()

    def test_extracts_all_ha_timing_fields(
        self, mock_config: MagicMock, mock_db: MagicMock
    ) -> None:
        """Test that all 10 timing fields are extracted for HA cluster."""
        cluster = ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            mock_config,
            mock_db,
            datetime.now(),
        )

        mock_node = MagicMock()
        mock_node.to_dict.return_value = {"ha": {"enabled": True}}

        # Create mock events for full maintenance lifecycle
        def create_event(
            name: str, time: str, parameters: list[dict[str, str]] | None = None
        ) -> MagicMock:
            event = MagicMock()
            event.to_dict.return_value = {
                "message": {"name": name, "severity": "notice"},
                "log_message": f"{name}: test",
                "node": {"name": "node-01"},
                "time": time,
                "parameters": parameters or [],
            }
            return event

        scheduled_event = create_event(
            "vsa.scheduledEvent.scheduled",
            "2024-01-15T10:00:00Z",
            [
                {"name": "event_id", "value": "event-123"},
                {"name": "event_type", "value": "Freeze"},
                {"name": "node", "value": "node-01"},
                {"name": "status", "value": "scheduled"},
                {"name": "not_before_time", "value": "01/15/2024 12:00:00"},
            ],
        )

        started_event = create_event(
            "vsa.scheduledEvent.update",
            "2024-01-15T12:00:00Z",
            [
                {"name": "event_id", "value": "event-123"},
                {"name": "status", "value": "started"},
            ],
        )

        complete_event = create_event(
            "vsa.scheduledEvent.update",
            "2024-01-15T12:05:00Z",
            [
                {"name": "event_id", "value": "event-123"},
                {"name": "status", "value": "complete"},
            ],
        )

        takeover_event = create_event("cf.fsm.nfo.startingGracefulShutdown", "2024-01-15T12:01:00Z")
        shutdown_event = create_event("kern.shutdown", "2024-01-15T12:02:00Z")
        boot_event = create_event("mgr.boot.disk_done", "2024-01-15T12:03:00Z")
        ready_event = create_event("cf.fsm.takeoverOfPartnerEnabled", "2024-01-15T12:04:00Z")
        giveback_start_event = create_event("clam.valid.config", "2024-01-15T12:05:00Z")
        giveback_complete_event = create_event("callhome.reboot.giveback", "2024-01-15T12:06:00Z")

        all_events = [
            scheduled_event,
            started_event,
            takeover_event,
            shutdown_event,
            boot_event,
            ready_event,
            complete_event,
            giveback_start_event,
            giveback_complete_event,
        ]

        with patch("netapp_ontap.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node, mock_node]

                with patch("netapp_ontap.resources.EmsEvent") as mock_ems:
                    mock_ems.get_collection.side_effect = [
                        [scheduled_event],  # Check for scheduled events
                        all_events,  # All events for processing
                    ]

                    cluster.gather_data()

        # Verify event was collected
        assert "event-123" in cluster.azmaints
        event = cluster.azmaints["event-123"]

        # Check all timing fields
        assert "az_maint_not_before" in event
        assert "az_maint_scheduled" in event
        assert event.get("az_maint_started") == "2024-01-15T12:00:00Z"
        assert event.get("az_maint_complete") == "2024-01-15T12:05:00Z"
        assert event.get("node_takeover_complete") == "2024-01-15T12:01:00Z"
        assert event.get("node_reboot_starts") == "2024-01-15T12:02:00Z"
        assert event.get("node_reboot_complete") == "2024-01-15T12:03:00Z"
        assert event.get("node_ready_for_giveback") == "2024-01-15T12:04:00Z"
        assert event.get("node_giveback_starts") == "2024-01-15T12:05:00Z"
        assert event.get("node_giveback_complete") == "2024-01-15T12:06:00Z"


class TestOutOfOrderEvents:
    """Tests for handling out-of-order events."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> MagicMock:
        """Create a mock Config object."""
        config = MagicMock()
        config.get_user.return_value = ("admin", "password123")
        config.db_dir = tmp_path
        return config

    def test_handles_out_of_order_update_event(self, mock_config: MagicMock) -> None:
        """Test that out-of-order update events are handled."""
        cluster = ClusterData(
            "test-cluster",
            {"ip": "10.0.0.1"},
            mock_config,
            MagicMock(),
            datetime.now(),
        )

        mock_node = MagicMock()
        mock_node.to_dict.return_value = {"ha": {"enabled": False}}

        def create_event(name: str, event_id: str, status: str, time: str) -> MagicMock:
            event = MagicMock()
            event.to_dict.return_value = {
                "message": {"name": name, "severity": "notice"},
                "log_message": f"{name}: test",
                "node": {"name": "node-01"},
                "time": time,
                "parameters": [
                    {"name": "event_id", "value": event_id},
                    {"name": "event_type", "value": "Freeze"},
                    {"name": "node", "value": "node-01"},
                    {"name": "status", "value": status},
                    {"name": "not_before_time", "value": "01/15/2024 12:00:00"},
                ],
            }
            return event

        # Event 1 scheduled
        event1_scheduled = create_event(
            "vsa.scheduledEvent.scheduled", "event-1", "scheduled", "2024-01-15T10:00:00Z"
        )
        # Event 2 update comes before event 1 completes (out of order)
        event2_update = create_event(
            "vsa.scheduledEvent.update", "event-2", "started", "2024-01-15T11:00:00Z"
        )
        # Event 1 complete
        event1_complete = create_event(
            "vsa.scheduledEvent.update", "event-1", "complete", "2024-01-15T12:00:00Z"
        )

        with patch("netapp_ontap.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node]

                with patch("netapp_ontap.resources.EmsEvent") as mock_ems:
                    mock_ems.get_collection.side_effect = [
                        [event1_scheduled],
                        [event1_scheduled, event2_update, event1_complete],
                    ]

                    with patch("pynetappfoundry.cli.commands.events.azevents.print_warning"):
                        cluster.gather_data()

        # Both events should be tracked
        assert "event-1" in cluster.azmaints
