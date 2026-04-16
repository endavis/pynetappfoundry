"""Tests for OpenAPI spec adapters."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.codegen.adapters import (
    ParsedEndpoint,
    _build_identifier_map,
    _detect_parent_path,
    _detect_records_path,
    _flatten_schema,
    _resolve_ref,
    detect_shared_schemas,
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
        """Nested $ref fields appear as sub_fields of the parent object."""
        schema = simple_spec["components"]["schemas"]["volume"]
        fields = _flatten_schema(simple_spec, schema, "", [])
        # Top-level should have the parent object "svm"
        svm_field = next(f for f in fields if f.api_path == "svm")
        assert svm_field.is_object
        # Sub-fields hold the nested paths
        sub_names = {sf.api_path for sf in svm_field.sub_fields}
        assert "svm.name" in sub_names
        assert "svm.uuid" in sub_names

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

        # analytics.state is now in sub_fields of the analytics object
        analytics_field = next(f for f in fields if f.api_path == "analytics")
        analytics_state = next(
            sf for sf in analytics_field.sub_fields if sf.api_path == "analytics.state"
        )
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

        # Check field structure (tree: svm.name is in svm.sub_fields)
        field_paths = {f.api_path for f in ep.fields}
        assert "uuid" in field_paths
        assert "name" in field_paths
        assert "svm" in field_paths
        svm_field = next(f for f in ep.fields if f.api_path == "svm")
        sub_paths = {sf.api_path for sf in svm_field.sub_fields}
        assert "svm.name" in sub_paths

    def test_expensive_fields_annotated(self, expensive_spec, tmp_path):
        spec_path = _write_spec(expensive_spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1

        ep = endpoints[0]
        assert len(ep.expensive_patterns) == 3

        # Expensive fields are now in sub_fields (tree structure)
        def _all_fields(fields):
            for f in fields:
                yield f
                yield from _all_fields(f.sub_fields)

        expensive_fields = [f for f in _all_fields(ep.fields) if f.requires_explicit_fetch]
        assert len(expensive_fields) > 0

    def test_non_ontap_no_expensive(self, expensive_spec, tmp_path):
        spec_path = _write_spec(expensive_spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "dii")
        assert len(endpoints) == 1

        ep = endpoints[0]
        assert ep.expensive_patterns == []

        def _all_fields(fields):
            for f in fields:
                yield f
                yield from _all_fields(f.sub_fields)

        expensive_fields = [f for f in _all_fields(ep.fields) if f.requires_explicit_fetch]
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
        spec_path = Path("docs/example-config/apis/ontap/openapi3.json")
        if not spec_path.exists():
            pytest.skip("ONTAP spec not available")

        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) > 100

        # Verify /storage/volumes is parsed
        vol = next((e for e in endpoints if e.path == "/storage/volumes"), None)
        assert vol is not None
        assert len(vol.fields) > 50
        assert len(vol.expensive_patterns) > 5


# ---------------------------------------------------------------------------
# _build_identifier_map tests (issue #601 — identifier_field inference)
# ---------------------------------------------------------------------------


class TestBuildIdentifierMap:
    def test_uuid_param(self):
        """A `/foo` + `/foo/{uuid}` pair yields identifier_field='uuid'."""
        paths = ["/storage/volumes", "/storage/volumes/{uuid}"]
        assert _build_identifier_map(paths) == {"/storage/volumes": "uuid"}

    def test_custom_param_name(self):
        """The inferred identifier uses whatever name the spec declares."""
        paths = ["/foo", "/foo/{id}"]
        assert _build_identifier_map(paths) == {"/foo": "id"}

        paths = ["/bar", "/bar/{key}"]
        assert _build_identifier_map(paths) == {"/bar": "key"}

    def test_no_sibling_item_endpoint(self):
        """Collection without a sibling item endpoint is absent from the map."""
        paths = ["/storage/volumes"]
        assert _build_identifier_map(paths) == {}

    def test_multi_param_item_skipped(self):
        """Item endpoints with >1 path parameter are skipped (composite keys)."""
        paths = [
            "/a/b",
            "/a/b/{x}/c/{y}",  # multi-param -- skip
        ]
        assert _build_identifier_map(paths) == {}

    def test_nested_parent_not_confused_with_collection(self):
        """Item endpoint under a parameterized parent (two params total) is skipped."""
        paths = [
            "/svm/svms/{svm.uuid}/web",
            "/svm/svms/{svm.uuid}/web/{uuid}",
        ]
        # The latter has two `{...}` segments, so it's skipped.
        # The former is not an item endpoint, so it's skipped too.
        assert _build_identifier_map(paths) == {}

    def test_item_without_collection(self):
        """An item endpoint whose collection path doesn't exist is ignored."""
        paths = ["/solo/{uuid}"]
        assert _build_identifier_map(paths) == {}


