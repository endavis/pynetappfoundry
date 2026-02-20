"""Tests for cache diff engine."""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.diff import (
    _ENTITY_CONFIGS,
    EntityConfig,
    _diff_cluster_info,
    _diff_entity_list,
    _diff_mediator_info,
    _get_display_name,
    _get_entities,
    _get_tracked_fields,
    compute_diff,
    format_diff_summary,
)
from pynetappfoundry.cache.ontap.cluster.mediators.model import OntapMediatorResponse
from pynetappfoundry.cache.ontap.cluster.model import ClusterInfo
from pynetappfoundry.cache.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.model import OntapExportPolicy
from pynetappfoundry.cache.ontap.snapmirror.relationships.model import (
    OntapSnapmirrorRelationship,
)
from pynetappfoundry.cache.ontap.storage.aggregates.model import OntapAggregate

# ---------------------------------------------------------------------------
# Constants — valid UUID strings for OntapUUID-validated fields
# ---------------------------------------------------------------------------

UUID1 = "00000000-0000-0000-0000-000000000001"
UUID2 = "00000000-0000-0000-0000-000000000002"
UUID3 = "00000000-0000-0000-0000-000000000003"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_metadata(**kwargs: Any) -> CachedClusterMetadata:
    """Create a CachedClusterMetadata with sensible defaults."""
    defaults: dict[str, Any] = {"cluster_name": "test-cluster"}
    defaults.update(kwargs)
    return CachedClusterMetadata(**defaults)


def _node(uuid: str, name: str, **kw: Any) -> OntapNodeResponse:
    return OntapNodeResponse(uuid=uuid, name=name, **kw)


def _aggregate(uuid: str, name: str, **kw: Any) -> OntapAggregate:
    return OntapAggregate(uuid=uuid, name=name, **kw)


def _snapmirror(uuid: str, source_path: str, destination_path: str) -> OntapSnapmirrorRelationship:
    return OntapSnapmirrorRelationship(
        uuid=uuid,
        source_path=source_path,
        destination_path=destination_path,
    )


# ---------------------------------------------------------------------------
# TestGetEntities
# ---------------------------------------------------------------------------


class TestGetEntities:
    """Verify _get_entities() path resolution."""

    def test_top_level_list(self) -> None:
        """'nodes' resolves to metadata.nodes."""
        md = _make_metadata(nodes=[_node(UUID1, "n1")])
        result = _get_entities(md, "nodes")
        assert len(result) == 1
        assert result[0].name == "n1"

    def test_nested_list(self) -> None:
        """'storage.aggregates' resolves to metadata.storage.aggregates."""
        from pynetappfoundry.cache.ontap.storage.model import StorageInfo

        aggr = _aggregate(UUID1, "aggr1")
        md = _make_metadata(storage=StorageInfo(aggregates=[aggr]))
        result = _get_entities(md, "storage.aggregates")
        assert len(result) == 1
        assert result[0].name == "aggr1"

    def test_missing_path_returns_empty(self) -> None:
        """Nonexistent path returns []."""
        md = _make_metadata()
        result = _get_entities(md, "nonexistent.path")
        assert result == []

    def test_none_intermediate_returns_empty(self) -> None:
        """Path through None intermediate returns []."""
        md = _make_metadata()
        # Force an intermediate to None via object manipulation
        object.__setattr__(md, "storage", None)
        result = _get_entities(md, "storage.aggregates")
        assert result == []


# ---------------------------------------------------------------------------
# TestGetTrackedFields
# ---------------------------------------------------------------------------


class TestGetTrackedFields:
    """Verify _get_tracked_fields()."""

    def test_excludes_key_field(self) -> None:
        """key_field is excluded from tracked fields."""
        config = EntityConfig(
            key_field="uuid",
            model_class=OntapNodeResponse,
            display_field="name",
        )
        tracked = _get_tracked_fields(config)
        assert "uuid" not in tracked

    def test_returns_all_other_fields(self) -> None:
        """All non-key fields are returned."""
        config = EntityConfig(
            key_field="uuid",
            model_class=OntapNodeResponse,
            display_field="name",
        )
        tracked = _get_tracked_fields(config)
        all_fields = list(OntapNodeResponse.model_fields)
        expected = [f for f in all_fields if f != "uuid"]
        assert tracked == expected


# ---------------------------------------------------------------------------
# TestGetDisplayName
# ---------------------------------------------------------------------------


