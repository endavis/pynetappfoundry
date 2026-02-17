"""Tests for cache database schema generation."""

from __future__ import annotations

import sqlite3

from pydantic import BaseModel, Field

from pynetappfoundry.cache._base import OntapUUID
from pynetappfoundry.cache.db_schema import (
    TableSpec,
    _python_type_to_sql,
    build_table_registry,
    generate_cluster_name_index_ddl,
    generate_table_ddl,
    generate_uuid_column_index_ddl,
)


class TestPythonTypeToSql:
    """Tests for _python_type_to_sql type mapping."""

    def test_str_maps_to_text(self) -> None:
        assert _python_type_to_sql(str) == "TEXT"

    def test_ontap_uuid_maps_to_text(self) -> None:
        assert _python_type_to_sql(OntapUUID) == "TEXT"

    def test_int_maps_to_integer(self) -> None:
        assert _python_type_to_sql(int) == "INTEGER"

    def test_bool_maps_to_integer(self) -> None:
        assert _python_type_to_sql(bool) == "INTEGER"

    def test_float_maps_to_real(self) -> None:
        assert _python_type_to_sql(float) == "REAL"

    def test_list_maps_to_text(self) -> None:
        assert _python_type_to_sql(list[str]) == "TEXT"

    def test_dict_maps_to_text(self) -> None:
        assert _python_type_to_sql(dict[str, int]) == "TEXT"

    def test_basemodel_maps_to_text(self) -> None:
        class Nested(BaseModel):
            x: int = 0

        assert _python_type_to_sql(Nested) == "TEXT"

    def test_datetime_maps_to_text(self) -> None:
        from datetime import datetime

        assert _python_type_to_sql(datetime) == "TEXT"


class _SimpleModel(BaseModel):
    """A model without uuid for DDL tests."""

    name: str = ""
    count: int = 0
    active: bool = False


class _UUIDModel(BaseModel):
    """A model with uuid for DDL tests."""

    uuid: str = ""
    name: str = ""
    tags: list[str] = Field(default_factory=list)


class TestGenerateTableDdl:
    """Tests for generate_table_ddl."""

    def test_simple_model_has_row_id(self) -> None:
        """Non-UUID model gets _row_id as PK."""
        ddl = generate_table_ddl("simple", _SimpleModel)
        assert "_row_id INTEGER PRIMARY KEY AUTOINCREMENT" in ddl
        assert "cluster_name TEXT NOT NULL" in ddl

    def test_uuid_model_has_row_id(self) -> None:
        """UUID model also gets _row_id (not composite PK) to avoid empty-uuid collisions."""
        ddl = generate_table_ddl("uuidmodel", _UUIDModel)
        assert "_row_id INTEGER PRIMARY KEY AUTOINCREMENT" in ddl

    def test_extra_json_column_present(self) -> None:
        """Every table should have _extra_json column."""
        ddl = generate_table_ddl("simple", _SimpleModel)
        assert "_extra_json TEXT DEFAULT NULL" in ddl

    def test_model_fields_present(self) -> None:
        """All model fields should appear as columns."""
        ddl = generate_table_ddl("simple", _SimpleModel)
        assert '"name" TEXT' in ddl
        assert '"count" INTEGER' in ddl
        assert '"active" INTEGER' in ddl

    def test_list_field_is_text(self) -> None:
        """List fields should be TEXT (for JSON storage)."""
        ddl = generate_table_ddl("uuidmodel", _UUIDModel)
        assert '"tags" TEXT' in ddl

    def test_ddl_is_valid_sql(self) -> None:
        """Generated DDL should execute without error."""
        conn = sqlite3.connect(":memory:")
        ddl = generate_table_ddl("test_table", _SimpleModel)
        conn.execute(ddl)
        conn.close()

    def test_model_with_cluster_name_field(self) -> None:
        """Model that has its own cluster_name should not duplicate the column."""

        class ModelWithClusterName(BaseModel):
            cluster_name: str = ""
            value: int = 0

        ddl = generate_table_ddl("test_cn", ModelWithClusterName)
        # Should have exactly one cluster_name column
        assert ddl.count("cluster_name") == 1

    def test_reserved_word_field_is_quoted(self) -> None:
        """Fields with SQLite reserved names should be quoted."""

        class ModelWithIndex(BaseModel):
            index: int = 0
            order: str = ""

        ddl = generate_table_ddl("reserved", ModelWithIndex)
        conn = sqlite3.connect(":memory:")
        conn.execute(ddl)  # Should not raise
        conn.close()


class TestGenerateIndexDdl:
    """Tests for index DDL generation."""

    def test_cluster_name_index(self) -> None:
        ddl = generate_cluster_name_index_ddl("mytable")
        assert "CREATE INDEX" in ddl
        assert "idx_mytable_cluster" in ddl
        assert '"cluster_name"' in ddl

    def test_uuid_column_index(self) -> None:
        ddl = generate_uuid_column_index_ddl("mytable")
        assert "CREATE INDEX" in ddl
        assert "idx_mytable_uuid" in ddl
        assert '"uuid"' in ddl


class TestBuildTableRegistry:
    """Tests for build_table_registry."""

    def test_registry_is_nonempty(self) -> None:
        registry = build_table_registry()
        assert len(registry) > 0

    def test_all_entries_are_table_specs(self) -> None:
        registry = build_table_registry()
        for spec in registry.values():
            assert isinstance(spec, TableSpec)

    def test_known_paths_present(self) -> None:
        """Known top-level and nested paths should be in the registry."""
        registry = build_table_registry()
        expected_paths = [
            "cloud",
            "cluster",
            "nodes",
            "mediator",
            "license_packages",
            "storage.volumes",
            "storage.aggregates",
            "storage.svms",
            "network.ip_interfaces",
            "network.dns",
            "protocols.nfs_export_policies",
            "protocols.cifs_shares",
            "relationships.snapmirror_destinations",
            "relationships.cluster_peers",
            "relationships.svm_peers",
        ]
        for path in expected_paths:
            assert path in registry, f"Missing path: {path}"

    def test_list_fields_marked_is_list(self) -> None:
        registry = build_table_registry()
        assert registry["nodes"].is_list is True
        assert registry["storage.volumes"].is_list is True

    def test_singleton_fields_marked_not_list(self) -> None:
        registry = build_table_registry()
        assert registry["cluster"].is_list is False
        assert registry["mediator"].is_list is False

    def test_uuid_fields_detected(self) -> None:
        registry = build_table_registry()
        # OntapNodeResponse has uuid field
        assert registry["nodes"].has_uuid is True
        # CloudMetadata does NOT have uuid field
        assert registry["cloud"].has_uuid is False

    def test_skip_metadata_fields(self) -> None:
        """cluster_name, cached_at, cache_version should not be in registry."""
        registry = build_table_registry()
        assert "cluster_name" not in registry
        assert "cached_at" not in registry
        assert "cache_version" not in registry

    def test_table_names_are_lowercase(self) -> None:
        registry = build_table_registry()
        for spec in registry.values():
            assert spec.table_name == spec.table_name.lower()

    def test_all_ddl_is_valid_sql(self) -> None:
        """Every table in the registry should produce valid DDL."""
        registry = build_table_registry()
        conn = sqlite3.connect(":memory:")
        for spec in registry.values():
            ddl = generate_table_ddl(spec.table_name, spec.model_class)
            conn.execute(ddl)
        conn.close()
