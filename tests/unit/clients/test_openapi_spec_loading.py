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


# --- YAML loader selection (#1009) ------------------------------------------


def _spy_yaml_load(monkeypatch: pytest.MonkeyPatch) -> list[type]:
    used: list[type] = []
    real_load = yaml.load

    def spy(stream: object, Loader: type) -> object:  # noqa: N803  # mirrors yaml.load's keyword
        used.append(Loader)
        return real_load(stream, Loader=Loader)  # type: ignore[arg-type]  # yaml stubs

    monkeypatch.setattr(yaml, "load", spy)
    return used


def _write_yaml(tmp_path: Path) -> Path:
    spec_path = tmp_path / "spec.yaml"
    spec_path.write_text(yaml.safe_dump(SPEC), encoding="utf-8")
    return spec_path


@pytest.mark.skipif(not hasattr(yaml, "CSafeLoader"), reason="PyYAML built without libyaml")
def test_yaml_uses_c_safe_loader_when_available(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    used = _spy_yaml_load(monkeypatch)
    assert _wrapper(_write_yaml(tmp_path)).api_spec == SPEC
    assert used == [yaml.CSafeLoader]


def test_yaml_falls_back_to_safe_loader_without_libyaml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delattr(yaml, "CSafeLoader", raising=False)
    used = _spy_yaml_load(monkeypatch)
    assert _wrapper(_write_yaml(tmp_path)).api_spec == SPEC
    assert used == [yaml.SafeLoader]


def test_yaml_loader_is_always_a_safe_loader(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    used = _spy_yaml_load(monkeypatch)
    _wrapper(_write_yaml(tmp_path))
    allowed = {yaml.SafeLoader, getattr(yaml, "CSafeLoader", yaml.SafeLoader)}
    assert used
    assert set(used) <= allowed


def test_both_loaders_give_the_same_dict() -> None:
    text = yaml.safe_dump(SPEC)
    safe = yaml.load(text, Loader=yaml.SafeLoader)
    c_loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    fast = yaml.load(text, Loader=c_loader)
    assert safe == fast == SPEC
