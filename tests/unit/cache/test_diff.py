"""Tests for cache diff computation."""

from __future__ import annotations

from pynetappfoundry.cache import CachedClusterMetadata, MediatorInfo, RelationshipsInfo
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.cluster.licensing.model import LicensePackage
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.cluster.nodes.model import NodeInfo
from pynetappfoundry.cache.cluster.peers.model import ClusterPeer
from pynetappfoundry.cache.cluster.schedules.model import ScheduleInfo
from pynetappfoundry.cache.diff import (
    ChangeEntry,
    EntityConfig,
    _get_display_name,
    _get_tracked_fields,
    compute_diff,
    format_diff_summary,
)
from pynetappfoundry.cache.name_services.dns.model import DNSInfo
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF
from pynetappfoundry.cache.network.ip.subnets.model import IPSubnetInfo
from pynetappfoundry.cache.network.model import NetworkInfo
from pynetappfoundry.cache.protocols.cifs.services.model import CIFSServiceInfo
from pynetappfoundry.cache.protocols.cifs.shares.model import CIFSShareInfo
from pynetappfoundry.cache.protocols.model import ProtocolsInfo
from pynetappfoundry.cache.protocols.nfs.export_policies.model import ExportPolicyInfo
from pynetappfoundry.cache.protocols.nfs.services.model import NFSServiceInfo
from pynetappfoundry.cache.protocols.s3.buckets.model import S3BucketInfo
from pynetappfoundry.cache.protocols.san.igroups.model import IgroupInfo
from pynetappfoundry.cache.snapmirror.relationships.model import (
    SnapMirrorRelationship,
)
from pynetappfoundry.cache.storage.aggregates.model import AggregateInfo
from pynetappfoundry.cache.storage.flexcache.model import FlexCacheInfo
from pynetappfoundry.cache.storage.luns.model import LunInfo
from pynetappfoundry.cache.storage.model import StorageInfo
from pynetappfoundry.cache.storage.qos.model import QosPolicyInfo
from pynetappfoundry.cache.storage.qtrees.model import QtreeInfo
from pynetappfoundry.cache.storage.snapshot_policies.model import SnapshotPolicyInfo
from pynetappfoundry.cache.storage.volumes.model import VolumeInfo
from pynetappfoundry.cache.svm.model import SVMInfo
from pynetappfoundry.cache.svm.peers.model import SVMPeerInfo


class TestEntityConfig:
    """Tests for EntityConfig and helpers."""

    def test_get_tracked_fields_excludes_key(self) -> None:
        """Tracked fields include all model fields except the key."""
        config = EntityConfig(key_field="uuid", model_class=NodeInfo, display_field="name")
        tracked = _get_tracked_fields(config)
        assert "uuid" not in tracked
        assert "name" in tracked
        assert "serial_number" in tracked

    def test_get_tracked_fields_includes_all_non_key(self) -> None:
        """All model fields except key are tracked."""
        config = EntityConfig(key_field="uuid", model_class=NodeInfo, display_field="name")
        tracked = _get_tracked_fields(config)
        expected = [f for f in NodeInfo.model_fields if f != "uuid"]
        assert tracked == expected

    def test_get_display_name_simple(self) -> None:
        """Simple display field returns attribute value."""
        node = NodeInfo(uuid="u1", name="node1")
        assert _get_display_name(node, "name") == "node1"

    def test_get_display_name_format_string(self) -> None:
        """Format string display field resolves placeholders."""
        sm = SnapMirrorRelationship(
            uuid="u1",
            source_path="svm1:vol1",
            destination_path="svm2:vol2",
        )
        result = _get_display_name(sm, "{source_path}->{destination_path}")
        assert result == "svm1:vol1->svm2:vol2"

    def test_get_display_name_fallback(self) -> None:
        """Empty display field falls back to str(entity)."""
        node = NodeInfo(uuid="u1", name="")
        result = _get_display_name(node, "name")
        # Falls back to str(entity) when name is empty
        assert result != ""


