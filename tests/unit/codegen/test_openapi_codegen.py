"""Tests for openapi_codegen endpoint deduplication."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.codegen.adapters import ParsedEndpoint, ParsedField
from tools.codegen.openapi_codegen import _deduplicate_endpoints, run


def _make_ep(path: str, field_count: int) -> ParsedEndpoint:
    """Build a minimal ParsedEndpoint with N scalar fields."""
    fields = [
        ParsedField(name=f"field_{i}", api_path=f"field_{i}", python_type="str")
        for i in range(field_count)
    ]
    return ParsedEndpoint(path=path, schema_name="test", fields=fields)


class TestDeduplicateEndpoints:
    def test_no_duplicates_passthrough(self) -> None:
        eps = [_make_ep("/storage/volumes", 10), _make_ep("/network/interfaces", 5)]
        result = _deduplicate_endpoints(eps)
        assert len(result) == 2

    def test_keeps_richest_endpoint(self) -> None:
        """When /storage/volumes (10 fields) and /storage/volumes/{uuid} (2 fields)
        collide, keep the one with more fields."""
        collection = _make_ep("/storage/volumes", 10)
        instance = _make_ep("/storage/volumes/{uuid}", 2)
        result = _deduplicate_endpoints([collection, instance])
        assert len(result) == 1
        assert result[0].path == "/storage/volumes"

    def test_keeps_richest_reversed_order(self) -> None:
        """Order shouldn't matter — richest endpoint wins."""
        collection = _make_ep("/storage/volumes", 10)
        instance = _make_ep("/storage/volumes/{uuid}", 2)
        result = _deduplicate_endpoints([instance, collection])
        assert len(result) == 1
        assert result[0].path == "/storage/volumes"

    def test_preserves_order_of_winners(self) -> None:
        """Winner position in the output should match its first appearance in input."""
        ep1 = _make_ep("/storage/volumes", 10)
        ep2 = _make_ep("/network/interfaces", 5)
        ep3 = _make_ep("/storage/volumes/{uuid}", 2)
        result = _deduplicate_endpoints([ep1, ep2, ep3])
        assert len(result) == 2
        assert result[0].path == "/storage/volumes"
        assert result[1].path == "/network/interfaces"

    def test_equal_leaves_envelope_beats_singleton(self) -> None:
        """On equal leaf counts the collection (envelope) wins in both orders (#925)."""
        collection = _make_ep("/storage/snaplock/litigations", 5)
        item = _make_ep("/storage/snaplock/litigations/{id}", 5)
        item.response_shape = "singleton"
        for order in ([collection, item], [item, collection]):
            result = _deduplicate_endpoints(order)
            assert len(result) == 1
            assert result[0].path == "/storage/snaplock/litigations"

    def test_envelope_beats_singleton_with_more_leaves(self) -> None:
        """Shape ranks before leaf count: the collection wins in both orders (#934)."""
        collection = _make_ep("/storage/snaplock/litigations", 5)
        item = _make_ep("/storage/snaplock/litigations/{id}", 6)
        item.response_shape = "singleton"
        for order in ([collection, item], [item, collection]):
            result = _deduplicate_endpoints(order)
            assert len(result) == 1
            assert result[0].path == "/storage/snaplock/litigations"

    def test_same_shape_singletons_most_leaves_wins(self) -> None:
        """Within one shape the endpoint with the most leaf fields wins."""
        few = _make_ep("/some/thing", 3)
        many = _make_ep("/some/thing/{id}", 6)
        few.response_shape = "singleton"
        many.response_shape = "singleton"
        for order in ([few, many], [many, few]):
            result = _deduplicate_endpoints(order)
            assert len(result) == 1
            assert result[0].path == "/some/thing/{id}"

    def test_empty_input(self) -> None:
        assert _deduplicate_endpoints([]) == []

    def test_single_endpoint(self) -> None:
        ep = _make_ep("/storage/volumes", 5)
        result = _deduplicate_endpoints([ep])
        assert result == [ep]

    def test_object_fields_excluded_from_leaf_count(self) -> None:
        """Dedup uses _select_leaf_fields, so pure object containers don't inflate count."""
        # 3 leaf fields + 1 object container = 3 effective leaves
        fields_with_object = [
            ParsedField(name="uuid", api_path="uuid"),
            ParsedField(name="name", api_path="name"),
            ParsedField(name="svm", api_path="svm", is_object=True),
            ParsedField(name="svm_name", api_path="svm.name"),
        ]
        ep_with_obj = ParsedEndpoint(path="/storage/volumes", fields=fields_with_object)

        # 4 plain leaf fields
        ep_instance = _make_ep("/storage/volumes/{uuid}", 4)

        result = _deduplicate_endpoints([ep_with_obj, ep_instance])
        assert len(result) == 1
        # Instance has 4 leaves vs collection's 3 leaves
        assert result[0].path == "/storage/volumes/{uuid}"