class TestGetDisplayName:
    """Verify _get_display_name()."""

    def test_simple_attribute(self) -> None:
        """Plain attribute name lookup."""
        node = _node(UUID1, "node-1")
        assert _get_display_name(node, "name") == "node-1"

    def test_format_template(self) -> None:
        """{source_path}->{destination_path} style template."""
        sm = _snapmirror(UUID1, "svm1:vol1", "svm2:vol2")
        result = _get_display_name(sm, "{source_path}->{destination_path}")
        assert result == "svm1:vol1->svm2:vol2"

    def test_int_display_field_zero(self) -> None:
        """Int display_field with value 0 returns '0', not model repr."""
        policy = OntapExportPolicy(index=0)
        result = _get_display_name(policy, "index")
        assert result == "0"

    def test_missing_attribute_fallback(self) -> None:
        """Falls back to str(entity) when attribute is empty."""
        node = _node(UUID1, "")
        result = _get_display_name(node, "name")
        # name is empty string, so falls back to str(entity)
        assert result == str(node)


# ---------------------------------------------------------------------------
# TestDiffEntityList
# ---------------------------------------------------------------------------


class TestDiffEntityList:
    """Verify _diff_entity_list()."""

    @pytest.fixture
    def node_config(self) -> EntityConfig:
        return EntityConfig(
            key_field="uuid",
            model_class=OntapNodeResponse,
            display_field="name",
        )

    def test_no_changes(self, node_config: EntityConfig) -> None:
        """Identical lists produce empty diff."""
        nodes = [_node(UUID1, "n1")]
        changes = _diff_entity_list("nodes", nodes, nodes, node_config)
        assert changes == []

    def test_entity_added(self, node_config: EntityConfig) -> None:
        """New entity detected as 'added'."""
        before: list[Any] = []
        after = [_node(UUID1, "n1")]
        changes = _diff_entity_list("nodes", before, after, node_config)
        assert len(changes) == 1
        assert changes[0]["type"] == "added"
        assert changes[0]["entity"] == "n1"
        assert changes[0]["category"] == "nodes"

    def test_entity_removed(self, node_config: EntityConfig) -> None:
        """Missing entity detected as 'removed'."""
        before = [_node(UUID1, "n1")]
        after: list[Any] = []
        changes = _diff_entity_list("nodes", before, after, node_config)
        assert len(changes) == 1
        assert changes[0]["type"] == "removed"
        assert changes[0]["entity"] == "n1"

    def test_entity_modified(self, node_config: EntityConfig) -> None:
        """Changed field detected with old/new values."""
        before = [_node(UUID1, "n1", serial_number="SN-OLD")]
        after = [_node(UUID1, "n1", serial_number="SN-NEW")]
        changes = _diff_entity_list("nodes", before, after, node_config)
        mod_changes = [c for c in changes if c["type"] == "modified"]
        assert len(mod_changes) == 1
        assert mod_changes[0]["field"] == "serial_number"
        assert mod_changes[0]["old"] == "SN-OLD"
        assert mod_changes[0]["new"] == "SN-NEW"

    def test_multiple_changes(self, node_config: EntityConfig) -> None:
        """Added + removed + modified in one diff."""
        before = [
            _node(UUID1, "n1", serial_number="SN1"),
            _node(UUID2, "n2"),
        ]
        after = [
            _node(UUID1, "n1", serial_number="SN1-MOD"),
            _node(UUID3, "n3"),
        ]
        changes = _diff_entity_list("nodes", before, after, node_config)
        types = {c["type"] for c in changes}
        assert types == {"added", "removed", "modified"}

    def test_entity_with_int_key_zero_added(self) -> None:
        """Entity with int key_field=0 detected as added."""
        config = _ENTITY_CONFIGS["protocols.nfs_export_policies"]
        before: list[Any] = []
        after = [OntapExportPolicy(index=0)]
        changes = _diff_entity_list("protocols.nfs_export_policies", before, after, config)
        assert len(changes) == 1
        assert changes[0]["type"] == "added"
        assert changes[0]["entity"] == "0"

    def test_entity_with_int_key_zero_removed(self) -> None:
        """Entity with int key_field=0 detected as removed."""
        config = _ENTITY_CONFIGS["protocols.nfs_export_policies"]
        before = [OntapExportPolicy(index=0)]
        after: list[Any] = []
        changes = _diff_entity_list("protocols.nfs_export_policies", before, after, config)
        assert len(changes) == 1
        assert changes[0]["type"] == "removed"
        assert changes[0]["entity"] == "0"

    def test_entity_with_int_key_zero_modified(self) -> None:
        """Entity with int key_field=0 and changed field detected as modified."""
        config = _ENTITY_CONFIGS["protocols.nfs_export_policies"]
        before = [OntapExportPolicy(index=0, chown_mode="restricted")]
        after = [OntapExportPolicy(index=0, chown_mode="unrestricted")]
        changes = _diff_entity_list("protocols.nfs_export_policies", before, after, config)
        mod_changes = [c for c in changes if c["type"] == "modified"]
        assert len(mod_changes) == 1
        assert mod_changes[0]["field"] == "chown_mode"
        assert mod_changes[0]["old"] == "restricted"
        assert mod_changes[0]["new"] == "unrestricted"


