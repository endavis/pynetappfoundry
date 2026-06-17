"""Tests for ``nf cifs session`` command body and CLI invocation."""

from __future__ import annotations

import csv as csv_module
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner
from rich.console import Console

from pynetappfoundry.cli.commands.cifs.session import (
    COLUMNS,
    _render_table,
    _resolve_csv_path,
    _scan_cluster,
    _write_csv,
    session,
)
from pynetappfoundry.models.ontap.protocols.cifs.sessions.model import (
    OntapCifsSession,
    OntapCifsSessionSvm,
)


def _make_session(
    *,
    user: str = "jdoe",
    mapped_unix_user: str = "",
    client_ip: str = "10.1.2.45",
    server_ip: str = "10.1.2.10",
    svm_name: str = "vs1",
    protocol: str = "smb3_1",
    authentication: str = "ntlmv2",
    smb_encryption: str = "unencrypted",
    connected_duration: str = "PT1H",
    idle_duration: str = "PT5M",
    open_files: int = 3,
    open_shares: int = 1,
) -> OntapCifsSession:
    return OntapCifsSession(
        authentication=authentication,
        client_ip=client_ip,
        connected_duration=connected_duration,
        idle_duration=idle_duration,
        mapped_unix_user=mapped_unix_user,
        open_files=open_files,
        open_shares=open_shares,
        protocol=protocol,
        server_ip=server_ip,
        smb_encryption=smb_encryption,
        svm=OntapCifsSessionSvm(name=svm_name, uuid="svm-uuid"),
        user=user,
    )


@pytest.fixture
def mock_config() -> MagicMock:
    cfg = MagicMock()
    cfg.output_dir = Path("/tmp")
    return cfg


def _make_qb(results: list[OntapCifsSession]) -> MagicMock:
    """Build a chainable QueryBuilder mock that yields *results* on iter."""
    qb = MagicMock()
    qb.filter.return_value = qb
    qb.__iter__.side_effect = lambda: iter(results)
    return qb


class TestScanCluster:
    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_no_filters_returns_all(self, ds_cls: MagicMock, mock_config: MagicMock) -> None:
        sessions = [_make_session(user="alice"), _make_session(user="bob")]
        qb = _make_qb(sessions)
        ds_cls.return_value.query.return_value = qb

        rows, scanned = _scan_cluster(mock_config, "c1", user=None, case_sensitive=False, ip=None)

        assert scanned == 2
        assert len(rows) == 2
        # No server-side filter applied when neither --user nor --ip is set.
        qb.filter.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_user_substring_filters_client_side(
        self, ds_cls: MagicMock, mock_config: MagicMock
    ) -> None:
        sessions = [
            _make_session(user="DOMAIN\\jdoe"),
            _make_session(user="DOMAIN\\alice"),
            _make_session(user="", mapped_unix_user="jdoe"),
        ]
        qb = _make_qb(sessions)
        ds_cls.return_value.query.return_value = qb

        rows, scanned = _scan_cluster(mock_config, "c1", user="jdoe", case_sensitive=False, ip=None)

        assert scanned == 3
        assert len(rows) == 2  # jdoe + mapped_unix_user

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_user_never_pushed_server_side(self, ds_cls: MagicMock, mock_config: MagicMock) -> None:
        """``--user`` is always client-side: server push would drop
        sessions matched only via ``mapped_unix_user``."""
        qb = _make_qb([])
        ds_cls.return_value.query.return_value = qb

        _scan_cluster(mock_config, "c1", user="jdoe", case_sensitive=True, ip=None)

        qb.filter.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_user_glob_not_pushed(self, ds_cls: MagicMock, mock_config: MagicMock) -> None:
        qb = _make_qb([])
        ds_cls.return_value.query.return_value = qb

        _scan_cluster(mock_config, "c1", user="*jdoe*", case_sensitive=True, ip=None)

        qb.filter.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_user_case_insensitive_not_pushed(
        self, ds_cls: MagicMock, mock_config: MagicMock
    ) -> None:
        qb = _make_qb([])
        ds_cls.return_value.query.return_value = qb

        _scan_cluster(mock_config, "c1", user="jdoe", case_sensitive=False, ip=None)

        qb.filter.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_query_uses_live_source(self, ds_cls: MagicMock, mock_config: MagicMock) -> None:
        """CIFS sessions are transient — every read must be ``source='live'``."""
        qb = _make_qb([])
        ds_cls.return_value.query.return_value = qb

        _scan_cluster(mock_config, "c1", user=None, case_sensitive=False, ip=None)

        ds_cls.return_value.query.assert_called_once_with(
            OntapCifsSession, cluster="c1", source="live"
        )

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_ip_plain_pushed(self, ds_cls: MagicMock, mock_config: MagicMock) -> None:
        qb = _make_qb([])
        ds_cls.return_value.query.return_value = qb

        _scan_cluster(mock_config, "c1", user=None, case_sensitive=False, ip="10.1.2.45")

        qb.filter.assert_called_once_with({"client_ip": "10.1.2.45"})

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_ip_cidr_not_pushed_but_client_filtered(
        self, ds_cls: MagicMock, mock_config: MagicMock
    ) -> None:
        sessions = [
            _make_session(client_ip="10.1.2.45"),
            _make_session(client_ip="10.1.3.45"),
        ]
        qb = _make_qb(sessions)
        ds_cls.return_value.query.return_value = qb

        rows, scanned = _scan_cluster(
            mock_config, "c1", user=None, case_sensitive=False, ip="10.1.2.0/24"
        )

        qb.filter.assert_not_called()
        assert scanned == 2
        assert len(rows) == 1

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_combined_user_and_ip_anded(self, ds_cls: MagicMock, mock_config: MagicMock) -> None:
        sessions = [
            _make_session(user="jdoe", client_ip="10.1.2.45"),
            _make_session(user="jdoe", client_ip="10.1.3.45"),
            _make_session(user="alice", client_ip="10.1.2.46"),
        ]
        qb = _make_qb(sessions)
        ds_cls.return_value.query.return_value = qb

        rows, scanned = _scan_cluster(
            mock_config,
            "c1",
            user="jdoe",
            case_sensitive=False,
            ip="10.1.2.0/24",
        )

        assert scanned == 3
        assert len(rows) == 1
        assert rows[0][2] == "jdoe"
        assert rows[0][4] == "10.1.2.45"


