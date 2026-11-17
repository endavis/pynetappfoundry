"""The shipped example config loads and demonstrates a scope (#1080)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pynetappfoundry.core.config import Config

_EXAMPLE = Path(__file__).parents[3] / "docs" / "example-config"


@pytest.fixture
def example(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Config:
    monkeypatch.chdir(tmp_path)
    return Config(config_dir=str(_EXAMPLE), script_name="test")


def test_org1_objects_are_attributed_to_the_scope(example: Config) -> None:
    assert set(example.scopes) == {"Org1"}
    assert example.get_scope("clusters", "ORG1-PROD-01") == "Org1"
    assert example.get_scope("connectors", "ORG1-CONNECTOR-01") == "Org1"
    assert example.get_scope("clusters", "AZURE-PROD-01") is None


def test_org1_scope_files_override_defaults(example: Config) -> None:
    assert example.get_user("clusters", "ORG1-PROD-01") == ("org1-admin", "org1_admin_password")
    assert example.get_user("clusters", "AZURE-PROD-01") == ("netappuser", "netappuser_password")
    inodes = ("settings", "default_thresholds", "inodes")
    assert example.get_object_setting("clusters", "ORG1-PROD-01", "monitoring", *inodes) == 70
    assert example.get_object_setting("clusters", "AZURE-PROD-01", "monitoring", *inodes) == 80


def test_org1_console_account_is_its_own(example: Config) -> None:
    settings = example.get_console_api_settings(scope="Org1")
    assert settings.org_id == "your-org1-id"
    assert settings.agent_ids == ["your-agent-idclients"]
