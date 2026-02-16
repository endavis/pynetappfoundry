"""Tests for code generation (models, mappings, TOML overlays)."""

from __future__ import annotations

from tools.codegen.adapters import ParsedEndpoint, ParsedField
from tools.codegen.generators import (
    _field_to_cache_attr,
    _path_to_class_name,
    _path_to_module_parts,
    _select_leaf_fields,
    _singularize,
    generate_init,
    generate_mapping,
    generate_model,
    generate_toml_overlay,
    write_endpoint_files,
)

# ---------------------------------------------------------------------------
# Helper: build a simple ParsedEndpoint
# ---------------------------------------------------------------------------


def _make_endpoint(
    path: str = "/storage/volumes",
    fields: list[ParsedField] | None = None,
    expensive_patterns: list[str] | None = None,
    has_parent: bool = False,
    parent_path: str = "",
) -> ParsedEndpoint:
    if fields is None:
        fields = [
            ParsedField(name="uuid", api_path="uuid", python_type="OntapUUID", is_uuid=True),
            ParsedField(name="name", api_path="name", python_type="str"),
            ParsedField(name="size", api_path="size", python_type="int", default=0),
            ParsedField(
                name="state", api_path="state", python_type="str", enum_values=["online", "offline"]
            ),
            ParsedField(
                name="svm",
                api_path="svm",
                python_type="object",
                is_object=True,
                sub_fields=[
                    ParsedField(name="name", api_path="svm.name", python_type="str"),
                ],
            ),
            ParsedField(name="name", api_path="svm.name", python_type="str"),
            ParsedField(
                name="tags",
                api_path="tags",
                python_type="list[str]",
                is_list=True,
                default=[],
            ),
        ]
    return ParsedEndpoint(
        path=path,
        schema_name="volume",
        fields=fields,
        expensive_patterns=expensive_patterns or [],
        has_parent=has_parent,
        parent_path=parent_path,
    )


# ---------------------------------------------------------------------------
# Naming utilities
# ---------------------------------------------------------------------------


class TestPathToModuleParts:
    def test_simple(self):
        assert _path_to_module_parts("/storage/volumes") == ["storage", "volumes"]

    def test_deep(self):
        assert _path_to_module_parts("/network/ip/interfaces") == ["network", "ip", "interfaces"]

    def test_hyphen_to_underscore(self):
        assert _path_to_module_parts("/network/ethernet/broadcast-domains") == [
            "network",
            "ethernet",
            "broadcast_domains",
        ]

    def test_skip_params(self):
        assert _path_to_module_parts("/svm/svms/{svm.uuid}/web") == ["svm", "svms", "web"]


class TestPathToClassName:
    def test_simple(self):
        assert _path_to_class_name("/storage/volumes") == "StorageVolume"

    def test_deep(self):
        assert _path_to_class_name("/network/ip/interfaces") == "NetworkIpInterface"

    def test_hyphen(self):
        assert _path_to_class_name("/network/ethernet/broadcast-domains") == (
            "NetworkEthernetBroadcastDomain"
        )


class TestSingularize:
    def test_regular_plural(self):
        assert _singularize("volumes") == "volume"

    def test_ies(self):
        assert _singularize("policies") == "policy"

    def test_ses(self):
        assert _singularize("addresses") == "address"

    def test_already_singular(self):
        assert _singularize("web") == "web"

    def test_double_s(self):
        assert _singularize("access") == "access"


class TestFieldToCacheAttr:
    def test_simple(self):
        f = ParsedField(name="name", api_path="name")
        assert _field_to_cache_attr(f) == "name"

    def test_nested(self):
        f = ParsedField(name="name", api_path="svm.name")
        assert _field_to_cache_attr(f) == "svm_name"

    def test_deep_nested(self):
        f = ParsedField(name="name", api_path="nas.export_policy.name")
        assert _field_to_cache_attr(f) == "nas_export_policy_name"


# ---------------------------------------------------------------------------
# Field selection
# ---------------------------------------------------------------------------


class TestSelectLeafFields:
    def test_filters_objects(self):
        fields = [
            ParsedField(name="svm", api_path="svm", is_object=True),
            ParsedField(name="name", api_path="svm.name"),
            ParsedField(name="uuid", api_path="uuid"),
        ]
        leaves = _select_leaf_fields(fields)
        assert len(leaves) == 2
        assert all(not (f.is_object and not f.is_list) for f in leaves)

    def test_keeps_list_objects(self):
        fields = [
            ParsedField(name="tags", api_path="tags", is_list=True, is_object=True),
        ]
        leaves = _select_leaf_fields(fields)
        assert len(leaves) == 1


# ---------------------------------------------------------------------------
# Model generation
# ---------------------------------------------------------------------------


class TestGenerateModel:
    def test_basic_structure(self):
        ep = _make_endpoint()
        code = generate_model(ep)
        assert "class StorageVolume(CacheModel):" in code
        assert "from pynetappfoundry.cache._base import CacheModel" in code

    def test_uuid_import(self):
        ep = _make_endpoint()
        code = generate_model(ep)
        assert "OntapUUID" in code

    def test_list_field_uses_field_factory(self):
        ep = _make_endpoint()
        code = generate_model(ep)
        assert "Field(default_factory=list)" in code
        assert "from pydantic import Field" in code

    def test_flat_field_names(self):
        ep = _make_endpoint()
        code = generate_model(ep)
        assert "svm_name: str" in code
        assert "    uuid: OntapUUID" in code

    def test_no_object_fields(self):
        """Object container fields (svm) should not appear as model attrs."""
        ep = _make_endpoint()
        code = generate_model(ep)
        # "svm: object" should not be in the model, only "svm_name: str"
        lines = code.split("\n")
        svm_lines = [line for line in lines if line.strip().startswith("svm:")]
        assert len(svm_lines) == 0