class TestRenderTable:
    def test_no_truncation_at_narrow_width(self) -> None:
        """All cell values appear verbatim with Console(width=80) — no '…'."""
        long_user = "DOMAIN\\very-long-username-that-would-normally-truncate"
        long_duration = "P0DT12H34M56S-extra"
        rows = [
            (
                "production-cluster-1",
                "vs-application-data",
                long_user,
                "mapped-very-long-unix-user",
                "10.255.255.255",
                "10.255.255.254",
                "smb3_1_1",
                "kerberos",
                "encrypted-aes-128-ccm",
                long_duration,
                "PT0S",
                "999",
                "888",
            )
        ]
        buf = StringIO()
        narrow = Console(file=buf, width=80, force_terminal=False)

        import sys

        session_mod = sys.modules["pynetappfoundry.cli.commands.cifs.session"]

        with patch.object(session_mod, "console", narrow):
            _render_table(rows, "CIFS Sessions")

        output = buf.getvalue()
        # No ellipsis character anywhere — Rich's truncation marker.
        assert "…" not in output
        # Every cell value appears verbatim.
        for cell in rows[0]:
            assert cell in output, f"missing {cell!r} in output:\n{output}"


class TestResolveCsvPath:
    def test_explicit_file(self, tmp_path: Path) -> None:
        target = tmp_path / "out.csv"
        result = _resolve_csv_path(str(target), tmp_path)
        assert result == target

    def test_directory_path_uses_timestamp(self, tmp_path: Path) -> None:
        result = _resolve_csv_path(str(tmp_path), tmp_path)
        assert result.parent == tmp_path
        assert result.name.startswith("cifs_sessions_")
        assert result.suffix == ".csv"


class TestWriteCsv:
    def test_header_and_rows(self, tmp_path: Path) -> None:
        target = tmp_path / "out.csv"
        rows = [
            (
                "c1",
                "vs1",
                "jdoe",
                "",
                "10.1.2.45",
                "10.1.2.10",
                "smb3",
                "ntlmv2",
                "unencrypted",
                "PT1H",
                "PT5M",
                "3",
                "1",
            )
        ]
        _write_csv(rows, target)

        with target.open(encoding="utf-8") as f:
            reader = csv_module.reader(f)
            data = list(reader)

        assert data[0] == list(COLUMNS)
        assert len(data) == 2
        assert data[1][0] == "c1"
        assert data[1][2] == "jdoe"

    def test_creates_parent(self, tmp_path: Path) -> None:
        target = tmp_path / "sub" / "out.csv"
        _write_csv([], target)
        assert target.exists()