class TestParseOpenAPISpecIdentifierField:
    def _spec_with_paths(self, paths: dict) -> dict:
        return {
            "openapi": "3.0.0",
            "info": {"title": "Test", "version": "1.0"},
            "paths": paths,
            "components": {
                "schemas": {
                    "volume": {
                        "type": "object",
                        "properties": {
                            "uuid": {"type": "string", "format": "uuid"},
                            "name": {"type": "string"},
                        },
                    }
                }
            },
        }

    def _collection_get(self) -> dict:
        """Returns a GET op that parses into a ParsedEndpoint."""
        return {
            "get": {
                "description": "List volumes.",
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

    def _item_get(self) -> dict:
        """Returns a GET op for an item endpoint (doesn't need to parse)."""
        return {"get": {"description": "Get one volume.", "responses": {}}}

    def test_uuid_inferred(self, tmp_path):
        spec = self._spec_with_paths(
            {
                "/storage/volumes": self._collection_get(),
                "/storage/volumes/{uuid}": self._item_get(),
            }
        )
        spec_path = _write_spec(spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1
        assert endpoints[0].identifier_field == "uuid"

    def test_alternative_param_name_inferred(self, tmp_path):
        spec = self._spec_with_paths(
            {
                "/foo": self._collection_get(),
                "/foo/{id}": self._item_get(),
            }
        )
        spec_path = _write_spec(spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1
        assert endpoints[0].identifier_field == "id"

    def test_none_when_no_sibling(self, tmp_path):
        spec = self._spec_with_paths({"/storage/volumes": self._collection_get()})
        spec_path = _write_spec(spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1
        assert endpoints[0].identifier_field is None

    def test_none_when_item_has_multi_params(self, tmp_path):
        spec = self._spec_with_paths(
            {
                "/a/b": self._collection_get(),
                "/a/b/{x}/c/{y}": self._item_get(),
            }
        )
        spec_path = _write_spec(spec, tmp_path)
        endpoints = parse_openapi_spec(spec_path, "ontap")
        assert len(endpoints) == 1
        assert endpoints[0].identifier_field is None


# ---------------------------------------------------------------------------
# detect_shared_schemas tests (issue #603 — shared-schema naming)
# ---------------------------------------------------------------------------


class TestDetectSharedSchemas:
    """Tests for ``detect_shared_schemas``.

    Identifies schema names referenced by more than one endpoint so the
    generators can switch to URL-path-derived class names and avoid
    registry collisions (ADR-0008).
    """

    def test_empty_when_all_schemas_unique(self):
        endpoints = [
            ParsedEndpoint(path="/a", schema_name="foo"),
            ParsedEndpoint(path="/b", schema_name="bar"),
            ParsedEndpoint(path="/c", schema_name="baz"),
        ]
        assert detect_shared_schemas(endpoints) == set()

    def test_shared_schema_detected(self):
        """Schema referenced twice → in result set."""
        endpoints = [
            ParsedEndpoint(path="/assets/storages/count", schema_name="Count"),
            ParsedEndpoint(path="/assets/fabrics/count", schema_name="Count"),
            ParsedEndpoint(path="/assets/storages", schema_name="Storage"),
        ]
        result = detect_shared_schemas(endpoints)
        assert result == {"Count"}

    def test_multiple_shared_schemas(self):
        """Every schema with count > 1 is in the result set."""
        endpoints = [
            ParsedEndpoint(path="/a/count", schema_name="Count"),
            ParsedEndpoint(path="/b/count", schema_name="Count"),
            ParsedEndpoint(path="/c", schema_name="Annotation"),
            ParsedEndpoint(path="/d", schema_name="Annotation"),
            ParsedEndpoint(path="/e", schema_name="Unique"),
        ]
        assert detect_shared_schemas(endpoints) == {"Count", "Annotation"}

    def test_empty_schema_names_ignored(self):
        """Endpoints with empty schema names (inline schemas) do not count."""
        endpoints = [
            ParsedEndpoint(path="/a", schema_name=""),
            ParsedEndpoint(path="/b", schema_name=""),
            ParsedEndpoint(path="/c", schema_name="Foo"),
        ]
        assert detect_shared_schemas(endpoints) == set()

    def test_empty_input(self):
        assert detect_shared_schemas([]) == set()

    def test_single_reference_not_shared(self):
        """Schema with count == 1 is NOT considered shared."""
        endpoints = [
            ParsedEndpoint(path="/a", schema_name="Foo"),
        ]
        assert detect_shared_schemas(endpoints) == set()
