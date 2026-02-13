"""Integration tests for model registry — verifies all models and mappings are discovered.

These tests import the full cache package and verify that __init_subclass__
auto-registration and explicit register_mapping() calls have correctly
populated the ModelRegistry singleton.
"""

from __future__ import annotations

from pynetappfoundry.cache import model_registry
from pynetappfoundry.cache._base import CacheModel


class TestModelRegistration:
    """Tests that all CacheModel subclasses are auto-registered."""

    def test_registry_contains_all_leaf_models(self) -> None:
        """All leaf cache models should be registered."""
        expected_models = {
            "AggregateInfo",
            "BroadcastDomain",
            "CIFSServiceInfo",
            "CIFSShareInfo",
            "CloudMetadata",
            "CloudTargetInfo",
            "ClusterInfo",
            "ClusterPeer",
            "DNSInfo",
            "ExportPolicyInfo",
            "ExportRuleInfo",
            "FlexCacheInfo",
            "MediatorInfo",
            "IgroupInfo",
            "IPSubnetInfo",
            "LicenseInstance",
            "LicensePackage",
            "LunInfo",
            "NFSServiceInfo",
            "NetworkInfo",
            "NetworkLIF",
            "NodeInfo",
            "ProtocolsInfo",
            "QosPolicyInfo",
            "QtreeInfo",
            "RelationshipsInfo",
            "S3BucketInfo",
            "SVMInfo",
            "SVMPeerInfo",
            "ScheduleInfo",
            "SnapMirrorRelationship",
            "SnapshotPolicyInfo",
            "SnapshotScheduleInfo",
            "StorageInfo",
            "VolumeInfo",
        }
        registered = set(model_registry.models.keys())
        missing = expected_models - registered
        assert not missing, f"Models not registered: {missing}"

    def test_registry_does_not_contain_base_or_container(self) -> None:
        """CachedClusterMetadata (register=False) should NOT be in registry."""
        assert "CachedClusterMetadata" not in model_registry.models

    def test_all_registered_models_are_cachemodel_subclasses(self) -> None:
        """Every registered model should be a CacheModel subclass."""
        for name, cls in model_registry.models.items():
            assert issubclass(cls, CacheModel), f"{name} is not a CacheModel subclass"

    def test_model_lookup_by_name(self) -> None:
        """get_model() should return the correct class for known names."""
        vol = model_registry.get_model("VolumeInfo")
        assert vol is not None
        assert vol.__name__ == "VolumeInfo"

    def test_model_lookup_unknown_returns_none(self) -> None:
        """get_model() should return None for unknown names."""
        assert model_registry.get_model("DoesNotExist") is None


class TestMappingRegistration:
    """Tests that all mappings are registered via register_mapping()."""

    def test_registry_contains_all_mappings(self) -> None:
        """All 11 type mappings should be registered."""
        expected_mappings = {
            "Aggregate",
            "CloudMetadata",
            "Cluster",
            "ClusterPeer",
            "DNS",
            "LicensePackage",
            "Mediator",
            "Node",
            "SnapMirror",
            "SVM",
            "Volume",
        }
        registered = set(model_registry.mappings.keys())
        missing = expected_mappings - registered
        assert not missing, f"Mappings not registered: {missing}"

    def test_mapping_count(self) -> None:
        """Registry should contain exactly 11 mappings."""
        assert len(model_registry.mappings) == 11

    def test_mapping_lookup_by_name(self) -> None:
        """get_mapping() should return the correct TypeMapping for known names."""
        agg = model_registry.get_mapping("Aggregate")
        assert agg is not None
        assert agg.name == "Aggregate"

    def test_mapping_lookup_unknown_returns_none(self) -> None:
        """get_mapping() should return None for unknown names."""
        assert model_registry.get_mapping("DoesNotExist") is None

    def test_mapping_model_class_matches_registered_model(self) -> None:
        """Each mapping's model_class should be a registered model."""
        for name, mapping in model_registry.mappings.items():
            model_name = mapping.model_class.__name__
            assert model_name in model_registry.models, (
                f"Mapping '{name}' references model '{model_name}' "
                f"which is not in the model registry"
            )
