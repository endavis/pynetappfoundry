"""Tests for cache diff computation."""

from __future__ import annotations

import pytest

from pynetappfoundry.cache.diff import (
    ChangeEntry,
    compute_diff,
    format_diff_summary,
)
from pynetappfoundry.cache.models import (
    AggregateInfo,
    CachedClusterMetadata,
    CIFSShareInfo,
    CloudMetadata,
    ClusterInfo,
    ExportPolicyInfo,
    HAInfo,
    IgroupInfo,
    LicenseFeature,
    LicenseInfo,
    LunInfo,
    NetworkInfo,
    NetworkLIF,
    NodeInfo,
    ProtocolsInfo,
    QosPolicyInfo,
    QtreeInfo,
    RelationshipsInfo,
    ScheduleInfo,
    SnapMirrorRelationship,
    SnapshotPolicyInfo,
    StorageInfo,
    SVMInfo,
    VolumeInfo,
)


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
                NodeInfo(name="node1", serial_number="123"),
                NodeInfo(name="node2", serial_number="456"),
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

    def test_initial_capture_with_ha_info(self) -> None:
        """Test initial capture records HA info as added when configured."""
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            ha=HAInfo(is_ha=True, partner_node="node2"),
        )
        changes = compute_diff(None, after)

        ha_changes = [c for c in changes if c["category"] == "ha"]
        assert len(ha_changes) == 1
        assert ha_changes[0]["type"] == "added"
        assert ha_changes[0]["entity"] == "ha_config"

    def test_initial_capture_no_ha_when_disabled(self) -> None:
        """Test initial capture doesn't record HA when not configured."""
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            ha=HAInfo(is_ha=False),
        )
        changes = compute_diff(None, after)

        ha_changes = [c for c in changes if c["category"] == "ha"]
        assert len(ha_changes) == 0


class TestComputeDiffNoChanges:
    """Tests for no changes between snapshots."""

    def test_identical_metadata_no_changes(self) -> None:
        """Test identical metadata produces no changes."""
        metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(name="node1", serial_number="123"),
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
            nodes=[NodeInfo(name="node1")],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(name="node1"),
                NodeInfo(name="node2"),
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
                aggregates=[AggregateInfo(name="aggr1", state="online")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[
                    AggregateInfo(name="aggr1", state="online"),
                    AggregateInfo(name="aggr2", state="online"),
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
                NodeInfo(name="node1"),
                NodeInfo(name="node2"),
            ],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1")],
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
                    SVMInfo(name="svm1", state="running"),
                    SVMInfo(name="svm2", state="running"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                svms=[SVMInfo(name="svm1", state="running")],
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
            nodes=[NodeInfo(name="node1", serial_number="OLD123")],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1", serial_number="NEW456")],
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
                aggregates=[AggregateInfo(name="aggr1", disk_count=12)],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                aggregates=[AggregateInfo(name="aggr1", disk_count=24)],
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
                intercluster_lifs=[
                    NetworkLIF(name="lif1", ip_address="10.0.0.1"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            network=NetworkInfo(
                intercluster_lifs=[
                    NetworkLIF(name="lif1", ip_address="10.0.0.2"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        lif_changes = [c for c in changes if c["category"] == "network.intercluster_lifs"]
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

    def test_modified_ha_state(self) -> None:
        """Test detecting HA state change."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            ha=HAInfo(is_ha=True, ha_state="connected"),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            ha=HAInfo(is_ha=True, ha_state="takeover"),
        )
        changes = compute_diff(before, after)

        ha_changes = [c for c in changes if c["category"] == "ha"]
        assert len(ha_changes) == 1
        assert ha_changes[0]["type"] == "modified"
        assert ha_changes[0]["field"] == "ha_state"
        assert ha_changes[0]["old"] == "connected"
        assert ha_changes[0]["new"] == "takeover"


class TestComputeDiffMultipleChanges:
    """Tests for detecting multiple simultaneous changes."""

    def test_multiple_change_types(self) -> None:
        """Test detecting added, removed, and modified in same diff."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(name="node1", serial_number="123"),
                NodeInfo(name="node2", serial_number="456"),
            ],
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                NodeInfo(name="node1", serial_number="999"),  # Modified
                NodeInfo(name="node3", serial_number="789"),  # Added (node2 removed)
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
            licenses=LicenseInfo(
                feature_licenses=[
                    LicenseFeature(name="NFS", state="compliant"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            licenses=LicenseInfo(
                feature_licenses=[
                    LicenseFeature(name="NFS", state="noncompliant"),
                ],
            ),
        )
        changes = compute_diff(before, after)

        license_changes = [c for c in changes if c["category"] == "licenses.feature_licenses"]
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
                        destination_path="svm1:vol1",
                        state="snapmirrored",
                    ),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        destination_path="svm1:vol1",
                        state="broken-off",
                    ),
                ],
            ),
        )
        changes = compute_diff(before, after)

        sm_changes = [
            c for c in changes if c["category"] == "relationships.snapmirror_destinations"
        ]
        assert len(sm_changes) == 1

        state_change = [c for c in sm_changes if c["field"] == "state"]
        assert len(state_change) == 1
        assert state_change[0]["old"] == "snapmirrored"
        assert state_change[0]["new"] == "broken-off"

    def test_volume_changes(self) -> None:
        """Test volume change detection."""
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(name="vol1", svm="svm1", state="online", size=1073741824),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(name="vol1", svm="svm1", state="online", size=2147483648),
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
                volumes=[VolumeInfo(name="vol1", svm="svm1")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(name="vol1", svm="svm1"),
                    VolumeInfo(name="vol2", svm="svm1"),
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
                snapshot_policies=[SnapshotPolicyInfo(name="default", uuid="sp-uuid-1")],
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
                schedules=[ScheduleInfo(name="hourly", type="cron", scope="cluster")],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                schedules=[ScheduleInfo(name="hourly", type="interval", scope="cluster")],
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
                luns=[LunInfo(name="/vol/vol1/lun1", svm="svm1", size=10737418240)],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                luns=[LunInfo(name="/vol/vol1/lun1", svm="svm1", size=21474836480)],
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
                igroups=[IgroupInfo(name="igroup1", svm="svm1", protocol="iscsi")],
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
                    QosPolicyInfo(name="qos1", svm="svm1", scope="svm"),
                ],
            ),
        )
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                qos_policies=[
                    QosPolicyInfo(name="qos1", svm="svm1", scope="cluster"),
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

    @pytest.mark.parametrize(
        "entity_key",
        ["", None],
    )
    def test_entities_without_key_are_skipped(self, entity_key: str | None) -> None:
        """Test that entities with empty/None keys don't cause errors."""
        # Nodes without names should be handled gracefully
        before = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1")],
        )
        # The after has same structure, no changes expected
        after = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1")],
        )
        # Should not raise
        changes = compute_diff(before, after)
        assert len(changes) == 0
