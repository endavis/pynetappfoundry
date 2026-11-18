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
        assert ws.auto_filter.ref == "A1:AK1"
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


class TestInventoryConsoleAgent:
    """#1077: the NetApp Console Agent column, found by header name since #1086 appended columns."""

    _AGENT = _HEADERS.index("NetApp Console Agent")

    @staticmethod
    def _row(
        connector: dict[str, Any] | None, base: str = "https://console.netapp.com"
    ) -> list[Any]:
        config = MagicMock()
        config.find_closest.return_value = connector
        config.get_setting.return_value = base
        with patch("pynetappfoundry.cli.commands.reports.inventory.DataSource") as ds:
            ds.return_value.query.return_value.first.return_value = None
            ds.return_value.query.return_value.__iter__.return_value = iter([])
            report = InventoryReport(config, {"cl1": _Entry(ip="10.0.0.1")})
            report.build()
        return report.rows[0]

    def test_header_follows_remark_and_lengths_match(self) -> None:
        assert _HEADERS[self._AGENT - 1] == "Remark"
        row = self._row(None)
        assert len(row) == len(_HEADERS) == len(_COL_WIDTHS)

    def test_existing_columns_unchanged(self) -> None:
        assert _HEADERS[16] == "BlueXP (NetApp Console) Connector IP"
        assert _HEADERS[17] == "BlueXP (NetApp Console) Name"
        assert _HEADERS[self._AGENT - 1] == "Remark"

    def test_link_tuple_when_agent_id(self) -> None:
        row = self._row({"ip": "10.9.9.9", "agent_id": "agentXXXX"})
        assert row[self._AGENT] == (
            "agentXXXX",
            "https://console.netapp.com/agents-mgmt/agentXXXX/edit",
        )

    def test_empty_without_agent_id(self) -> None:
        assert self._row({"ip": "10.9.9.9"})[self._AGENT] == ""

    def test_empty_without_connector(self) -> None:
        assert self._row(None)[self._AGENT] == ""

    def test_ui_base_url_override(self) -> None:
        row = self._row({"agent_id": "agentXXXX"}, "https://ui.example.test/")
        assert row[self._AGENT] == (
            "agentXXXX",
            "https://ui.example.test/agents-mgmt/agentXXXX/edit",
        )


def _occm_details(*, aggregates: bool = True) -> Any:
    from pynetappfoundry.cache.occm_cloud_metadata import ConsoleWorkingEnvironmentLinks
    from pynetappfoundry.cli.commands.reports._cloud_source import CloudDetails
    from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

    meta = [
        CloudMetadata(
            node="n1",
            provider="AWS",
            region="us-east-1",
            account_id="111122223333",
            instance_type="m5.xlarge",
            vm_name="i-1",
        ),
        CloudMetadata(node="n2", provider="AWS", vm_name="i-2"),
    ]
    base = "https://ui.example.test/storage/cloud-volumes-ontap/VsaWorkingEnvironment-AAAA"
    console = ConsoleWorkingEnvironmentLinks(
        public_id="VsaWorkingEnvironment-AAAA",
        agent_id="agent-1",
        agent_name="agent",
        scopes=(None,),
        working_environment=base,
        volumes=f"{base}/volumes",
        aggregates=f"{base}/aggregates" if aggregates else "",
    )
    return CloudDetails("occm", meta, console)


