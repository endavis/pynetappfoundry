"""Tests for the ``nf cache occm`` commands (#1087)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch

from click.testing import CliRunner, Result
from rich.console import Console

from pynetappfoundry.cache import OccmCacheDB
from pynetappfoundry.cache.occm_collector import OccmAgentSnapshot, OccmSnapshot
from pynetappfoundry.cli.main import nf
from pynetappfoundry.console.discovery import AccountInventory, ConsoleInventory
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.models.console_types import ConsoleAgentInfo

_MAPPING = "OccmOnpremWorkingEnvironment"
_REFRESH = "pynetappfoundry.cli.commands.cache.occm.refresh_occm_cache"


def _config_dir(tmp_path: Path) -> Path:
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    (config_dir / "settings.toml").write_text(
        '[ontapapi]\n[ontapapi.general]\nbase_api_path = "/api"\n'
    )
    return config_dir


def _run(tmp_path: Path, *args: str, input: str | None = None) -> Result:
    with patch("pynetappfoundry.cli.commands.cache.occm.console", Console(width=250)):
        return CliRunner().invoke(
            nf, ["-c", str(_config_dir(tmp_path)), "cache", "occm", *args], input=input
        )


def _agent(
    agent_id: str, records: list[dict[str, Any]], cached_at: datetime | None = None
) -> OccmAgentSnapshot:
    return OccmAgentSnapshot(
        agent_id=agent_id,
        scope="prod",
        organization_id="org-1",
        cached_at=cached_at or datetime.now(UTC),
        records={_MAPPING: records},
    )


def _populate(
    tmp_path: Path,
    agents: list[OccmAgentSnapshot],
    inventory: ConsoleInventory | None = None,
) -> None:
    config = Config(config_dir=str(_config_dir(tmp_path)), script_name="t")
    with OccmCacheDB(config=config) as db:
        db.set(
            OccmSnapshot(
                cached_at=datetime.now(UTC),
                inventory=inventory or ConsoleInventory(),
                agents=tuple(agents),
            )
        )


def _snapshot(**kwargs: Any) -> OccmSnapshot:
    return OccmSnapshot(cached_at=datetime.now(UTC), inventory=ConsoleInventory(), **kwargs)


class TestRefresh:
    def test_success_lists_agents(self, tmp_path: Path) -> None:
        snap = _snapshot(
            agents=(_agent("a[b]1", [{"publicId": "p1"}, {"publicId": "p2"}]),),
            skipped_agents=("a2",),
            failed_mappings=(("a[b]1", "OccmAwsWorkingEnvironment"),),
        )
        with patch(_REFRESH, return_value=snap) as refresh:
            result = _run(tmp_path, "refresh")
        assert result.exit_code == 0, result.output
        refresh.assert_called_once()
        assert refresh.call_args.kwargs["scopes"] is None
        assert "a[b]1" in result.output
        assert "a2" in result.output
        assert "OccmAwsWorkingEnvironment" in result.output
        assert " 2 " in result.output

    def test_failed_agent_exits_1(self, tmp_path: Path) -> None:
        snap = _snapshot(agents=(_agent("a1", []),), failed_agents=("bad",))
        with patch(_REFRESH, return_value=snap):
            result = _run(tmp_path, "refresh")
        assert result.exit_code == 1
        assert "bad" in result.output

    def test_discovery_error(self, tmp_path: Path) -> None:
        with patch(_REFRESH, side_effect=RuntimeError("boom")):
            result = _run(tmp_path, "refresh")
        assert result.exit_code == 1
        assert "OCCM discovery failed: boom" in result.output

    def test_valid_scope_is_forwarded(self, tmp_path: Path) -> None:
        with (
            patch.object(Config, "console_account_scopes", return_value=[None, "prod"]),
            patch(_REFRESH, return_value=_snapshot()) as refresh,
        ):
            result = _run(tmp_path, "refresh", "--scope", "prod")
        assert result.exit_code == 0, result.output
        assert refresh.call_args.kwargs["scopes"] == ("prod",)

    def test_unknown_scope_lists_available(self, tmp_path: Path) -> None:
        with (
            patch.object(Config, "console_account_scopes", return_value=[None, "prod", "dev"]),
            patch(_REFRESH) as refresh,
        ):
            result = _run(tmp_path, "refresh", "--scope", "nope")
        assert result.exit_code == 1
        assert "Unknown Console scope" in result.output
        assert "dev, prod" in result.output
        refresh.assert_not_called()

    def test_scope_configuration_error(self, tmp_path: Path) -> None:
        with (
            patch.object(Config, "console_account_scopes", side_effect=ConfigurationError("bad")),
            patch(_REFRESH) as refresh,
        ):
            result = _run(tmp_path, "refresh", "--scope", "prod")
        assert result.exit_code == 1
        assert "bad" in result.output
        refresh.assert_not_called()

    def test_missing_config_dir(self, tmp_path: Path) -> None:
        result = CliRunner().invoke(
            nf, ["-c", str(tmp_path / "missing"), "cache", "occm", "refresh"]
        )
        assert result.exit_code == 1
        assert "Configuration directory not found" in result.output


class TestStatus:
    def test_empty_cache(self, tmp_path: Path) -> None:
        result = _run(tmp_path, "status")
        assert result.exit_code == 0
        assert "No OCCM cache data" in result.output
        assert "nf cache occm refresh" in result.output

    def test_fresh_stale_and_not_collected(self, tmp_path: Path) -> None:
        old = datetime.now(UTC) - timedelta(days=40)
        inventory = ConsoleInventory(
            accounts=[
                AccountInventory(
                    scope="prod",
                    agents=[
                        ConsoleAgentInfo(agentId=a, scope="prod", name=n, status="active")
                        for a, n in (("fresh1", "Fresh[x]"), ("stale1", "S"), ("none1", "N"))
                    ],
                )
            ]
        )
        _populate(
            tmp_path,
            [_agent("fresh1", [{"publicId": "p1"}]), _agent("stale1", [], cached_at=old)],
            inventory,
        )
        result = _run(tmp_path, "status")
        assert result.exit_code == 0, result.output
        assert "Fresh[x]" in result.output
        assert "Not collected" in result.output
        assert "Stale" in result.output
        assert "1 fresh, 1 stale, 1 not collected" in result.output

    def test_ttl_option(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [], cached_at=datetime.now(UTC) - timedelta(days=10))])
        assert "1 stale" not in _run(tmp_path, "status").output
        assert "1 stale" in _run(tmp_path, "status", "--ttl", "5").output

    def test_agent_not_in_inventory_is_shown(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("orphan", [])])
        result = _run(tmp_path, "status")
        assert "orphan" in result.output


class TestAgents:
    def test_with_id(self, tmp_path: Path) -> None:
        _populate(
            tmp_path, [_agent("a1", [{"publicId": "p1"}]), _agent("a2", [{"publicId": "p1"}])]
        )
        result = _run(tmp_path, "agents", "p1")
        assert result.exit_code == 0
        assert "a1" in result.output and "a2" in result.output

    def test_unknown_id_exits_1(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [{"publicId": "p1"}])])
        result = _run(tmp_path, "agents", "zzz")
        assert result.exit_code == 1
        assert "zzz" in result.output

    def test_table_without_id(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [{"publicId": "p[1]"}])])
        result = _run(tmp_path, "agents")
        assert result.exit_code == 0
        assert "p[1]" in result.output
        assert "a1" in result.output

    def test_none_cached(self, tmp_path: Path) -> None:
        result = _run(tmp_path, "agents")
        assert result.exit_code == 0
        assert "No working environments cached" in result.output


class TestClear:
    def _agents(self, tmp_path: Path) -> list[str]:
        config = Config(config_dir=str(_config_dir(tmp_path)), script_name="t")
        with OccmCacheDB(config=config) as db:
            return db.list_agents()

    def test_requires_agent_or_all(self, tmp_path: Path) -> None:
        result = _run(tmp_path, "clear")
        assert result.exit_code == 1
        assert "--all" in result.output

    def test_clear_agent_with_force(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [{"publicId": "p1"}]), _agent("a2", [])])
        result = _run(tmp_path, "clear", "a1", "-f")
        assert result.exit_code == 0, result.output
        assert self._agents(tmp_path) == ["a2"]

    def test_unknown_agent_warns_exit_0(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [])])
        result = _run(tmp_path, "clear", "zzz", "-f")
        assert result.exit_code == 0
        assert "No cached data found for agent" in result.output
        assert self._agents(tmp_path) == ["a1"]

    def test_declined(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [])])
        result = _run(tmp_path, "clear", "a1", input="n\n")
        assert result.exit_code == 0
        assert "Cancelled" in result.output
        assert self._agents(tmp_path) == ["a1"]

    def test_confirmed_all(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [{"publicId": "p1"}]), _agent("a2", [])])
        result = _run(tmp_path, "clear", "--all", input="y\n")
        assert result.exit_code == 0
        assert self._agents(tmp_path) == []

    def test_all_force(self, tmp_path: Path) -> None:
        _populate(tmp_path, [_agent("a1", [])])
        result = _run(tmp_path, "clear", "--all", "-f")
        assert result.exit_code == 0
        assert self._agents(tmp_path) == []


def test_help_lists_commands() -> None:
    result = CliRunner().invoke(nf, ["cache", "occm", "--help"])
    assert result.exit_code == 0
    for name in ("refresh", "status", "agents", "clear"):
        assert name in result.output


def test_cache_help_lists_occm() -> None:
    assert "occm" in CliRunner().invoke(nf, ["cache", "--help"]).output
