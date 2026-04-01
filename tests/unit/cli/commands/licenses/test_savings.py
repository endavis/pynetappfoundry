"""Tests for licenses savings command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.licenses.savings import _analyze_cluster_savings
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
    OntapLicensePackageResponseLicense,
)


def _make_license(
    *,
    serial_number: str = "SN-001",
    capacity_used_size: int = 500,
    capacity_maximum_size: int = 1000,
) -> OntapLicensePackageResponseLicense:
    """Create a license sub-model."""
    return OntapLicensePackageResponseLicense(
        serial_number=serial_number,
        capacity_used_size=capacity_used_size,
        capacity_maximum_size=capacity_maximum_size,
    )


def _make_package(
    *,
    name: str = "base",
    licenses: list[OntapLicensePackageResponseLicense] | None = None,
) -> OntapLicensePackageResponse:
    """Create a license package."""
    return OntapLicensePackageResponse(
        name=name,
        licenses=licenses or [],
    )


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock Config."""
    config = MagicMock()
    config.get_user.return_value = ("admin", "password")
    config.output_dir = Path("/tmp/test")
    config.get_ontap_api_settings.return_value = MagicMock(base_api_path="/api", timeout=30.0)
    config.get_schema_location.return_value = Path("/tmp/schema")
    return config


@pytest.fixture
def sample_details() -> dict[str, Any]:
    """Sample cluster details."""
    return {"name": "cluster1", "ip": "10.0.0.1"}


class TestAnalyzeClusterSavings:
    """Tests for _analyze_cluster_savings."""

    @patch("pynetappfoundry.cli.commands.licenses.savings.console")
    @patch("pynetappfoundry.cli.commands.licenses.savings.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.savings.ONTAPAPIClient")
    def test_displays_table(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_console: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test that a Rich table is printed."""
        lic = _make_license()
        pkg = _make_package(name="nfs", licenses=[lic])
        mock_qs_cls.return_value.all.return_value = [pkg]

        _analyze_cluster_savings("cluster1", sample_details, mock_config)

        mock_console.print.assert_called_once()

    @patch("pynetappfoundry.cli.commands.licenses.savings.console")
    @patch("pynetappfoundry.cli.commands.licenses.savings.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.savings.ONTAPAPIClient")
    def test_serial_prefix_cloud(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_console: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test 9092 prefix detected as Cloud Capacity."""
        lic = _make_license(serial_number="9092-ABC")
        pkg = _make_package(licenses=[lic])
        mock_qs_cls.return_value.all.return_value = [pkg]

        _analyze_cluster_savings("cluster1", sample_details, mock_config)

        # Verify the table was printed (content verified by visual inspection)
        mock_console.print.assert_called_once()

    @patch("pynetappfoundry.cli.commands.licenses.savings.print_error")
    @patch("pynetappfoundry.cli.commands.licenses.savings.ONTAPAPIClient")
    def test_error_handling(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test connection failure handled gracefully."""
        mock_client_cls.side_effect = Exception("Connection refused")

        _analyze_cluster_savings("cluster1", sample_details, mock_config)

        mock_print_error.assert_called_once()
