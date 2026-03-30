"""Tests for collector endpoint usage and derived field evaluation."""

from __future__ import annotations

import logging
from typing import Any
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.collector import MetadataCollector
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.mapping import compute_is_ha
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.snapshot_policies.mapping import (
    ONTAPSNAPSHOTPOLICY_MAPPING,
)
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo


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


# ---------------------------------------------------------------------------
# _collect_parameterized tests
# ---------------------------------------------------------------------------


class _ParentModel(BaseModel):
    """Parent model with uuid for parameterized tests."""

    name: str = ""
    uuid: str = ""


class _ChildModel(BaseModel):
    """Child model for parameterized tests."""

    name: str = ""
    parent_uuid: str = ""


_CHILD_MAPPING = TypeMapping(
    name="Child",
    model_class=_ChildModel,
    api_endpoint="/parents/{parent.uuid}/children?fields=*",
    fields=(
        FieldMapping(cache_attr="name", api_path="name"),
        FieldMapping(cache_attr="parent_uuid", api_path="parent.uuid", default=""),
    ),
    parent_mapping="Parent",
    parent_id_field="uuid",
)


class TestCollectParameterized:
    """Tests for MetadataCollector._collect_parameterized."""

    @pytest.fixture
    def collector(self) -> MetadataCollector:
        """Collector with no clients (for unit testing)."""
        return MetadataCollector(api_client=None, cli_client=None)

    def test_iterates_parents_aggregates_results(self, collector: MetadataCollector) -> None:
        """2 parents each returning 2 children → 4 total."""
        parents = [
            _ParentModel(name="p1", uuid="uuid-1"),
            _ParentModel(name="p2", uuid="uuid-2"),
        ]
        responses = {
            "/parents/uuid-1/children?fields=*": {
                "records": [
                    {"name": "c1", "parent": {"uuid": "uuid-1"}},
                    {"name": "c2", "parent": {"uuid": "uuid-1"}},
                ],
            },
            "/parents/uuid-2/children?fields=*": {
                "records": [
                    {"name": "c3", "parent": {"uuid": "uuid-2"}},
                    {"name": "c4", "parent": {"uuid": "uuid-2"}},
                ],
            },
        }

        with patch.object(
            collector, "_cached_api_call", side_effect=lambda url, **kw: responses[url]
        ):
            result = collector._collect_parameterized(_CHILD_MAPPING, parents)
        assert len(result) == 4
        names = [r.name for r in result]  # type: ignore[attr-defined]
        assert names == ["c1", "c2", "c3", "c4"]

    def test_empty_parent_list_returns_empty(self, collector: MetadataCollector) -> None:
        """No parents → empty list."""
        result = collector._collect_parameterized(_CHILD_MAPPING, [])
        assert result == []

    def test_parent_missing_id_field_skipped(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Parent without the id attr → logged warning, skipped."""
        # _ParentModel has uuid="" by default (empty → falsy → skip)
        parents = [_ParentModel(name="no-uuid")]

        with caplog.at_level(logging.WARNING):
            result = collector._collect_parameterized(_CHILD_MAPPING, parents)
        assert result == []
        assert any("SKIP_PARENT" in r.message for r in caplog.records)

    def test_parent_empty_id_skipped(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Parent with empty string id → skipped."""
        parents = [_ParentModel(name="empty-uuid", uuid="")]

        with caplog.at_level(logging.WARNING):
            result = collector._collect_parameterized(_CHILD_MAPPING, parents)
        assert result == []
        assert any("SKIP_PARENT" in r.message for r in caplog.records)

    def test_failed_child_fetch_continues(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """API error on one parent → warns, continues, returns partial results."""
        parents = [
            _ParentModel(name="p1", uuid="uuid-1"),
            _ParentModel(name="p2", uuid="uuid-2"),
        ]

        def side_effect(url: str, **kw: Any) -> dict[str, Any]:
            if "uuid-1" in url:
                raise ConnectionError("timeout")
            return {"records": [{"name": "c1", "parent": {"uuid": "uuid-2"}}]}

        with (
            caplog.at_level(logging.WARNING),
            patch.object(collector, "_cached_api_call", side_effect=side_effect),
        ):
            result = collector._collect_parameterized(_CHILD_MAPPING, parents)
        assert len(result) == 1
        assert any("CHILD_FETCH_FAILED" in r.message for r in caplog.records)

    def test_raises_if_no_parent_mapping(self, collector: MetadataCollector) -> None:
        """parent_mapping=None → ValueError."""
        mapping = TypeMapping(
            name="Bad",
            model_class=_ChildModel,
            api_endpoint="/bad",
            fields=(),
            parent_mapping=None,
            parent_id_field="uuid",
        )
        with pytest.raises(ValueError, match="parent_mapping must be set"):
            collector._collect_parameterized(mapping, [])

    def test_raises_if_no_parent_id_field(self, collector: MetadataCollector) -> None:
        """parent_id_field=None → ValueError."""
        mapping = TypeMapping(
            name="Bad",
            model_class=_ChildModel,
            api_endpoint="/bad",
            fields=(),
            parent_mapping="Parent",
            parent_id_field=None,
        )
        with pytest.raises(ValueError, match="parent_id_field must be set"):
            collector._collect_parameterized(mapping, [])


# ---------------------------------------------------------------------------
# _collect_svm_top_metrics_users integration tests
# ---------------------------------------------------------------------------


class TestCollectSvmTopMetricsUsers:
    """Tests for MetadataCollector._collect_svm_top_metrics_users."""

    @pytest.fixture
    def collector(self) -> MetadataCollector:
        """Collector with no clients (for unit testing)."""
        return MetadataCollector(api_client=None, cli_client=None)

    def test_returns_empty_without_api_client(self, collector: MetadataCollector) -> None:
        """No API client → empty list without attempting collection."""
        from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm

        svms = [OntapSvm(name="svm1", uuid="uuid-1")]
        result = collector._collect_svm_top_metrics_users(svms)
        assert result == []

    def test_delegates_to_collect_parameterized(self, collector: MetadataCollector) -> None:
        """Delegates to _collect_parameterized with correct mapping and parents."""
        from pynetappfoundry.cache.ontap.svm.svms.top_metrics.users.mapping import (
            ONTAPTOPMETRICSSVMUSER_MAPPING,
        )
        from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm

        svms = [OntapSvm(name="svm1", uuid="uuid-1")]
        captured_args: list[tuple[Any, Any]] = []

        def fake_collect_parameterized(mapping: Any, parents: Any) -> list[Any]:
            captured_args.append((mapping, parents))
            return []

        collector.api_client = True  # type: ignore[assignment]
        with patch.object(
            collector, "_collect_parameterized", side_effect=fake_collect_parameterized
        ):
            collector._collect_svm_top_metrics_users(svms)

        assert len(captured_args) == 1
        assert captured_args[0][0] is ONTAPTOPMETRICSSVMUSER_MAPPING
        assert captured_args[0][1] is svms
