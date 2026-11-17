"""Tests for the hand-written spec fragments and their offline merge (#1078)."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from tools.console_openapi import cli as cli_module
from tools.console_openapi.fragments import (
    FRAGMENTS_DIR,
    FragmentError,
    load_fragments,
    merge_fragments,
    strip_fragments,
)
from tools.console_openapi.models import ParsedEndpoint
from tools.console_openapi.openapi.builder import (
    _OPERATION_SERVERS,
    BuildError,
    _enforce_invariants,
    build_spec,
)
from tools.console_openapi.parser.endpoint import parse_endpoint

_ROOT = Path(__file__).resolve().parents[3]
_SPEC_PATH = _ROOT / "tools/console_openapi/generated/console_openapi.yaml"
_FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "console_openapi"
_LIST_PATH = "/agents-mgmt/list-connectors/{organization_id}"
_AGENT_PATH = "/agents-mgmt/agent/{agent_id}"


def _base_spec() -> dict[str, Any]:
    return {
        "openapi": "3.0.3",
        "info": {"title": "t", "version": "1"},
        "paths": {},
        "components": {"schemas": {}},
    }


def _fragment(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "x-namespace": "ns",
        "paths": {
            "/ns/{item_id}": {
                "get": {
                    "operationId": "ns_get_item",
                    "x-evidence": "live",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "ok",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ns.get-item.ResponseBody"
                                    }
                                }
                            },
                        }
                    },
                }
            }
        },
        "components": {"schemas": {"ns.get-item.ResponseBody": {"type": "object"}}},
    }
    data.update(overrides)
    return data


def test_the_real_fragment_loads_with_live_evidence() -> None:
    ((name, fragment),) = load_fragments()

    assert name == "agents_mgmt.yaml"
    assert fragment["x-namespace"] == "agentsmgmt"
    assert set(fragment["paths"]) == {_LIST_PATH, _AGENT_PATH}
    for item in fragment["paths"].values():
        op = item["get"]
        assert op["x-evidence"] == "live"
        assert op["servers"] == list(_OPERATION_SERVERS)
        assert "x-token-type" not in op
        (param,) = op["parameters"]
        assert param["in"] == "path"
        assert param["required"] is True


def test_merge_adds_paths_and_schemas_and_records_them() -> None:
    spec = _base_spec()

    merge_fragments(spec, [("f.yaml", _fragment())])

    assert "/ns/{item_id}" in spec["paths"]
    assert "ns.get-item.ResponseBody" in spec["components"]["schemas"]
    assert spec["info"]["x-fragments"] == {
        "f.yaml": {"paths": ["/ns/{item_id}"], "schemas": ["ns.get-item.ResponseBody"]}
    }
    _enforce_invariants(spec)


def test_merge_copies_the_fragment() -> None:
    spec = _base_spec()
    fragment = _fragment()

    merge_fragments(spec, [("f.yaml", fragment)])
    spec["paths"]["/ns/{item_id}"]["get"]["operationId"] = "changed"

    assert fragment["paths"]["/ns/{item_id}"]["get"]["operationId"] == "ns_get_item"


def test_merge_without_fragments_leaves_the_spec_alone() -> None:
    spec = _base_spec()
    merge_fragments(spec, [])
    assert "x-fragments" not in spec["info"]


def test_strip_removes_exactly_what_was_merged() -> None:
    spec = _base_spec()
    spec["paths"]["/docs"] = {"get": {}}
    spec["components"]["schemas"]["docs.X"] = {}
    before = copy.deepcopy(spec)
    merge_fragments(spec, [("f.yaml", _fragment())])

    strip_fragments(spec)

    assert spec == before


def test_merge_rejects_an_existing_path() -> None:
    spec = _base_spec()
    spec["paths"]["/ns/{item_id}"] = {}
    with pytest.raises(FragmentError, match="already exists"):
        merge_fragments(spec, [("f.yaml", _fragment())])


def test_merge_rejects_a_schema_outside_the_namespace() -> None:
    fragment = _fragment(components={"schemas": {"other.X": {}}})
    with pytest.raises(FragmentError, match="outside the namespace"):
        merge_fragments(_base_spec(), [("f.yaml", fragment)])


def test_merge_rejects_a_duplicate_schema() -> None:
    spec = _base_spec()
    spec["components"]["schemas"]["ns.get-item.ResponseBody"] = {}
    with pytest.raises(FragmentError, match="already exists"):
        merge_fragments(spec, [("f.yaml", _fragment())])


def test_merge_rejects_a_missing_namespace() -> None:
    fragment = _fragment()
    del fragment["x-namespace"]
    with pytest.raises(FragmentError, match="x-namespace"):
        merge_fragments(_base_spec(), [("f.yaml", fragment)])


@pytest.mark.parametrize("evidence", [None, "swagger"])
def test_merge_requires_live_evidence(evidence: str | None) -> None:
    fragment = _fragment()
    op = fragment["paths"]["/ns/{item_id}"]["get"]
    if evidence is None:
        del op["x-evidence"]
    else:
        op["x-evidence"] = evidence
    with pytest.raises(FragmentError, match="x-evidence"):
        merge_fragments(_base_spec(), [("f.yaml", fragment)])


def test_a_fragment_error_is_a_build_error() -> None:
    assert issubclass(FragmentError, BuildError)


def test_committed_spec_matches_the_fragments() -> None:
    """Offline drift guard: strip then merge reproduces the committed spec byte for byte."""
    text = _SPEC_PATH.read_text(encoding="utf-8")
    spec = yaml.safe_load(text)

    strip_fragments(spec)
    merge_fragments(spec, load_fragments(FRAGMENTS_DIR))

    assert yaml.safe_dump(spec, sort_keys=False) == text


def test_apply_fragments_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "spec.yaml"
    target.write_text(_SPEC_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    before = target.read_text(encoding="utf-8")

    for _ in range(2):
        result = CliRunner().invoke(cli_module.cli, ["apply-fragments", "--spec", str(target)])
        assert result.exit_code == 0, result.output
        assert target.read_text(encoding="utf-8") == before


def test_apply_fragments_picks_up_a_new_fragment(tmp_path: Path) -> None:
    target = tmp_path / "spec.yaml"
    target.write_text(_SPEC_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    frag_dir = tmp_path / "frags"
    frag_dir.mkdir()
    (frag_dir / "extra.yaml").write_text(
        yaml.safe_dump(
            _fragment(
                components={"schemas": {"ns.get-item.ResponseBody": {"type": "object"}}},
            )
        ),
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        cli_module.cli,
        ["apply-fragments", "--spec", str(target), "--fragments-dir", str(frag_dir)],
    )

    assert result.exit_code == 0, result.output
    spec = yaml.safe_load(target.read_text(encoding="utf-8"))
    assert "/ns/{item_id}" in spec["paths"]
    assert _LIST_PATH not in spec["paths"]


def _cvo_endpoint() -> ParsedEndpoint:
    text = (_FIXTURES / "cvo_status_default.adoc").read_text(encoding="utf-8")
    endpoint = parse_endpoint(text, source_file="fixtures/cvo_status_default.adoc", service="cvo")
    assert endpoint is not None
    return endpoint


def test_build_spec_places_fragment_paths_after_the_docs_paths() -> None:
    endpoint = _cvo_endpoint()

    spec = build_spec([endpoint], included_services=("cvo",), fragments=[("f.yaml", _fragment())])

    paths = list(spec["paths"])
    assert paths[-1] == "/ns/{item_id}"
    assert len(paths) > 1
    assert "f.yaml" in spec["info"]["x-fragments"]


def test_build_spec_without_fragments_has_no_record() -> None:
    endpoint = _cvo_endpoint()

    assert "x-fragments" not in build_spec([endpoint], included_services=("cvo",))["info"]
