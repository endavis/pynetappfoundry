"""Tests for space usage report generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.reports.space_usage import SpaceUsageReport


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock Config object."""
    config = MagicMock()
    config.output_dir = Path("/tmp/test-output")
    config.get_user.return_value = ("admin", "password123")
    return config


@pytest.fixture
def sample_clusters() -> dict[str, dict[str, Any]]:
    """Sample cluster configuration."""
    return {
        "test-cluster-1": {
            "name": "test-cluster-1",
            "ip": "10.0.0.1",
            "div": "Engineering",
            "bu": "Platform",
            "app": "MyApp",
            "env": "Prod",
            "subapp": "",
            "cloud": "azure",
            "region": "eastus",
            "tags": ["active"],
        },
    }


class TestSpaceUsageReport:
    """Tests for SpaceUsageReport class."""

    def test_init_creates_workbook(
        self, mock_config: MagicMock, sample_clusters: dict[str, dict[str, Any]]
    ) -> None:
        """Test that initialization creates workbook and worksheets."""
        with patch("xlsxwriter.Workbook") as mock_workbook:
            mock_wb = MagicMock()
            mock_workbook.return_value = mock_wb

            _ = SpaceUsageReport(mock_config, sample_clusters)

            mock_workbook.assert_called_once()
            assert mock_wb.add_worksheet.call_count == 3

    def test_build_hierarchy(
        self, mock_config: MagicMock, sample_clusters: dict[str, dict[str, Any]]
    ) -> None:
        """Test that hierarchy is built from cluster details."""
        with patch("xlsxwriter.Workbook"):
            report = SpaceUsageReport(mock_config, sample_clusters)

            assert "Engineering" in report.divisions
            assert "Platform" in report.divisions["Engineering"]
            assert "MyApp" in report.divisions["Engineering"]["Platform"]

    def test_hierarchy_initializes_cluster_types(
        self, mock_config: MagicMock, sample_clusters: dict[str, dict[str, Any]]
    ) -> None:
        """Test that hierarchy initializes CVO and CVO HA types."""
        with patch("xlsxwriter.Workbook"):
            report = SpaceUsageReport(mock_config, sample_clusters)

            region_data = report.divisions["Engineering"]["Platform"]["MyApp"]["Prod"][""]["azure"][
                "eastus"
            ]
            assert "CVO" in region_data
            assert "CVO HA" in region_data
            assert region_data["CVO"]["RW"] is False
            assert region_data["CVO"]["DP"] is False
            assert region_data["CVO HA"]["RW"] is False
            assert region_data["CVO HA"]["DP"] is False


