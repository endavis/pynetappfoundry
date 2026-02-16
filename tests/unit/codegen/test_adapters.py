"""Tests for OpenAPI spec adapters."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.codegen.adapters import (
    _detect_parent_path,
    _detect_records_path,
    _flatten_schema,
    _resolve_ref,
    parse_openapi_spec,
)

# ---------------------------------------------------------------------------
# Fixtures: synthetic OpenAPI specs
# ---------------------------------------------------------------------------


@pytest.fixture
def simple_spec() -> dict:
    """Minimal OpenAPI 3.0 spec with one GET endpoint."""
    return {
        "openapi": "3.0.0",
        "info": {"title": "Test", "version": "1.0"},
        "paths": {
            "/storage/volumes": {
                "get": {
                    "description": "Retrieves volumes.",
                    "tags": ["storage"],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "records": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/volume"},
                                            },
                                            "num_records": {"type": "integer"},
                                        },
                                    }
                                }
                            }
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "volume": {
                    "type": "object",
                    "properties": {
                        "uuid": {"type": "string", "format": "uuid"},
                        "name": {"type": "string"},
                        "size": {"type": "integer"},
                        "state": {
                            "type": "string",
                            "enum": ["online", "offline", "restricted"],
                        },
                        "svm": {"$ref": "#/components/schemas/svm_ref"},
                    },
                },
                "svm_ref": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "uuid": {"type": "string", "format": "uuid"},
                    },
                },
            }
        },
    }


@pytest.fixture
def expensive_spec() -> dict:
    """Spec with expensive properties in the description."""
    return {
        "openapi": "3.0.0",
        "info": {"title": "Test", "version": "1.0"},
        "paths": {
            "/storage/volumes": {
                "get": {
                    "description": (
                        "Retrieves volumes.\n"
                        "### Expensive properties\n"
                        "* `analytics.*`\n"
                        "* `autosize.*`\n"
                        "* `statistics.*`\n"
                    ),
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "records": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/volume"},
                                            }
                                        },
                                    }
                                }
                            }
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "volume": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "analytics": {
                            "type": "object",
                            "properties": {
                                "state": {"type": "string"},
                                "progress": {"type": "integer"},
                            },
                        },
                        "autosize": {
                            "type": "object",
                            "properties": {
                                "mode": {"type": "string"},
                                "maximum": {"type": "integer"},
                            },
                        },
                        "statistics": {
                            "type": "object",
                            "properties": {
                                "iops_total": {"type": "integer"},
                            },
                        },
                    },
                }
            }
        },
    }


@pytest.fixture
def parameterized_spec() -> dict:
    """Spec with a parameterized endpoint."""
    return {
        "openapi": "3.0.0",
        "info": {"title": "Test", "version": "1.0"},
        "paths": {
            "/svm/svms/{svm.uuid}/web": {
                "get": {
                    "description": "Get SVM web config.",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "enabled": {"type": "boolean"},
                                            "certificate": {"type": "string"},
                                        },
                                    }
                                }
                            }
                        }
                    },
                }
            }
        },
        "components": {"schemas": {}},
    }


def _write_spec(spec: dict, tmp_path: Path) -> Path:
    """Write a spec dict to a temp JSON file."""
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    return path


# ---------------------------------------------------------------------------
# _resolve_ref tests
# ---------------------------------------------------------------------------


class TestResolveRef:
    def test_valid_ref(self, simple_spec):
        result = _resolve_ref(simple_spec, "#/components/schemas/volume")
        assert "properties" in result
        assert "uuid" in result["properties"]

    def test_invalid_ref_returns_empty(self, simple_spec):
        result = _resolve_ref(simple_spec, "#/components/schemas/nonexistent")
        assert result == {}

    def test_ref_with_spaces_returns_empty(self, simple_spec):
        result = _resolve_ref(simple_spec, "#/components/schemas/CSV file")
        assert result == {}


# ---------------------------------------------------------------------------
# _flatten_schema tests
# ---------------------------------------------------------------------------


class TestFlattenSchema:
    def test_flat_properties(self, simple_spec):
        schema = simple_spec["components"]["schemas"]["volume"]
        fields = _flatten_schema(simple_spec, schema, "", [])
        names = {f.api_path for f in fields}
        assert "uuid" in names
        assert "name" in names
        assert "size" in names

    def test_nested_ref_resolved(self, simple_spec):
        schema = simple_spec["components"]["schemas"]["volume"]
        fields = _flatten_schema(simple_spec, schema, "", [])
        names = {f.api_path for f in fields}
        assert "svm.name" in names
        assert "svm.uuid" in names

    def test_uuid_detected(self, simple_spec):
        schema = simple_spec["components"]["schemas"]["volume"]
        fields = _flatten_schema(simple_spec, schema, "", [])
        uuid_field = next(f for f in fields if f.api_path == "uuid")
        assert uuid_field.is_uuid

    def test_type_mapping(self, simple_spec):
        schema = simple_spec["components"]["schemas"]["volume"]
        fields = _flatten_schema(simple_spec, schema, "", [])
        size_field = next(f for f in fields if f.api_path == "size")
        assert size_field.python_type == "int"
        assert size_field.default == 0

    def test_expensive_annotation(self, expensive_spec):
        schema = expensive_spec["components"]["schemas"]["volume"]
        patterns = ["analytics.*", "autosize.*", "statistics.*"]
        fields = _flatten_schema(expensive_spec, schema, "", patterns)

        analytics_state = next(f for f in fields if f.api_path == "analytics.state")
        assert analytics_state.requires_explicit_fetch

        name_field = next(f for f in fields if f.api_path == "name")
        assert not name_field.requires_explicit_fetch

    def test_enum_values(self, simple_spec):
        schema = simple_spec["components"]["schemas"]["volume"]
        fields = _flatten_schema(simple_spec, schema, "", [])
        state_field = next(f for f in fields if f.api_path == "state")
        assert state_field.enum_values == ["online", "offline", "restricted"]

    def test_max_depth_prevents_infinite_recursion(self, simple_spec):
        # Create a self-referencing schema
        simple_spec["components"]["schemas"]["recursive"] = {
            "type": "object",
            "properties": {
                "child": {"$ref": "#/components/schemas/recursive"},
            },
        }
        schema = simple_spec["components"]["schemas"]["recursive"]
        fields = _flatten_schema(simple_spec, schema, "", [], max_depth=2)
        # Should not hang or crash
        assert isinstance(fields, list)

    def test_underscore_prefix_skipped(self):
        spec = {"components": {"schemas": {}}}
        schema = {
            "type": "object",
            "properties": {
                "_links": {"type": "object"},
                "name": {"type": "string"},
            },
        }
        fields = _flatten_schema(spec, schema, "", [])
        names = {f.name for f in fields}
        assert "_links" not in names
        assert "name" in names


# ---------------------------------------------------------------------------
# _detect_records_path tests
# ---------------------------------------------------------------------------


class TestDetectRecordsPath:
    def test_ontap_records_pattern(self, simple_spec):
        response_schema = {
            "type": "object",
            "properties": {
                "records": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/volume"},
                },
                "num_records": {"type": "integer"},
            },
        }
        path, schema = _detect_records_path(simple_spec, response_schema)
        assert path == "records"
        assert "properties" in schema

    def test_direct_array(self):
        spec = {"components": {"schemas": {}}}
        response_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            },
        }
        path, schema = _detect_records_path(spec, response_schema)
        assert path == ""
        assert "properties" in schema


# ---------------------------------------------------------------------------
# _detect_parent_path tests
# ---------------------------------------------------------------------------


class TestDetectParentPath:
    def test_no_parent(self):
        has_parent, parent = _detect_parent_path("/storage/volumes")
        assert not has_parent
        assert parent == ""

    def test_with_parent(self):
        has_parent, parent = _detect_parent_path("/svm/svms/{svm.uuid}/web")
        assert has_parent
        assert parent == "/svm/svms"

    def test_nested_parent(self):
        has_parent, parent = _detect_parent_path("/a/b/{id}/c/{id2}/d")
        assert has_parent
        assert parent == "/a/b"


# ---------------------------------------------------------------------------
# parse_openapi_spec integration tests
# ---------------------------------------------------------------------------


class TestParseOpenAPISpec:
    def test_simple_spec(self, simple_spec, tmp_path):
        spec_path = _write_spec(simple_spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1

        ep = endpoints[0]
        assert ep.path == "/storage/volumes"
        assert ep.schema_name == "volume"
        assert ep.records_path == "records"
        assert len(ep.fields) > 0

        # Check field structure
        field_paths = {f.api_path for f in ep.fields}
        assert "uuid" in field_paths
        assert "name" in field_paths
        assert "svm.name" in field_paths

    def test_expensive_fields_annotated(self, expensive_spec, tmp_path):
        spec_path = _write_spec(expensive_spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1

        ep = endpoints[0]
        assert len(ep.expensive_patterns) == 3

        expensive_fields = [f for f in ep.fields if f.requires_explicit_fetch]
        assert len(expensive_fields) > 0

    def test_non_ontap_no_expensive(self, expensive_spec, tmp_path):
        spec_path = _write_spec(expensive_spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "dii")
        assert len(endpoints) == 1

        ep = endpoints[0]
        assert ep.expensive_patterns == []
        expensive_fields = [f for f in ep.fields if f.requires_explicit_fetch]
        assert len(expensive_fields) == 0

    def test_parameterized_endpoint(self, parameterized_spec, tmp_path):
        spec_path = _write_spec(parameterized_spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1

        ep = endpoints[0]
        assert ep.has_parent
        assert ep.parent_path == "/svm/svms"

    def test_real_ontap_spec(self):
        """Smoke test with the real ONTAP spec if available."""
        spec_path = Path("example-config/apis/ontap/openapi3.json")
        if not spec_path.exists():
            pytest.skip("ONTAP spec not available")

        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) > 100

        # Verify /storage/volumes is parsed
        vol = next((e for e in endpoints if e.path == "/storage/volumes"), None)
        assert vol is not None
        assert len(vol.fields) > 50
        assert len(vol.expensive_patterns) > 5