class TestSessionCommand:
    """End-to-end CLI invocation tests via :class:`CliRunner`."""

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_no_clusters_warns_and_exits_zero(
        self, mock_config_cls: MagicMock, ds_cls: MagicMock
    ) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {}
        cfg.output_dir = Path("/tmp")
        mock_config_cls.return_value = cfg

        result = CliRunner().invoke(session, [], obj={})

        assert result.exit_code == 0, result.output
        ds_cls.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_lists_all_no_filter(self, mock_config_cls: MagicMock, ds_cls: MagicMock) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {"c1": {"ip": "1.1.1.1"}}
        cfg.output_dir = Path("/tmp")
        mock_config_cls.return_value = cfg

        qb = _make_qb([_make_session(user="jdoe"), _make_session(user="alice")])
        ds_cls.return_value.query.return_value = qb

        with patch("pynetappfoundry.cli.commands.cifs.session._render_table") as mock_render:
            result = CliRunner().invoke(session, [], obj={})

        assert result.exit_code == 0, result.output
        mock_render.assert_called_once()
        rendered_rows = mock_render.call_args[0][0]
        users = {row[2] for row in rendered_rows}
        assert users == {"jdoe", "alice"}
        # Server-side filter NOT applied without --user/--ip.
        qb.filter.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_no_matches_yellow_message(self, mock_config_cls: MagicMock, ds_cls: MagicMock) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {"c1": {"ip": "1.1.1.1"}}
        cfg.output_dir = Path("/tmp")
        mock_config_cls.return_value = cfg

        qb = _make_qb([_make_session(user="alice")])
        ds_cls.return_value.query.return_value = qb

        result = CliRunner().invoke(session, ["-u", "jdoe"], obj={})

        assert result.exit_code == 0, result.output
        assert "No CIFS sessions matched" in result.output

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_per_cluster_exception_continues(
        self, mock_config_cls: MagicMock, ds_cls: MagicMock
    ) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {
            "broken": {"ip": "1.1.1.1"},
            "ok": {"ip": "2.2.2.2"},
        }
        cfg.output_dir = Path("/tmp")
        mock_config_cls.return_value = cfg

        good_qb = _make_qb([_make_session(user="jdoe")])

        def query_side_effect(*_a: Any, **kwargs: Any) -> Any:
            if kwargs.get("cluster") == "broken":
                raise RuntimeError("boom")
            return good_qb

        ds_cls.return_value.query.side_effect = query_side_effect

        with patch("pynetappfoundry.cli.commands.cifs.session._render_table") as mock_render:
            result = CliRunner().invoke(session, [], obj={})

        assert result.exit_code == 0, result.output
        # Per-cluster error surfaced but scan continued.
        assert "boom" in result.output
        mock_render.assert_called_once()
        rendered_rows = mock_render.call_args[0][0]
        assert [row[2] for row in rendered_rows] == ["jdoe"]

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    def test_live_flag_rejected(self, ds_cls: MagicMock) -> None:
        """``--live`` is intentionally not exposed: CIFS sessions are
        always live (transient data is never cached)."""
        result = CliRunner().invoke(session, ["--live"], obj={})

        assert result.exit_code != 0
        assert "no such option" in result.output.lower() or "--live" in result.output

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_csv_export_additive(
        self,
        mock_config_cls: MagicMock,
        ds_cls: MagicMock,
        tmp_path: Path,
    ) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {"c1": {"ip": "1.1.1.1"}}
        cfg.output_dir = tmp_path
        mock_config_cls.return_value = cfg

        qb = _make_qb([_make_session(user="jdoe")])
        ds_cls.return_value.query.return_value = qb

        out = tmp_path / "out.csv"
        with patch("pynetappfoundry.cli.commands.cifs.session._render_table") as mock_render:
            result = CliRunner().invoke(session, ["--csv", str(out)], obj={})

        assert result.exit_code == 0, result.output
        # Table still rendered (CSV is additive, not a replacement).
        mock_render.assert_called_once()
        # CSV written and confirmation line printed.
        assert out.exists()
        flat_output = " ".join(result.output.split())
        assert str(out.resolve()) in flat_output
        assert "row(s)" in flat_output

        with out.open(encoding="utf-8") as f:
            data = list(csv_module.reader(f))
        assert data[0] == list(COLUMNS)
        assert data[1][2] == "jdoe"

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_csv_directory_uses_timestamped_name(
        self,
        mock_config_cls: MagicMock,
        ds_cls: MagicMock,
        tmp_path: Path,
    ) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {"c1": {"ip": "1.1.1.1"}}
        cfg.output_dir = tmp_path
        mock_config_cls.return_value = cfg

        qb = _make_qb([_make_session(user="jdoe")])
        ds_cls.return_value.query.return_value = qb

        result = CliRunner().invoke(session, ["--csv", str(tmp_path)], obj={})

        assert result.exit_code == 0, result.output
        files = list(tmp_path.glob("cifs_sessions_*.csv"))
        assert len(files) == 1

    @patch("pynetappfoundry.cli.commands.cifs.session.DataSource")
    @patch("pynetappfoundry.cli.decorators.Config")
    def test_invalid_ip_returns_bad_parameter(
        self, mock_config_cls: MagicMock, ds_cls: MagicMock
    ) -> None:
        cfg = MagicMock()
        cfg.get_clusters.return_value = {"c1": {"ip": "1.1.1.1"}}
        cfg.output_dir = Path("/tmp")
        mock_config_cls.return_value = cfg

        result = CliRunner().invoke(session, ["--ip", "not-an-ip"], obj={})

        assert result.exit_code != 0
        assert "Invalid IP" in result.output or "Get CIFS sessions failed" in result.output
