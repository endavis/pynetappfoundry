"""Tests for dict_path utility module."""

from __future__ import annotations

import pytest

from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value


class TestGetNestedValue:
    """Tests for get_nested_value function."""

    def test_simple_field_access(self) -> None:
        """Test accessing a simple top-level field."""
        data = {"name": "test-cluster"}
        assert get_nested_value(data, "name") == "test-cluster"

    def test_nested_field_access(self) -> None:
        """Test accessing nested fields with dot notation."""
        data = {"cloud": {"instance_type": "m5.xlarge"}}
        assert get_nested_value(data, "cloud.instance_type") == "m5.xlarge"

    def test_deeply_nested_access(self) -> None:
        """Test accessing deeply nested fields."""
        data = {"a": {"b": {"c": {"d": "value"}}}}
        assert get_nested_value(data, "a.b.c.d") == "value"

    def test_array_index_access(self) -> None:
        """Test accessing array elements by index."""
        data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}]}
        assert get_nested_value(data, "nodes[0].name") == "node-01"
        assert get_nested_value(data, "nodes[1].name") == "node-02"

    def test_array_index_only(self) -> None:
        """Test accessing array element directly."""
        data = {"items": ["first", "second", "third"]}
        assert get_nested_value(data, "items[0]") == "first"
        assert get_nested_value(data, "items[2]") == "third"

    def test_array_of_dicts(self) -> None:
        """Test accessing complex nested array structures."""
        data = {
            "cluster": {
                "nodes": [
                    {"name": "node-01", "status": "healthy"},
                    {"name": "node-02", "status": "warning"},
                ]
            }
        }
        assert get_nested_value(data, "cluster.nodes[0].name") == "node-01"
        assert get_nested_value(data, "cluster.nodes[1].status") == "warning"

    def test_returns_various_types(self) -> None:
        """Test returning various value types."""
        data = {
            "string": "text",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }
        assert get_nested_value(data, "string") == "text"
        assert get_nested_value(data, "number") == 42
        assert get_nested_value(data, "float") == 3.14
        assert get_nested_value(data, "boolean") is True
        assert get_nested_value(data, "null") is None
        assert get_nested_value(data, "list") == [1, 2, 3]
        assert get_nested_value(data, "dict") == {"nested": "value"}


class TestPathNotFoundError:
    """Tests for PathNotFoundError exception."""

    def test_missing_field_error(self) -> None:
        """Test error when field doesn't exist."""
        data = {"name": "test"}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "missing")
        assert exc_info.value.path == "missing"
        assert exc_info.value.position == "missing"
        assert "key not found" in exc_info.value.reason

    def test_missing_nested_field_error(self) -> None:
        """Test error when nested field doesn't exist."""
        data = {"cloud": {"provider": "AWS"}}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "cloud.missing")
        assert exc_info.value.path == "cloud.missing"
        assert exc_info.value.position == "cloud.missing"
        assert "key not found" in exc_info.value.reason

    def test_index_out_of_range_error(self) -> None:
        """Test error when array index is out of range."""
        data = {"nodes": [{"name": "node-01"}]}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "nodes[5]")
        assert exc_info.value.path == "nodes[5]"
        assert "index 5 out of range" in exc_info.value.reason
        assert "list has 1 items" in exc_info.value.reason

    def test_non_dict_access_error(self) -> None:
        """Test error when trying to access field on non-dict."""
        data = {"name": "test"}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "name.sub")
        assert exc_info.value.path == "name.sub"
        assert "expected dict" in exc_info.value.reason
        assert "got str" in exc_info.value.reason

    def test_non_list_index_access_error(self) -> None:
        """Test error when trying array access on non-list."""
        data = {"cloud": {"provider": "AWS"}}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "cloud.provider[0]")
        assert exc_info.value.path == "cloud.provider[0]"
        assert "expected list for index access" in exc_info.value.reason

    def test_empty_path_error(self) -> None:
        """Test error when path is empty."""
        data = {"name": "test"}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "")
        assert "empty path" in exc_info.value.reason

    def test_empty_segment_error(self) -> None:
        """Test error when path has empty segment."""
        data = {"a": {"b": "value"}}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "a..b")
        assert "empty path segment" in exc_info.value.reason

    def test_error_message_format(self) -> None:
        """Test that error message contains useful information."""
        data = {"cloud": {"provider": "AWS"}}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "cloud.missing_field")
        error = exc_info.value
        error_str = str(error)
        assert "cloud.missing_field" in error_str
        assert "not found" in error_str

    def test_exception_attributes(self) -> None:
        """Test PathNotFoundError has correct attributes."""
        error = PathNotFoundError(
            path="a.b.c",
            position="a.b",
            reason="key not found",
        )
        assert error.path == "a.b.c"
        assert error.position == "a.b"
        assert error.reason == "key not found"


