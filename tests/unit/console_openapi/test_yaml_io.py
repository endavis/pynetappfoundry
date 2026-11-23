"""Tests for the libyaml-aware YAML helpers and the shared spec fixtures (#1148)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from tools.console_openapi.yaml_io import dump_yaml, load_yaml

_SAMPLE: dict[str, Any] = {
    "zeta": {"$ref": "#/components/schemas/A", "n": 1},
    "alpha": ["x", "y", {"k": None}],
    "text": ("long words " * 40).strip(),
    "accent": "café",
    "flag": True,
}


def _no_libyaml(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delattr(yaml, "CSafeLoader", raising=False)
    monkeypatch.delattr(yaml, "CSafeDumper", raising=False)


def test_load_yaml_text_matches_safe_load() -> None:
    text = yaml.safe_dump(_SAMPLE, sort_keys=False)
    assert load_yaml(text) == yaml.safe_load(text) == _SAMPLE


def test_load_yaml_open_file_matches_safe_load(tmp_path: Path) -> None:
    path = tmp_path / "s.yaml"
    path.write_text(yaml.safe_dump(_SAMPLE, sort_keys=False), encoding="utf-8")
    with path.open(encoding="utf-8") as f:
        assert load_yaml(f) == _SAMPLE


def test_dump_yaml_matches_safe_dump_and_keeps_key_order() -> None:
    out = dump_yaml(_SAMPLE)
    assert out == yaml.safe_dump(_SAMPLE, sort_keys=False)
    assert list(load_yaml(out)) == ["zeta", "alpha", "text", "accent", "flag"]


def test_dump_yaml_matches_safe_dump_on_long_non_ascii_text() -> None:
    # CSafeDumper wraps this scalar differently from SafeDumper (#1148); dump_yaml must not use it.
    data = {"description": "r\u00e9sum\u00e9 " * 40}
    assert dump_yaml(data) == yaml.safe_dump(data, sort_keys=False)


def test_helpers_fall_back_without_libyaml(monkeypatch: pytest.MonkeyPatch) -> None:
    _no_libyaml(monkeypatch)
    out = dump_yaml(_SAMPLE)
    assert out == yaml.safe_dump(_SAMPLE, sort_keys=False)
    assert load_yaml(out) == _SAMPLE


def test_load_yaml_stays_a_safe_loader() -> None:
    with pytest.raises(yaml.constructor.ConstructorError):
        load_yaml("!!python/object/apply:os.system ['true']")


def test_load_yaml_stays_safe_without_libyaml(monkeypatch: pytest.MonkeyPatch) -> None:
    _no_libyaml(monkeypatch)
    with pytest.raises(yaml.constructor.ConstructorError):
        load_yaml("!!python/object/apply:os.system ['true']")


def test_committed_spec_fixture_is_a_private_copy(
    request: pytest.FixtureRequest, committed_spec: dict[str, Any]
) -> None:
    shared: dict[str, Any] = request.getfixturevalue("_committed_spec_parsed")
    paths_before = len(shared["paths"])
    committed_spec["paths"].clear()
    assert len(shared["paths"]) == paths_before > 0
