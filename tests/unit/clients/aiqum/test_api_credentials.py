"""Tests that AIQUMAPIClient resolves per-object credentials (#1045)."""

from __future__ import annotations

import base64
import json
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.core.config import Config

FILES = {
    "data/inventory.toml": """\
[settings]
type = "data"

[aiqums.own]
ip = "10.0.0.1"
user = "own-user"
enc = "own-pass"

[aiqums.plain]
ip = "10.0.0.2"
""",
    "users.toml": '[aiqums]\nuser = "default-user"\nenc = "default-pass"\n',
    "aiqumapi.toml": '[general]\nbase_api_path = "/api"\n',
}


@pytest.fixture
def config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Config]:
    monkeypatch.chdir(tmp_path)
    for key in ("NF_OWN_USER", "NF_OWN_PASSWORD", "NF_PLAIN_USER", "NF_PLAIN_PASSWORD"):
        monkeypatch.delenv(key, raising=False)
    for rel, content in FILES.items():
        path = tmp_path / "cfg" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    (schema_dir / "all.json").write_text(json.dumps({"swagger": "2.0", "paths": {}}))
    cfg = Config(config_dir="cfg", script_name="test")
    with patch.object(Config, "get_schema_location", return_value=schema_dir):
        yield cfg


def _auth(client: AIQUMAPIClient) -> str:
    return str(client.session.headers["authorization"])


def _basic(user: str, password: str) -> str:
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def test_object_credentials_beat_users_toml_default(config: Config) -> None:
    client = AIQUMAPIClient("own", config)
    try:
        assert _auth(client) == _basic("own-user", "own-pass")
    finally:
        client.session.close()


def test_object_without_own_credentials_gets_default(config: Config) -> None:
    client = AIQUMAPIClient("plain", config)
    try:
        assert _auth(client) == _basic("default-user", "default-pass")
    finally:
        client.session.close()