def _get(schema: dict, *, envelope: bool) -> dict:
    body: dict = (
        {
            "type": "object",
            "properties": {"records": {"type": "array", "items": schema}},
        }
        if envelope
        else schema
    )
    return {"get": {"responses": {"200": {"content": {"application/json": {"schema": body}}}}}}


def _synthetic_spec(tmp_path: Path) -> Path:
    thing = {
        "type": "object",
        "properties": {"uuid": {"type": "string"}, "name": {"type": "string"}},
    }
    kid = {"type": "object", "properties": {"label": {"type": "string"}}}
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "T", "version": "1"},
        "paths": {
            "/things": _get(thing, envelope=True),
            "/things/{uuid}": _get(thing, envelope=False),
            "/things/{uuid}/kids": _get(kid, envelope=True),
            "/a/{x}/b/{y}/c": _get(kid, envelope=True),
            "/n/{svm.uuid}": _get(kid, envelope=False),
        },
        "components": {"schemas": {}},
    }
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    return path


def _mapping_sources(written: list[Path]) -> dict[str, str]:
    return {str(p): p.read_text() for p in written if p.name == "mapping.py"}


class TestRunFilterAndDrop:
    def test_filtered_child_keeps_parent_mapping(self, tmp_path: Path) -> None:
        """#952: --endpoints must not hide the parent from a child."""
        written = run(
            spec=_synthetic_spec(tmp_path),
            output=tmp_path / "out",
            api_type="ontap",
            endpoint_filter=["/things/{uuid}/kids"],
        )
        sources = _mapping_sources(written)
        assert len(sources) == 1
        (source,) = sources.values()
        assert 'parent_mapping="OntapThing"' in source

    def test_drops_unfetchable_ontap_endpoints(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        written = run(
            spec=_synthetic_spec(tmp_path),
            output=tmp_path / "out",
            api_type="ontap",
        )
        out = capsys.readouterr().out
        assert "skipped (unfillable placeholder): /a/{x}/b/{y}/c" in out
        assert "skipped (unfillable placeholder): /n/{svm.uuid}" in out
        joined = " ".join(str(p) for p in written)
        assert "/a/" not in joined
        assert "/n/" not in joined
        assert any("/things/" in str(p) for p in written)

    def test_filtering_on_dropped_endpoint_returns_nothing(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        written = run(
            spec=_synthetic_spec(tmp_path),
            output=tmp_path / "out",
            api_type="ontap",
            endpoint_filter=["/a/{x}/b/{y}/c"],
        )
        assert written == []
        assert "skipped (unfillable placeholder): /a/{x}/b/{y}/c" in capsys.readouterr().out

    def test_non_ontap_does_not_drop(self, tmp_path: Path) -> None:
        written = run(
            spec=_synthetic_spec(tmp_path),
            output=tmp_path / "out",
            api_type="dii",
            endpoint_filter=["/n/{svm.uuid}"],
        )
        assert written != []