# ---------------------------------------------------------------------------
# TestComputeDiff
# ---------------------------------------------------------------------------


class TestComputeDiff:
    """Verify compute_diff() end-to-end."""

    def test_initial_capture_all_added(self) -> None:
        """before=None records all entities as 'added'."""
        md = _make_metadata(
            nodes=[_node(UUID1, "n1")],
            cluster=ClusterInfo(cluster_name="test-cluster"),
        )
        changes = compute_diff(None, md)
        added = [c for c in changes if c["type"] == "added"]
        # At minimum: 1 node + 1 cluster
        assert len(added) >= 2
        entities = [c["entity"] for c in added]
        assert "n1" in entities
        assert "test-cluster" in entities

    def test_no_changes(self) -> None:
        """Identical snapshots produce empty diff."""
        md = _make_metadata(
            nodes=[_node(UUID1, "n1")],
            cluster=ClusterInfo(cluster_name="test-cluster"),
        )
        changes = compute_diff(md, md)
        assert changes == []

    def test_changes_across_categories(self) -> None:
        """Detects changes in storage and nodes simultaneously."""
        from pynetappfoundry.cache.ontap.storage.model import StorageInfo

        before = _make_metadata(
            nodes=[_node(UUID1, "n1")],
            storage=StorageInfo(aggregates=[_aggregate(UUID2, "aggr1", state="online")]),
        )
        after = _make_metadata(
            nodes=[_node(UUID1, "n1", serial_number="NEW-SN")],
            storage=StorageInfo(aggregates=[_aggregate(UUID2, "aggr1", state="offline")]),
        )
        changes = compute_diff(before, after)
        categories = {c["category"] for c in changes}
        assert "nodes" in categories
        assert "storage.aggregates" in categories


# ---------------------------------------------------------------------------
# TestDiffClusterInfo
# ---------------------------------------------------------------------------


class TestDiffClusterInfo:
    """Verify _diff_cluster_info()."""

    def test_initial_capture(self) -> None:
        """Records cluster as 'added' on initial capture."""
        md = _make_metadata(cluster=ClusterInfo(cluster_name="test-cluster"))
        changes = _diff_cluster_info(None, md)
        assert len(changes) == 1
        assert changes[0]["type"] == "added"
        assert changes[0]["entity"] == "test-cluster"
        assert changes[0]["category"] == "cluster"

    def test_no_change(self) -> None:
        """Identical cluster info produces empty diff."""
        md = _make_metadata(cluster=ClusterInfo(cluster_name="c1", ontap_version="9.14"))
        changes = _diff_cluster_info(md, md)
        assert changes == []

    def test_field_modified(self) -> None:
        """Changed field detected."""
        before = _make_metadata(
            cluster=ClusterInfo(cluster_name="c1", ontap_version="9.13"),
        )
        after = _make_metadata(
            cluster=ClusterInfo(cluster_name="c1", ontap_version="9.14"),
        )
        changes = _diff_cluster_info(before, after)
        assert len(changes) == 1
        assert changes[0]["type"] == "modified"
        assert changes[0]["field"] == "ontap_version"
        assert changes[0]["old"] == "9.13"
        assert changes[0]["new"] == "9.14"


# ---------------------------------------------------------------------------
# TestDiffMediatorInfo
# ---------------------------------------------------------------------------


