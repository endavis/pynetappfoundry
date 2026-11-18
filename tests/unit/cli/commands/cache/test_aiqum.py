"""Tests for the ``nf cache aiqum`` commands (#1072)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache import AiqumCacheDB, CollectionError
from pynetappfoundry.cache.aiqum_collector import AiqumSnapshot
from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config import ConfigurationError

_MOD = "pynetappfoundry.cli.commands.cache.aiqum"


def _snap(instance: str, cached_at: datetime | None = None) -> AiqumSnapshot:
    return AiqumSnapshot(
        instance=instance,
        cached_at=cached_at or datetime.now(UTC),
        records={"AiqumVolume": [{"key": "k1", "name": "v1"}, {"key": "k2", "name": "v2"}]},
    )


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    path = tmp_path / "config"
    (path / "data").mkdir(parents=True)
    (path / "settings.toml").write_text('[ontapapi]\n[ontapapi.general]\nbase_api_path = "/api"\n')
    (path / "data" / "aiqums.toml").write_text(
        '[settings]\ntype = "data"\n\n[aiqums]\n'
        'aiq1 = {ip = "10.0.0.1"}\naiq2 = {ip = "10.0.0.2"}\n'
    )
    return path


@pytest.fixture
def seeded(config_dir: Path) -> Iterator[Path]:
    """A config dir whose cache already holds aiq1 and aiq2."""
    with _open(config_dir) as db:
        db.set("aiq1", _snap("aiq1"))
        db.set("aiq2", _snap("aiq2"))
    yield config_dir


def _run(runner: CliRunner, config_dir: Path, *args: str, **kw: Any) -> Any:
    return runner.invoke(nf, ["-c", str(config_dir), "cache", "aiqum", *args], **kw)


def _open(config_dir: Path) -> AiqumCacheDB:
    (config_dir / ".cache").mkdir(exist_ok=True)
    return AiqumCacheDB(db_path=config_dir / ".cache" / "aiqum_cache.db")


def _instances(config_dir: Path) -> list[str]:
    with _open(config_dir) as db:
        return db.list_instances()


class TestRefresh:
    def test_single(self, runner: CliRunner, config_dir: Path) -> None:
        with patch(f"{_MOD}.refresh_aiqum_cache", return_value=_snap("aiq1")) as m:
            result = _run(runner, config_dir, "refresh", "aiq1")
        assert result.exit_code == 0
        assert m.call_count == 1
        assert m.call_args.args[1] == "aiq1"
        assert "AiqumVolume: 2" in result.output

    def test_all(self, runner: CliRunner, config_dir: Path) -> None:
        with patch(f"{_MOD}.refresh_aiqum_cache", side_effect=lambda c, n, db: _snap(n)) as m:
            result = _run(runner, config_dir, "refresh", "--all")
        assert result.exit_code == 0
        assert [c.args[1] for c in m.call_args_list] == ["aiq1", "aiq2"]

    def test_no_args(self, runner: CliRunner, config_dir: Path) -> None:
        result = _run(runner, config_dir, "refresh")
        assert result.exit_code != 0
        assert "Specify an AIQUM instance" in result.output

    @pytest.mark.parametrize("exc", [CollectionError("boom"), ConfigurationError("badcfg")])
    def test_failure(self, runner: CliRunner, config_dir: Path, exc: Exception) -> None:
        with patch(f"{_MOD}.refresh_aiqum_cache", side_effect=exc):
            result = _run(runner, config_dir, "refresh", "aiq1")
        assert result.exit_code != 0
        assert str(exc) in result.output

    def test_partial_failure(self, runner: CliRunner, config_dir: Path) -> None:
        def fake(config: Any, name: str, db: Any) -> AiqumSnapshot:
            if name == "aiq1":
                raise CollectionError("down")
            return _snap(name)

        with patch(f"{_MOD}.refresh_aiqum_cache", side_effect=fake) as m:
            result = _run(runner, config_dir, "refresh", "--all")
        assert m.call_count == 2
        assert result.exit_code != 0
        assert "Refresh failed for: aiq1" in result.output
        assert "Refreshed AIQUM 'aiq2'" in result.output

    def test_all_without_inventory(self, runner: CliRunner, config_dir: Path) -> None:
        (config_dir / "data" / "aiqums.toml").unlink()
        mock = MagicMock()
        with patch(f"{_MOD}.refresh_aiqum_cache", mock):
            result = _run(runner, config_dir, "refresh", "--all")
        assert result.exit_code == 0
        mock.assert_not_called()
        assert "No AIQUM instances" in result.output


class TestStatus:
    def test_fresh_and_not_cached(self, runner: CliRunner, config_dir: Path) -> None:
        with _open(config_dir) as db:
            db.set("aiq1", _snap("aiq1"))
        result = _run(runner, config_dir, "status")
        assert result.exit_code == 0
        assert "Fresh" in result.output
        assert "Not cached" in result.output

    def test_stale_and_ttl(self, runner: CliRunner, config_dir: Path) -> None:
        old = datetime.now(UTC) - timedelta(days=10)
        with _open(config_dir) as db:
            db.set("aiq1", _snap("aiq1", old))
            db.set("aiq2", _snap("aiq2", old))
        assert "Stale (>30 days): 0" in _run(runner, config_dir, "status").output
        result = _run(runner, config_dir, "status", "--ttl", "7")
        assert "Stale" in result.output
        assert "Stale (>7 days): 2" in result.output

    def test_orphaned(self, runner: CliRunner, config_dir: Path) -> None:
        with _open(config_dir) as db:
            db.set("gone", _snap("gone"))
        result = _run(runner, config_dir, "status")
        assert "Orphaned" in result.output


class TestClear:
    def test_single_force_keeps_other(self, runner: CliRunner, seeded: Path) -> None:
        result = _run(runner, seeded, "clear", "aiq1", "-f")
        assert result.exit_code == 0
        assert _instances(seeded) == ["aiq2"]

    def test_confirm_decline(self, runner: CliRunner, seeded: Path) -> None:
        result = _run(runner, seeded, "clear", "aiq1", input="n\n")
        assert result.exit_code == 0
        assert "Cancelled." in result.output
        assert _instances(seeded) == ["aiq1", "aiq2"]

    def test_confirm_accept(self, runner: CliRunner, seeded: Path) -> None:
        result = _run(runner, seeded, "clear", "aiq1", input="y\n")
        assert result.exit_code == 0
        assert _instances(seeded) == ["aiq2"]

    def test_missing_instance(self, runner: CliRunner, seeded: Path) -> None:
        result = _run(runner, seeded, "clear", "nope", "-f")
        assert result.exit_code == 0
        assert "No cached data found" in result.output
        assert _instances(seeded) == ["aiq1", "aiq2"]

    def test_all_force(self, runner: CliRunner, seeded: Path) -> None:
        result = _run(runner, seeded, "clear", "--all", "-f")
        assert result.exit_code == 0
        assert "2 instance(s)" in result.output
        assert _instances(seeded) == []

    def test_all_empty(self, runner: CliRunner, config_dir: Path) -> None:
        result = _run(runner, config_dir, "clear", "--all", "-f")
        assert result.exit_code == 0
        assert "No cached data found" in result.output

    def test_no_args(self, runner: CliRunner, config_dir: Path) -> None:
        result = _run(runner, config_dir, "clear")
        assert result.exit_code != 0
        assert "Specify an AIQUM instance" in result.output
