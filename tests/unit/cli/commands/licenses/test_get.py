"""Tests for licenses get command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.licenses.get import (
    _get_cluster_licenses,
    _print_table,
    _write_csv,
)
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
    OntapLicensePackageResponseLicense,
)


def _make_license(
    *,
    owner: str = "node1",
    serial: str = "SN-001",
    expiry: str = "2026-12-31T00:00:00Z",
) -> OntapLicensePackageResponseLicense:
    """Create a license sub-model with common defaults."""
    return OntapLicensePackageResponseLicense(
        owner=owner,
        serial_number=serial,
        expiry_time=expiry,
    )


def _make_package(
    *,
    description: str = "Base License",
    licenses: list[OntapLicensePackageResponseLicense] | None = None,
) -> OntapLicensePackageResponse:
    """Create a license package model with common defaults."""
    return OntapLicensePackageResponse(
        name="base",
        description=description,
        licenses=licenses or [],
    )


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock Config object."""
    config = MagicMock()
    config.get_user.return_value = ("admin", "password123")
    config.output_dir = Path("/tmp/test_output")
    config.get_ontap_api_settings.return_value = MagicMock(
        base_api_path="/api",
        timeout=30.0,
    )
    config.get_schema_location.return_value = Path("/tmp/schema")
    return config


@pytest.fixture
def sample_details() -> dict[str, Any]:
    """Sample cluster connection details."""
    return {"ip": "10.0.0.1", "bu": "Platform", "env": "Prod"}


class TestGetClusterLicenses:
    """Tests for _get_cluster_licenses."""

    @patch("pynetappfoundry.cli.commands.licenses.get.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.get.ONTAPAPIClient")
    def test_returns_filtered_rows(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test that licenses with expiry and valid owner are included."""
        lic = _make_license()
        pkg = _make_package(description="Cloud ONTAP License", licenses=[lic])
        mock_qs_cls.return_value.all.return_value = [pkg]

        rows = _get_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(rows) == 1
        assert rows[0] == (
            "cluster1",
            "Cloud ONTAP License",
            "node1",
            "SN-001",
            "2026-12-31T00:00:00Z",
        )

    @patch("pynetappfoundry.cli.commands.licenses.get.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.get.ONTAPAPIClient")
    def test_no_expiry_shows_as_no_expiry(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test that licenses without expiry_time show 'No expiry'."""
        lic = _make_license(expiry="")
        pkg = _make_package(description="Cloud ONTAP License", licenses=[lic])
        mock_qs_cls.return_value.all.return_value = [pkg]

        rows = _get_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(rows) == 1
        assert rows[0] == ("cluster1", "Cloud ONTAP License", "node1", "SN-001", "No expiry")

    @patch("pynetappfoundry.cli.commands.licenses.get.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.get.ONTAPAPIClient")
    def test_filters_owner_none(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test that licenses with owner 'none' are excluded."""
        lic = _make_license(owner="none")
        pkg = _make_package(description="Cloud ONTAP License", licenses=[lic])
        mock_qs_cls.return_value.all.return_value = [pkg]

        rows = _get_cluster_licenses("cluster1", sample_details, mock_config)

        assert rows == []

    @patch("pynetappfoundry.cli.commands.licenses.get.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.get.ONTAPAPIClient")
    def test_filters_empty_owner(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test that licenses with empty owner are excluded."""
        lic = _make_license(owner="")
        pkg = _make_package(description="Cloud ONTAP License", licenses=[lic])
        mock_qs_cls.return_value.all.return_value = [pkg]

        rows = _get_cluster_licenses("cluster1", sample_details, mock_config)

        assert rows == []

    @patch("pynetappfoundry.cli.commands.licenses.get.print_error")
    @patch("pynetappfoundry.cli.commands.licenses.get.ONTAPAPIClient")
    def test_error_handling_returns_empty(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test that connection errors are handled gracefully."""
        mock_client_cls.side_effect = Exception("Connection refused")

        rows = _get_cluster_licenses("cluster1", sample_details, mock_config)

        assert rows == []
        mock_print_error.assert_called_once()

    @patch("pynetappfoundry.cli.commands.licenses.get.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.get.ONTAPAPIClient")
    def test_multiple_packages_and_licenses(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test processing multiple packages with multiple licenses."""
        lic1 = _make_license(owner="node1", serial="SN-001")
        lic2 = _make_license(owner="node2", serial="SN-002")
        pkg1 = _make_package(description="Cloud ONTAP License", licenses=[lic1, lic2])

        lic3 = _make_license(owner="node1", serial="SN-003")
        pkg2 = _make_package(description="NFS License", licenses=[lic3])

        mock_qs_cls.return_value.all.return_value = [pkg1, pkg2]

        rows = _get_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(rows) == 3
        assert rows[0][3] == "SN-001"
        assert rows[1][3] == "SN-002"
        assert rows[2][3] == "SN-003"


class TestPrintTable:
    """Tests for _print_table."""

    @patch("pynetappfoundry.cli.commands.licenses.get.console")
    def test_prints_table(self, mock_console: MagicMock) -> None:
        """Test that a Rich table is printed to console."""
        rows = [("cluster1", "Base License", "node1", "SN-001", "2026-12-31")]
        _print_table(rows)

        mock_console.print.assert_called_once()
        table = mock_console.print.call_args[0][0]
        assert table.title == "Cluster Licenses"

    @patch("pynetappfoundry.cli.commands.licenses.get.console")
    def test_empty_rows(self, mock_console: MagicMock) -> None:
        """Test table with no rows."""
        _print_table([])
        mock_console.print.assert_called_once()


class TestWriteCsv:
    """Tests for _write_csv."""

    def test_creates_csv_file(self, tmp_path: Path, mock_config: MagicMock) -> None:
        """Test that CSV file is created at specified path."""
        output = tmp_path / "licenses.csv"
        rows = [("cluster1", "Base License", "node1", "SN-001", "2026-12-31")]

        _write_csv(rows, mock_config, str(output))

        assert output.exists()

    def test_csv_has_header_and_data(self, tmp_path: Path, mock_config: MagicMock) -> None:
        """Test that CSV contains header and data rows."""
        output = tmp_path / "licenses.csv"
        rows = [
            ("cluster1", "Base License", "node1", "SN-001", "2026-12-31"),
            ("cluster2", "NFS License", "node2", "SN-002", "2027-06-30"),
        ]

        _write_csv(rows, mock_config, str(output))

        content = output.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 3  # header + 2 data rows
        assert "Cluster" in lines[0]
        assert "License Description" in lines[0]
        assert "cluster1" in lines[1]
        assert "cluster2" in lines[2]

    def test_csv_default_path(self, tmp_path: Path, mock_config: MagicMock) -> None:
        """Test timestamped default path when output_file is None."""
        mock_config.output_dir = tmp_path

        _write_csv([], mock_config, None)

        csv_files = list(tmp_path.glob("get_licenses_*.csv"))
        assert len(csv_files) == 1

    def test_csv_custom_path(self, tmp_path: Path, mock_config: MagicMock) -> None:
        """Test custom output path."""
        output = tmp_path / "subdir" / "custom.csv"
        _write_csv([], mock_config, str(output))

        assert output.exists()

    def test_csv_empty_rows(self, tmp_path: Path, mock_config: MagicMock) -> None:
        """Test CSV with no data rows still has header."""
        output = tmp_path / "empty.csv"
        _write_csv([], mock_config, str(output))

        content = output.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 1  # header only
        assert "Cluster" in lines[0]