class TestComputeDiffInitialCapture:
    """Tests for initial capture (no before snapshot)."""

    def test_initial_capture_empty_metadata(self) -> None:
        """Test initial capture with empty metadata."""
        after = CachedClusterMetadata(cluster_name="test-cluster")
        changes = compute_diff(None, after)
        # Should have no changes since all lists are empty
        assert len(changes) == 0

    def test_initial_capture_with_nodes(self) -> None:
        """Test initial capture records all nodes as added."""
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1", serial_number="123"),
                NodeInfo(uuid="uuid-2", name="node2", serial_number="456"),
            ],
        )
        changes = compute_diff(None, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 2
        assert all(c["type"] == "added" for c in node_changes)
        entities = {c["entity"] for c in node_changes}
        assert entities == {"node1", "node2"}

    def test_initial_capture_with_cluster_info(self) -> None:
        """Test initial capture records cluster info as added."""
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                cluster_uuid="uuid-123",
                ontap_version="9.14.1",
            ),
        )
        changes = compute_diff(None, after)

        cluster_changes = [c for c in changes if c["category"] == "cluster"]
        assert len(cluster_changes) == 1
        assert cluster_changes[0]["type"] == "added"
        assert cluster_changes[0]["entity"] == "test-cluster"

    def test_initial_capture_with_mediator_info(self) -> None:
        """Test initial capture records mediator as added when configured."""
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            mediator=MediatorInfo(mediator_uuid="med-uuid-1"),
        )
        changes = compute_diff(None, after)

        mediator_changes = [c for c in changes if c["category"] == "mediator"]
        assert len(mediator_changes) == 1
        assert mediator_changes[0]["type"] == "added"
        assert mediator_changes[0]["entity"] == "mediator_config"

    def test_initial_capture_no_mediator_when_empty(self) -> None:
        """Test initial capture doesn't record mediator when not configured."""
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            mediator=MediatorInfo(),
        )
        changes = compute_diff(None, after)

        mediator_changes = [c for c in changes if c["category"] == "mediator"]
        assert len(mediator_changes) == 0


class TestComputeDiffNoChanges:
    """Tests for no changes between snapshots."""

    def test_identical_metadata_no_changes(self) -> None:
        """Test identical metadata produces no changes."""
        metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1", serial_number="123"),
            ],
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                ontap_version="9.14.1",
            ),
        )
        # Create identical copies
        before = metadata.model_copy(deep=True)
        after = metadata.model_copy(deep=True)

        changes = compute_diff(before, after)
        assert len(changes) == 0


class TestComputeDiffAddedEntities:
    """Tests for detecting added entities."""

    def test_added_node(self) -> None:
        """Test detecting a new node."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="node1")],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1"),
                NodeInfo(uuid="uuid-2", name="node2"),
            ],
        )
        changes = compute_diff(before, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 1
        assert node_changes[0]["type"] == "added"
        assert node_changes[0]["entity"] == "node2"

    def test_added_aggregate(self) -> None:
        """Test detecting a new aggregate."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[AggregateInfo(uuid="aggr-uuid-1", name="aggr1", state="online")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[
                    AggregateInfo(uuid="aggr-uuid-1", name="aggr1", state="online"),
                    AggregateInfo(uuid="aggr-uuid-2", name="aggr2", state="online"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        aggr_changes = [c for c in changes if c["category"] == "storage.aggregates"]
        assert len(aggr_changes) == 1
        assert aggr_changes[0]["type"] == "added"
        assert aggr_changes[0]["entity"] == "aggr2"


class TestComputeDiffRemovedEntities:
    """Tests for detecting removed entities."""

    def test_removed_node(self) -> None:
        """Test detecting a removed node."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1"),
                NodeInfo(uuid="uuid-2", name="node2"),
            ],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="node1")],
        )
        changes = compute_diff(before, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 1
        assert node_changes[0]["type"] == "removed"
        assert node_changes[0]["entity"] == "node2"

    def test_removed_svm(self) -> None:
        """Test detecting a removed SVM."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                svms=[
                    SVMInfo(uuid="svm-uuid-1", name="svm1", state="running"),
                    SVMInfo(uuid="svm-uuid-2", name="svm2", state="running"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                svms=[SVMInfo(uuid="svm-uuid-1", name="svm1", state="running")],
            ),
        )
        changes = compute_diff(before, after)

        svm_changes = [c for c in changes if c["category"] == "storage.svms"]
        assert len(svm_changes) == 1
        assert svm_changes[0]["type"] == "removed"
        assert svm_changes[0]["entity"] == "svm2"


