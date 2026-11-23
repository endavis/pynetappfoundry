"""Tests for reports space-usage command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import openpyxl
import pytest
from openpyxl.workbook import Workbook

from pynetappfoundry.cli.commands.reports.space_usage import SpaceUsageReport
from pynetappfoundry.models.ontap.cluster.nodes.model import (
    OntapNodeResponse,
    OntapNodeResponseHa,
)
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume, OntapVolumeSpace


def _make_volume(
    *,
    name: str = "vol1",
    size: int = 1099511627776,  # 1 TiB in bytes
    space_used: int = 549755813888,  # 0.5 TiB
    state: str = "online",
    type_: str = "rw",
) -> OntapVolume:
    """Create a test volume model."""
    return OntapVolume(
        name=name,
        size=size,
        space=OntapVolumeSpace(used=space_used),
        state=state,
        type_=type_,
    )


def _make_node(*, name: str = "node1", ha_enabled: bool = False) -> OntapNodeResponse:
    """Create a test node model."""
    return OntapNodeResponse(name=name, ha=OntapNodeResponseHa(enabled=ha_enabled))


@pytest.fixture
def mock_config(tmp_path: Path) -> MagicMock:
    """Create a mock Config with output_dir."""
    config = MagicMock()
    config.output_dir = tmp_path
    config.get_user.return_value = ("admin", "password")
    config.get_ontap_api_settings.return_value = MagicMock(
        base_api_path="/api",
        timeout=30.0,
    )
    config.get_schema_location.return_value = Path("/tmp/schema")
    return config


@pytest.fixture
def sample_clusters() -> dict[str, dict[str, Any]]:
    """Sample cluster details."""
    return {
        "cluster1": {
            "name": "cluster1",
            "ip": "10.0.0.1",
            "div": "IT",
            "bu": "Platform",
            "app": "Storage",
            "env": "Prod",
            "subapp": "",
            "cloud": "Azure",
            "region": "eastus",
            "tags": ["prod", "azure"],
        }
    }


def _mock_queryset(nodes: list[Any], volumes: list[Any]) -> Any:
    """Create a side_effect for QuerySet that returns nodes then volumes."""
    call_count = 0

    def side_effect(*args: Any, **kwargs: Any) -> MagicMock:
        nonlocal call_count
        call_count += 1
        qs = MagicMock()
        if call_count % 2 == 1:  # odd calls are nodes
            qs.all.return_value = nodes
        else:  # even calls are volumes
            qs.filter.return_value.all.return_value = volumes
        return qs

    return side_effect


class TestGatherData:
    """Tests for SpaceUsageReport.gather_data()."""

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_cvo_ha_detection(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test CVO HA detected with 2+ nodes and HA enabled."""
        nodes = [_make_node(name="n1", ha_enabled=True), _make_node(name="n2", ha_enabled=True)]
        mock_qs_cls.side_effect = _mock_queryset(nodes, [_make_volume()])

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert len(report.volume_data) == 1
        assert report.volume_data[0][8] == "CVO HA"

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_cvo_detection(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test CVO detected with single node."""
        mock_qs_cls.side_effect = _mock_queryset([_make_node()], [_make_volume()])

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert len(report.volume_data) == 1
        assert report.volume_data[0][8] == "CVO"

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_volume_fields(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test volume data row has correct field values."""
        mock_qs_cls.side_effect = _mock_queryset(
            [_make_node()],
            [_make_volume(name="testvol", type_="rw", state="online")],
        )

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        row = report.volume_data[0]
        assert row[10] == "testvol"  # volume name
        assert row[9] == "RW"  # data_type (uppercased)
        assert row[11] == "online"  # state

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_offline_volume_zero_used(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test offline volume has used_tib=0."""
        mock_qs_cls.side_effect = _mock_queryset(
            [_make_node()],
            [_make_volume(state="offline", space_used=999999)],
        )

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert report.volume_data[0][14] == 0.0  # used_tib

    @patch("pynetappfoundry.cli.commands.reports.space_usage.print_error")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_error_handling(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test connection failure is handled gracefully."""
        mock_client_cls.side_effect = Exception("Connection refused")

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert len(report.volume_data) == 0
        mock_print_error.assert_called_once()


_MOD = "pynetappfoundry.cli.commands.reports.space_usage"
_TIB = 1099511627776
_TOL = 0.0001


@pytest.fixture
def two_clusters() -> dict[str, dict[str, Any]]:
    """An Azure CVO HA cluster and an AWS CVO cluster in different hierarchies."""
    return {
        "az1": {
            "name": "az1",
            "ip": "10.0.0.1",
            "div": "IT",
            "bu": "Platform",
            "app": "Storage",
            "env": "Prod",
            "subapp": "",
            "cloud": "Azure",
            "region": "eastus",
            "tags": ["prod", "azure"],
        },
        "aw1": {
            "name": "aw1",
            "ip": "10.0.0.2",
            "div": "Ops",
            "bu": "Infra",
            "app": "Backup",
            "env": "Dev",
            "subapp": "sub",
            "cloud": "AWS",
            "region": "us-east-1",
            "tags": [],
        },
    }


def _sequenced_queryset(per_cluster: list[tuple[list[Any], list[Any]]]) -> Any:
    """QuerySet side_effect serving (nodes, volumes) per cluster, in call order."""
    calls: list[list[Any]] = []
    for nodes, volumes in per_cluster:
        calls.extend([nodes, volumes])
    iterator = iter(calls)

    def side_effect(*args: Any, **kwargs: Any) -> MagicMock:
        data = next(iterator)
        qs = MagicMock()
        qs.all.return_value = data
        qs.filter.return_value.all.return_value = data
        return qs

    return side_effect


def _default_per_cluster() -> list[tuple[list[Any], list[Any]]]:
    """Azure HA cluster with RW+DP volumes, AWS single node with one RW volume."""
    return [
        (
            [_make_node(name="n1", ha_enabled=True), _make_node(name="n2", ha_enabled=True)],
            [
                _make_volume(name="az_rw_volume_with_long_name", size=2 * _TIB, space_used=_TIB),
                _make_volume(name="az_dp", type_="dp"),
            ],
        ),
        ([_make_node(name="n3")], [_make_volume(name="aw_rw")]),
    ]


def _generate(
    mock_qs_cls: MagicMock,
    config: MagicMock,
    clusters: dict[str, dict[str, Any]],
    per_cluster: list[tuple[list[Any], list[Any]]] | None = None,
) -> tuple[Workbook, MagicMock]:
    """Run generate() with mocked API calls and load the saved workbook."""
    mock_qs_cls.side_effect = _sequenced_queryset(per_cluster or _default_per_cluster())
    with (
        patch(f"{_MOD}.print_success") as mock_success,
        patch(f"{_MOD}.print_info"),
    ):
        report = SpaceUsageReport(config, clusters)
        report.generate()
    mock_success.assert_called_once_with(f"Report saved to {report.filename}")
    return openpyxl.load_workbook(report.filename), mock_success


def _widths(ws: Any) -> dict[str, float]:
    """Column letter -> stored width."""
    return {key: dim.width for key, dim in ws.column_dimensions.items()}


def _cf_rules(ws: Any) -> list[tuple[str, str, str, list[str]]]:
    """(range, type, operator, formula) for each conditional format rule."""
    return [
        (str(rng.sqref), rule.type, rule.operator, list(rule.formula))
        for rng, rules in ws.conditional_formatting._cf_rules.items()
        for rule in rules
    ]


class TestGenerate:
    """Tests for SpaceUsageReport.generate()."""

    @patch(f"{_MOD}.QuerySet")
    @patch(f"{_MOD}.ONTAPAPIClient")
    def test_generate_with_data_saves_workbook(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        two_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """A report with data is saved with the three sheets built."""
        wb, _ = _generate(mock_qs_cls, mock_config, two_clusters)

        assert wb.sheetnames == ["Totals", "Usage Breakdown", "Volumes"]
        assert wb["Totals"]["A1"].value == "Type"
        assert wb["Usage Breakdown"]["A1"].value == "Division"
        assert wb["Volumes"]["A1"].value == "Division"

    @patch(f"{_MOD}.print_success")
    @patch(f"{_MOD}.print_error")
    @patch(f"{_MOD}.ONTAPAPIClient")
    def test_generate_without_data_reports_error(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_print_success: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """No volume data prints an error, saves an empty workbook, and skips success."""
        mock_client_cls.side_effect = Exception("Connection refused")

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.generate()

        mock_print_error.assert_any_call("No volume data collected. Check cluster connectivity.")
        mock_print_success.assert_not_called()
        wb = openpyxl.load_workbook(report.filename)
        assert wb.sheetnames == ["Totals", "Usage Breakdown", "Volumes"]
        assert wb["Totals"]["A1"].value is None
        assert wb["Usage Breakdown"]["A1"].value is None
        assert wb["Volumes"]["A1"].value is None


class TestVolumesSheet:
    """Workbook read-back tests for build_volumes_sheet()."""

    @pytest.fixture
    def ws(
        self,
        mock_config: MagicMock,
        two_clusters: dict[str, dict[str, Any]],
    ) -> Any:
        with (
            patch(f"{_MOD}.QuerySet") as mock_qs_cls,
            patch(f"{_MOD}.ONTAPAPIClient"),
        ):
            wb, _ = _generate(mock_qs_cls, mock_config, two_clusters)
        return wb["Volumes"]

    def test_headers(self, ws: Any) -> None:
        headers = [ws.cell(row=1, column=c).value for c in range(1, 16)]
        assert headers == [
            "Division",
            "BU",
            "Cluster",
            "App",
            "Environment",
            "SubApp",
            "Cloud",
            "Region",
            "Cluster Type",
            "Data Type",
            "Volume",
            "State",
            "Tags",
            "Provisioned (Licensing) TiB",
            "Used TiB",
        ]

    def test_first_volume_row(self, ws: Any) -> None:
        row = [ws.cell(row=2, column=c).value for c in range(1, 16)]
        assert row == [
            "IT",
            "Platform",
            "az1",
            "Storage",
            "Prod",
            None,
            "Azure",
            "eastus",
            "CVO HA",
            "RW",
            "az_rw_volume_with_long_name",
            "online",
            "prod,azure",
            2.0,
            1.0,
        ]

    def test_other_rows(self, ws: Any) -> None:
        assert ws["J3"].value == "DP"
        assert ws["K3"].value == "az_dp"
        assert ws["N3"].value == 1.0
        assert ws["O3"].value == 0.5
        aws = [ws.cell(row=4, column=c).value for c in range(1, 14)]
        assert aws == [
            "Ops",
            "Infra",
            "aw1",
            "Backup",
            "Dev",
            "sub",
            "AWS",
            "us-east-1",
            "CVO",
            "RW",
            "aw_rw",
            "online",
            None,
        ]
        # Row 5 is the table's totals row, not data: text columns carry no total.
        for col in "ABCDEFGHIJKLM":
            assert ws[f"{col}5"].value is None
        # The average total of the % Used column (header text is not pinned here).
        assert str(ws["P5"].value).startswith("=SUBTOTAL(101,")

    def test_table(self, ws: Any) -> None:
        table = ws.tables["volume_table"]
        assert table.ref == "A1:P5"
        assert table.totalsRowCount == 1
        assert table.autoFilter is not None
        assert table.tableStyleInfo.name == "TableStyleMedium9"
        by_name = {c.name: c.totalsRowFunction for c in table.tableColumns}
        assert by_name["Provisioned (Licensing) TiB"] == "sum"
        assert by_name["Used TiB"] == "sum"
        assert ws["N5"].value == "=SUBTOTAL(109,[Provisioned (Licensing) TiB])"
        assert ws["O5"].value == "=SUBTOTAL(109,[Used TiB])"

    def test_percent_used_column_is_calculated(self, ws: Any) -> None:
        """The table's calculated column overwrites the percent value written per row."""
        for row in (2, 3, 4):
            assert (
                ws[f"P{row}"].value
                == "=[[#This Row],[Used TiB]]/[[#This Row],[Provisioned (Licensing) TiB]] * 100"
            )

    def test_conditional_format_flags_high_usage(self, ws: Any) -> None:
        assert _cf_rules(ws) == [("P2:P4", "cellIs", "greaterThanOrEqual", ["90"])]

    def test_number_formats(self, ws: Any) -> None:
        for row in (2, 3, 4):
            assert ws[f"N{row}"].number_format == "0.00000"
            assert ws[f"O{row}"].number_format == "0.00000"
            assert ws[f"P{row}"].number_format == "0.00000"
            for col in "ABCDEFGHIJKLM":
                assert ws[f"{col}{row}"].number_format == "General"

    def test_cell_font(self, ws: Any) -> None:
        # Header cells are rewritten by the table, so check a data cell.
        assert ws["A2"].font.name == "Cascadia Mono"
        assert ws["A2"].font.sz == 10

    def test_column_widths_fit_longest_value(self, ws: Any) -> None:
        widths = _widths(ws)
        # width = longest value (or header + 1) + 4, plus xlsxwriter's 0.7109375 padding.
        pad = 0.7109375
        assert widths["A"] == pytest.approx(len("Division") + 1 + 4 + pad, abs=_TOL)
        assert widths["K"] == pytest.approx(len("az_rw_volume_with_long_name") + 4 + pad, abs=_TOL)
        prov = len("Provisioned (Licensing) TiB")
        assert widths["N"] == pytest.approx(prov + 1 + 4 + pad, abs=_TOL)
        assert widths["M"] == pytest.approx(len("prod,azure") + 4 + pad, abs=_TOL)
        assert widths["H"] == pytest.approx(len("us-east-1") + 4 + pad, abs=_TOL)


class TestUsageSheet:
    """Workbook read-back tests for build_usage_sheet()."""

    @pytest.fixture
    def ws(
        self,
        mock_config: MagicMock,
        two_clusters: dict[str, dict[str, Any]],
    ) -> Any:
        with (
            patch(f"{_MOD}.QuerySet") as mock_qs_cls,
            patch(f"{_MOD}.ONTAPAPIClient"),
        ):
            wb, _ = _generate(mock_qs_cls, mock_config, two_clusters)
        return wb["Usage Breakdown"]

    @staticmethod
    def _expected_filter(fields: list[str], last: int) -> str:
        cols = ["A", "B", "D", "E", "F", "G", "H", "I", "J"]
        return ",".join(
            f'Volumes!${col}$2:${col}${last},"{value}"'
            for col, value in zip(cols, fields, strict=True)
        )

    def test_headers(self, ws: Any) -> None:
        headers = [ws.cell(row=1, column=c).value for c in range(1, 13)]
        assert headers == [
            "Division",
            "BU",
            "App",
            "Environment",
            "SubApp",
            "Cloud",
            "Region",
            "Cluster Type",
            "Data Type",
            "Provisioned (Licensing) TiB",
            "Used TiB",
            "% Used",
        ]

    def test_one_row_per_combination_with_data(self, ws: Any) -> None:
        rows = [[ws.cell(row=r, column=c).value for c in range(1, 10)] for r in (2, 3, 4)]
        assert rows == [
            ["IT", "Platform", "Storage", "Prod", None, "Azure", "eastus", "CVO HA", "RW"],
            ["IT", "Platform", "Storage", "Prod", None, "Azure", "eastus", "CVO HA", "DP"],
            ["Ops", "Infra", "Backup", "Dev", "sub", "AWS", "us-east-1", "CVO", "RW"],
        ]
        # Row 5 is the table's totals row: text columns carry no total.
        for col in "ABCDEFGHI":
            assert ws[f"{col}5"].value is None

    def test_combination_without_data_has_no_row(
        self,
        mock_config: MagicMock,
        two_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Only RW volumes exist, so no DP and no CVO row appear."""
        per_cluster = [
            (
                [_make_node(name="n1", ha_enabled=True), _make_node(name="n2", ha_enabled=True)],
                [_make_volume()],
            ),
            ([_make_node()], []),
        ]
        with (
            patch(f"{_MOD}.QuerySet") as mock_qs_cls,
            patch(f"{_MOD}.ONTAPAPIClient"),
        ):
            wb, _ = _generate(mock_qs_cls, mock_config, two_clusters, per_cluster)
        ws = wb["Usage Breakdown"]
        assert ws["I2"].value == "RW"
        assert ws["A3"].value is None
        assert ws.tables["usage_table"].ref == "A1:L3"

    def test_sumifs_formulas(self, ws: Any) -> None:
        last = 4  # three volume rows, last data row on the Volumes sheet
        fields = [
            ["IT", "Platform", "Storage", "Prod", "", "Azure", "eastus", "CVO HA", "RW"],
            ["IT", "Platform", "Storage", "Prod", "", "Azure", "eastus", "CVO HA", "DP"],
            ["Ops", "Infra", "Backup", "Dev", "sub", "AWS", "us-east-1", "CVO", "RW"],
        ]
        for row, values in zip((2, 3, 4), fields, strict=True):
            crit = self._expected_filter(values, last)
            assert ws[f"J{row}"].value == f"=SUMIFS(Volumes!$N$2:$N${last},{crit})"
            assert ws[f"K{row}"].value == f"=SUMIFS(Volumes!$O$2:$O${last},{crit})"

    def test_table(self, ws: Any) -> None:
        table = ws.tables["usage_table"]
        assert table.ref == "A1:L5"
        assert table.totalsRowCount == 1
        assert table.autoFilter is not None
        assert table.tableStyleInfo.name == "TableStyleMedium9"
        by_name = {c.name: c.totalsRowFunction for c in table.tableColumns}
        assert by_name["Provisioned (Licensing) TiB"] == "sum"
        assert by_name["Used TiB"] == "sum"
        assert by_name["% Used"] == "average"
        assert ws["J5"].value == "=SUBTOTAL(109,[Provisioned (Licensing) TiB])"
        assert ws["K5"].value == "=SUBTOTAL(109,[Used TiB])"
        assert ws["L5"].value == "=SUBTOTAL(101,[% Used])"

    def test_percent_used_column_is_calculated(self, ws: Any) -> None:
        for row in (2, 3, 4):
            assert (
                ws[f"L{row}"].value
                == "=[[#This Row],[Used TiB]]/[[#This Row],[Provisioned (Licensing) TiB]] * 100"
            )

    def test_conditional_format_is_on_percent_used_column(self, ws: Any) -> None:
        # Only the column and rule are pinned, not the end row (see issue #1150).
        rules = _cf_rules(ws)
        assert len(rules) == 1
        rng, rule_type, operator, formula = rules[0]
        assert rng.startswith("L2:L")
        assert (rule_type, operator, formula) == ("cellIs", "greaterThanOrEqual", ["90"])

    def test_number_formats(self, ws: Any) -> None:
        for row in (2, 3, 4):
            assert ws[f"J{row}"].number_format == "0.00000"
            assert ws[f"K{row}"].number_format == "0.00000"
            assert ws[f"L{row}"].number_format == "0.00000"
            for col in "ABCDEFGHI":
                assert ws[f"{col}{row}"].number_format == "General"

    def test_cell_font(self, ws: Any) -> None:
        # Header cells are rewritten by the table, so check a data cell.
        assert ws["A2"].font.name == "Cascadia Mono"
        assert ws["A2"].font.sz == 10

    def test_column_widths_ignore_formulas(self, ws: Any) -> None:
        widths = _widths(ws)
        pad = 0.7109375
        # Header + 1 + 2 for short columns.
        assert widths["A"] == pytest.approx(len("Division") + 1 + 2 + pad, abs=_TOL)
        # The long SUMIFS formula does not widen column J.
        prov = len("Provisioned (Licensing) TiB")
        assert widths["J"] == pytest.approx(prov + 1 + 2 + pad, abs=_TOL)
        assert widths["K"] == pytest.approx(len("Used TiB") + 1 + 2 + pad, abs=_TOL)
        # A long text value widens its column.
        assert widths["G"] == pytest.approx(len("us-east-1") + 2 + pad, abs=_TOL)
        assert widths["D"] == pytest.approx(len("Environment") + 1 + 2 + pad, abs=_TOL)


class TestTotalsSheet:
    """Workbook read-back tests for build_totals_sheet()."""

    @pytest.fixture
    def ws(
        self,
        mock_config: MagicMock,
        two_clusters: dict[str, dict[str, Any]],
    ) -> Any:
        with (
            patch(f"{_MOD}.QuerySet") as mock_qs_cls,
            patch(f"{_MOD}.ONTAPAPIClient"),
        ):
            wb, _ = _generate(mock_qs_cls, mock_config, two_clusters)
        return wb["Totals"]

    def test_headers(self, ws: Any) -> None:
        assert [ws.cell(row=1, column=c).value for c in range(1, 5)] == [
            "Type",
            "Total Provisioned (Licensing) (TiB)",
            "Used (TiB)",
            "Percent Used",
        ]

    def test_column_widths(self, ws: Any) -> None:
        widths = _widths(ws)
        assert widths["A"] == pytest.approx(17.7109375, abs=_TOL)
        assert widths["B"] == pytest.approx(32.28515625, abs=_TOL)
        assert widths["C"] == pytest.approx(14.7109375, abs=_TOL)
        assert widths["D"] == pytest.approx(13.7109375, abs=_TOL)
        # Only the four table columns are sized.
        assert set(widths) == {"A", "B", "C", "D"}
        # openpyxl groups adjacent equal-width columns into one min..max entry.
        assert [(d.min, d.max) for d in ws.column_dimensions.values()] == [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
        ]

    @pytest.mark.parametrize(
        ("row", "label", "cloud", "cluster_type", "data_type"),
        [
            (2, "Azure CVO RW", "azure", "CVO", "RW"),
            (3, "Azure CVO DP", "azure", "CVO", "DP"),
            (4, "Azure CVO HA RW", "azure", "CVO HA", "RW"),
            (5, "Azure CVO HA DP", "azure", "CVO HA", "DP"),
            (8, "AWS CVO RW", "aws", "CVO", "RW"),
            (9, "AWS CVO DP", "aws", "CVO", "DP"),
            (10, "AWS CVO HA RW", "aws", "CVO HA", "RW"),
            (11, "AWS CVO HA DP", "aws", "CVO HA", "DP"),
        ],
    )
    def test_data_rows(
        self, ws: Any, row: int, label: str, cloud: str, cluster_type: str, data_type: str
    ) -> None:
        crit = (
            f'usage_table[Cloud],"{cloud}",usage_table[Cluster Type],"{cluster_type}",'
            f'usage_table[Data Type],"{data_type}")'
        )
        assert ws[f"A{row}"].value == label
        assert ws[f"B{row}"].value == f"=SUMIFS(usage_table[Provisioned (Licensing) TiB],{crit}"
        assert ws[f"C{row}"].value == f"=SUMIFS(usage_table[Used TiB],{crit}"
        assert ws[f"D{row}"].value == f"=IFERROR($C${row}/$B${row}, 0)"
        assert ws[f"B{row}"].number_format == "0.00000"
        assert ws[f"C{row}"].number_format == "0.00000"
        assert ws[f"D{row}"].number_format == "0.00%"

    @pytest.mark.parametrize(
        ("row", "label", "first", "last"),
        [(6, "Azure Totals", 2, 5), (12, "AWS Totals", 8, 11)],
    )
    def test_total_rows(self, ws: Any, row: int, label: str, first: int, last: int) -> None:
        assert ws[f"A{row}"].value == label
        assert ws[f"B{row}"].value == f"=SUM($B{first}:$B{last})"
        assert ws[f"C{row}"].value == f"=SUM($C{first}:$C{last})"
        assert ws[f"D{row}"].value == f"=IFERROR($C${row}/$B${row}, 0)"
        assert ws[f"B{row}"].number_format == "0.00000"
        assert ws[f"C{row}"].number_format == "0.00000"
        assert ws[f"D{row}"].number_format == "0.00%"

    def test_spacer_row_is_empty(self, ws: Any) -> None:
        for col in "ABCD":
            assert ws[f"{col}7"].value is None
        assert ws.max_row == 12
