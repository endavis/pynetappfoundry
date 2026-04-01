"""Tests for licenses check command."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.licenses.check import (
    _build_styled_html,
    _check_cluster_licenses,
    _send_license_email,
    _send_no_issues_email,
)
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
    OntapLicensePackageResponseLicense,
)
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse


def _make_license(
    *,
    owner: str = "node1",
    serial: str = "SN-001",
    expiry: str = "",
    active: bool = True,
) -> OntapLicensePackageResponseLicense:
    """Create a license sub-model with common defaults."""
    return OntapLicensePackageResponseLicense(
        owner=owner,
        serial_number=serial,
        expiry_time=expiry,
        active=active,
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


def _make_node(*, name: str = "node1", serial_number: str = "NODE-SN-001") -> OntapNodeResponse:
    """Create a node model with common defaults."""
    return OntapNodeResponse(name=name, serial_number=serial_number)


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock Config object."""
    config = MagicMock()
    config.get_user.return_value = ("admin", "password123")
    config.get_ontap_api_settings.return_value = MagicMock(
        base_api_path="/api",
        timeout=30.0,
    )
    return config


@pytest.fixture
def sample_details() -> dict[str, Any]:
    """Sample cluster connection details."""
    return {"ip": "10.0.0.1", "bu": "Platform", "env": "Prod"}


