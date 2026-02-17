"""Tests for openapi_codegen endpoint deduplication."""

from __future__ import annotations

from tools.codegen.adapters import ParsedEndpoint, ParsedField
from tools.codegen.openapi_codegen import _deduplicate_endpoints


def _make_ep(path: str, field_count: int) -> ParsedEndpoint:
    """Build a minimal ParsedEndpoint with N scalar fields."""
    fields = [
        ParsedField(name=f"field_{i}", api_path=f"field_{i}", python_type="str")
        for i in range(field_count)
    ]
    return ParsedEndpoint(path=path, schema_name="test", fields=fields)


class TestDeduplicateEndpoints:
    def test_no_duplicates_passthrough(self):
        eps = [_make_ep("/storage/volumes", 10), _make_ep("/network/interfaces", 5)]
        result = _deduplicate_endpoints(eps)
        assert len(result) == 2

    def test_keeps_richest_endpoint(self):
        """When /storage/volumes (10 fields) and /storage/volumes/{uuid} (2 fields)
        collide, keep the one with more fields."""
        collection = _make_ep("/storage/volumes", 10)
        instance = _make_ep("/storage/volumes/{uuid}", 2)
        result = _deduplicate_endpoints([collection, instance])
        assert len(result) == 1
        assert result[0].path == "/storage/volumes"

    def test_keeps_richest_reversed_order(self):
        """Order shouldn't matter — richest endpoint wins."""
        collection = _make_ep("/storage/volumes", 10)
        instance = _make_ep("/storage/volumes/{uuid}", 2)
        result = _deduplicate_endpoints([instance, collection])
        assert len(result) == 1
        assert result[0].path == "/storage/volumes"

    def test_preserves_order_of_winners(self):
        """Winner position in the output should match its first appearance in input."""
        ep1 = _make_ep("/storage/volumes", 10)
        ep2 = _make_ep("/network/interfaces", 5)
        ep3 = _make_ep("/storage/volumes/{uuid}", 2)
        result = _deduplicate_endpoints([ep1, ep2, ep3])
        assert len(result) == 2
        assert result[0].path == "/storage/volumes"
        assert result[1].path == "/network/interfaces"

    def test_empty_input(self):
        assert _deduplicate_endpoints([]) == []

    def test_single_endpoint(self):
        ep = _make_ep("/storage/volumes", 5)
        result = _deduplicate_endpoints([ep])
        assert result == [ep]

    def test_object_fields_excluded_from_leaf_count(self):
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
