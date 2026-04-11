"""Tests for collector endpoint usage and derived field evaluation."""

from __future__ import annotations

import logging
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.collector import MetadataCollector
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.mapping import (
    _is_cloud_node,
    compute_is_cloud,
    compute_is_ha,
)
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.snapshot_policies.mapping import (
    ONTAPSNAPSHOTPOLICY_MAPPING,
)
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse


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
        """CLUSTER_MAPPING declares is_ha as a derived field with a node dependency."""
        from pynetappfoundry.cache.ontap.cluster.mapping import CLUSTER_MAPPING

        derived = CLUSTER_MAPPING.derived_fields()
        by_attr = {f.cache_attr: f for f in derived}
        assert "is_ha" in by_attr
        field = by_attr["is_ha"]
        assert field.cache_strategy == "derived"
        assert field.post_collection is compute_is_ha
        assert field.depends_on == (OntapNodeResponse,)

    def test_cluster_mapping_has_is_cloud_derived_field(self) -> None:
        """CLUSTER_MAPPING declares is_cloud as a derived field with a node dependency."""
        from pynetappfoundry.cache.ontap.cluster.mapping import CLUSTER_MAPPING

        derived = CLUSTER_MAPPING.derived_fields()
        by_attr = {f.cache_attr: f for f in derived}
        assert "is_cloud" in by_attr
        field = by_attr["is_cloud"]
        assert field.cache_strategy == "derived"
        assert field.post_collection is compute_is_cloud
        assert field.depends_on == (OntapNodeResponse,)


# ---------------------------------------------------------------------------
# _is_cloud_node / compute_is_cloud tests (issue #547)
# ---------------------------------------------------------------------------


class TestIsCloudNode:
    """Truth table for :func:`_is_cloud_node`."""

    def test_onprem_node_returns_false(self) -> None:
        """FAS hardware with non-cloud serial is not cloud."""
        node = OntapNodeResponse(name="fas", model_="FAS8200", serial_number="123456789")
        assert _is_cloud_node(node) is False

    def test_cvo_by_model_prefix(self) -> None:
        """CDvM200 model is detected as cloud regardless of serial."""
        node = OntapNodeResponse(name="cvo", model_="CDvM200", serial_number="")
        assert _is_cloud_node(node) is True

    def test_cvo_by_serial_prefix_ha(self) -> None:
        """9092014* HA serial is detected as cloud regardless of model."""
        node = OntapNodeResponse(name="cvo", model_="", serial_number="9092014567")
        assert _is_cloud_node(node) is True

    def test_cvo_by_serial_prefix_single(self) -> None:
        """9092013* single-node serial is detected as cloud."""
        node = OntapNodeResponse(name="cvo", model_="", serial_number="9092013001")
        assert _is_cloud_node(node) is True

    def test_both_populated_cvo(self) -> None:
        """Both fields populated with CVO values is cloud."""
        node = OntapNodeResponse(name="cvo", model_="CDvM200", serial_number="9092014567")
        assert _is_cloud_node(node) is True

    def test_both_empty_returns_false(self) -> None:
        """Empty model + empty serial is not cloud."""
        node = OntapNodeResponse(name="x", model_="", serial_number="")
        assert _is_cloud_node(node) is False

    def test_aff_hardware_returns_false(self) -> None:
        """AFF hardware with on-prem serial is not cloud."""
        node = OntapNodeResponse(name="aff", model_="AFF-A400", serial_number="721234567")
        assert _is_cloud_node(node) is False


class TestComputeIsCloud:
    """Tests for the compute_is_cloud derived field function."""

    def test_empty_nodes_returns_false(self) -> None:
        """No nodes → is_cloud=False."""
        cluster = ClusterInfo(cluster_name="test")
        updated = compute_is_cloud(cluster, {"nodes": []})
        assert updated.is_cloud is False

    def test_all_onprem_returns_false(self) -> None:
        """All on-prem nodes → is_cloud=False."""
        cluster = ClusterInfo(cluster_name="test")
        nodes = [
            OntapNodeResponse(name="n1", model_="FAS8200", serial_number="721234"),
            OntapNodeResponse(name="n2", model_="FAS8200", serial_number="721235"),
        ]
        updated = compute_is_cloud(cluster, {"nodes": nodes})
        assert updated.is_cloud is False

    def test_one_cvo_node_returns_true(self) -> None:
        """Single CVO node → is_cloud=True."""
        cluster = ClusterInfo(cluster_name="test")
        nodes = [OntapNodeResponse(name="cvo", model_="CDvM200")]
        updated = compute_is_cloud(cluster, {"nodes": nodes})
        assert updated.is_cloud is True

    def test_mixed_nodes_returns_true(self) -> None:
        """Mixed set with any CVO node → is_cloud=True."""
        cluster = ClusterInfo(cluster_name="test")
        nodes = [
            OntapNodeResponse(name="fas", model_="FAS8200"),
            OntapNodeResponse(name="cvo", serial_number="9092014999"),
        ]
        updated = compute_is_cloud(cluster, {"nodes": nodes})
        assert updated.is_cloud is True

    def test_reads_registry_key_alias(self) -> None:
        """compute_is_cloud reads either 'OntapNodeResponse' or 'nodes' key."""
        cluster = ClusterInfo(cluster_name="test")
        nodes = [OntapNodeResponse(name="cvo", model_="CDvM200")]
        updated = compute_is_cloud(cluster, {"OntapNodeResponse": nodes})
        assert updated.is_cloud is True

    def test_preserves_other_fields(self) -> None:
        """compute_is_cloud preserves other ClusterInfo fields."""
        cluster = ClusterInfo(cluster_name="prod", ontap_version="9.14.1")
        nodes = [OntapNodeResponse(name="cvo", model_="CDvM200")]
        updated = compute_is_cloud(cluster, {"nodes": nodes})
        assert updated.cluster_name == "prod"
        assert updated.ontap_version == "9.14.1"
        assert updated.is_cloud is True


