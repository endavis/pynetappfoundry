"""Tests for the hand-written spec overrides and their offline re-application (#1095)."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from tools.console_openapi import cli as cli_module
from tools.console_openapi.openapi.builder import BuildError, build_spec
from tools.console_openapi.overrides import (
    OVERRIDES_PATH,
    Override,
    OverrideError,
    apply_overrides,
    load_overrides,
    strip_overrides,
)
from tools.console_openapi.parser.endpoint import parse_endpoint

_ROOT = Path(__file__).resolve().parents[3]
_SPEC_PATH = _ROOT / "tools/console_openapi/generated/console_openapi.yaml"
_FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "console_openapi"
_MAP = {"type": "object", "additionalProperties": {"type": "string"}}


def _spec() -> dict[str, Any]:
    return {
        "openapi": "3.0.3",
        "info": {"title": "t", "version": "1"},
        "paths": {},
        "components": {
            "schemas": {
                "a.Cron": {
                    "x-source-file": "a.adoc",
                    "title": "Cron",
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "days of the month",
                        },
                        "months": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "a.tags": {
                    "x-source-file": "a.adoc",
                    "x-source-anchor": "tags",
                    "title": "tags",
                    "type": "object",
                    "description": "the tags",
                },
            }
        },
    }


def _property_override(**changes: Any) -> Override:
    fields: dict[str, Any] = {
        "schema": "a.Cron",
        "property": "days",
        "replace": {"type": "array", "items": {"type": "integer"}},
        "evidence": "live",
        "reason": "measured",
    }
    fields.update(changes)
    return Override(**fields)


def _schema_override(**changes: Any) -> Override:
    return _property_override(schema="a.tags", property=None, replace=dict(_MAP), **changes)


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "overrides.yaml"
    path.write_text(text, encoding="utf-8")
    return path


_ENTRY = """\
overrides:
  - schemas: [a.Cron, b.Cron]
    properties: [days, hours]
    evidence: live
    reason: measured
    replace: {type: integer}
