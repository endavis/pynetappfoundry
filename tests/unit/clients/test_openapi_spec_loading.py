"""Tests that APIWrapper loads JSON and YAML OpenAPI spec files (#1011)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from pynetappfoundry.clients.openapi import APIWrapper

SPEC = {
    "swagger": "2.0",
    "basePath": "/api/v1",
    "paths": {"/users": {"get": {"responses": {"200": {"description": "ok"}}}}},
}


def _wrapper(spec_path: Path) -> APIWrapper:
    return APIWrapper(api_json_file=str(spec_path), base_url="https://api.example.test")


def test_loads_json_spec(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(SPEC), encoding="utf-8")
    assert _wrapper(spec_path).api_spec == SPEC


@pytest.mark.parametrize("name", ["spec.yaml", "spec.yml", "SPEC.YAML"])
def test_loads_yaml_spec(tmp_path: Path, name: str) -> None:
    spec_path = tmp_path / name
    spec_path.write_text(yaml.safe_dump(SPEC), encoding="utf-8")
    assert _wrapper(spec_path).api_spec == SPEC


def test_json_content_under_yaml_name_loads(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.yaml"
    spec_path.write_text(json.dumps(SPEC), encoding="utf-8")
    assert _wrapper(spec_path).api_spec == SPEC