# ---------------------------------------------------------------------------
# collect_cloud_metadata gating (issue #547)
# ---------------------------------------------------------------------------


class TestCollectCloudMetadataGate:
    """Verify that collect_cloud_metadata gates on node cloud detection."""

    def test_skips_when_no_nodes_in_cache(self) -> None:
        """Empty nodes cache → skip CLI, return []."""
        cli = MagicMock()
        collector = MetadataCollector(api_client=MagicMock(), cli_client=cli)
        collector._results_cache = {"nodes": []}
        result = collector.collect_cloud_metadata()
        assert result == []
        cli.run_command.assert_not_called()

    def test_skips_when_only_onprem_nodes(self) -> None:
        """On-prem nodes only → skip CLI, return []."""
        cli = MagicMock()
        collector = MetadataCollector(api_client=MagicMock(), cli_client=cli)
        collector._results_cache = {"nodes": [OntapNodeResponse(name="fas", model_="FAS8200")]}
        result = collector.collect_cloud_metadata()
        assert result == []
        cli.run_command.assert_not_called()

    def test_proceeds_when_cvo_node_present(self) -> None:
        """Any CVO node → call into CLI path."""
        cli = MagicMock()
        cli.run_command.return_value = ""  # empty → parse_cli_records yields []
        collector = MetadataCollector(api_client=MagicMock(), cli_client=cli)
        collector._results_cache = {"nodes": [OntapNodeResponse(name="cvo", model_="CDvM200")]}
        collector.collect_cloud_metadata()
        cli.run_command.assert_called_once()


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


# ---------------------------------------------------------------------------
# Issue #541: byte-identity regression + parallelism + fetch() integration
# ---------------------------------------------------------------------------


_REFRESH_NODE_UUID_1 = "11111111-1111-1111-1111-111111111111"
_REFRESH_NODE_UUID_2 = "22222222-2222-2222-2222-222222222222"


def _build_mock_api_client() -> Any:
    """Build a mock ONTAP API client whose responses cover the minimum
    surface required by ``collect_all`` (cluster, nodes, all envelope
    phases). All envelope endpoints return an empty records list except
    nodes; cluster returns a populated singleton. Used by the byte-identity
    regression test and the parallelism check.
    """
    cluster_response = {
        "name": "test-cluster",
        "uuid": "33333333-3333-3333-3333-333333333333",
        "version": {
            "full": "NetApp Release 9.14.1",
            "generation": 9,
            "major": 14,
            "minor": 1,
        },
        "contact": "ops@example.com",
        "location": "lab",
    }
    nodes_response = {
        "records": [
            {"name": "node1", "uuid": _REFRESH_NODE_UUID_1},
            {"name": "node2", "uuid": _REFRESH_NODE_UUID_2},
        ],
        "num_records": 2,
    }
    empty_envelope = {"records": [], "num_records": 0}

    client = MagicMock()

    def fake_call_endpoint(url: str, method: str = "GET") -> Any:
        if url.startswith("/cluster?"):
            return cluster_response
        return None

    def fake_get_all_records(url: str, method: str = "GET") -> Any:
        if "/cluster/nodes" in url:
            return nodes_response
        return empty_envelope

    client.call_endpoint = MagicMock(side_effect=fake_call_endpoint)
    client.get_all_records = MagicMock(side_effect=fake_get_all_records)
    return client


