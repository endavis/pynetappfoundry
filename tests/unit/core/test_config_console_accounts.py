"""Tests for ``Config.console_account_scopes`` (#1078, ADR-0028)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pynetappfoundry.core.config import Config


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("NF_CONSOLE_USER", "NF_CONSOLE_PASSWORD"):
        monkeypatch.delenv(key, raising=False)


def _load(base: Path, monkeypatch: pytest.MonkeyPatch, files: dict[str, str]) -> Config:
    monkeypatch.chdir(base)
    for rel, content in files.items():
        path = base / "cfg" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir="cfg", script_name="test")


def _scope(name: str, with_console: bool = True) -> dict[str, str]:
    files = {f"{name}/scope.toml": f'name = "{name}"\n'}
    if with_console:
        files[f"{name}/consoleapi.toml"] = '[general]\nservice_token = "placeholder-token"\n'
    return files


def test_root_with_credentials_is_an_account(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _load(
        tmp_path,
        monkeypatch,
        {
            "consoleapi.toml": (
                '[general]\nbase_url = "https://api.example.invalid"\nuser_token = "t"\n'
            )
        },
    )
    assert config.console_account_scopes() == [None]


@pytest.mark.parametrize(
    "credential",
    ['service_token = "t"', 'client_id = "cid"'],
)
def test_other_root_credentials_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, credential: str
) -> None:
    config = _load(tmp_path, monkeypatch, {"consoleapi.toml": f"[general]\n{credential}\n"})
    assert config.console_account_scopes() == [None]


def test_root_with_only_inherited_keys_is_not_an_account(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _load(
        tmp_path,
        monkeypatch,
        {"consoleapi.toml": '[general]\nbase_url = "https://api.example.invalid"\n'},
    )
    assert config.console_account_scopes() == []


def test_root_refresh_token_alone_is_an_account(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _load(
        tmp_path,
        monkeypatch,
        {"users.toml": '[console]\nuser = "label"\nenc = "placeholder-refresh"\n'},
    )
    assert config.console_account_scopes() == [None]


def test_no_console_configuration_gives_no_accounts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _load(tmp_path, monkeypatch, {"other.toml": "[settings]\nx = 1\n"})
    assert config.console_account_scopes() == []


def test_root_then_sorted_scopes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    files = {"consoleapi.toml": '[general]\nservice_token = "t"\n'}
    files.update(_scope("B"))
    files.update(_scope("A"))
    config = _load(tmp_path, monkeypatch, files)
    assert config.console_account_scopes() == [None, "A", "B"]


def test_scope_without_consoleapi_is_excluded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = _scope("A")
    files.update(_scope("NoConsole", with_console=False))
    config = _load(tmp_path, monkeypatch, files)
    assert config.console_account_scopes() == ["A"]