class TestSpaceUsageReportGatherData:
    """Tests for SpaceUsageReport.gather_data method."""

    @pytest.fixture
    def mock_volume(self) -> MagicMock:
        """Create a mock ONTAP Volume."""
        volume = MagicMock()
        volume.__getitem__ = MagicMock(
            side_effect=lambda key: {
                "name": "data_vol1",
                "type": "rw",
                "state": "online",
                "size": 1099511627776,  # 1 TiB
                "space": {"used": 549755813888},  # 0.5 TiB
            }.get(key)
        )
        return volume

    @pytest.fixture
    def mock_node(self) -> MagicMock:
        """Create a mock ONTAP Node."""
        node = MagicMock()
        node.__getitem__ = MagicMock(side_effect=lambda key: {"ha": {"enabled": True}}.get(key))
        return node

    def test_gather_data_collects_volumes(
        self,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
        mock_node: MagicMock,
        mock_volume: MagicMock,
    ) -> None:
        """Test that gather_data collects volume data."""
        with patch("xlsxwriter.Workbook"):
            report = SpaceUsageReport(mock_config, sample_clusters)

        with patch("netapp_ontap.host_connection.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node, mock_node]

                with patch("netapp_ontap.resources.Volume") as mock_vol_class:
                    mock_vol_class.get_collection.return_value = [mock_volume]

                    report.gather_data()

        assert len(report.volume_data) == 1
        vol_row = report.volume_data[0]
        assert vol_row[0] == "Engineering"  # div
        assert vol_row[1] == "Platform"  # bu
        assert vol_row[2] == "test-cluster-1"  # cluster name
        assert vol_row[8] == "CVO HA"  # cluster type (2 nodes with HA)
        assert vol_row[9] == "RW"  # data type

    def test_gather_data_handles_offline_volumes(
        self,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
        mock_node: MagicMock,
    ) -> None:
        """Test that offline volumes have used=0."""
        offline_volume = MagicMock()
        offline_volume.__getitem__ = MagicMock(
            side_effect=lambda key: {
                "name": "offline_vol",
                "type": "rw",
                "state": "offline",
                "size": 1099511627776,
                "space": {"used": 549755813888},
            }.get(key)
        )

        with patch("xlsxwriter.Workbook"):
            report = SpaceUsageReport(mock_config, sample_clusters)

        with patch("netapp_ontap.host_connection.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [mock_node]

                with patch("netapp_ontap.resources.Volume") as mock_vol_class:
                    mock_vol_class.get_collection.return_value = [offline_volume]

                    report.gather_data()

        assert len(report.volume_data) == 1
        vol_row = report.volume_data[0]
        assert vol_row[14] == 0.0  # used_tib should be 0 for offline

    def test_gather_data_handles_connection_error(
        self,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test that connection errors are handled gracefully."""
        with patch("xlsxwriter.Workbook"):
            report = SpaceUsageReport(mock_config, sample_clusters)

        with patch("netapp_ontap.host_connection.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(side_effect=Exception("Connection failed"))

            with patch(
                "pynetappfoundry.cli.commands.reports.space_usage.print_error"
            ) as mock_print:
                report.gather_data()
                mock_print.assert_called()

        assert len(report.volume_data) == 0

    def test_gather_data_detects_single_node_cluster(
        self,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
        mock_volume: MagicMock,
    ) -> None:
        """Test that single node clusters are detected as CVO."""
        single_node = MagicMock()
        single_node.__getitem__ = MagicMock(
            side_effect=lambda key: {"ha": {"enabled": False}}.get(key)
        )

        with patch("xlsxwriter.Workbook"):
            report = SpaceUsageReport(mock_config, sample_clusters)

        with patch("netapp_ontap.host_connection.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=None)

            with patch("netapp_ontap.resources.Node") as mock_node_class:
                mock_node_class.get_collection.return_value = [single_node]

                with patch("netapp_ontap.resources.Volume") as mock_vol_class:
                    mock_vol_class.get_collection.return_value = [mock_volume]

                    report.gather_data()

        assert len(report.volume_data) == 1
        vol_row = report.volume_data[0]
        assert vol_row[8] == "CVO"  # single node = CVO


class TestSpaceUsageReportBuildSheets:
    """Tests for SpaceUsageReport sheet building methods."""

    @pytest.fixture
    def report_with_data(
        self, mock_config: MagicMock, sample_clusters: dict[str, dict[str, Any]]
    ) -> SpaceUsageReport:
        """Create a report with mock data."""
        with patch("xlsxwriter.Workbook") as mock_wb_class:
            mock_wb = MagicMock()
            mock_wb_class.return_value = mock_wb
            mock_wb.add_worksheet.return_value = MagicMock()
            mock_wb.add_format.return_value = MagicMock()

            report = SpaceUsageReport(mock_config, sample_clusters)

            # Add test data
            report.volume_data = [
                [
                    "Engineering",  # div
                    "Platform",  # bu
                    "test-cluster-1",  # cluster
                    "MyApp",  # app
                    "Prod",  # env
                    "",  # subapp
                    "azure",  # cloud
                    "eastus",  # region
                    "CVO HA",  # cluster type
                    "RW",  # data type
                    "vol1",  # volume name
                    "online",  # state
                    "active",  # tags
                    1.0,  # size_tib
                    0.5,  # used_tib
                    50.0,  # percent_used
                ],
            ]

            # Mark the hierarchy as having data
            report.divisions["Engineering"]["Platform"]["MyApp"]["Prod"][""]["azure"]["eastus"][
                "CVO HA"
            ]["RW"] = True

            return report

    def test_build_volumes_sheet_writes_headers(self, report_with_data: SpaceUsageReport) -> None:
        """Test that volumes sheet writes headers."""
        report_with_data.build_volumes_sheet()

        # Check that write was called for headers
        assert report_with_data.volumes_ws.write.called

    def test_build_volumes_sheet_adds_table(self, report_with_data: SpaceUsageReport) -> None:
        """Test that volumes sheet adds a table."""
        report_with_data.build_volumes_sheet()

        report_with_data.volumes_ws.add_table.assert_called_once()

    def test_build_volumes_sheet_adds_conditional_formatting(
        self, report_with_data: SpaceUsageReport
    ) -> None:
        """Test that volumes sheet adds conditional formatting."""
        report_with_data.build_volumes_sheet()

        report_with_data.volumes_ws.conditional_format.assert_called_once()

    def test_build_usage_sheet_writes_sumifs_formulas(
        self, report_with_data: SpaceUsageReport
    ) -> None:
        """Test that usage sheet writes SUMIFS formulas."""
        report_with_data.build_usage_sheet()

        # Check that write was called with formulas
        calls = report_with_data.usage_ws.write.call_args_list
        formula_calls = [c for c in calls if "SUMIFS" in str(c)]
        assert len(formula_calls) > 0

    def test_build_totals_sheet_writes_formulas(self, report_with_data: SpaceUsageReport) -> None:
        """Test that totals sheet writes SUMIFS formulas."""
        report_with_data.build_totals_sheet()

        # Check that write_formula was called
        assert report_with_data.totals_ws.write_formula.called


class TestSpaceUsageReportGenerate:
    """Tests for SpaceUsageReport.generate method."""

    def test_generate_with_no_data_prints_error(
        self, mock_config: MagicMock, sample_clusters: dict[str, dict[str, Any]]
    ) -> None:
        """Test that generate prints error when no data collected."""
        with patch("xlsxwriter.Workbook") as mock_wb_class:
            mock_wb = MagicMock()
            mock_wb_class.return_value = mock_wb
            mock_wb.add_worksheet.return_value = MagicMock()
            mock_wb.add_format.return_value = MagicMock()

            report = SpaceUsageReport(mock_config, sample_clusters)

        with patch("netapp_ontap.host_connection.HostConnection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(side_effect=Exception("Connection failed"))

            with patch(
                "pynetappfoundry.cli.commands.reports.space_usage.print_error"
            ) as mock_print:
                report.generate()
                # Should print error about no data
                assert any("No volume data" in str(c) for c in mock_print.call_args_list)