class TestCheckClusterLicenses:
    """Tests for _check_cluster_licenses."""

    @patch("pynetappfoundry.cli.commands.licenses.check.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_expiring_license(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """License expiring within threshold is reported."""
        expiry = (datetime.now(UTC) + timedelta(days=10)).isoformat()
        lic = _make_license(expiry=expiry)
        pkg = _make_package(licenses=[lic])
        node = _make_node()

        qs_instance = MagicMock()
        qs_instance.all.side_effect = [[pkg], [node]]
        mock_qs_cls.return_value = qs_instance

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 1
        assert issues[0]["error"] == "Expiring license"
        assert issues[0]["days_checked"] in (9, 10)

    @patch("pynetappfoundry.cli.commands.licenses.check.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_license_ok(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """License not expiring within threshold generates no issues."""
        expiry = (datetime.now(UTC) + timedelta(days=100)).isoformat()
        lic = _make_license(expiry=expiry)
        pkg = _make_package(licenses=[lic])
        node = _make_node()

        qs_instance = MagicMock()
        qs_instance.all.side_effect = [[pkg], [node]]
        mock_qs_cls.return_value = qs_instance

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 0

    @patch("pynetappfoundry.cli.commands.licenses.check.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_expired_license(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Expired license (days < 0) is reported."""
        expiry = (datetime.now(UTC) - timedelta(days=5)).isoformat()
        lic = _make_license(expiry=expiry)
        pkg = _make_package(licenses=[lic])
        node = _make_node()

        qs_instance = MagicMock()
        qs_instance.all.side_effect = [[pkg], [node]]
        mock_qs_cls.return_value = qs_instance

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 1
        assert issues[0]["days_checked"] < 0

    @patch("pynetappfoundry.cli.commands.licenses.check.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_no_license_node(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Node without a license is flagged."""
        # License owned by node1, but node2 exists without a license
        expiry = (datetime.now(UTC) + timedelta(days=100)).isoformat()
        lic = _make_license(owner="node1", expiry=expiry)
        pkg = _make_package(licenses=[lic])
        node1 = _make_node(name="node1")
        node2 = _make_node(name="node2", serial_number="NODE-SN-002")

        qs_instance = MagicMock()
        qs_instance.all.side_effect = [[pkg], [node1, node2]]
        mock_qs_cls.return_value = qs_instance

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 1
        assert issues[0]["error"] == "No License"
        assert issues[0]["node"] == "node2"

    @patch("pynetappfoundry.cli.commands.licenses.check.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_serial_prefix_9092(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Serial prefix 9092 uses 13-day check and Cloud Capacity type."""
        # 10 days out: under 13-day threshold for 9092 prefix
        expiry = (datetime.now(UTC) + timedelta(days=10)).isoformat()
        lic = _make_license(serial="90920001", expiry=expiry)
        pkg = _make_package(licenses=[lic])
        node = _make_node()

        qs_instance = MagicMock()
        qs_instance.all.side_effect = [[pkg], [node]]
        mock_qs_cls.return_value = qs_instance

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 1
        assert issues[0]["license_type"] == "ONTAP Cloud Capacity"

    @patch("pynetappfoundry.cli.commands.licenses.check.QuerySet")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_serial_prefix_2265(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Serial prefix 2265 uses 13-day check and Data Tiering type."""
        expiry = (datetime.now(UTC) + timedelta(days=10)).isoformat()
        lic = _make_license(serial="22650001", expiry=expiry)
        pkg = _make_package(licenses=[lic])
        node = _make_node()

        qs_instance = MagicMock()
        qs_instance.all.side_effect = [[pkg], [node]]
        mock_qs_cls.return_value = qs_instance

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 1
        assert issues[0]["license_type"] == "Data Tiering"

    @patch("pynetappfoundry.cli.commands.licenses.check.print_error")
    @patch("pynetappfoundry.cli.commands.licenses.check.ONTAPAPIClient")
    def test_error_handling(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Connection failure is handled gracefully."""
        mock_client_cls.side_effect = Exception("Connection refused")

        issues = _check_cluster_licenses("cluster1", sample_details, mock_config)

        assert len(issues) == 1
        assert "Connection refused" in issues[0]["error"]
        mock_print_error.assert_called_once()


class TestBuildStyledHtml:
    """Tests for _build_styled_html."""

    def test_expired_issue_has_red_class(self) -> None:
        """Expired license uses red-white styling."""
        issues = [
            {
                "cluster": "cluster1",
                "owner": "node1",
                "serial_number": "SN-001",
                "license_type": "ONTAP BYOL",
                "days_checked": -5,
                "expires": datetime(2026, 3, 27, tzinfo=UTC),
            }
        ]

        html = _build_styled_html(issues)

        assert "red-white" in html
        assert "has expired 5 days ago" in html
        assert "cluster1" in html
        assert "node1" in html
        assert "SN-001" in html
        assert "ONTAP BYOL" in html

    def test_expiring_issue_has_yellow_class(self) -> None:
        """Expiring license uses yellow-black styling."""
        issues = [
            {
                "cluster": "cluster1",
                "owner": "node1",
                "serial_number": "SN-001",
                "license_type": "ONTAP BYOL",
                "days_checked": 10,
                "expires": datetime(2026, 4, 11, tzinfo=UTC),
            }
        ]

        html = _build_styled_html(issues)

        assert "yellow-black" in html
        assert "expires in 10 days" in html

    def test_html_has_style_tag(self) -> None:
        """HTML includes style definitions."""
        html = _build_styled_html([])

        assert "<style>" in html
        assert "background-color: red" in html
        assert "background-color: yellow" in html

    def test_html_has_intro_paragraph(self) -> None:
        """HTML includes introductory text."""
        html = _build_styled_html([])

        assert "The following licenses should be checked" in html


class TestSendLicenseEmail:
    """Tests for _send_license_email."""

    @patch("pynetappfoundry.cli.commands.licenses.check.send_email")
    def test_sends_styled_html(
        self,
        mock_send: MagicMock,
        mock_config: MagicMock,
    ) -> None:
        """Email body contains styled HTML with issue details."""
        licensing = MagicMock()
        licensing.mailfrom = "from@test.com"
        licensing.mailto = "to@test.com"
        mock_config.get_licensing_settings.return_value = licensing

        issues = [
            {
                "cluster": "cluster1",
                "owner": "node1",
                "serial_number": "SN-001",
                "license_type": "ONTAP BYOL",
                "days_checked": 10,
                "expires": datetime(2026, 4, 11, tzinfo=UTC),
            }
        ]

        _send_license_email(mock_config, issues)

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args
        body = call_kwargs.kwargs.get("body") or call_kwargs[1].get("body")
        assert "yellow-black" in body
        assert "cluster1" in body
        assert call_kwargs.kwargs.get("high_priority") or call_kwargs[1].get("high_priority")

    @patch("pynetappfoundry.cli.commands.licenses.check.print_warning")
    def test_no_settings_skips(
        self,
        mock_warn: MagicMock,
        mock_config: MagicMock,
    ) -> None:
        """Skips email when licensing settings are not configured."""
        mock_config.get_licensing_settings.return_value = None

        _send_license_email(mock_config, [])

        mock_warn.assert_called_once()


class TestSendNoIssuesEmail:
    """Tests for _send_no_issues_email."""

    @patch("pynetappfoundry.cli.commands.licenses.check.send_email")
    def test_sends_no_issues(
        self,
        mock_send: MagicMock,
        mock_config: MagicMock,
    ) -> None:
        """Sends 'no issues' email with correct subject."""
        licensing = MagicMock()
        licensing.mailfrom = "from@test.com"
        licensing.mailto = "to@test.com"
        mock_config.get_licensing_settings.return_value = licensing

        _send_no_issues_email(mock_config)

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args
        subject = call_kwargs.kwargs.get("subject") or call_kwargs[1].get("subject")
        body = call_kwargs.kwargs.get("body") or call_kwargs[1].get("body")
        assert "No licensing issues found" in subject
        assert "No licensing issues" in body

    @patch("pynetappfoundry.cli.commands.licenses.check.print_warning")
    def test_no_settings_skips(
        self,
        mock_warn: MagicMock,
        mock_config: MagicMock,
    ) -> None:
        """Skips email when licensing settings are not configured."""
        mock_config.get_licensing_settings.return_value = None

        _send_no_issues_email(mock_config)

        mock_warn.assert_called_once()