class TestComputeDiffModifiedEntities:
    """Tests for detecting modified entities."""

    def test_modified_node_serial(self) -> None:
        """Test detecting node serial number change."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="node1", serial_number="OLD123")],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="node1", serial_number="NEW456")],
        )
        changes = compute_diff(before, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 1
        assert node_changes[0]["type"] == "modified"
        assert node_changes[0]["entity"] == "node1"
        assert node_changes[0]["field"] == "serial_number"
        assert node_changes[0]["old"] == "OLD123"
        assert node_changes[0]["new"] == "NEW456"

    def test_modified_aggregate_disk_count(self) -> None:
        """Test detecting aggregate disk count change."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[AggregateInfo(uuid="aggr-uuid-1", name="aggr1", disk_count=12)],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[AggregateInfo(uuid="aggr-uuid-1", name="aggr1", disk_count=24)],
            ),
        )
        changes = compute_diff(before, after)

        aggr_changes = [c for c in changes if c["category"] == "storage.aggregates"]
        assert len(aggr_changes) == 1
        assert aggr_changes[0]["type"] == "modified"
        assert aggr_changes[0]["field"] == "disk_count"
        assert aggr_changes[0]["old"] == 12
        assert aggr_changes[0]["new"] == 24

    def test_modified_lif_ip_address(self) -> None:
        """Test detecting LIF IP address change."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                lifs=[
                    NetworkLIF(uuid="lif-uuid-1", name="lif1", ip_address="10.0.0.1"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                lifs=[
                    NetworkLIF(uuid="lif-uuid-1", name="lif1", ip_address="10.0.0.2"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        lif_changes = [c for c in changes if c["category"] == "network.lifs"]
        assert len(lif_changes) == 1
        assert lif_changes[0]["type"] == "modified"
        assert lif_changes[0]["field"] == "ip_address"
        assert lif_changes[0]["old"] == "10.0.0.1"
        assert lif_changes[0]["new"] == "10.0.0.2"

    def test_modified_ontap_version(self) -> None:
        """Test detecting ONTAP version change."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                ontap_version="9.14.1",
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                ontap_version="9.15.0",
            ),
        )
        changes = compute_diff(before, after)

        cluster_changes = [c for c in changes if c["category"] == "cluster"]
        assert len(cluster_changes) == 1
        assert cluster_changes[0]["type"] == "modified"
        assert cluster_changes[0]["field"] == "ontap_version"
        assert cluster_changes[0]["old"] == "9.14.1"
        assert cluster_changes[0]["new"] == "9.15.0"

    def test_modified_mediator_port(self) -> None:
        """Test detecting mediator port change."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            mediator=MediatorInfo(mediator_port=31784),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            mediator=MediatorInfo(mediator_port=31785),
        )
        changes = compute_diff(before, after)

        mediator_changes = [c for c in changes if c["category"] == "mediator"]
        assert len(mediator_changes) == 1
        assert mediator_changes[0]["type"] == "modified"
        assert mediator_changes[0]["field"] == "mediator_port"
        assert mediator_changes[0]["old"] == 31784
        assert mediator_changes[0]["new"] == 31785


class TestComputeDiffMultipleChanges:
    """Tests for detecting multiple simultaneous changes."""

    def test_multiple_change_types(self) -> None:
        """Test detecting added, removed, and modified in same diff."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1", serial_number="123"),
                NodeInfo(uuid="uuid-2", name="node2", serial_number="456"),
            ],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1", serial_number="999"),  # Modified
                NodeInfo(
                    uuid="uuid-3", name="node3", serial_number="789"
                ),  # Added (uuid-2 removed)
            ],
        )
        changes = compute_diff(before, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 3

        added = [c for c in node_changes if c["type"] == "added"]
        removed = [c for c in node_changes if c["type"] == "removed"]
        modified = [c for c in node_changes if c["type"] == "modified"]

        assert len(added) == 1
        assert added[0]["entity"] == "node3"

        assert len(removed) == 1
        assert removed[0]["entity"] == "node2"

        assert len(modified) == 1
        assert modified[0]["entity"] == "node1"
        assert modified[0]["field"] == "serial_number"


class TestComputeDiffAllCategories:
    """Tests for all supported categories."""

    def test_cloud_metadata_changes(self) -> None:
        """Test cloud metadata change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            cloud=[CloudMetadata(node="node1", instance_type="m5.xlarge")],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            cloud=[CloudMetadata(node="node1", instance_type="m5.2xlarge")],
        )
        changes = compute_diff(before, after)

        cloud_changes = [c for c in changes if c["category"] == "cloud"]
        assert len(cloud_changes) == 1
        assert cloud_changes[0]["type"] == "modified"
        assert cloud_changes[0]["field"] == "instance_type"

    def test_license_changes(self) -> None:
        """Test license change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            license_packages=[
                LicensePackage(name="NFS", state="compliant", scope="cluster"),
            ],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            license_packages=[
                LicensePackage(name="NFS", state="noncompliant", scope="cluster"),
            ],
        )
        changes = compute_diff(before, after)

        license_changes = [c for c in changes if c["category"] == "license_packages"]
        assert len(license_changes) == 1
        assert license_changes[0]["type"] == "modified"
        assert license_changes[0]["field"] == "state"

    def test_snapmirror_changes(self) -> None:
        """Test SnapMirror relationship change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="svm1:vol1",
                        destination_path="svm2:vol2",
                        relationship_type="async",
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="svm1:vol1",
                        destination_path="svm2:vol2",
                        relationship_type="sync",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        sm_changes = [
            c for c in changes if c["category"] == "relationships.snapmirror_destinations"
        ]
        assert len(sm_changes) == 1
        assert sm_changes[0]["type"] == "modified"
        assert sm_changes[0]["field"] == "relationship_type"
        assert sm_changes[0]["old"] == "async"
        assert sm_changes[0]["new"] == "sync"
        # Display name uses composite format
        assert sm_changes[0]["entity"] == "svm1:vol1->svm2:vol2"

    def test_snapmirror_transfer_schedule_change(self) -> None:
        """Test SnapMirror transfer_schedule_uuid change is detected (original bug)."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="svm1:vol1",
                        destination_path="svm2:vol2",
                        transfer_schedule_uuid="schedule-old",
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="svm1:vol1",
                        destination_path="svm2:vol2",
                        transfer_schedule_uuid="schedule-new",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        sm_changes = [
            c for c in changes if c["category"] == "relationships.snapmirror_destinations"
        ]
        assert len(sm_changes) == 1
        assert sm_changes[0]["field"] == "transfer_schedule_uuid"
        assert sm_changes[0]["old"] == "schedule-old"
        assert sm_changes[0]["new"] == "schedule-new"

    def test_volume_changes(self) -> None:
        """Test volume change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(
                        uuid="vol-uuid-1",
                        name="vol1",
                        svm="svm1",
                        state="online",
                        size=1073741824,
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(
                        uuid="vol-uuid-1",
                        name="vol1",
                        svm="svm1",
                        state="online",
                        size=2147483648,
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        vol_changes = [c for c in changes if c["category"] == "storage.volumes"]
        assert len(vol_changes) == 1
        assert vol_changes[0]["type"] == "modified"
        assert vol_changes[0]["field"] == "size"
        assert vol_changes[0]["old"] == 1073741824
        assert vol_changes[0]["new"] == 2147483648

    def test_volume_added_removed(self) -> None:
        """Test volume addition and removal detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[VolumeInfo(uuid="vol-uuid-1", name="vol1", svm="svm1")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(uuid="vol-uuid-1", name="vol1", svm="svm1"),
                    VolumeInfo(uuid="vol-uuid-2", name="vol2", svm="svm1"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        vol_changes = [c for c in changes if c["category"] == "storage.volumes"]
        assert len(vol_changes) == 1
        assert vol_changes[0]["type"] == "added"
        assert vol_changes[0]["entity"] == "vol2"

    def test_export_policy_changes(self) -> None:
        """Test export policy change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                export_policies=[
                    ExportPolicyInfo(name="default", id=1, svm="svm1"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                export_policies=[
                    ExportPolicyInfo(name="default", id=1, svm="svm2"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        policy_changes = [c for c in changes if c["category"] == "protocols.export_policies"]
        assert len(policy_changes) == 1
        assert policy_changes[0]["type"] == "modified"
        assert policy_changes[0]["field"] == "svm"
        assert policy_changes[0]["old"] == "svm1"
        assert policy_changes[0]["new"] == "svm2"

    def test_export_policy_added(self) -> None:
        """Test export policy addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                export_policies=[ExportPolicyInfo(name="default", id=1, svm="svm1")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                export_policies=[
                    ExportPolicyInfo(name="default", id=1, svm="svm1"),
                    ExportPolicyInfo(name="data_export", id=2, svm="svm1"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        policy_changes = [c for c in changes if c["category"] == "protocols.export_policies"]
        assert len(policy_changes) == 1
        assert policy_changes[0]["type"] == "added"
        assert policy_changes[0]["entity"] == "data_export"

    def test_qtree_changes(self) -> None:
        """Test qtree change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                qtrees=[QtreeInfo(name="qt1", svm="svm1", security_style="unix")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                qtrees=[QtreeInfo(name="qt1", svm="svm1", security_style="ntfs")],
            ),
        )
        changes = compute_diff(before, after)

        qt_changes = [c for c in changes if c["category"] == "storage.qtrees"]
        assert len(qt_changes) == 1
        assert qt_changes[0]["type"] == "modified"
        assert qt_changes[0]["field"] == "security_style"
        assert qt_changes[0]["old"] == "unix"
        assert qt_changes[0]["new"] == "ntfs"

    def test_snapshot_policy_added(self) -> None:
        """Test snapshot policy addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(snapshot_policies=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                snapshot_policies=[
                    SnapshotPolicyInfo(uuid="sp-uuid-1", name="default"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        sp_changes = [c for c in changes if c["category"] == "storage.snapshot_policies"]
        assert len(sp_changes) == 1
        assert sp_changes[0]["type"] == "added"
        assert sp_changes[0]["entity"] == "default"

    def test_schedule_changes(self) -> None:
        """Test schedule change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                schedules=[
                    ScheduleInfo(uuid="sched-uuid-1", name="hourly", type="cron", scope="cluster"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                schedules=[
                    ScheduleInfo(
                        uuid="sched-uuid-1",
                        name="hourly",
                        type="interval",
                        scope="cluster",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        sched_changes = [c for c in changes if c["category"] == "storage.schedules"]
        assert len(sched_changes) == 1
        assert sched_changes[0]["type"] == "modified"
        assert sched_changes[0]["field"] == "type"

    def test_cifs_share_changes(self) -> None:
        """Test CIFS share change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                cifs_shares=[CIFSShareInfo(name="share1", path="/vol1", svm="svm1")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                cifs_shares=[CIFSShareInfo(name="share1", path="/vol2", svm="svm1")],
            ),
        )
        changes = compute_diff(before, after)

        share_changes = [c for c in changes if c["category"] == "protocols.cifs_shares"]
        assert len(share_changes) == 1
        assert share_changes[0]["type"] == "modified"
        assert share_changes[0]["field"] == "path"
        assert share_changes[0]["old"] == "/vol1"
        assert share_changes[0]["new"] == "/vol2"

    def test_cifs_share_added(self) -> None:
        """Test CIFS share addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(cifs_shares=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                cifs_shares=[CIFSShareInfo(name="share1", svm="svm1")],
            ),
        )
        changes = compute_diff(before, after)

        share_changes = [c for c in changes if c["category"] == "protocols.cifs_shares"]
        assert len(share_changes) == 1
        assert share_changes[0]["type"] == "added"
        assert share_changes[0]["entity"] == "share1"

    def test_lun_changes(self) -> None:
        """Test LUN change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                luns=[
                    LunInfo(
                        uuid="lun-uuid-1",
                        name="/vol/vol1/lun1",
                        svm="svm1",
                        size=10737418240,
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                luns=[
                    LunInfo(
                        uuid="lun-uuid-1",
                        name="/vol/vol1/lun1",
                        svm="svm1",
                        size=21474836480,
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        lun_changes = [c for c in changes if c["category"] == "storage.luns"]
        assert len(lun_changes) == 1
        assert lun_changes[0]["type"] == "modified"
        assert lun_changes[0]["field"] == "size"

    def test_igroup_added(self) -> None:
        """Test igroup addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(igroups=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                igroups=[
                    IgroupInfo(uuid="ig-uuid-1", name="igroup1", svm="svm1", protocol="iscsi"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        ig_changes = [c for c in changes if c["category"] == "storage.igroups"]
        assert len(ig_changes) == 1
        assert ig_changes[0]["type"] == "added"
        assert ig_changes[0]["entity"] == "igroup1"

    def test_qos_policy_changes(self) -> None:
        """Test QoS policy change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                qos_policies=[
                    QosPolicyInfo(uuid="qos-uuid-1", name="qos1", svm="svm1", scope="svm"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                qos_policies=[
                    QosPolicyInfo(uuid="qos-uuid-1", name="qos1", svm="svm1", scope="cluster"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        qos_changes = [c for c in changes if c["category"] == "storage.qos_policies"]
        assert len(qos_changes) == 1
        assert qos_changes[0]["type"] == "modified"
        assert qos_changes[0]["field"] == "scope"
        assert qos_changes[0]["old"] == "svm"
        assert qos_changes[0]["new"] == "cluster"

    def test_nfs_service_changes(self) -> None:
        """Test NFS service change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                nfs_services=[
                    NFSServiceInfo(svm="svm1", enabled=True, protocol_v3_enabled=True),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                nfs_services=[
                    NFSServiceInfo(svm="svm1", enabled=True, protocol_v3_enabled=False),
                ],
            ),
        )
        changes = compute_diff(before, after)

        nfs_changes = [c for c in changes if c["category"] == "protocols.nfs_services"]
        assert len(nfs_changes) == 1
        assert nfs_changes[0]["type"] == "modified"
        assert nfs_changes[0]["field"] == "protocol_v3_enabled"
        assert nfs_changes[0]["old"] is True
        assert nfs_changes[0]["new"] is False

    def test_nfs_service_added(self) -> None:
        """Test NFS service addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(nfs_services=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                nfs_services=[NFSServiceInfo(svm="svm1", enabled=True)],
            ),
        )
        changes = compute_diff(before, after)

        nfs_changes = [c for c in changes if c["category"] == "protocols.nfs_services"]
        assert len(nfs_changes) == 1
        assert nfs_changes[0]["type"] == "added"
        assert nfs_changes[0]["entity"] == "svm1"

    def test_cifs_service_changes(self) -> None:
        """Test CIFS service change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                cifs_services=[
                    CIFSServiceInfo(svm="svm1", name="OLDNAME", enabled=True),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                cifs_services=[
                    CIFSServiceInfo(svm="svm1", name="NEWNAME", enabled=True),
                ],
            ),
        )
        changes = compute_diff(before, after)

        cifs_changes = [c for c in changes if c["category"] == "protocols.cifs_services"]
        assert len(cifs_changes) == 1
        assert cifs_changes[0]["type"] == "modified"
        assert cifs_changes[0]["field"] == "name"
        assert cifs_changes[0]["old"] == "OLDNAME"
        assert cifs_changes[0]["new"] == "NEWNAME"

    def test_dns_changes(self) -> None:
        """Test DNS change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                dns=[
                    DNSInfo(
                        uuid="dns-uuid-1", svm_uuid="svm-uuid-1", scope="svm", servers=["10.0.0.1"]
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                dns=[
                    DNSInfo(
                        uuid="dns-uuid-1",
                        svm_uuid="svm-uuid-1",
                        scope="svm",
                        servers=["10.0.0.1", "10.0.0.2"],
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        dns_changes = [c for c in changes if c["category"] == "network.dns"]
        assert len(dns_changes) == 1
        assert dns_changes[0]["type"] == "modified"
        assert dns_changes[0]["field"] == "servers"
        assert dns_changes[0]["old"] == ["10.0.0.1"]
        assert dns_changes[0]["new"] == ["10.0.0.1", "10.0.0.2"]

    def test_dns_added(self) -> None:
        """Test DNS addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(dns=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                dns=[
                    DNSInfo(
                        uuid="dns-uuid-1",
                        svm_uuid="svm-uuid-1",
                        scope="svm",
                        domains=["example.com"],
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        dns_changes = [c for c in changes if c["category"] == "network.dns"]
        assert len(dns_changes) == 1
        assert dns_changes[0]["type"] == "added"
        assert dns_changes[0]["entity"] == "svm-uuid-1"

    def test_flexcache_changes(self) -> None:
        """Test FlexCache change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                flexcaches=[
                    FlexCacheInfo(uuid="fc-uuid-1", name="fc1", svm="svm1", size=1073741824),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                flexcaches=[
                    FlexCacheInfo(uuid="fc-uuid-1", name="fc1", svm="svm1", size=2147483648),
                ],
            ),
        )
        changes = compute_diff(before, after)

        fc_changes = [c for c in changes if c["category"] == "storage.flexcaches"]
        assert len(fc_changes) == 1
        assert fc_changes[0]["type"] == "modified"
        assert fc_changes[0]["field"] == "size"
        assert fc_changes[0]["old"] == 1073741824
        assert fc_changes[0]["new"] == 2147483648

    def test_flexcache_added(self) -> None:
        """Test FlexCache addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(flexcaches=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                flexcaches=[FlexCacheInfo(uuid="fc-uuid-1", name="fc1", svm="svm1")],
            ),
        )
        changes = compute_diff(before, after)

        fc_changes = [c for c in changes if c["category"] == "storage.flexcaches"]
        assert len(fc_changes) == 1
        assert fc_changes[0]["type"] == "added"
        assert fc_changes[0]["entity"] == "fc1"

    def test_svm_peer_changes(self) -> None:
        """Test SVM peer change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                svm_peers=[
                    SVMPeerInfo(uuid="peer-uuid-1", name="svm1_to_svm2", state="peered"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                svm_peers=[
                    SVMPeerInfo(uuid="peer-uuid-1", name="svm1_to_svm2", state="initiated"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        peer_changes = [c for c in changes if c["category"] == "relationships.svm_peers"]
        assert len(peer_changes) == 1
        assert peer_changes[0]["type"] == "modified"
        assert peer_changes[0]["field"] == "state"
        assert peer_changes[0]["old"] == "peered"
        assert peer_changes[0]["new"] == "initiated"

    def test_svm_peer_added(self) -> None:
        """Test SVM peer addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(svm_peers=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                svm_peers=[
                    SVMPeerInfo(
                        uuid="peer-uuid-1",
                        name="svm1_to_svm2",
                        svm="svm1",
                        state="peered",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        peer_changes = [c for c in changes if c["category"] == "relationships.svm_peers"]
        assert len(peer_changes) == 1
        assert peer_changes[0]["type"] == "added"
        assert peer_changes[0]["entity"] == "svm1_to_svm2"

    def test_s3_bucket_changes(self) -> None:
        """Test S3 bucket change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                s3_buckets=[
                    S3BucketInfo(uuid="s3-uuid-1", name="mybucket", svm="svm1", size=1073741824),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                s3_buckets=[
                    S3BucketInfo(uuid="s3-uuid-1", name="mybucket", svm="svm1", size=2147483648),
                ],
            ),
        )
        changes = compute_diff(before, after)

        bucket_changes = [c for c in changes if c["category"] == "protocols.s3_buckets"]
        assert len(bucket_changes) == 1
        assert bucket_changes[0]["type"] == "modified"
        assert bucket_changes[0]["field"] == "size"

    def test_s3_bucket_added(self) -> None:
        """Test S3 bucket addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(s3_buckets=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            protocols=ProtocolsInfo(
                s3_buckets=[S3BucketInfo(uuid="s3-uuid-1", name="mybucket", svm="svm1")],
            ),
        )
        changes = compute_diff(before, after)

        bucket_changes = [c for c in changes if c["category"] == "protocols.s3_buckets"]
        assert len(bucket_changes) == 1
        assert bucket_changes[0]["type"] == "added"
        assert bucket_changes[0]["entity"] == "mybucket"

    def test_subnet_changes(self) -> None:
        """Test IP subnet change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                subnets=[
                    IPSubnetInfo(
                        uuid="sub-uuid-1",
                        name="data-subnet",
                        subnet="10.0.0.0/24",
                        gateway="10.0.0.1",
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                subnets=[
                    IPSubnetInfo(
                        uuid="sub-uuid-1",
                        name="data-subnet",
                        subnet="10.0.0.0/24",
                        gateway="10.0.0.254",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        subnet_changes = [c for c in changes if c["category"] == "network.subnets"]
        assert len(subnet_changes) == 1
        assert subnet_changes[0]["type"] == "modified"
        assert subnet_changes[0]["field"] == "gateway"
        assert subnet_changes[0]["old"] == "10.0.0.1"
        assert subnet_changes[0]["new"] == "10.0.0.254"

    def test_subnet_added(self) -> None:
        """Test IP subnet addition detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(subnets=[]),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                subnets=[
                    IPSubnetInfo(uuid="sub-uuid-1", name="data-subnet", subnet="10.0.0.0/24"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        subnet_changes = [c for c in changes if c["category"] == "network.subnets"]
        assert len(subnet_changes) == 1
        assert subnet_changes[0]["type"] == "added"
        assert subnet_changes[0]["entity"] == "data-subnet"

    def test_cluster_peer_changes(self) -> None:
        """Test cluster peer change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                cluster_peers=[
                    ClusterPeer(
                        uuid="cp-uuid-1",
                        name="peer1",
                        authentication_state="ok",
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                cluster_peers=[
                    ClusterPeer(
                        uuid="cp-uuid-1",
                        name="peer1",
                        authentication_state="expired",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        peer_changes = [c for c in changes if c["category"] == "relationships.cluster_peers"]
        assert len(peer_changes) == 1
        assert peer_changes[0]["type"] == "modified"
        assert peer_changes[0]["field"] == "authentication_state"


class TestDynamicFieldTracking:
    """Tests for dynamic field tracking (all model fields tracked automatically)."""

    def test_previously_untracked_node_field_detected(self) -> None:
        """Node version_full was previously untracked — now it is detected."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1", version_full="9.14.1P1"),
            ],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1", version_full="9.15.0"),
            ],
        )
        changes = compute_diff(before, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 1
        assert node_changes[0]["field"] == "version_full"

    def test_uuid_keyed_rename_detected_as_modification(self) -> None:
        """Renaming a uuid-keyed entity is a modification, not remove+add."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="old-name")],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="new-name")],
        )
        changes = compute_diff(before, after)

        node_changes = [c for c in changes if c["category"] == "nodes"]
        assert len(node_changes) == 1
        assert node_changes[0]["type"] == "modified"
        assert node_changes[0]["field"] == "name"
        assert node_changes[0]["old"] == "old-name"
        assert node_changes[0]["new"] == "new-name"
        # Display shows the new name
        assert node_changes[0]["entity"] == "new-name"

    def test_display_name_shows_name_not_uuid(self) -> None:
        """Change entries for uuid-keyed models show name, not uuid."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[
                    AggregateInfo(uuid="aggr-uuid-1", name="aggr1", state="online"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[
                    AggregateInfo(uuid="aggr-uuid-1", name="aggr1", state="offline"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        aggr_changes = [c for c in changes if c["category"] == "storage.aggregates"]
        assert len(aggr_changes) >= 1
        # Entity should be the human-readable name, not the uuid
        assert aggr_changes[0]["entity"] == "aggr1"
        assert aggr_changes[0]["entity"] != "aggr-uuid-1"

    def test_snapmirror_composite_display(self) -> None:
        """SnapMirror entity display uses composite format."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="src_svm:vol1",
                        destination_path="dst_svm:vol1_dp",
                        throttle=0,
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="src_svm:vol1",
                        destination_path="dst_svm:vol1_dp",
                        throttle=1000,
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        sm_changes = [
            c for c in changes if c["category"] == "relationships.snapmirror_destinations"
        ]
        assert len(sm_changes) == 1
        assert sm_changes[0]["entity"] == "src_svm:vol1->dst_svm:vol1_dp"

    def test_singleton_cluster_tracks_all_fields(self) -> None:
        """Cluster info singleton tracks all ClusterInfo model fields."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                contact="old-contact",
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                contact="new-contact",
            ),
        )
        changes = compute_diff(before, after)

        cluster_changes = [c for c in changes if c["category"] == "cluster"]
        assert len(cluster_changes) == 1
        assert cluster_changes[0]["field"] == "contact"

    def test_singleton_mediator_tracks_all_fields(self) -> None:
        """Mediator singleton tracks all MediatorInfo model fields."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            mediator=MediatorInfo(mediator_address="10.0.0.1"),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            mediator=MediatorInfo(mediator_address="10.0.0.2"),
        )
        changes = compute_diff(before, after)

        mediator_changes = [c for c in changes if c["category"] == "mediator"]
        assert len(mediator_changes) == 1
        assert mediator_changes[0]["field"] == "mediator_address"


class TestFormatDiffSummary:
    """Tests for format_diff_summary function."""

    def test_empty_changes(self) -> None:
        """Test formatting empty changes list."""
        result = format_diff_summary([])
        assert result == "No changes detected."

    def test_added_only(self) -> None:
        """Test formatting added changes only."""
        changes = [
            {"category": "nodes", "type": "added", "entity": "node1"},
            {"category": "nodes", "type": "added", "entity": "node2"},
        ]
        result = format_diff_summary(changes)
        assert "Added (2):" in result
        assert "+ nodes: node1" in result
        assert "+ nodes: node2" in result

    def test_removed_only(self) -> None:
        """Test formatting removed changes only."""
        changes = [
            {"category": "storage.svms", "type": "removed", "entity": "svm1"},
        ]
        result = format_diff_summary(changes)
        assert "Removed (1):" in result
        assert "- storage.svms: svm1" in result

    def test_modified_only(self) -> None:
        """Test formatting modified changes only."""
        changes = [
            {
                "category": "nodes",
                "type": "modified",
                "entity": "node1",
                "field": "serial_number",
                "old": "OLD",
                "new": "NEW",
            },
        ]
        result = format_diff_summary(changes)
        assert "Modified (1):" in result
        assert "~ nodes: node1.serial_number: OLD -> NEW" in result

    def test_mixed_changes(self) -> None:
        """Test formatting mixed change types."""
        changes = [
            {"category": "nodes", "type": "added", "entity": "node3"},
            {"category": "nodes", "type": "removed", "entity": "node2"},
            {
                "category": "nodes",
                "type": "modified",
                "entity": "node1",
                "field": "model",
                "old": "A",
                "new": "B",
            },
        ]
        result = format_diff_summary(changes)
        assert "Added (1):" in result
        assert "Removed (1):" in result
        assert "Modified (1):" in result


class TestChangeEntry:
    """Tests for ChangeEntry model."""

    def test_create_added_entry(self) -> None:
        """Test creating an added entry."""
        entry = ChangeEntry(
            category="nodes",
            change_type="added",
            entity="node1",
        )
        assert entry.category == "nodes"
        assert entry.change_type == "added"
        assert entry.entity == "node1"
        assert entry.field is None
        assert entry.old_value is None
        assert entry.new_value is None

    def test_create_modified_entry(self) -> None:
        """Test creating a modified entry with field values."""
        entry = ChangeEntry(
            category="storage.aggregates",
            change_type="modified",
            entity="aggr1",
            field="used_size",
            old_value=100,
            new_value=200,
        )
        assert entry.field == "used_size"
        assert entry.old_value == 100
        assert entry.new_value == 200


class TestComputeDiffEdgeCases:
    """Tests for edge cases in diff computation."""

    def test_entities_without_uuid_key_are_skipped(self) -> None:
        """Entities with empty uuid keys don't cause errors."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(uuid="uuid-1", name="node1")],
        )
        # After has the same node plus one with empty uuid (should be skipped)
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(uuid="uuid-1", name="node1"),
                NodeInfo(uuid="", name="phantom"),
            ],
        )
        changes = compute_diff(before, after)
        node_changes = [c for c in changes if c["category"] == "nodes"]
        # The empty-uuid node should not appear as added
        assert len(node_changes) == 0

    def test_entities_without_name_key_are_skipped(self) -> None:
        """Entities with empty name keys (for name-keyed models) are skipped."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                lifs=[NetworkLIF(uuid="lif-uuid-1", name="lif1", ip_address="10.0.0.1")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                lifs=[NetworkLIF(uuid="lif-uuid-1", name="lif1", ip_address="10.0.0.1")],
            ),
        )
        changes = compute_diff(before, after)
        lif_changes = [c for c in changes if c["category"] == "network.lifs"]
        assert len(lif_changes) == 0
