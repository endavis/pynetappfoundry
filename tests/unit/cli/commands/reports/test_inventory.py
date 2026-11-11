"""Tests for reports inventory command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import openpyxl

from pynetappfoundry.cli.commands.reports.inventory import (
    _COL_WIDTHS,
    _HEADERS,
    InventoryReport,
    _cloud_type,
    _license_expiration,
    _node_mgmt_ip,
    _short_version,
)
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
    OntapLicensePackageResponseLicense,
)
from pynetappfoundry.models.ontap.cluster.model import OntapCluster
from pynetappfoundry.models.ontap.cluster.nodes.model import (
    OntapNodeResponse,
    OntapNodeResponseManagementInterface,
    OntapNodeResponseManagementInterface2,
    OntapNodeResponseManagementInterface2Ip,
    OntapNodeResponseManagementInterfaceIp,
)
from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits


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
        info = ClusterTraits(is_cloud=True, is_ha=True)
        assert _cloud_type(info) == "CVO HA"

    def test_cloud_single(self) -> None:
        info = ClusterTraits(is_cloud=True, is_ha=False)
        assert _cloud_type(info) == "CVO"

    def test_on_prem(self) -> None:
        info = ClusterTraits(is_cloud=False)
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


class TestInventoryWorkbook:
    """Read-back tests of the saved inventory workbook."""

    @staticmethod
    def _build(tmp_path: Path) -> Any:
        config = MagicMock()
        config.find_closest.return_value = {"ip": "10.9.9.9", "azure": {"vmname": "conn-vm"}}
        clusters: dict[str, Any] = {
            "cl1": {"ip": "10.0.0.1", "div": "D", "bu": "B", "env": "Prod", "contacts": "a@b.c"},
            "cl2": {"div": "D2"},
        }
        with patch("pynetappfoundry.cli.commands.reports.inventory.DataSource") as ds:
            ds.return_value.query.return_value.first.return_value = None
            report = InventoryReport(config, clusters)
            report.build()
        path = tmp_path / "inv.xlsx"
        report.save(str(path))
        return openpyxl.load_workbook(path)

    def test_sheet_headers_and_values(self, tmp_path: Path) -> None:
        wb = self._build(tmp_path)
        assert wb.sheetnames == ["NetApps"]
        ws = wb["NetApps"]
        assert [c.value for c in ws[1]] == _HEADERS
        assert ws.cell(row=2, column=1).value == "cl1"
        assert ws.cell(row=2, column=2).value == "D"
        assert ws.cell(row=3, column=1).value == "cl2"
        assert ws.cell(row=2, column=23).value == "NA"

    def test_hyperlinks(self, tmp_path: Path) -> None:
        ws = self._build(tmp_path)["NetApps"]
        sys_mgr = ws.cell(row=2, column=16)
        assert sys_mgr.value == "https://10.0.0.1"
        assert sys_mgr.hyperlink is not None
        assert sys_mgr.hyperlink.target == "https://10.0.0.1"
        assert ws.cell(row=2, column=17).hyperlink.target == "https://10.9.9.9/"
        assert ws.cell(row=3, column=16).hyperlink is None
        assert ws.cell(row=3, column=16).value in (None, "")

    def test_layout(self, tmp_path: Path) -> None:
        ws = self._build(tmp_path)["NetApps"]
        assert ws.freeze_panes == "A2"
        assert ws.auto_filter.ref == "A1:AG1"
        assert ws.row_dimensions[1].height == 30
        # openpyxl groups adjacent equal-width columns into one min..max entry.
        widths: dict[int, float] = {}
        for dim in ws.column_dimensions.values():
            for idx in range(dim.min, dim.max + 1):
                widths[idx] = dim.width
        for idx, width in enumerate(_COL_WIDTHS, 1):
            assert abs(widths[idx] - width) < 1

    def test_formats(self, tmp_path: Path) -> None:
        ws = self._build(tmp_path)["NetApps"]
        header = ws.cell(row=1, column=1)
        assert header.fill.fgColor.rgb.endswith("1F4E79")
        assert header.font.bold
        assert header.font.color.rgb.endswith("FFFFFF")
        assert header.font.name == "Calibri"
        assert header.font.size == 11
        assert header.alignment.vertical == "top"
        body = ws.cell(row=2, column=1)
        assert body.font.size == 10
        assert not body.alignment.wrap_text
        assert ws.cell(row=2, column=5).alignment.wrap_text
        assert ws.cell(row=2, column=32).alignment.wrap_text
        assert not ws.cell(row=2, column=7).alignment.wrap_text
        link = ws.cell(row=2, column=16)
        assert link.font.underline == "single"
        assert link.font.color.rgb.endswith("0563C1")


class _Entry(dict[str, Any]):
    """Cluster config entry with no cached ONTAP data."""

    ontap = None


class TestInventoryClusterType:
    """#967: the cluster type column follows ``ClusterTraits``, not ``OntapCluster``."""

    @staticmethod
    def _row(traits: ClusterTraits | None) -> list[Any]:
        config = MagicMock()
        config.find_closest.return_value = {}

        def query(model: type, **_: Any) -> MagicMock:
            result = MagicMock()
            if model is OntapCluster:
                result.first.return_value = OntapCluster(name="cl1")
            elif model is ClusterTraits:
                result.first.return_value = traits
            else:
                result.first.return_value = None
                result.__iter__.return_value = iter([])
            return result

        with patch("pynetappfoundry.cli.commands.reports.inventory.DataSource") as ds:
            ds.return_value.query.side_effect = query
            report = InventoryReport(config, {"cl1": _Entry(ip="10.0.0.1")})
            report.build()
        return report.rows[0]

    def test_missing_traits_row_is_on_prem(self) -> None:
        assert "OnTap Select" in self._row(None)

    def test_cloud_ha_traits(self) -> None:
        assert "CVO HA" in self._row(ClusterTraits(is_cloud=True, is_ha=True))

    def test_cloud_single_traits(self) -> None:
        assert "CVO" in self._row(ClusterTraits(is_cloud=True, is_ha=False))
