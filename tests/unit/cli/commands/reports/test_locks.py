"""Tests for reports locks command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import openpyxl
import pytest

from pynetappfoundry.cli.commands.reports.locks import _gather_lock_data
from pynetappfoundry.models.ontap.protocols.locks.model import (
    OntapClientLock,
    OntapClientLockShareLock,
    OntapClientLockVolume,
)
from pynetappfoundry.utils.excel import ExcelWorkbook


def _make_lock(
    *,
    volume_name: str = "vol1",
    protocol: str = "cifs",
    type_: str = "share_level",
    path: str = "/data/file.txt",
    share_lock_mode: str = "read",
    oplock_level: str = "",
    state: str = "granted",
    client_address: str = "192.168.1.10",
) -> OntapClientLock:
    """Create an OntapClientLock with common defaults."""
    return OntapClientLock(
        volume=OntapClientLockVolume(name=volume_name),
        protocol=protocol,
        type_=type_,
        path=path,
        share_lock=OntapClientLockShareLock(mode=share_lock_mode),
        oplock_level=oplock_level,
        state=state,
        client_address=client_address,
    )


def _read(wb: ExcelWorkbook, tmp_path: Path, sheet: str) -> Any:
    """Close the workbook and read one sheet back."""
    wb.close()
    return openpyxl.load_workbook(tmp_path / "out.xlsx")[sheet]


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


class TestGatherLockData:
    """Tests for _gather_lock_data."""

    @patch("pynetappfoundry.cli.commands.reports.locks.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient")
    def test_creates_sheet(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test that a sheet is created for the cluster."""
        lock = _make_lock()
        mock_qs_cls.return_value.all.return_value = [lock]

        wb = ExcelWorkbook(tmp_path / "out.xlsx")

        _gather_lock_data("cluster1", sample_details, mock_config, wb)
        ws = _read(wb, tmp_path, "cluster1")

        # Header row
        assert ws.cell(row=1, column=1).value == "Volume"
        assert ws.cell(row=1, column=7).value == "IP Address"
        # Data row
        assert ws.cell(row=2, column=1).value == "vol1"
        # Verify config= is threaded to QuerySet (DataSource shim)
        for call in mock_qs_cls.call_args_list:
            assert call.kwargs.get("config") is mock_config

    @patch("pynetappfoundry.cli.commands.reports.locks.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient")
    def test_share_level_lock_row(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test that share_level lock row has correct columns."""
        lock = _make_lock(
            type_="share_level",
            share_lock_mode="read_write",
        )
        mock_qs_cls.return_value.all.return_value = [lock]

        wb = ExcelWorkbook(tmp_path / "out.xlsx")

        _gather_lock_data("cluster1", sample_details, mock_config, wb)
        ws = _read(wb, tmp_path, "cluster1")

        # Row 2 is data (row 1 is header)
        assert ws.cell(row=2, column=1).value == "vol1"
        assert ws.cell(row=2, column=2).value == "cifs"
        assert ws.cell(row=2, column=3).value == "share_level"
        assert ws.cell(row=2, column=4).value == "/data/file.txt"
        assert ws.cell(row=2, column=5).value == "read_write"
        assert ws.cell(row=2, column=6).value == "granted"
        assert ws.cell(row=2, column=7).value == "192.168.1.10"
        # Verify config= is threaded to QuerySet (DataSource shim)
        for call in mock_qs_cls.call_args_list:
            assert call.kwargs.get("config") is mock_config

    @patch("pynetappfoundry.cli.commands.reports.locks.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient")
    def test_op_lock_row(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test that op_lock row has correct columns."""
        lock = _make_lock(
            type_="op_lock",
            share_lock_mode="",
            oplock_level="batch",
        )
        mock_qs_cls.return_value.all.return_value = [lock]

        wb = ExcelWorkbook(tmp_path / "out.xlsx")

        _gather_lock_data("cluster1", sample_details, mock_config, wb)
        ws = _read(wb, tmp_path, "cluster1")

        assert ws.cell(row=2, column=3).value == "op_lock"
        assert ws.cell(row=2, column=5).value == "batch"
        # Verify config= is threaded to QuerySet (DataSource shim)
        for call in mock_qs_cls.call_args_list:
            assert call.kwargs.get("config") is mock_config

    @patch("pynetappfoundry.cli.commands.reports.locks.print_error")
    @patch("pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient")
    def test_error_handling_creates_error_sheet(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test that connection failure creates an error sheet."""
        mock_client_cls.side_effect = Exception("Connection refused")

        wb = ExcelWorkbook(tmp_path / "out.xlsx")

        _gather_lock_data("cluster1", sample_details, mock_config, wb)
        ws = _read(wb, tmp_path, "cluster1")

        assert ws.cell(row=1, column=1).value == "Error"
        assert "Connection refused" in ws.cell(row=1, column=2).value
        mock_print_error.assert_called_once()

    @patch("pynetappfoundry.cli.commands.reports.locks.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient")
    def test_empty_locks_creates_header_only(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test that no locks creates a sheet with header only."""
        mock_qs_cls.return_value.all.return_value = []

        wb = ExcelWorkbook(tmp_path / "out.xlsx")

        _gather_lock_data("cluster1", sample_details, mock_config, wb)
        ws = _read(wb, tmp_path, "cluster1")

        assert ws.cell(row=1, column=1).value == "Volume"
        assert ws.cell(row=2, column=1).value is None
        # Verify config= is threaded to QuerySet (DataSource shim)
        for call in mock_qs_cls.call_args_list:
            assert call.kwargs.get("config") is mock_config


class TestLocksExitCode:
    """Exit-code behaviour of the locks command."""

    @staticmethod
    def _run(results: list[bool]) -> Any:
        from click.testing import CliRunner

        from pynetappfoundry.cli.commands.reports.locks import locks

        clusters = {f"c{i}": {"ip": "1.1.1.1"} for i in range(len(results))}
        cfg = MagicMock()
        cfg.get_clusters.return_value = clusters
        cfg.output_dir = Path("/tmp/test_output")
        with (
            patch("pynetappfoundry.cli.decorators.Config", return_value=cfg),
            patch(
                "pynetappfoundry.cli.commands.reports.locks._gather_lock_data",
                side_effect=results,
            ),
            patch("pynetappfoundry.cli.commands.reports.locks.ExcelWorkbook"),
        ):
            return CliRunner().invoke(locks, [], obj={})

    def test_all_clusters_fail_exits_nonzero(self) -> None:
        assert self._run([False, False]).exit_code != 0

    def test_partial_failure_exits_zero(self) -> None:
        result = self._run([False, True])
        assert result.exit_code == 0, result.output

    def test_gather_returns_false_on_error(
        self, mock_config: MagicMock, sample_details: dict[str, Any], tmp_path: Path
    ) -> None:
        with patch(
            "pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient",
            side_effect=RuntimeError("down"),
        ):
            wb = ExcelWorkbook(tmp_path / "o.xlsx")
            assert _gather_lock_data("c", sample_details, mock_config, wb) is False


class TestLocksReadBack:
    """Command-level read-back of the saved workbook."""

    @staticmethod
    def _run(tmp_path: Path, names: list[str], locks_data: list[OntapClientLock]) -> Path:
        from click.testing import CliRunner

        from pynetappfoundry.cli.commands.reports.locks import locks

        cfg = MagicMock()
        cfg.get_clusters.return_value = {n: {"ip": "1.1.1.1"} for n in names}
        cfg.output_dir = tmp_path
        with (
            patch("pynetappfoundry.cli.decorators.Config", return_value=cfg),
            patch("pynetappfoundry.cli.commands.reports.locks.ONTAPAPIClient"),
            patch("pynetappfoundry.cli.commands.reports.locks.QuerySet") as qs,
        ):
            qs.return_value.all.return_value = locks_data
            result = CliRunner().invoke(locks, [], obj={})
        assert result.exit_code == 0, result.output
        (path,) = tmp_path.glob("locks_*.xlsx")
        return path

    def test_rows_read_back(self, tmp_path: Path) -> None:
        path = self._run(
            tmp_path, ["c1"], [_make_lock(), _make_lock(type_="op_lock", oplock_level="batch")]
        )
        ws = openpyxl.load_workbook(path)["c1"]
        assert [c.value for c in ws[1]][:2] == ["Volume", "Protocol"]
        assert ws.cell(row=2, column=5).value == "read"
        assert ws.cell(row=3, column=5).value == "batch"

    def test_long_and_colliding_names(self, tmp_path: Path) -> None:
        long_a = "a" * 40
        long_b = "a" * 35 + "bbbbb"
        path = self._run(tmp_path, [long_a, long_b, "Alpha", "alpha"], [_make_lock()])
        names = openpyxl.load_workbook(path).sheetnames
        assert len(names) == 4
        assert len({n.lower() for n in names}) == 4
        assert all(len(n) <= 31 for n in names)
        assert names[0] == "a" * 31
