"""The generated CVO list models accept the shapes real agents return (#1095, #1093).

``tests/fixtures/console_models/cvo_working_environment_shapes.json`` holds the
measured path -> JSON-type tables of ``fields=*`` for the AWS HA, Azure HA and
Azure single-node lists. It carries no values, names or ids. Each test rebuilds
placeholder items from it, a ``rich`` one (every union takes its widest type)
and a ``lean`` one (every union takes its narrowest type, so nullable branches
stay ``None`` and lists stay empty), and validates them against the generated
``ResponseBody``.
"""

from __future__ import annotations

import importlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, ValidationError

from pynetappfoundry.cache.occm._working_environments import DEFAULT_FIELDS
from pynetappfoundry.clients.console.generated import ConsoleAgentOps

_FIXTURE = (
    Path(__file__).resolve().parents[3]
    / "fixtures"
    / "console_models"
    / "cvo_working_environment_shapes.json"
)
_DATA: dict[str, Any] = json.loads(_FIXTURE.read_text(encoding="utf-8"))
_LISTS: dict[str, dict[str, Any]] = _DATA["lists"]
_VOCABULARY = frozenset({"str", "int", "float", "bool", "null", "dict", "list", "list(empty)"})
_SEGMENT = re.compile(r"^(<tag-key>|[A-Za-z][A-Za-z0-9]*)(\[\])?$")
_TAG_KEY = "<tag-key>"
_PLACEHOLDERS: dict[str, Any] = {"str": "placeholder", "int": 1, "float": 1.5, "bool": True}
#: Narrowest to widest: ``lean`` takes the first member of a union, ``rich`` the last.
_RANK = ("null", "list(empty)", "int", "float", "bool", "str", "list", "dict")


@dataclass
class _Node:
    token: str | None = None
    fields: dict[str, _Node] = field(default_factory=dict)
    elem: _Node | None = None


def _tree(paths: dict[str, str]) -> _Node:
    root = _Node()
    for path, token in paths.items():
        node = root
        for segment in path.split("."):
            match = _SEGMENT.match(segment)
            assert match is not None, segment
            node = node.fields.setdefault(match.group(1), _Node())
            if match.group(2):
                node.elem = node.elem or _Node()
                node = node.elem
        node.token = token
    return root


def _pick(token: str | None, variant: str) -> str | None:
    if token is None:
        return None
    members = sorted(token.split("|"), key=_RANK.index)
    return members[0] if variant == "lean" else members[-1]


def _value(node: _Node, variant: str) -> Any:
    kind = _pick(node.token, variant)
    if kind is None:
        kind = "list" if node.elem is not None else "dict"
    if kind == "null":
        return None
    if kind == "list(empty)":
        return []
    if kind == "list":
        return [_value(node.elem, variant)] if node.elem is not None else []
    if kind == "dict":
        return {name: _value(child, variant) for name, child in node.fields.items()}
    return _PLACEHOLDERS[kind]


def _build(key: str, variant: str) -> dict[str, Any]:
    """Rebuild one ``fields=*`` item of the measured list ``key`` from the fixture."""
    root = _tree(_LISTS[key]["paths"])
    item: dict[str, Any] = {name: _value(child, variant) for name, child in root.fields.items()}
    for name, token in _DATA["default_paths"].items():
        item[name] = _PLACEHOLDERS[token]
    return item


def _model(key: str) -> type[BaseModel]:
    module = importlib.import_module(
        f"pynetappfoundry.models.console.cvo.{_LISTS[key]['module'].replace('-', '_')}"
    )
    model: type[BaseModel] = module.ResponseBody
    return model


def _op(key: str) -> str:
    return f"list_{key.replace('-', '_')}_working_environments"


def _errors(key: str, item: dict[str, Any]) -> list[str]:
    try:
        _model(key).model_validate(item)
    except ValidationError as exc:
        return [".".join(str(p) for p in e["loc"]) for e in exc.errors()]
    return []


_KEYS = list(_LISTS)
_CASES = [(key, variant) for key in _KEYS for variant in ("rich", "lean")]
_CASE_IDS = [f"{key}-{variant}" for key, variant in _CASES]