# ---------------------------------------------------------------------------
# Mapping generation
# ---------------------------------------------------------------------------


class TestGenerateMapping:
    def test_basic_structure(self):
        ep = _make_endpoint()
        code = generate_mapping(ep)
        assert "STORAGEVOLUME_MAPPING = TypeMapping(" in code
        assert 'name="StorageVolume"' in code
        assert "model_class=StorageVolume" in code

    def test_field_mappings(self):
        ep = _make_endpoint()
        code = generate_mapping(ep)
        assert 'cache_attr="uuid"' in code
        assert 'api_path="svm.name"' in code

    def test_expensive_fields_in_endpoint(self):
        fields = [
            ParsedField(name="name", api_path="name"),
            ParsedField(name="state", api_path="analytics.state", requires_explicit_fetch=True),
        ]
        ep = _make_endpoint(fields=fields, expensive_patterns=["analytics.*"])
        code = generate_mapping(ep)
        assert "requires_explicit_fetch=True" in code

    def test_parent_mapping(self):
        ep = _make_endpoint(
            path="/svm/svms/{svm.uuid}/web",
            has_parent=True,
            parent_path="/svm/svms",
            fields=[
                ParsedField(name="enabled", api_path="enabled", python_type="bool", default=False)
            ],
        )
        code = generate_mapping(ep)
        assert 'parent_mapping="SvmSvm"' in code
        assert 'parent_id_field="uuid"' in code

    def test_registry_call(self):
        ep = _make_endpoint()
        code = generate_mapping(ep)
        assert 'model_registry.register_mapping("StorageVolume"' in code


# ---------------------------------------------------------------------------
# Init generation
# ---------------------------------------------------------------------------


class TestGenerateInit:
    def test_exports_class(self):
        ep = _make_endpoint()
        code = generate_init(ep)
        assert "from pynetappfoundry.cache.storage.volumes.model import StorageVolume" in code
        assert '__all__ = ["StorageVolume"]' in code


# ---------------------------------------------------------------------------
# TOML overlay
# ---------------------------------------------------------------------------


class TestGenerateTomlOverlay:
    def test_basic_structure(self):
        ep = _make_endpoint()
        toml = generate_toml_overlay(ep)
        assert "[endpoint]" in toml
        assert 'path = "/storage/volumes"' in toml
        assert "[fields.uuid]" in toml
        assert 'cache_strategy = "cache"' in toml

    def test_expensive_field_marked(self):
        fields = [
            ParsedField(
                name="stats",
                api_path="stats",
                python_type="int",
                default=0,
                requires_explicit_fetch=True,
            ),
        ]
        ep = _make_endpoint(fields=fields)
        toml = generate_toml_overlay(ep)
        assert "requires_explicit_fetch = true" in toml

    def test_preserves_existing_edits(self, tmp_path):
        fields = [
            ParsedField(name="name", api_path="name"),
            ParsedField(name="size", api_path="size", python_type="int", default=0),
        ]
        ep = _make_endpoint(fields=fields)

        # Write initial overlay
        existing = tmp_path / "overlay.toml"
        existing.write_text(
            '[endpoint]\npath = "/storage/volumes"\n\n[fields.name]\ncache_strategy = "realtime"\n'
        )

        toml = generate_toml_overlay(ep, existing)
        # User's "realtime" edit should be preserved
        assert '"realtime"' in toml
        # New field should get default
        assert "[fields.size]" in toml

    def test_warns_removed_fields(self, tmp_path):
        fields = [ParsedField(name="name", api_path="name")]
        ep = _make_endpoint(fields=fields)

        existing = tmp_path / "overlay.toml"
        existing.write_text(
            '[endpoint]\npath = "/test"\n\n[fields.old_field]\ncache_strategy = "cache"\n'
        )

        toml = generate_toml_overlay(ep, existing)
        assert "old_field" in toml  # listed in _removed_fields


# ---------------------------------------------------------------------------
# Full file write
# ---------------------------------------------------------------------------


class TestWriteEndpointFiles:
    def test_creates_directory_tree(self, tmp_path):
        ep = _make_endpoint()
        written = write_endpoint_files(ep, tmp_path)

        assert (tmp_path / "storage" / "volumes" / "model.py").exists()
        assert (tmp_path / "storage" / "volumes" / "mapping.py").exists()
        assert (tmp_path / "storage" / "volumes" / "__init__.py").exists()
        assert (tmp_path / "storage" / "volumes" / "volumes.toml").exists()
        assert len(written) == 4

    def test_intermediate_init_files(self, tmp_path):
        ep = _make_endpoint(
            path="/network/ip/interfaces",
            fields=[
                ParsedField(name="name", api_path="name"),
            ],
        )
        write_endpoint_files(ep, tmp_path)

        assert (tmp_path / "network" / "__init__.py").exists()
        assert (tmp_path / "network" / "ip" / "__init__.py").exists()

    def test_generated_model_is_valid_python(self, tmp_path):
        ep = _make_endpoint()
        write_endpoint_files(ep, tmp_path)

        model_code = (tmp_path / "storage" / "volumes" / "model.py").read_text()
        # Should compile without syntax errors
        compile(model_code, "model.py", "exec")

    def test_generated_mapping_is_valid_python(self, tmp_path):
        ep = _make_endpoint()
        write_endpoint_files(ep, tmp_path)

        mapping_code = (tmp_path / "storage" / "volumes" / "mapping.py").read_text()
        compile(mapping_code, "mapping.py", "exec")
