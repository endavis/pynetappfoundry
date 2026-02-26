"""Tests for code generation (models, mappings, TOML overlays)."""

from __future__ import annotations

from tools.codegen.adapters import ParsedEndpoint, ParsedField
from tools.codegen.generators import (
    _CLASS_NAME_OVERRIDES,
    _SINGULAR_EXCEPTIONS,
    _field_to_cache_attr,
    _has_typed_sub_fields,
    _path_to_class_name,
    _path_to_module_parts,
    _safe_attr_name,
    _schema_to_pascal,
    _select_leaf_fields,
    _singularize,
    _sub_model_name,
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
    schema_name: str = "volume",
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
        schema_name=schema_name,
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


class TestSchemaToPascal:
    def test_simple(self):
        assert _schema_to_pascal("volume") == "Volume"

    def test_snake_case(self):
        assert _schema_to_pascal("cloud_target") == "CloudTarget"

    def test_multi_segment(self):
        assert _schema_to_pascal("ip_interface") == "IpInterface"

    def test_single_word(self):
        assert _schema_to_pascal("svm") == "Svm"


class TestPathToClassName:
    def test_schema_name_with_api_prefix(self):
        """When schema_name is provided, use {ApiType}{SchemaName}."""
        assert _path_to_class_name("/storage/volumes", "volume", "ontap") == "OntapVolume"

    def test_schema_name_snake_case(self):
        assert _path_to_class_name("/cloud/targets", "cloud_target", "ontap") == "OntapCloudTarget"

    def test_schema_name_different_api_type(self):
        assert _path_to_class_name("/some/path", "node", "aiqum") == "AiqumNode"

    def test_inline_fallback_simple(self):
        """When schema_name is empty, fall back to URL-path-derived name with api prefix."""
        assert _path_to_class_name("/cluster", "", "ontap") == "OntapCluster"

    def test_inline_fallback_deep(self):
        assert (
            _path_to_class_name("/cluster/licensing/licenses", "", "ontap")
            == "OntapClusterLicensingLicense"
        )

    def test_inline_fallback_redundant_dedup(self):
        """Inline fallback still deduplicates redundant segments."""
        assert _path_to_class_name("/svm/svms", "", "ontap") == "OntapSvm"

    def test_inline_fallback_hyphen(self):
        assert (
            _path_to_class_name("/network/ethernet/broadcast-domains", "", "ontap")
            == "OntapNetworkEthernetBroadcastDomain"
        )

    def test_override_map_takes_precedence(self):
        """_CLASS_NAME_OVERRIDES should override the algorithm."""
        _CLASS_NAME_OVERRIDES["/test/override"] = "MyCustomName"
        try:
            assert _path_to_class_name("/test/override", "test", "ontap") == "MyCustomName"
        finally:
            del _CLASS_NAME_OVERRIDES["/test/override"]

    def test_default_api_type(self):
        """Default api_type is ontap."""
        assert _path_to_class_name("/storage/volumes", "volume") == "OntapVolume"


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

    def test_exception_dns(self):
        assert _singularize("dns") == "dns"

    def test_exception_licenses(self):
        assert _singularize("licenses") == "license"

    def test_exception_chassis(self):
        assert _singularize("chassis") == "chassis"

    def test_exception_flexcaches(self):
        assert _singularize("flexcaches") == "flexcache"

    def test_exception_status(self):
        assert _singularize("status") == "status"

    def test_exception_alias(self):
        assert _singularize("alias") == "alias"

    def test_exception_bus(self):
        assert _singularize("bus") == "bus"

    def test_exception_nfs(self):
        assert _singularize("nfs") == "nfs"

    def test_exception_cifs(self):
        assert _singularize("cifs") == "cifs"

    def test_all_exceptions_covered(self):
        """Every entry in _SINGULAR_EXCEPTIONS should produce the expected value."""
        for plural, expected in _SINGULAR_EXCEPTIONS.items():
            assert _singularize(plural) == expected, f"_singularize({plural!r}) != {expected!r}"


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
        assert "class OntapVolume(CacheModel):" in code
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
        assert "ONTAPVOLUME_MAPPING = TypeMapping(" in code
        assert 'name="OntapVolume"' in code
        assert "model_class=OntapVolume" in code

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

    def test_parent_mapping_with_schema_lookup(self):
        ep = _make_endpoint(
            path="/svm/svms/{svm.uuid}/web",
            has_parent=True,
            parent_path="/svm/svms",
            schema_name="web",
            fields=[
                ParsedField(name="enabled", api_path="enabled", python_type="bool", default=False)
            ],
        )
        # Provide schema_lookup so parent path resolves correctly
        schema_lookup = {"/svm/svms": "svm"}
        code = generate_mapping(ep, schema_lookup=schema_lookup)
        assert 'parent_mapping="OntapSvm"' in code
        assert 'parent_id_field="uuid"' in code

    def test_parent_mapping_inline_fallback(self):
        """When parent has no schema_name in lookup, use URL-path fallback."""
        ep = _make_endpoint(
            path="/svm/svms/{svm.uuid}/web",
            has_parent=True,
            parent_path="/svm/svms",
            schema_name="web",
            fields=[
                ParsedField(name="enabled", api_path="enabled", python_type="bool", default=False)
            ],
        )
        # No schema_lookup — parent falls back to URL-path
        code = generate_mapping(ep)
        assert 'parent_mapping="OntapSvm"' in code

    def test_registry_call(self):
        ep = _make_endpoint()
        code = generate_mapping(ep)
        assert 'model_registry.register_mapping("OntapVolume"' in code


# ---------------------------------------------------------------------------
# Init generation
# ---------------------------------------------------------------------------


class TestGenerateInit:
    def test_exports_class(self):
        ep = _make_endpoint()
        code = generate_init(ep)
        assert "from pynetappfoundry.cache.ontap.storage.volumes.model import OntapVolume" in code
        assert '__all__ = ["OntapVolume"]' in code


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
        assert 'class_name = "OntapVolume"' in toml

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

        assert (tmp_path / "ontap" / "storage" / "volumes" / "model.py").exists()
        assert (tmp_path / "ontap" / "storage" / "volumes" / "mapping.py").exists()
        assert (tmp_path / "ontap" / "storage" / "volumes" / "__init__.py").exists()
        assert (tmp_path / "ontap" / "storage" / "volumes" / "volumes.toml").exists()
        assert len(written) == 4

    def test_intermediate_init_files(self, tmp_path):
        ep = _make_endpoint(
            path="/network/ip/interfaces",
            schema_name="ip_interface",
            fields=[
                ParsedField(name="name", api_path="name"),
            ],
        )
        write_endpoint_files(ep, tmp_path)

        assert (tmp_path / "ontap" / "network" / "__init__.py").exists()
        assert (tmp_path / "ontap" / "network" / "ip" / "__init__.py").exists()

    def test_generated_model_is_valid_python(self, tmp_path):
        ep = _make_endpoint()
        write_endpoint_files(ep, tmp_path)

        model_code = (tmp_path / "ontap" / "storage" / "volumes" / "model.py").read_text()
        # Should compile without syntax errors
        compile(model_code, "model.py", "exec")

    def test_generated_mapping_is_valid_python(self, tmp_path):
        ep = _make_endpoint()
        write_endpoint_files(ep, tmp_path)

        mapping_code = (tmp_path / "ontap" / "storage" / "volumes" / "mapping.py").read_text()
        compile(mapping_code, "mapping.py", "exec")

    def test_schema_lookup_passed_to_mapping(self, tmp_path):
        """Verify schema_lookup is used for parent resolution in generated mappings."""
        ep = _make_endpoint(
            path="/svm/svms/{svm.uuid}/web",
            has_parent=True,
            parent_path="/svm/svms",
            schema_name="web",
            fields=[
                ParsedField(name="enabled", api_path="enabled", python_type="bool", default=False)
            ],
        )
        schema_lookup = {"/svm/svms": "svm"}
        write_endpoint_files(ep, tmp_path, schema_lookup=schema_lookup)

        mapping_code = (tmp_path / "ontap" / "svm" / "svms" / "web" / "mapping.py").read_text()
        assert 'parent_mapping="OntapSvm"' in mapping_code

    def test_no_orphan_dirs_under_output_dir(self, tmp_path):
        """Only the api_type subdirectory should exist directly under output_dir."""
        ep = _make_endpoint()
        write_endpoint_files(ep, tmp_path)

        subdirs = [p.name for p in tmp_path.iterdir() if p.is_dir()]
        assert subdirs == ["ontap"]

    def test_custom_api_type(self, tmp_path):
        """Files should land under the custom api_type subdirectory."""
        ep = _make_endpoint()
        write_endpoint_files(ep, tmp_path, api_type="aiqum")

        assert (tmp_path / "aiqum" / "storage" / "volumes" / "model.py").exists()
        assert (tmp_path / "aiqum" / "storage" / "volumes" / "mapping.py").exists()
        assert (tmp_path / "aiqum" / "storage" / "volumes" / "__init__.py").exists()
        # No ontap directory should exist
        assert not (tmp_path / "ontap").exists()


# ---------------------------------------------------------------------------
# Sub-model helpers
# ---------------------------------------------------------------------------


class TestSubModelName:
    def test_basic(self):
        f = ParsedField(name="copies", api_path="copies", is_list=True, is_object=True)
        assert _sub_model_name("OntapSnapshotPolicy", f) == "OntapSnapshotPolicyCopy"

    def test_underscored_field(self):
        f = ParsedField(name="ip_ranges", api_path="ip_ranges", is_list=True, is_object=True)
        assert _sub_model_name("OntapIpSubnet", f) == "OntapIpSubnetIpRange"


class TestHasTypedSubFields:
    def test_true_for_list_object_with_sub_fields(self):
        f = ParsedField(
            name="copies",
            api_path="copies",
            is_list=True,
            is_object=True,
            sub_fields=[
                ParsedField(name="count", api_path="copies.count", python_type="int", default=0)
            ],
        )
        assert _has_typed_sub_fields(f) is True

    def test_false_for_list_without_sub_fields(self):
        f = ParsedField(name="tags", api_path="tags", is_list=True, is_object=False)
        assert _has_typed_sub_fields(f) is False

    def test_false_for_empty_sub_fields(self):
        f = ParsedField(name="copies", api_path="copies", is_list=True, is_object=True)
        assert _has_typed_sub_fields(f) is False

    def test_false_for_only_object_sub_fields(self):
        """If all sub_fields are pure objects (no leaves), return False."""
        f = ParsedField(
            name="copies",
            api_path="copies",
            is_list=True,
            is_object=True,
            sub_fields=[
                ParsedField(name="nested", api_path="copies.nested", is_object=True),
            ],
        )
        assert _has_typed_sub_fields(f) is False


# ---------------------------------------------------------------------------
# Sub-model generation
# ---------------------------------------------------------------------------


def _make_endpoint_with_sub_model(
    path: str = "/storage/snapshot-policies",
) -> ParsedEndpoint:
    """Build an endpoint with an array-of-objects field for sub-model testing."""
    copy_sub_fields = [
        ParsedField(name="count", api_path="copies.count", python_type="int", default=0),
        ParsedField(
            name="schedule",
            api_path="copies.schedule",
            python_type="object",
            is_object=True,
            sub_fields=[
                ParsedField(name="name", api_path="copies.schedule.name", python_type="str"),
            ],
        ),
        ParsedField(name="name", api_path="copies.schedule.name", python_type="str"),
    ]
    return ParsedEndpoint(
        path=path,
        schema_name="snapshot_policy",
        fields=[
            ParsedField(name="uuid", api_path="uuid", python_type="OntapUUID", is_uuid=True),
            ParsedField(name="name", api_path="name", python_type="str"),
            ParsedField(
                name="copies",
                api_path="copies",
                python_type="list[dict[str, Any]]",
                is_list=True,
                is_object=True,
                default=[],
                sub_fields=copy_sub_fields,
            ),
        ],
    )


class TestGenerateModelSubModel:
    def test_sub_model_class_generated(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_model(ep)
        assert "class OntapSnapshotPolicyCopy(CacheModel):" in code

    def test_sub_model_before_parent(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_model(ep)
        sub_pos = code.index("class OntapSnapshotPolicyCopy")
        parent_pos = code.index("class OntapSnapshotPolicy(CacheModel)")
        assert sub_pos < parent_pos

    def test_parent_field_typed_with_sub_model(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_model(ep)
        assert "copies: list[OntapSnapshotPolicyCopy]" in code

    def test_no_any_import_when_all_sub_models_typed(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_model(ep)
        assert "from typing import Any" not in code

    def test_sub_model_has_leaf_fields(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_model(ep)
        # The sub-model should have leaf fields from copies sub_fields
        # Field names use full api_path (dots -> underscores)
        assert "    copies_count: int = 0" in code
        assert "    copies_schedule_name: str" in code

    def test_valid_python(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_model(ep)
        compile(code, "model.py", "exec")


class TestGenerateMappingSubModel:
    def test_transform_function_generated(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_mapping(ep)
        assert "def _transform_copies(record: dict[str, Any])" in code
        assert "OntapSnapshotPolicyCopy(**item)" in code

    def test_field_mapping_uses_transform(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_mapping(ep)
        assert "transform=_transform_copies" in code

    def test_sub_model_imported(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_mapping(ep)
        assert "OntapSnapshotPolicyCopy" in code

    def test_valid_python(self):
        ep = _make_endpoint_with_sub_model()
        code = generate_mapping(ep)
        compile(code, "mapping.py", "exec")


# ---------------------------------------------------------------------------
# _safe_attr_name
# ---------------------------------------------------------------------------


class TestSafeAttrName:
    """Direct tests for _safe_attr_name."""

    def test_python_keyword(self):
        assert _safe_attr_name("class") == "class_"

    def test_pydantic_reserved(self):
        assert _safe_attr_name("model_config") == "model_config_"

    def test_unreserved(self):
        assert _safe_attr_name("name") == "name"

    def test_compound_not_reserved(self):
        assert _safe_attr_name("space_metadata") == "space_metadata"