# --- fixture hygiene ---------------------------------------------------------------


def test_fixture_lists_and_counts() -> None:
    assert _KEYS == ["aws-ha", "azure-ha", "azure-vsa"]
    assert {key: _LISTS[key]["path_count"] for key in _KEYS} == {
        "aws-ha": 311,
        "azure-ha": 300,
        "azure-vsa": 303,
    }
    for key in _KEYS:
        assert len(_LISTS[key]["paths"]) == _LISTS[key]["path_count"]


def test_fixture_holds_only_paths_and_json_types() -> None:
    for key in _KEYS:
        for path, token in _LISTS[key]["paths"].items():
            assert all(_SEGMENT.match(segment) for segment in path.split(".")), path
            assert set(token.split("|")) <= _VOCABULARY, (path, token)


def test_default_paths_are_the_cache_default_fields() -> None:
    assert set(_DATA["default_paths"]) == set(DEFAULT_FIELDS)
    assert set(_DATA["default_paths"].values()) <= {"str", "bool"}


# --- the measured shapes validate -----------------------------------------------------


@pytest.mark.parametrize(("key", "variant"), _CASES, ids=_CASE_IDS)
def test_measured_item_validates(key: str, variant: str) -> None:
    errors = _errors(key, _build(key, variant))
    assert not errors, f"{len(errors)} validation errors at: {errors}"


@pytest.mark.parametrize(("key", "variant"), _CASES, ids=_CASE_IDS)
def test_op_returns_response_bodies_for_measured_items(key: str, variant: str) -> None:
    dispatch = MagicMock(return_value=[_build(key, variant)])
    result = getattr(ConsoleAgentOps(dispatch), _op(key))(fields="*")
    assert isinstance(result[0], _model(key))


# --- #1093: tags and availability zones -----------------------------------------------


def _dump(key: str, item: dict[str, Any]) -> dict[str, Any]:
    dumped: dict[str, Any] = _model(key).model_validate(item).model_dump(mode="json")
    return dumped


def test_aws_instance_tags_round_trip() -> None:
    dumped = _dump("aws-ha", _build("aws-ha", "rich"))
    assert dumped["awsProperties"]["instances"][0]["tags"] == {_TAG_KEY: "placeholder"}


@pytest.mark.parametrize("key", ["azure-ha", "azure-vsa"])
def test_azure_tags_round_trip(key: str) -> None:
    provider = _dump(key, _build(key, "rich"))["providerProperties"]
    assert provider["tags"] == {_TAG_KEY: "placeholder"}
    assert provider["resourceGroup"]["tags"] == {_TAG_KEY: "placeholder"}


def test_a_list_at_tags_is_rejected() -> None:
    item = _build("aws-ha", "rich")
    item["awsProperties"]["instances"][0]["tags"] = ["not-a-map"]
    assert _errors("aws-ha", item)


@pytest.mark.parametrize("key", ["azure-ha", "azure-vsa"])
@pytest.mark.parametrize("zone", ["zone-placeholder", None])
def test_azure_availability_zone_is_a_nullable_string(key: str, zone: str | None) -> None:
    item = _build(key, "rich")
    item["providerProperties"]["availabilityZone"] = zone
    item["haProperties"]["node1Info"]["availabilityZone"] = zone
    assert not _errors(key, item)
    dumped = _dump(key, item)
    assert dumped["providerProperties"]["availabilityZone"] == zone
    assert dumped["haProperties"]["node1Info"]["availabilityZone"] == zone


def test_azure_availability_zone_rejects_a_list() -> None:
    item = _build("azure-ha", "rich")
    item["haProperties"]["node1Info"]["availabilityZone"] = ["1"]
    assert _errors("azure-ha", item)


# --- the cron schedule lists are integers -----------------------------------------------


def test_aws_ha_cron_days_are_integers() -> None:
    item = _build("aws-ha", "rich")
    item["cronJobSchedules"][0]["days"] = [1]
    assert not _errors("aws-ha", item)
    item["cronJobSchedules"][0]["days"] = ["a"]
    assert _errors("aws-ha", item)
