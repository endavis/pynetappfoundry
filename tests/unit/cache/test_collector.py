"""Tests for collector endpoint usage and derived field evaluation."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.collector import MetadataCollector
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.mapping import compute_is_ha
from pynetappfoundry.cache.ontap.cluster.model import ClusterInfo
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.snapshot_policies.mapping import (
    ONTAPSNAPSHOTPOLICY_MAPPING,
)


class TestCollectorMappingEndpoints:
    """Verify that collector-relevant mappings have correct endpoints."""

    def test_snapshot_policies_api_endpoint_simplified(self) -> None:
        """Snapshot-policies api_endpoint is now simplified to ?fields=*."""
        assert ONTAPSNAPSHOTPOLICY_MAPPING.api_endpoint == "/storage/snapshot-policies?fields=*"

    def test_snapshot_policies_build_collection_url_includes_copies(self) -> None:
        """build_collection_url() dynamically appends copies."""
        url = ONTAPSNAPSHOTPOLICY_MAPPING.build_collection_url()
        assert ",copies" in url

    def test_snapshot_policies_collection_url(self) -> None:
        """Snapshot-policies build_collection_url() has the expected full URL."""
        assert (
            ONTAPSNAPSHOTPOLICY_MAPPING.build_collection_url()
            == "/storage/snapshot-policies?fields=*,copies"
        )

    def test_export_policies_bulk_endpoint(self) -> None:
        """Export-policies api_endpoint has no {id} placeholder."""
        assert "{" not in ONTAPEXPORTPOLICY_MAPPING.api_endpoint

    def test_export_policies_api_endpoint_simplified(self) -> None:
        """Export-policies api_endpoint is now simplified to ?fields=*."""
        assert ONTAPEXPORTPOLICY_MAPPING.api_endpoint == "/protocols/nfs/export-policies?fields=*"

    def test_export_policies_build_collection_url(self) -> None:
        """build_collection_url() returns base endpoint (no expensive fields annotated)."""
        url = ONTAPEXPORTPOLICY_MAPPING.build_collection_url()
        assert url == "/protocols/nfs/export-policies?fields=*"

    def test_export_policies_records_path(self) -> None:
        """Export-policies mapping uses standard records path."""
        assert ONTAPEXPORTPOLICY_MAPPING.records_path == "records"

    def test_export_policies_no_parent_mapping(self) -> None:
        """Export-policies mapping has no parent_mapping for bulk collection."""
        assert ONTAPEXPORTPOLICY_MAPPING.parent_mapping is None

    def test_snapshot_policies_copies_requires_explicit_fetch(self) -> None:
        """Snapshot-policies copies field has requires_explicit_fetch=True."""
        copies_field = next(
            f for f in ONTAPSNAPSHOTPOLICY_MAPPING.fields if f.cache_attr == "copies"
        )
        assert copies_field.requires_explicit_fetch is True


# ---------------------------------------------------------------------------
# _SampleModel for derived-field tests
# ---------------------------------------------------------------------------


class _DerivedModel(BaseModel):
    """Minimal model for derived field tests."""

    name: str = ""
    computed: int = 0


# ---------------------------------------------------------------------------
# compute_is_ha tests
# ---------------------------------------------------------------------------


class TestComputeIsHa:
    """Tests for the compute_is_ha derived field function."""

    def test_is_ha_true_multi_node(self) -> None:
        """2+ nodes sets is_ha=True."""
        cluster = ClusterInfo(cluster_name="test")
        results: dict[str, Any] = {"nodes": ["node1", "node2"]}
        updated = compute_is_ha(cluster, results)
        assert updated.is_ha is True

    def test_is_ha_false_single_node(self) -> None:
        """1 node sets is_ha=False."""
        cluster = ClusterInfo(cluster_name="test")
        results: dict[str, Any] = {"nodes": ["node1"]}
        updated = compute_is_ha(cluster, results)
        assert updated.is_ha is False

    def test_is_ha_false_no_nodes(self) -> None:
        """Empty nodes list sets is_ha=False."""
        cluster = ClusterInfo(cluster_name="test")
        results: dict[str, Any] = {"nodes": []}
        updated = compute_is_ha(cluster, results)
        assert updated.is_ha is False

    def test_is_ha_false_missing_nodes_key(self) -> None:
        """Missing 'nodes' key in results sets is_ha=False."""
        cluster = ClusterInfo(cluster_name="test")
        results: dict[str, Any] = {}
        updated = compute_is_ha(cluster, results)
        assert updated.is_ha is False

    def test_preserves_other_fields(self) -> None:
        """compute_is_ha preserves other ClusterInfo fields."""
        cluster = ClusterInfo(cluster_name="prod", ontap_version="9.14.1")
        results: dict[str, Any] = {"nodes": ["n1", "n2"]}
        updated = compute_is_ha(cluster, results)
        assert updated.cluster_name == "prod"
        assert updated.ontap_version == "9.14.1"
        assert updated.is_ha is True


# ---------------------------------------------------------------------------
# _evaluate_derived_fields tests
# ---------------------------------------------------------------------------


class TestEvaluateDerivedFields:
    """Tests for MetadataCollector._evaluate_derived_fields."""

    @pytest.fixture
    def collector(self) -> MetadataCollector:
        """Collector with no clients (for unit testing derived evaluation)."""
        return MetadataCollector(api_client=None, cli_client=None)

    def test_derived_fields_evaluated_for_singular_result(
        self, collector: MetadataCollector
    ) -> None:
        """Derived field is evaluated on a singular (non-list) result."""
        call_log: list[str] = []

        def post_fn(item: _DerivedModel, results: dict[str, Any]) -> _DerivedModel:
            call_log.append(item.name)
            return item.model_copy(update={"computed": 42})

        mapping = TypeMapping(
            name="TestSingular",
            model_class=_DerivedModel,
            api_endpoint="/t",
            fields=(
                FieldMapping(cache_attr="name", api_path="name"),
                FieldMapping(
                    cache_attr="computed",
                    cache_strategy="derived",
                    post_collection=post_fn,
                ),
            ),
        )
        model_registry.register_mapping("TestSingular", mapping)
        try:
            with patch.object(
                MetadataCollector,
                "_MAPPING_RESULTS_KEYS",
                [("TestSingular", "test_singular")],
            ):
                results: dict[str, Any] = {
                    "test_singular": _DerivedModel(name="item1"),
                }
                updated = collector._evaluate_derived_fields(results)
                assert updated["test_singular"].computed == 42
                assert call_log == ["item1"]
        finally:
            model_registry._mappings.pop("TestSingular", None)

    def test_derived_fields_evaluated_for_list_results(self, collector: MetadataCollector) -> None:
        """Derived field is evaluated on each item in a list result."""

        def post_fn(item: _DerivedModel, results: dict[str, Any]) -> _DerivedModel:
            return item.model_copy(update={"computed": len(results.get("other", []))})

        mapping = TypeMapping(
            name="TestList",
            model_class=_DerivedModel,
            api_endpoint="/t",
            fields=(
                FieldMapping(cache_attr="name", api_path="name"),
                FieldMapping(
                    cache_attr="computed",
                    cache_strategy="derived",
                    post_collection=post_fn,
                ),
            ),
        )
        model_registry.register_mapping("TestList", mapping)
        try:
            with patch.object(
                MetadataCollector,
                "_MAPPING_RESULTS_KEYS",
                [("TestList", "test_list")],
            ):
                results: dict[str, Any] = {
                    "test_list": [
                        _DerivedModel(name="a"),
                        _DerivedModel(name="b"),
                    ],
                    "other": [1, 2, 3],
                }
                updated = collector._evaluate_derived_fields(results)
                assert len(updated["test_list"]) == 2
                assert updated["test_list"][0].computed == 3
                assert updated["test_list"][1].computed == 3
        finally:
            model_registry._mappings.pop("TestList", None)

    def test_derived_fields_skips_missing_post_collection(
        self, collector: MetadataCollector
    ) -> None:
        """Derived field with no post_collection callable is skipped."""
        mapping = TypeMapping(
            name="TestNoCallable",
            model_class=_DerivedModel,
            api_endpoint="/t",
            fields=(
                FieldMapping(cache_attr="name", api_path="name"),
                FieldMapping(
                    cache_attr="computed",
                    cache_strategy="derived",
                    # No post_collection set
                ),
            ),
        )
        model_registry.register_mapping("TestNoCallable", mapping)
        try:
            with patch.object(
                MetadataCollector,
                "_MAPPING_RESULTS_KEYS",
                [("TestNoCallable", "test_no_callable")],
            ):
                original = _DerivedModel(name="x", computed=0)
                results: dict[str, Any] = {"test_no_callable": original}
                updated = collector._evaluate_derived_fields(results)
                # Should be unchanged
                assert updated["test_no_callable"].computed == 0
        finally:
            model_registry._mappings.pop("TestNoCallable", None)

    def test_derived_field_error_propagates(self, collector: MetadataCollector) -> None:
        """Bad post_collection callable raises and is logged."""

        def bad_fn(item: _DerivedModel, results: dict[str, Any]) -> _DerivedModel:
            raise ValueError("boom")

        mapping = TypeMapping(
            name="TestBad",
            model_class=_DerivedModel,
            api_endpoint="/t",
            fields=(
                FieldMapping(
                    cache_attr="computed",
                    cache_strategy="derived",
                    post_collection=bad_fn,
                ),
            ),
        )
        model_registry.register_mapping("TestBad", mapping)
        try:
            with patch.object(
                MetadataCollector,
                "_MAPPING_RESULTS_KEYS",
                [("TestBad", "test_bad")],
            ):
                results: dict[str, Any] = {"test_bad": _DerivedModel(name="x")}
                with pytest.raises(ValueError, match="boom"):
                    collector._evaluate_derived_fields(results)
        finally:
            model_registry._mappings.pop("TestBad", None)

    def test_skips_missing_results_key(self, collector: MetadataCollector) -> None:
        """Mapping whose results key is absent from results dict is skipped."""
        results: dict[str, Any] = {"other_key": "something"}
        # Should not raise even though _MAPPING_RESULTS_KEYS references keys not in results
        updated = collector._evaluate_derived_fields(results)
        assert updated == results

    def test_skips_unregistered_mapping(self, collector: MetadataCollector) -> None:
        """Mapping name not in registry is skipped."""
        with patch.object(
            MetadataCollector,
            "_MAPPING_RESULTS_KEYS",
            [("NonexistentMapping", "some_key")],
        ):
            results: dict[str, Any] = {"some_key": _DerivedModel(name="x")}
            updated = collector._evaluate_derived_fields(results)
            # Should be unchanged
            assert updated["some_key"].name == "x"


# ---------------------------------------------------------------------------
# Cluster mapping is_ha integration test
# ---------------------------------------------------------------------------


class TestClusterMappingIsHa:
    """Verify the is_ha derived field is declared on CLUSTER_MAPPING."""

    def test_cluster_mapping_has_is_ha_derived_field(self) -> None:
        """CLUSTER_MAPPING declares is_ha as a derived field."""
        from pynetappfoundry.cache.ontap.cluster.mapping import CLUSTER_MAPPING

        derived = CLUSTER_MAPPING.derived_fields()
        assert len(derived) == 1
        assert derived[0].cache_attr == "is_ha"
        assert derived[0].cache_strategy == "derived"
        assert derived[0].post_collection is compute_is_ha