class TestWildcardArrayAccess:
    """Tests for wildcard array access [*] syntax."""

    def test_wildcard_simple_field(self) -> None:
        """Test wildcard access to get field from all array items."""
        data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}, {"name": "node-03"}]}
        assert get_nested_value(data, "nodes[*].name") == ["node-01", "node-02", "node-03"]

    def test_wildcard_nested_path(self) -> None:
        """Test wildcard access with nested paths after the wildcard."""
        data = {
            "clusters": [
                {"info": {"name": "cluster-1", "status": "healthy"}},
                {"info": {"name": "cluster-2", "status": "warning"}},
            ]
        }
        assert get_nested_value(data, "clusters[*].info.name") == ["cluster-1", "cluster-2"]
        assert get_nested_value(data, "clusters[*].info.status") == ["healthy", "warning"]

    def test_wildcard_no_remaining_path(self) -> None:
        """Test wildcard without remaining path returns all items."""
        data = {"items": ["a", "b", "c"]}
        assert get_nested_value(data, "items[*]") == ["a", "b", "c"]

    def test_wildcard_with_nested_prefix(self) -> None:
        """Test wildcard with nested path before the array."""
        data = {
            "cluster": {
                "nodes": [
                    {"name": "node-01", "cpus": 4},
                    {"name": "node-02", "cpus": 8},
                ]
            }
        }
        assert get_nested_value(data, "cluster.nodes[*].name") == ["node-01", "node-02"]
        assert get_nested_value(data, "cluster.nodes[*].cpus") == [4, 8]

    def test_wildcard_empty_array(self) -> None:
        """Test wildcard on empty array returns empty list."""
        data = {"nodes": []}
        assert get_nested_value(data, "nodes[*].name") == []
        assert get_nested_value(data, "nodes[*]") == []

    def test_wildcard_single_item(self) -> None:
        """Test wildcard on single-item array."""
        data = {"nodes": [{"name": "only-node"}]}
        assert get_nested_value(data, "nodes[*].name") == ["only-node"]

    def test_wildcard_on_non_list_error(self) -> None:
        """Test error when using wildcard on non-list value."""
        data = {"config": {"name": "test"}}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "config[*].name")
        assert "expected list for wildcard access" in exc_info.value.reason

    def test_wildcard_missing_key_error(self) -> None:
        """Test error when wildcard key doesn't exist."""
        data = {"nodes": [{"name": "node-01"}]}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "missing[*].name")
        assert "key not found" in exc_info.value.reason

    def test_wildcard_nested_field_missing_error(self) -> None:
        """Test error when nested field after wildcard doesn't exist."""
        data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}]}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "nodes[*].missing")
        assert "key not found" in exc_info.value.reason

    def test_wildcard_on_primitive_array_with_path_error(self) -> None:
        """Test error when using path after wildcard on primitive array."""
        data = {"items": ["a", "b", "c"]}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "items[*].name")
        assert "expected dict for nested access" in exc_info.value.reason

    def test_wildcard_complex_nested_objects(self) -> None:
        """Test wildcard with complex nested structures."""
        data = {
            "relationships": {
                "cluster_peers": [
                    {"name": "peer-1", "state": "available"},
                    {"name": "peer-2", "state": "unavailable"},
                    {"name": "peer-3", "state": "available"},
                ]
            }
        }
        assert get_nested_value(data, "relationships.cluster_peers[*].name") == [
            "peer-1",
            "peer-2",
            "peer-3",
        ]
        assert get_nested_value(data, "relationships.cluster_peers[*].state") == [
            "available",
            "unavailable",
            "available",
        ]


class TestEdgeCases:
    """Tests for edge cases."""

    def test_key_with_underscores(self) -> None:
        """Test keys containing underscores."""
        data = {"instance_type": "m5.xlarge", "is_ha": True}
        assert get_nested_value(data, "instance_type") == "m5.xlarge"
        assert get_nested_value(data, "is_ha") is True

    def test_key_with_numbers(self) -> None:
        """Test keys containing numbers."""
        data = {"node1": {"name": "first"}, "node2": {"name": "second"}}
        assert get_nested_value(data, "node1.name") == "first"
        assert get_nested_value(data, "node2.name") == "second"

    def test_empty_list(self) -> None:
        """Test accessing index on empty list."""
        data = {"items": []}
        with pytest.raises(PathNotFoundError) as exc_info:
            get_nested_value(data, "items[0]")
        assert "index 0 out of range" in exc_info.value.reason
        assert "list has 0 items" in exc_info.value.reason

    def test_empty_dict(self) -> None:
        """Test accessing key on empty dict."""
        data: dict[str, object] = {"nested": {}}
        with pytest.raises(PathNotFoundError):
            get_nested_value(data, "nested.key")

    def test_zero_index(self) -> None:
        """Test accessing index 0."""
        data = {"items": ["zero", "one", "two"]}
        assert get_nested_value(data, "items[0]") == "zero"

    def test_nested_list_in_list(self) -> None:
        """Test nested arrays (arrays within arrays)."""
        data = {"matrix": [[1, 2], [3, 4]]}
        # First access gets [1, 2], but we can't do [0][1] in dot notation
        result = get_nested_value(data, "matrix[0]")
        assert result == [1, 2]

    def test_mixed_access_patterns(self) -> None:
        """Test combining dict and array access in complex paths."""
        data = {
            "clusters": [
                {
                    "name": "cluster-1",
                    "nodes": [
                        {"name": "node-a", "cpus": 4},
                        {"name": "node-b", "cpus": 8},
                    ],
                },
                {
                    "name": "cluster-2",
                    "nodes": [
                        {"name": "node-c", "cpus": 16},
                    ],
                },
            ]
        }
        assert get_nested_value(data, "clusters[0].name") == "cluster-1"
        assert get_nested_value(data, "clusters[0].nodes[1].cpus") == 8
        assert get_nested_value(data, "clusters[1].nodes[0].name") == "node-c"