class TestCollectAllByteIdentity:
    """Issue #541 regression: collect_all() output must remain stable.

    The byte-identity guarantee is that successive runs against an
    identical mock response set produce identical JSON dumps (excluding
    the cluster-level ``cached_at`` timestamp). This catches accidental
    ordering, default-value, or exception-path drift introduced by the
    fetch() refactor.
    """

    def test_collect_all_is_deterministic(self) -> None:
        """Two collect_all() runs against the same mock data agree byte-for-byte."""
        client_a = _build_mock_api_client()
        collector_a = MetadataCollector(api_client=client_a, parallel=False)
        result_a = collector_a.collect_all("test-cluster")

        client_b = _build_mock_api_client()
        collector_b = MetadataCollector(api_client=client_b, parallel=False)
        result_b = collector_b.collect_all("test-cluster")

        json_a = result_a.model_dump_json(exclude={"cached_at"})
        json_b = result_b.model_dump_json(exclude={"cached_at"})
        assert json_a == json_b

    def test_collect_all_populates_expected_shape(self) -> None:
        """The collected metadata exposes the cluster, nodes, and is_ha."""
        client = _build_mock_api_client()
        collector = MetadataCollector(api_client=client, parallel=False)
        result = collector.collect_all("test-cluster")

        assert result.cluster_name == "test-cluster"
        assert result.cluster.cluster_name == "test-cluster"
        assert result.cluster.cluster_uuid == "33333333-3333-3333-3333-333333333333"
        assert len(result.nodes) == 2
        # is_ha is a derived field — must be True given two nodes.
        assert result.cluster.is_ha is True
        # Composite phases default to empty containers (no records).
        assert result.storage.aggregates == []
        assert result.storage.volumes == []
        assert result.network.ip_interfaces == []
        assert result.protocols.cifs_shares == []
        assert result.relationships.snapmirror_destinations == []

    def test_collect_all_parallel_matches_sequential(self) -> None:
        """Parallel and sequential modes produce the same JSON dump."""
        client_seq = _build_mock_api_client()
        seq_result = MetadataCollector(api_client=client_seq, parallel=False).collect_all(
            "test-cluster"
        )
        client_par = _build_mock_api_client()
        par_result = MetadataCollector(
            api_client=client_par, parallel=True, max_workers=4
        ).collect_all("test-cluster")
        assert seq_result.model_dump_json(exclude={"cached_at"}) == par_result.model_dump_json(
            exclude={"cached_at"}
        )


class TestCollectorParallelism:
    """Issue #541: composite phase methods still submit per-model fetches in parallel."""

    def test_storage_phase_submits_one_task_per_submodel(self) -> None:
        """The storage composite submits 11 fetch() calls — one per sub-model."""
        client = _build_mock_api_client()
        collector = MetadataCollector(api_client=client, parallel=True, max_workers=11)
        # Track every _fetch_model invocation; the storage composite is the
        # one that exercises the executor path with 11 tasks.
        call_log: list[type[BaseModel]] = []
        original_fetch_model = collector._fetch_model

        def tracking_fetch(mc: type[BaseModel]) -> Any:
            call_log.append(mc)
            return original_fetch_model(mc)

        with patch.object(collector, "_fetch_model", side_effect=tracking_fetch):
            collector._cluster_name = "test"
            collector._collect_storage_via_api()

        # Storage phase has 11 sub-models per the model_tasks list.
        assert len(call_log) == 11

    def test_network_phase_submits_four_model_tasks(self) -> None:
        """Network composite still issues a model task per sub-model."""
        client = _build_mock_api_client()
        collector = MetadataCollector(api_client=client, parallel=True, max_workers=5)
        call_log: list[type[BaseModel]] = []
        original_fetch_model = collector._fetch_model

        def tracking_fetch(mc: type[BaseModel]) -> Any:
            call_log.append(mc)
            return original_fetch_model(mc)

        with patch.object(collector, "_fetch_model", side_effect=tracking_fetch):
            collector._cluster_name = "test"
            collector._collect_network_via_api()
        # Network composite has 4 model-fetch tasks (LIFs, BCDs, DNS, subnets);
        # the IPspaces endpoint is fetched separately as a raw API call.
        assert len(call_log) == 4


class TestEvaluateDerivedFieldsStillRuns:
    """Issue #541: ``_evaluate_derived_fields`` continues to run for non-cluster
    mappings whose derived fields are not routed through the inline fetch
    hook path.
    """

    def test_synthetic_derived_field_still_evaluated_after_collect(self) -> None:
        """A registered synthetic derived field is invoked by _evaluate_derived_fields."""
        invocations: list[str] = []

        def post_fn(item: _DerivedModel, results: dict[str, Any]) -> _DerivedModel:
            invocations.append(item.name)
            return item.model_copy(update={"computed": 99})

        mapping = TypeMapping(
            name="DerivedMapping541",
            model_class=_DerivedModel,
            api_endpoint="/x",
            fields=(
                FieldMapping(cache_attr="name", api_path="name"),
                FieldMapping(
                    cache_attr="computed",
                    cache_strategy="derived",
                    post_collection=post_fn,
                ),
            ),
        )
        model_registry.register_mapping("DerivedMapping541", mapping)
        try:
            collector = MetadataCollector(api_client=None)
            with patch.object(
                MetadataCollector,
                "_MAPPING_RESULTS_KEYS",
                [("DerivedMapping541", "synthetic")],
            ):
                results: dict[str, Any] = {"synthetic": _DerivedModel(name="thing")}
                updated = collector._evaluate_derived_fields(results)
            assert invocations == ["thing"]
            assert updated["synthetic"].computed == 99
        finally:
            model_registry._mappings.pop("DerivedMapping541", None)
            model_registry._mappings_by_class.pop(_DerivedModel, None)