class TestInventoryOccmCloud:
    """#1086: cloud columns from a ``ReportCloudSource`` and the Console link columns."""

    @staticmethod
    def _report(
        source: Any, traits: ClusterTraits | None = None
    ) -> tuple[InventoryReport, list[Any]]:
        config = MagicMock()
        config.find_closest.return_value = {}
        config.get_setting.return_value = "https://console.netapp.com"

        def query(model: type, **_: Any) -> MagicMock:
            result = MagicMock()
            if model is OntapCluster:
                result.first.return_value = OntapCluster(name="cl1")
            elif model is ClusterTraits:
                result.first.return_value = traits or ClusterTraits(is_cloud=True, is_ha=True)
            elif model is OntapNodeResponse:
                result.__iter__.return_value = iter(
                    [OntapNodeResponse(name="n1"), OntapNodeResponse(name="n2")]
                )
            else:
                result.first.return_value = None
                result.__iter__.return_value = iter([])
            return result

        with patch("pynetappfoundry.cli.commands.reports.inventory.DataSource") as ds:
            ds.return_value.query.side_effect = query
            report = InventoryReport(config, {"cl1": _Entry(ip="10.0.0.1")}, cloud_source=source)
            report.build()
        return report, report.rows[0]

    def test_cloud_columns_come_from_the_source(self) -> None:
        source = MagicMock()
        source.details.return_value = _occm_details()
        _, row = self._report(source)
        assert row[_HEADERS.index("Site")] == "East 1"
        assert row[_HEADERS.index("Subscription ID")] == "111122223333"
        assert row[_HEADERS.index("VM SKU Type")] == "m5.xlarge"
        assert row[_HEADERS.index("VM Names")] == "i-1, i-2"
        assert row[_HEADERS.index("Cloud Location")] == "AWS"
        kwargs = source.details.call_args.kwargs
        assert kwargs["is_cloud"] is True
        assert kwargs["node_names"] == ["n1", "n2"]

    def test_console_columns_are_link_tuples(self) -> None:
        source = MagicMock()
        source.details.return_value = _occm_details()
        _, row = self._report(source)
        we = row[_HEADERS.index("Console Working Environment")]
        assert we[0] == "Working environment"
        assert we[1].endswith("VsaWorkingEnvironment-AAAA")
        assert row[_HEADERS.index("Console Volumes")][0] == "Volumes"
        assert row[_HEADERS.index("Console Aggregates")][1].endswith("/aggregates")
        assert "VsaWorkingEnvironment-AAAA" not in str(
            [row[_HEADERS.index(h)][0] for h in _HEADERS[-3:]]
        )

    def test_on_prem_has_no_aggregates_cell(self) -> None:
        source = MagicMock()
        source.details.return_value = _occm_details(aggregates=False)
        _, row = self._report(source)
        assert row[_HEADERS.index("Console Aggregates")] == ""

    def test_no_console_links_gives_empty_cells(self) -> None:
        from pynetappfoundry.cli.commands.reports._cloud_source import CloudDetails

        source = MagicMock()
        source.details.return_value = CloudDetails("none", [], None)
        _, row = self._report(source)
        assert row[-3:] == ["", "", ""]

    def test_without_a_source_the_cli_path_is_unchanged(self) -> None:
        _, row = self._report(None)
        assert row[-3:] == ["", "", ""]
        assert len(row) == len(_HEADERS) == len(_COL_WIDTHS)

    def test_headers_widths_and_filter(self) -> None:
        assert _HEADERS[-3:] == [
            "Console Working Environment",
            "Console Volumes",
            "Console Aggregates",
        ]
        assert len(_HEADERS) == len(_COL_WIDTHS)


class TestInventoryConsoleLinks:
    """#1086: the Console link columns are written as hyperlinks."""

    def test_hyperlinks_read_back(self, tmp_path: Path) -> None:
        source = MagicMock()
        source.details.return_value = _occm_details()
        report, _ = TestInventoryOccmCloud._report(source)
        path = tmp_path / "inv.xlsx"
        report.save(str(path))
        ws = openpyxl.load_workbook(path)["NetApps"]
        assert ws.auto_filter.ref == "A1:AK1"
        for idx, label in enumerate(("Working environment", "Volumes", "Aggregates")):
            cell = ws.cell(row=2, column=len(_HEADERS) - 2 + idx)
            assert cell.value == label
            assert cell.hyperlink is not None
            assert cell.hyperlink.target.startswith("https://ui.example.test/storage/")
