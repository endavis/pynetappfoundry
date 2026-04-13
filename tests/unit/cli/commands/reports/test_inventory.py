"""Tests for reports inventory command."""

from __future__ import annotations

from pynetappfoundry.cli.commands.reports.inventory import (
    _cloud_type,
    _license_expiration,
    _node_mgmt_ip,
    _short_version,
)
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
    OntapLicensePackageResponseLicense,
)
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import (
    OntapNodeResponse,
    OntapNodeResponseManagementInterface,
    OntapNodeResponseManagementInterface2,
    OntapNodeResponseManagementInterface2Ip,
    OntapNodeResponseManagementInterfaceIp,
)


class TestShortVersion:
    """Tests for _short_version helper."""

    def test_extracts_version_from_full_string(self) -> None:
        result = _short_version("NetApp Release 9.16.1P3: Mon Jan 01 00:00:00 UTC 2026")
        assert result == "9.16.1P3"

    def test_simple_version(self) -> None:
        result = _short_version("9.14.1")
        assert result == "9.14.1"

    def test_returns_original_on_no_match(self) -> None:
        result = _short_version("unknown")
        assert result == "unknown"

    def test_empty_string(self) -> None:
        result = _short_version("")
        assert result == ""


class TestCloudType:
    """Tests for _cloud_type helper."""

    def test_cloud_ha(self) -> None:
        info = ClusterInfo(is_cloud=True, is_ha=True)
        assert _cloud_type(info) == "CVO HA"

    def test_cloud_single(self) -> None:
        info = ClusterInfo(is_cloud=True, is_ha=False)
        assert _cloud_type(info) == "CVO"

    def test_on_prem(self) -> None:
        info = ClusterInfo(is_cloud=False)
        assert _cloud_type(info) == "OnTap Select"


class TestNodeMgmtIp:
    """Tests for _node_mgmt_ip helper."""

    def test_returns_primary_ip(self) -> None:
        node = OntapNodeResponse(
            management_interface=OntapNodeResponseManagementInterface(
                ip=OntapNodeResponseManagementInterfaceIp(address="10.0.0.1"),
            ),
        )
        assert _node_mgmt_ip(node) == "10.0.0.1"

    def test_falls_back_to_management_interfaces_list(self) -> None:
        node = OntapNodeResponse(
            management_interface=OntapNodeResponseManagementInterface(
                ip=OntapNodeResponseManagementInterfaceIp(address=""),
            ),
            management_interfaces=[
                OntapNodeResponseManagementInterface2(
                    ip=OntapNodeResponseManagementInterface2Ip(address="10.0.0.2"),
                ),
            ],
        )
        assert _node_mgmt_ip(node) == "10.0.0.2"

    def test_returns_empty_when_no_ip(self) -> None:
        node = OntapNodeResponse(
            management_interface=OntapNodeResponseManagementInterface(
                ip=OntapNodeResponseManagementInterfaceIp(address=""),
            ),
        )
        assert _node_mgmt_ip(node) == ""


class TestLicenseExpiration:
    """Tests for _license_expiration helper."""

    def test_returns_earliest_expiry(self) -> None:
        packages = [
            OntapLicensePackageResponse(
                name="pkg1",
                licenses=[
                    OntapLicensePackageResponseLicense(
                        expiry_time="2027-06-15T00:00:00Z",
                    ),
                    OntapLicensePackageResponseLicense(
                        expiry_time="2026-03-01T00:00:00Z",
                    ),
                ],
            ),
        ]
        assert _license_expiration(packages) == "2026-03-01T00:00:00Z"

    def test_skips_empty_expiry(self) -> None:
        packages = [
            OntapLicensePackageResponse(
                name="pkg1",
                licenses=[
                    OntapLicensePackageResponseLicense(expiry_time=""),
                    OntapLicensePackageResponseLicense(
                        expiry_time="2027-01-01T00:00:00Z",
                    ),
                ],
            ),
        ]
        assert _license_expiration(packages) == "2027-01-01T00:00:00Z"

    def test_returns_empty_when_no_licenses(self) -> None:
        assert _license_expiration([]) == ""

    def test_returns_empty_when_all_expiry_empty(self) -> None:
        packages = [
            OntapLicensePackageResponse(
                name="pkg1",
                licenses=[OntapLicensePackageResponseLicense(expiry_time="")],
            ),
        ]
        assert _license_expiration(packages) == ""
