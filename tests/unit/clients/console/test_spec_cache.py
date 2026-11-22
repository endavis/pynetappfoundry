"""Tests for the session-cached real Console spec fixtures (#1139)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import yaml
from pydantic import SecretStr

import pynetappfoundry.clients.openapi as openapi
from pynetappfoundry.clients.console.api import ConsoleAPIClient
from pynetappfoundry.core.models import ConsoleAPISettings

from .conftest import REAL_SPEC


def test_real_spec_path_returns_session_dict(
    real_spec_dir: Path, real_console_spec: dict[str, Any]
) -> None:
    assert openapi._load_spec(REAL_SPEC) is real_console_spec
    assert openapi._load_spec(REAL_SPEC) is real_console_spec


def test_str_path_hits_the_cache(real_spec_dir: Path, real_console_spec: dict[str, Any]) -> None:
    path: Any = str(real_spec_dir / "console_openapi.yaml")
    assert openapi._load_spec(path) is real_console_spec


def test_other_paths_use_the_real_loader(real_spec_dir: Path, tmp_path: Path) -> None:
    yaml_path = tmp_path / "small.yaml"
    yaml_path.write_text(yaml.safe_dump({"openapi": "3.0.0", "x": 1}), encoding="utf-8")
    json_path = tmp_path / "small.json"
    json_path.write_text(json.dumps({"openapi": "3.0.0", "y": 2}), encoding="utf-8")

    assert openapi._load_spec(yaml_path) == {"openapi": "3.0.0", "x": 1}
    assert openapi._load_spec(json_path) == {"openapi": "3.0.0", "y": 2}


def test_client_construction_reuses_the_session_dict(
    real_spec_dir: Path, real_console_spec: dict[str, Any]
) -> None:
    config = MagicMock()
    config.get_console_api_settings.return_value = ConsoleAPISettings(
        user_token=SecretStr("user-jwt"),
        service_token=SecretStr("service-jwt"),
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
    )
    config.get_schema_location.return_value = real_spec_dir

    client = ConsoleAPIClient(config)

    assert client._require_user().api_spec is real_console_spec
    assert client._require_service().api_spec is real_console_spec