class TestDiffMediatorInfo:
    """Verify _diff_mediator_info()."""

    def test_initial_capture_empty(self) -> None:
        """Empty mediator not recorded."""
        md = _make_metadata(mediator=OntapMediatorResponse())
        changes = _diff_mediator_info(None, md)
        assert changes == []

    def test_initial_capture_populated(self) -> None:
        """Populated mediator recorded as 'added'."""
        md = _make_metadata(
            mediator=OntapMediatorResponse(ip_address="10.0.0.1", port=31784),
        )
        changes = _diff_mediator_info(None, md)
        assert len(changes) == 1
        assert changes[0]["type"] == "added"
        assert changes[0]["entity"] == "mediator_config"

    def test_field_modified(self) -> None:
        """Changed field detected."""
        before = _make_metadata(
            mediator=OntapMediatorResponse(ip_address="10.0.0.1"),
        )
        after = _make_metadata(
            mediator=OntapMediatorResponse(ip_address="10.0.0.2"),
        )
        changes = _diff_mediator_info(before, after)
        mod = [c for c in changes if c["field"] == "ip_address"]
        assert len(mod) == 1
        assert mod[0]["old"] == "10.0.0.1"
        assert mod[0]["new"] == "10.0.0.2"


# ---------------------------------------------------------------------------
# TestFormatDiffSummary
# ---------------------------------------------------------------------------


class TestFormatDiffSummary:
    """Verify format_diff_summary()."""

    def test_no_changes(self) -> None:
        """Returns 'No changes detected.' for empty list."""
        assert format_diff_summary([]) == "No changes detected."

    def test_added_format(self) -> None:
        """'Added (N):' section with '+ category: entity'."""
        changes: list[dict[str, object]] = [
            {"type": "added", "category": "nodes", "entity": "n1"},
        ]
        result = format_diff_summary(changes)
        assert "Added (1):" in result
        assert "+ nodes: n1" in result

    def test_removed_format(self) -> None:
        """'Removed (N):' section."""
        changes: list[dict[str, object]] = [
            {"type": "removed", "category": "nodes", "entity": "n1"},
        ]
        result = format_diff_summary(changes)
        assert "Removed (1):" in result
        assert "- nodes: n1" in result

    def test_modified_format(self) -> None:
        """'Modified (N):' section with field/old/new."""
        changes: list[dict[str, object]] = [
            {
                "type": "modified",
                "category": "nodes",
                "entity": "n1",
                "field": "state",
                "old": "up",
                "new": "down",
            },
        ]
        result = format_diff_summary(changes)
        assert "Modified (1):" in result
        assert "~ nodes: n1.state: up -> down" in result

    def test_mixed_changes(self) -> None:
        """All three sections present."""
        changes: list[dict[str, object]] = [
            {"type": "added", "category": "nodes", "entity": "n1"},
            {"type": "removed", "category": "nodes", "entity": "n2"},
            {
                "type": "modified",
                "category": "nodes",
                "entity": "n3",
                "field": "state",
                "old": "up",
                "new": "down",
            },
        ]
        result = format_diff_summary(changes)
        assert "Added (1):" in result
        assert "Removed (1):" in result
        assert "Modified (1):" in result


# ---------------------------------------------------------------------------
# TestEntityConfigsIntegrity
# ---------------------------------------------------------------------------


class TestEntityConfigsIntegrity:
    """Verify _ENTITY_CONFIGS are correct."""

    def test_all_category_paths_resolve(self) -> None:
        """Every _ENTITY_CONFIGS key resolves on a default CachedClusterMetadata."""
        md = _make_metadata()
        for category in _ENTITY_CONFIGS:
            result = _get_entities(md, category)
            assert isinstance(result, list), f"{category} did not resolve to a list"

    def test_all_key_fields_exist_on_model(self) -> None:
        """Each config's key_field is in model_class.model_fields."""
        for category, config in _ENTITY_CONFIGS.items():
            assert config.key_field in config.model_class.model_fields, (
                f"{category}: key_field '{config.key_field}' not in "
                f"{config.model_class.__name__}.model_fields"
            )

    def test_all_display_fields_exist_or_are_templates(self) -> None:
        """Each config's display_field is a valid field name or contains '{'."""
        for category, config in _ENTITY_CONFIGS.items():
            if "{" in config.display_field:
                continue  # Template — valid
            assert config.display_field in config.model_class.model_fields, (
                f"{category}: display_field '{config.display_field}' not in "
                f"{config.model_class.__name__}.model_fields"
            )

    def test_entity_config_count(self) -> None:
        """Currently 26 configs (catches accidental additions/removals)."""
        assert len(_ENTITY_CONFIGS) == 26
