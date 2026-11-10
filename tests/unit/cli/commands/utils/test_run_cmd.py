"""Tests for the run-cmd and sqlite-to-excel exit codes."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from rich.errors import MarkupError

from pynetappfoundry.cli.commands.utils.run_cmd import run_cmd
from pynetappfoundry.cli.commands.utils.sqlite_to_excel import sqlite_to_excel


def _cfg() -> MagicMock:
    cfg = MagicMock()
    cfg.get_clusters.return_value = {"c1": {"ip": "1.1.1.1"}}
    cfg.get_user.return_value = ("admin", "pw")
    return cfg


class TestRunCmdExitCode:
    @patch("pynetappfoundry.cli.commands.utils.run_cmd.ONTAPCLI")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_failure_exits_nonzero(self, mock_config_cls: MagicMock, cli_cls: MagicMock) -> None:
        mock_config_cls.return_value = _cfg()
        cli_cls.return_value.run_command.side_effect = RuntimeError("unreachable")

        result = CliRunner().invoke(run_cmd, ["vol show"], obj={})

        assert result.exit_code != 0
        assert "unreachable" in result.output

    @patch("pynetappfoundry.cli.commands.utils.run_cmd.ONTAPCLI")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_success_exits_zero(self, mock_config_cls: MagicMock, cli_cls: MagicMock) -> None:
        mock_config_cls.return_value = _cfg()
        cli_cls.return_value.run_command.return_value = ["line"]

        result = CliRunner().invoke(run_cmd, ["vol show"], obj={})

        assert result.exit_code == 0, result.output


class TestSqliteToExcelExitCode:
    def test_empty_db_exits_nonzero(self, tmp_path: Path) -> None:
        db = tmp_path / "e.db"
        sqlite3.connect(db).close()
        assert CliRunner().invoke(sqlite_to_excel, [str(db)]).exit_code != 0

    def test_conversion_error_exits_nonzero(self, tmp_path: Path) -> None:
        db = tmp_path / "bad.db"
        db.write_text("not a database")
        assert CliRunner().invoke(sqlite_to_excel, [str(db)]).exit_code != 0

    def test_success_exits_zero(self, tmp_path: Path) -> None:
        db = tmp_path / "ok.db"
        conn = sqlite3.connect(db)
        conn.execute("CREATE TABLE t (a INTEGER)")
        conn.execute("INSERT INTO t VALUES (1)")
        conn.commit()
        conn.close()
        result = CliRunner().invoke(sqlite_to_excel, [str(db)])
        assert result.exit_code == 0, result.output


class TestRunCmdMarkupEscaping:
    """Remote output and exception text with markup-like content must not crash."""

    @patch("pynetappfoundry.cli.commands.utils.run_cmd.ONTAPCLI")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_output_line_with_closing_tag(
        self, mock_config_cls: MagicMock, cli_cls: MagicMock
    ) -> None:
        mock_config_cls.return_value = _cfg()
        cli_cls.return_value.run_command.return_value = ["foo [/x] bar"]

        result = CliRunner().invoke(run_cmd, ["vol show"], obj={})

        assert result.exit_code == 0, result.output
        assert "foo [/x] bar" in result.output

    @patch("pynetappfoundry.cli.commands.utils.run_cmd.ONTAPCLI")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_exception_text_with_closing_tag(
        self, mock_config_cls: MagicMock, cli_cls: MagicMock
    ) -> None:
        mock_config_cls.return_value = _cfg()
        cli_cls.return_value.run_command.side_effect = RuntimeError("bad [/x]")

        result = CliRunner().invoke(run_cmd, ["vol show"], obj={})

        assert result.exit_code != 0
        assert "bad [/x]" in result.output
        assert not isinstance(result.exception, MarkupError)