"""


# --- loading ---------------------------------------------------------------------------


def test_load_expands_schemas_times_properties(tmp_path: Path) -> None:
    loaded = load_overrides(_write(tmp_path, _ENTRY))

    assert [(o.schema, o.property) for o in loaded] == [
        ("a.Cron", "days"),
        ("a.Cron", "hours"),
        ("b.Cron", "days"),
        ("b.Cron", "hours"),
    ]
    assert {o.evidence for o in loaded} == {"live"}
    assert loaded[0].replace == {"type": "integer"}
    assert loaded[0].replace is not loaded[1].replace


def test_load_a_schema_override_has_no_property(tmp_path: Path) -> None:
    text = (
        "overrides:\n  - {schemas: [a.tags], evidence: inferred, reason: r, replace: {type: x}}\n"
    )
    (loaded,) = load_overrides(_write(tmp_path, text))
    assert loaded.property is None
    assert loaded.target == "a.tags"


def test_load_rejects_an_unknown_key(tmp_path: Path) -> None:
    with pytest.raises(OverrideError, match="unknown key"):
        load_overrides(_write(tmp_path, _ENTRY + "    extra: 1\n"))


@pytest.mark.parametrize("evidence", [None, "guess", "Live"])
def test_load_rejects_bad_evidence(tmp_path: Path, evidence: str | None) -> None:
    line = "" if evidence is None else f"    evidence: {evidence}\n"
    text = _ENTRY.replace("    evidence: live\n", line)
    with pytest.raises(OverrideError, match="evidence"):
        load_overrides(_write(tmp_path, text))


@pytest.mark.parametrize("reason_line", ["", "    reason: ''\n", "    reason: '  '\n"])
def test_load_rejects_an_empty_reason(tmp_path: Path, reason_line: str) -> None:
    text = _ENTRY.replace("    reason: measured\n", reason_line)
    with pytest.raises(OverrideError, match="reason"):
        load_overrides(_write(tmp_path, text))


@pytest.mark.parametrize("replace", ["", "replace: {}", "replace: [1]", "replace: text"])
def test_load_rejects_an_empty_or_non_mapping_replace(tmp_path: Path, replace: str) -> None:
    text = _ENTRY.replace("replace: {type: integer}", replace)
    with pytest.raises(OverrideError, match="replace"):
        load_overrides(_write(tmp_path, text))


def test_load_rejects_a_duplicate_target(tmp_path: Path) -> None:
    text = _ENTRY + _ENTRY.split("overrides:\n")[1]
    with pytest.raises(OverrideError, match="twice"):
        load_overrides(_write(tmp_path, text))


def test_load_rejects_a_file_without_an_overrides_list(tmp_path: Path) -> None:
    with pytest.raises(OverrideError, match="overrides"):
        load_overrides(_write(tmp_path, "- a\n"))


def test_an_override_error_is_a_build_error() -> None:
    assert issubclass(OverrideError, BuildError)


def test_the_real_overrides_file_loads() -> None:
    loaded = load_overrides(OVERRIDES_PATH)
    assert loaded
    assert {o.evidence for o in loaded} == {"live", "inferred"}
    assert all(o.reason for o in loaded)


# --- applying --------------------------------------------------------------------------


def test_apply_a_property_override_keeps_the_description_and_records_the_original() -> None:
    spec = _spec()
    original = copy.deepcopy(spec["components"]["schemas"]["a.Cron"]["properties"]["days"])

    apply_overrides(spec, [_property_override()])

    days = spec["components"]["schemas"]["a.Cron"]["properties"]["days"]
    assert days["items"] == {"type": "integer"}
    assert days["description"] == "days of the month"
    assert days["x-override"] == {"evidence": "live", "reason": "measured", "original": original}
    assert spec["components"]["schemas"]["a.Cron"]["properties"]["months"]["items"] == {
        "type": "string"
    }


def test_apply_a_property_override_may_replace_the_description() -> None:
    spec = _spec()
    override = _property_override(replace={"type": "string", "description": "new"})
    apply_overrides(spec, [override])
    assert spec["components"]["schemas"]["a.Cron"]["properties"]["days"]["description"] == "new"


def test_apply_a_schema_override_keeps_source_title_and_description() -> None:
    spec = _spec()
    original = copy.deepcopy(spec["components"]["schemas"]["a.tags"])

    apply_overrides(spec, [_schema_override()])

    tags = spec["components"]["schemas"]["a.tags"]
    assert tags["x-source-file"] == "a.adoc"
    assert tags["x-source-anchor"] == "tags"
    assert tags["title"] == "tags"
    assert tags["description"] == "the tags"
    assert tags["additionalProperties"] == {"type": "string"}
    assert tags["type"] == "object"
    assert tags["x-override"]["original"] == original


def test_apply_rejects_an_unknown_schema() -> None:
    with pytest.raises(OverrideError, match="no such schema"):
        apply_overrides(_spec(), [_property_override(schema="a.Missing")])


def test_apply_rejects_an_unknown_property() -> None:
    with pytest.raises(OverrideError, match="no such property"):
        apply_overrides(_spec(), [_property_override(property="missing")])


def test_apply_rejects_a_property_of_a_schema_without_properties() -> None:
    with pytest.raises(OverrideError, match="no such property"):
        apply_overrides(_spec(), [_property_override(schema="a.tags")])


def test_apply_rejects_a_fragment_target() -> None:
    spec = _spec()
    spec["info"]["x-fragments"] = {"f.yaml": {"paths": [], "schemas": ["a.tags"]}}
    with pytest.raises(OverrideError, match="fragment"):
        apply_overrides(spec, [_schema_override()])


@pytest.mark.parametrize("make", [_property_override, _schema_override])
def test_apply_twice_without_a_strip_is_rejected(make: Any) -> None:
    spec = _spec()
    apply_overrides(spec, [make()])
    with pytest.raises(OverrideError, match="already overridden"):
        apply_overrides(spec, [make()])


def test_apply_with_no_overrides_changes_nothing() -> None:
    spec = _spec()
    apply_overrides(spec, [])
    assert spec == _spec()


def test_strip_restores_the_original() -> None:
    spec = _spec()
    apply_overrides(spec, [_property_override(), _schema_override()])

    strip_overrides(spec)

    assert spec == _spec()


def test_strip_without_overrides_changes_nothing() -> None:
    spec = _spec()
    strip_overrides(spec)
    assert spec == _spec()


# --- build_spec ------------------------------------------------------------------------


def _fixture_endpoint() -> Any:
    text = (_FIXTURES / "prose_and_hash_definitions.adoc").read_text(encoding="utf-8")
    ep = parse_endpoint(text, source_file="fixtures/prose_and_hash_definitions.adoc", service="f")
    assert ep is not None
    return ep


def test_build_spec_applies_overrides_after_the_fragments() -> None:
    ep = _fixture_endpoint()
    plain = build_spec([ep], included_services=("f",))
    key = next(k for k in plain["components"]["schemas"] if k.endswith(".targetSchema"))
    fragment = {
        "x-namespace": "ns",
        "components": {"schemas": {"ns.Frag": {"type": "object"}}},
    }
    override = Override(key, None, dict(_MAP), "inferred", "r")

    spec = build_spec(
        [ep], included_services=("f",), fragments=[("f.yaml", fragment)], overrides=[override]
    )

    assert spec["components"]["schemas"][key]["additionalProperties"] == {"type": "string"}
    assert spec["components"]["schemas"][key]["x-override"]["evidence"] == "inferred"
    assert "ns.Frag" in spec["components"]["schemas"]


def test_build_spec_without_overrides_has_no_override_nodes() -> None:
    spec = build_spec([_fixture_endpoint()], included_services=("f",))
    assert "x-override" not in yaml.safe_dump(spec)


def test_build_spec_rejects_an_override_of_a_fragment_schema() -> None:
    fragment = {"x-namespace": "ns", "components": {"schemas": {"ns.Frag": {"type": "object"}}}}
    override = Override("ns.Frag", None, {"type": "string"}, "live", "r")
    with pytest.raises(OverrideError, match="fragment"):
        build_spec(
            [_fixture_endpoint()],
            included_services=("f",),
            fragments=[("f.yaml", fragment)],
            overrides=[override],
        )


# --- the committed spec ----------------------------------------------------------------


def test_committed_spec_matches_the_overrides() -> None:
    """Offline drift guard: strip then apply reproduces the committed spec byte for byte."""
    text = _SPEC_PATH.read_text(encoding="utf-8")
    spec = yaml.safe_load(text)

    strip_overrides(spec)
    apply_overrides(spec, load_overrides(OVERRIDES_PATH))

    assert yaml.safe_dump(spec, sort_keys=False) == text


def test_every_override_target_in_the_committed_spec_is_marked() -> None:
    schemas = yaml.safe_load(_SPEC_PATH.read_text(encoding="utf-8"))["components"]["schemas"]
    for o in load_overrides(OVERRIDES_PATH):
        node = (
            schemas[o.schema] if o.property is None else schemas[o.schema]["properties"][o.property]
        )
        assert node["x-override"]["evidence"] == o.evidence, o.target
        assert node["x-override"]["reason"] == o.reason, o.target


def test_no_prose_anchor_is_typed_in_the_committed_spec() -> None:
    schemas = yaml.safe_load(_SPEC_PATH.read_text(encoding="utf-8"))["components"]["schemas"]
    untyped = [k for k, v in schemas.items() if "type" not in v and "$ref" not in v]
    assert len(untyped) > 700
    assert all("properties" not in schemas[k] for k in untyped)


def test_apply_fragments_cli_is_idempotent_with_overrides(tmp_path: Path) -> None:
    target = tmp_path / "spec.yaml"
    target.write_text(_SPEC_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    before = target.read_text(encoding="utf-8")

    for _ in range(2):
        result = CliRunner().invoke(cli_module.cli, ["apply-fragments", "--spec", str(target)])
        assert result.exit_code == 0, result.output
        assert target.read_text(encoding="utf-8") == before
