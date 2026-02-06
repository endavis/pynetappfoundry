"""Tests for cache Pydantic models."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pynetappfoundry.cache.models import (
    AggregateInfo,
    BroadcastDomain,
    CachedClusterMetadata,
    CapacityLicense,
    CIFSShareInfo,
    CloudMetadata,
    CloudTargetInfo,
    ClusterInfo,
    ClusterPeer,
    ExportPolicyInfo,
    ExportRuleInfo,
    HAInfo,
    LicenseFeature,
    LicenseInfo,
    NetworkInfo,
    NetworkLIF,
    NodeInfo,
    ProtocolsInfo,
    QtreeInfo,
    RelationshipsInfo,
    ScheduleInfo,
    SnapMirrorRelationship,
    SnapshotPolicyInfo,
    SnapshotScheduleInfo,
    StorageInfo,
    SVMInfo,
    VolumeInfo,
)


class TestCloudMetadata:
    """Tests for CloudMetadata model."""

    def test_default_values(self) -> None:
        """Test that all fields have empty string defaults."""
        cloud = CloudMetadata()
        assert cloud.instance_id == ""
        assert cloud.provider == ""
        assert cloud.region == ""
        assert cloud.availability_zone == ""

    def test_aws_metadata(self) -> None:
        """Test AWS-specific fields."""
        cloud = CloudMetadata(
            instance_id="i-0abc123def456",
            account_id="123456789012",
            instance_type="m5.2xlarge",
            region="us-east-1",
            provider="AWS",
            availability_zone="us-east-1a",
            availability_zone_id="use1-az1",
        )
        assert cloud.provider == "AWS"
        assert cloud.instance_id == "i-0abc123def456"
        assert cloud.availability_zone == "us-east-1a"

    def test_azure_metadata(self) -> None:
        """Test Azure-specific fields."""
        cloud = CloudMetadata(
            instance_id="azure-vm-123",
            provider="Azure",
            region="eastus",
            fault_domain="0",
            update_domain="1",
            resource_group_name="rg-storage",
            offer="netapp-ontap-cloud",
            sku="standard",
        )
        assert cloud.provider == "Azure"
        assert cloud.fault_domain == "0"
        assert cloud.resource_group_name == "rg-storage"

    def test_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed."""
        cloud = CloudMetadata(
            provider="GCP",
            custom_field="custom_value",
        )
        assert cloud.custom_field == "custom_value"  # type: ignore[attr-defined]


class TestClusterInfo:
    """Tests for ClusterInfo model."""

    def test_default_values(self) -> None:
        """Test default empty values."""
        cluster = ClusterInfo()
        assert cluster.cluster_name == ""
        assert cluster.cluster_uuid == ""
        assert cluster.ontap_version == ""

    def test_with_values(self) -> None:
        """Test with cluster data."""
        cluster = ClusterInfo(
            cluster_name="mycluster",
            cluster_uuid="abc-123-def-456",
            ontap_version="NetApp Release 9.14.1",
            model="SIMULATED",
        )
        assert cluster.cluster_name == "mycluster"
        assert cluster.cluster_uuid == "abc-123-def-456"
        assert "9.14.1" in cluster.ontap_version


class TestNodeInfo:
    """Tests for NodeInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        node = NodeInfo()
        assert node.uuid == ""
        assert node.name == ""
        assert node.serial_number == ""
        assert node.is_epsilon is False
        assert node.location == ""

    def test_with_values(self) -> None:
        """Test with node data."""
        node = NodeInfo(
            uuid="node-uuid-1",
            name="node1",
            serial_number="123456789",
            system_id="0123456789",
            model="SIMULATED",
            is_epsilon=True,
            location="rack-1",
        )
        assert node.uuid == "node-uuid-1"
        assert node.name == "node1"
        assert node.serial_number == "123456789"
        assert node.is_epsilon is True
        assert node.location == "rack-1"


class TestNetworkLIF:
    """Tests for NetworkLIF model."""

    def test_default_values(self) -> None:
        """Test default values."""
        lif = NetworkLIF()
        assert lif.name == ""
        assert lif.ip_address == ""

    def test_with_values(self) -> None:
        """Test with LIF data."""
        lif = NetworkLIF(
            name="data_lif1",
            ip_address="10.0.0.10",
            netmask="255.255.255.0",
            home_node="node1",
            home_port="e0d",
            role="data",
            svm="svm1",
        )
        assert lif.name == "data_lif1"
        assert lif.ip_address == "10.0.0.10"
        assert lif.role == "data"


class TestBroadcastDomain:
    """Tests for BroadcastDomain model."""

    def test_default_values(self) -> None:
        """Test default values."""
        bd = BroadcastDomain()
        assert bd.name == ""
        assert bd.ports == []

    def test_with_values(self) -> None:
        """Test with broadcast domain data."""
        bd = BroadcastDomain(
            name="Default",
            ipspace="Default",
            mtu=1500,
            ports=["node1:e0c", "node1:e0d"],
        )
        assert bd.name == "Default"
        assert len(bd.ports) == 2


class TestNetworkInfo:
    """Tests for NetworkInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        network = NetworkInfo()
        assert network.intercluster_lifs == []
        assert network.data_lifs == []
        assert network.ipspaces == []

    def test_with_lifs(self) -> None:
        """Test with LIF data."""
        lif = NetworkLIF(name="ic_lif1", ip_address="10.0.1.1")
        network = NetworkInfo(
            intercluster_lifs=[lif],
            ipspaces=["Default", "Cluster"],
        )
        assert len(network.intercluster_lifs) == 1
        assert network.intercluster_lifs[0].name == "ic_lif1"


class TestAggregateInfo:
    """Tests for AggregateInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        aggr = AggregateInfo()
        assert aggr.uuid == ""
        assert aggr.name == ""
        assert aggr.total_size == 0
        assert aggr.disk_count == 0
        assert aggr.disk_type == ""
        assert aggr.raid_type == ""

    def test_with_values(self) -> None:
        """Test with aggregate data."""
        aggr = AggregateInfo(
            uuid="aggr-uuid-1",
            name="aggr1",
            node="node1",
            state="online",
            type="ssd",
            total_size=1099511627776,  # 1TB
            disk_count=24,
            disk_type="ssd",
            raid_type="raid_dp",
        )
        assert aggr.uuid == "aggr-uuid-1"
        assert aggr.name == "aggr1"
        assert aggr.total_size == 1099511627776
        assert aggr.disk_count == 24
        assert aggr.raid_type == "raid_dp"


class TestSVMInfo:
    """Tests for SVMInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        svm = SVMInfo()
        assert svm.uuid == ""
        assert svm.name == ""
        assert svm.state == ""
        assert svm.allowed_protocols == []
        assert svm.language == ""

    def test_with_values(self) -> None:
        """Test with SVM data."""
        svm = SVMInfo(
            uuid="svm-uuid-1",
            name="svm1",
            state="running",
            subtype="default",
            root_volume="svm1_root",
            root_volume_aggregate="aggr1",
            allowed_protocols=["nfs", "cifs"],
            language="c.utf_8",
        )
        assert svm.uuid == "svm-uuid-1"
        assert svm.name == "svm1"
        assert svm.state == "running"
        assert svm.allowed_protocols == ["nfs", "cifs"]
        assert svm.language == "c.utf_8"


class TestCloudTargetInfo:
    """Tests for CloudTargetInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        target = CloudTargetInfo()
        assert target.name == ""
        assert target.uuid == ""
        assert target.provider_type == ""
        assert target.ssl_enabled is True

    def test_with_aws_values(self) -> None:
        """Test with AWS S3 cloud target data."""
        target = CloudTargetInfo(
            name="s3-target-1",
            uuid="abc-123-def-456",
            provider_type="AWS_S3",
            server="s3.us-east-1.amazonaws.com",
            container="my-bucket",
            owner="fabricpool",
            scope="cluster",
            ssl_enabled=True,
            authentication_type="key",
            ipspace="Default",
        )
        assert target.name == "s3-target-1"
        assert target.provider_type == "AWS_S3"
        assert target.container == "my-bucket"
        assert target.owner == "fabricpool"

    def test_with_azure_values(self) -> None:
        """Test with Azure cloud target data."""
        target = CloudTargetInfo(
            name="azure-target-1",
            provider_type="Azure_Cloud",
            server="mystorageaccount.blob.core.windows.net",
            container="mycontainer",
            owner="snapmirror",
            scope="svm",
            svm="svm1",
            snapmirror_use="data_protection",
        )
        assert target.provider_type == "Azure_Cloud"
        assert target.owner == "snapmirror"
        assert target.svm == "svm1"
        assert target.snapmirror_use == "data_protection"

    def test_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed."""
        target = CloudTargetInfo(
            name="test-target",
            custom_field="custom_value",
        )
        assert target.custom_field == "custom_value"  # type: ignore[attr-defined]


class TestStorageInfo:
    """Tests for StorageInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        storage = StorageInfo()
        assert storage.aggregates == []
        assert storage.svms == []
        assert storage.cloud_targets == []
        assert storage.volumes == []
        assert storage.qtrees == []
        assert storage.snapshot_policies == []
        assert storage.schedules == []

    def test_with_data(self) -> None:
        """Test with storage data."""
        aggr = AggregateInfo(name="aggr1")
        svm = SVMInfo(name="svm1")
        storage = StorageInfo(aggregates=[aggr], svms=[svm])
        assert len(storage.aggregates) == 1
        assert len(storage.svms) == 1

    def test_with_cloud_targets(self) -> None:
        """Test with cloud targets."""
        target = CloudTargetInfo(name="s3-target", provider_type="AWS_S3")
        storage = StorageInfo(cloud_targets=[target])
        assert len(storage.cloud_targets) == 1
        assert storage.cloud_targets[0].name == "s3-target"


class TestVolumeInfo:
    """Tests for VolumeInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        vol = VolumeInfo()
        assert vol.uuid == ""
        assert vol.name == ""
        assert vol.svm == ""
        assert vol.size == 0
        assert vol.aggregates == []
        assert vol.autosize_mode == ""
        assert vol.tiering_policy == ""

    def test_with_values(self) -> None:
        """Test with volume data."""
        vol = VolumeInfo(
            uuid="vol-uuid-1",
            name="vol1",
            svm="svm1",
            state="online",
            type="rw",
            style="flexvol",
            size=1099511627776,
            autosize_mode="grow",
            autosize_grow_threshold=85,
            autosize_maximum=2199023255552,
            aggregate="aggr1",
            snapshot_policy="default",
            export_policy="default",
            junction_path="/vol1",
            nas_security_style="unix",
        )
        assert vol.uuid == "vol-uuid-1"
        assert vol.name == "vol1"
        assert vol.size == 1099511627776
        assert vol.junction_path == "/vol1"
        assert vol.autosize_mode == "grow"

    def test_flexgroup_aggregates(self) -> None:
        """Test FlexGroup volume with multiple aggregates."""
        vol = VolumeInfo(
            name="fg_vol1",
            style="flexgroup",
            aggregates=["aggr1", "aggr2", "aggr3"],
        )
        assert vol.style == "flexgroup"
        assert len(vol.aggregates) == 3


class TestExportRuleInfo:
    """Tests for ExportRuleInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        rule = ExportRuleInfo()
        assert rule.index == 0
        assert rule.clients == []
        assert rule.protocols == []
        assert rule.anonymous_user == ""

    def test_with_values(self) -> None:
        """Test with rule data."""
        rule = ExportRuleInfo(
            index=1,
            clients=["0.0.0.0/0"],
            protocols=["nfs"],
            ro_rule=["sys"],
            rw_rule=["sys"],
            superuser=["sys"],
            anonymous_user="65534",
        )
        assert rule.index == 1
        assert rule.clients == ["0.0.0.0/0"]
        assert rule.ro_rule == ["sys"]


class TestExportPolicyInfo:
    """Tests for ExportPolicyInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        policy = ExportPolicyInfo()
        assert policy.id == 0
        assert policy.name == ""
        assert policy.svm == ""
        assert policy.rules == []

    def test_with_rules(self) -> None:
        """Test with rules."""
        rule = ExportRuleInfo(index=1, clients=["0.0.0.0/0"], protocols=["nfs"])
        policy = ExportPolicyInfo(
            id=1,
            name="default",
            svm="svm1",
            rules=[rule],
        )
        assert policy.name == "default"
        assert len(policy.rules) == 1
        assert policy.rules[0].index == 1


class TestQtreeInfo:
    """Tests for QtreeInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        qtree = QtreeInfo()
        assert qtree.id == 0
        assert qtree.name == ""
        assert qtree.svm == ""
        assert qtree.volume == ""
        assert qtree.security_style == ""
        assert qtree.export_policy == ""

    def test_with_values(self) -> None:
        """Test with qtree data."""
        qtree = QtreeInfo(
            id=1,
            name="qt1",
            svm="svm1",
            volume="vol1",
            path="/vol1/qt1",
            security_style="unix",
            unix_permissions="0755",
            export_policy="default",
        )
        assert qtree.name == "qt1"
        assert qtree.security_style == "unix"
        assert qtree.unix_permissions == "0755"


class TestSnapshotScheduleInfo:
    """Tests for SnapshotScheduleInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        sched = SnapshotScheduleInfo()
        assert sched.schedule == ""
        assert sched.count == 0
        assert sched.prefix == ""
        assert sched.snapmirror_label == ""

    def test_with_values(self) -> None:
        """Test with schedule data."""
        sched = SnapshotScheduleInfo(
            schedule="hourly",
            count=6,
            prefix="hourly",
            snapmirror_label="hourly",
        )
        assert sched.schedule == "hourly"
        assert sched.count == 6


class TestSnapshotPolicyInfo:
    """Tests for SnapshotPolicyInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        policy = SnapshotPolicyInfo()
        assert policy.uuid == ""
        assert policy.name == ""
        assert policy.enabled is True
        assert policy.schedules == []

    def test_with_schedules(self) -> None:
        """Test with snapshot policy schedules."""
        sched = SnapshotScheduleInfo(schedule="hourly", count=6)
        policy = SnapshotPolicyInfo(
            uuid="sp-uuid-1",
            name="default",
            svm="svm1",
            enabled=True,
            scope="svm",
            schedules=[sched],
        )
        assert policy.name == "default"
        assert len(policy.schedules) == 1
        assert policy.schedules[0].schedule == "hourly"


class TestScheduleInfo:
    """Tests for ScheduleInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        sched = ScheduleInfo()
        assert sched.uuid == ""
        assert sched.name == ""
        assert sched.type == ""
        assert sched.cron == {}
        assert sched.interval == ""

    def test_with_cron(self) -> None:
        """Test with cron schedule data."""
        sched = ScheduleInfo(
            uuid="sched-uuid-1",
            name="hourly",
            type="cron",
            scope="cluster",
            cron={"minutes": [0], "hours": [0, 1, 2, 3]},
        )
        assert sched.name == "hourly"
        assert sched.type == "cron"
        assert sched.cron["minutes"] == [0]

    def test_with_interval(self) -> None:
        """Test with interval schedule data."""
        sched = ScheduleInfo(
            uuid="sched-uuid-2",
            name="5min",
            type="interval",
            interval="PT5M",
        )
        assert sched.type == "interval"
        assert sched.interval == "PT5M"


class TestCIFSShareInfo:
    """Tests for CIFSShareInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        share = CIFSShareInfo()
        assert share.name == ""
        assert share.path == ""
        assert share.svm == ""
        assert share.home_directory is False
        assert share.oplocks is True
        assert share.access_based_enumeration is False
        assert share.change_notify is True
        assert share.encryption is False

    def test_with_values(self) -> None:
        """Test with CIFS share data."""
        share = CIFSShareInfo(
            name="share1",
            path="/vol1",
            svm="svm1",
            comment="Test share",
            home_directory=False,
            oplocks=True,
            access_based_enumeration=True,
            encryption=True,
            unix_symlink="local",
        )
        assert share.name == "share1"
        assert share.access_based_enumeration is True
        assert share.encryption is True
        assert share.unix_symlink == "local"


class TestProtocolsInfo:
    """Tests for ProtocolsInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        protocols = ProtocolsInfo()
        assert protocols.export_policies == []
        assert protocols.cifs_shares == []

    def test_with_export_policies(self) -> None:
        """Test with export policy data."""
        policy = ExportPolicyInfo(name="default", svm="svm1")
        protocols = ProtocolsInfo(export_policies=[policy])
        assert len(protocols.export_policies) == 1
        assert protocols.export_policies[0].name == "default"

    def test_with_cifs_shares(self) -> None:
        """Test with CIFS share data."""
        share = CIFSShareInfo(name="share1", svm="svm1")
        protocols = ProtocolsInfo(cifs_shares=[share])
        assert len(protocols.cifs_shares) == 1
        assert protocols.cifs_shares[0].name == "share1"


class TestLicenseFeature:
    """Tests for LicenseFeature model."""

    def test_with_values(self) -> None:
        """Test with license data."""
        license = LicenseFeature(
            name="NFS",
            state="compliant",
            scope="cluster",
        )
        assert license.name == "NFS"
        assert license.state == "compliant"


class TestCapacityLicense:
    """Tests for CapacityLicense model."""

    def test_with_values(self) -> None:
        """Test with capacity license data."""
        cap = CapacityLicense(
            name="Cloud Volumes ONTAP",
            licensed_capacity=109951162777600,  # 100TB
            used_capacity=54975581388800,  # 50TB
        )
        assert cap.licensed_capacity == 109951162777600
        assert cap.used_capacity == 54975581388800


class TestLicenseInfo:
    """Tests for LicenseInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        licenses = LicenseInfo()
        assert licenses.feature_licenses == []
        assert licenses.capacity_licenses == []

    def test_with_data(self) -> None:
        """Test with license data."""
        feature = LicenseFeature(name="NFS", state="compliant", scope="cluster")
        capacity = CapacityLicense(name="CVO", licensed_capacity=100)
        licenses = LicenseInfo(
            feature_licenses=[feature],
            capacity_licenses=[capacity],
        )
        assert len(licenses.feature_licenses) == 1
        assert len(licenses.capacity_licenses) == 1


class TestHAInfo:
    """Tests for HAInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        ha = HAInfo()
        assert ha.is_ha is False
        assert ha.partner_node == ""

    def test_ha_enabled(self) -> None:
        """Test HA enabled configuration."""
        ha = HAInfo(
            is_ha=True,
            partner_node="node2",
            ha_state="connected",
            mediator_address="10.0.0.100",
        )
        assert ha.is_ha is True
        assert ha.partner_node == "node2"
        assert ha.mediator_address == "10.0.0.100"


class TestSnapMirrorRelationship:
    """Tests for SnapMirrorRelationship model."""

    def test_default_values(self) -> None:
        """Test default values."""
        sm = SnapMirrorRelationship()
        assert sm.uuid == ""
        assert sm.source_path == ""

    def test_with_values(self) -> None:
        """Test with relationship data."""
        sm = SnapMirrorRelationship(
            uuid="sm-uuid-1",
            source_path="svm1:vol1",
            destination_path="svm2:vol1_dp",
            relationship_type="extended_data_protection",
            state="snapmirrored",
        )
        assert sm.uuid == "sm-uuid-1"
        assert sm.source_path == "svm1:vol1"
        assert sm.state == "snapmirrored"


class TestClusterPeer:
    """Tests for ClusterPeer model."""

    def test_default_values(self) -> None:
        """Test default values."""
        peer = ClusterPeer()
        assert peer.name == ""
        assert peer.peer_addresses == []

    def test_with_values(self) -> None:
        """Test with peer data."""
        peer = ClusterPeer(
            name="peer1",
            uuid="abc-123",
            remote_cluster_name="remote-cluster",
            peer_addresses=["10.0.1.1", "10.0.1.2"],
            authentication_state="ok",
        )
        assert peer.remote_cluster_name == "remote-cluster"
        assert len(peer.peer_addresses) == 2


class TestRelationshipsInfo:
    """Tests for RelationshipsInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        rel = RelationshipsInfo()
        assert rel.snapmirror_destinations == []
        assert rel.cluster_peers == []


class TestCachedClusterMetadata:
    """Tests for CachedClusterMetadata model."""

    def test_minimal_creation(self) -> None:
        """Test creating with minimal required fields."""
        metadata = CachedClusterMetadata(cluster_name="test-cluster")
        assert metadata.cluster_name == "test-cluster"
        assert metadata.cache_version == "1.0"
        assert metadata.cached_at is not None

    def test_cached_at_default(self) -> None:
        """Test cached_at defaults to current time."""
        before = datetime.now(UTC)
        metadata = CachedClusterMetadata(cluster_name="test")
        after = datetime.now(UTC)
        assert before <= metadata.cached_at <= after

    def test_full_metadata(self) -> None:
        """Test with full metadata."""
        metadata = CachedClusterMetadata(
            cluster_name="production-cluster",
            cloud=[CloudMetadata(provider="AWS", region="us-east-1")],
            cluster=ClusterInfo(
                cluster_name="production-cluster",
                ontap_version="9.14.1",
            ),
            nodes=[
                NodeInfo(name="node1", serial_number="123"),
                NodeInfo(name="node2", serial_number="456"),
            ],
        )
        assert metadata.cloud[0].provider == "AWS"
        assert len(metadata.nodes) == 2
        assert metadata.cluster.ontap_version == "9.14.1"

    def test_is_stale_fresh(self) -> None:
        """Test is_stale returns False for fresh cache."""
        metadata = CachedClusterMetadata(cluster_name="test")
        assert metadata.is_stale(ttl_days=30) is False

    def test_is_stale_old(self) -> None:
        """Test is_stale returns True for old cache."""
        old_time = datetime.now(UTC) - timedelta(days=35)
        metadata = CachedClusterMetadata(
            cluster_name="test",
            cached_at=old_time,
        )
        assert metadata.is_stale(ttl_days=30) is True

    def test_is_stale_boundary(self) -> None:
        """Test is_stale at boundary."""
        # Exactly 30 days old - should not be stale (> not >=)
        boundary_time = datetime.now(UTC) - timedelta(days=30)
        metadata = CachedClusterMetadata(
            cluster_name="test",
            cached_at=boundary_time,
        )
        assert metadata.is_stale(ttl_days=30) is False

        # 31 days old - should be stale
        old_time = datetime.now(UTC) - timedelta(days=31)
        metadata_old = CachedClusterMetadata(
            cluster_name="test",
            cached_at=old_time,
        )
        assert metadata_old.is_stale(ttl_days=30) is True

    def test_to_flat_dict(self) -> None:
        """Test converting to flat dictionary."""
        metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            cloud=[
                CloudMetadata(
                    instance_id="i-123",
                    provider="AWS",
                    region="us-east-1",
                    instance_type="m5.xlarge",
                )
            ],
            cluster=ClusterInfo(
                cluster_uuid="abc-123",
                ontap_version="9.14.1",
                model="SIMULATED",
            ),
        )
        flat = metadata.to_flat_dict()

        assert flat["instance_id"] == "i-123"
        assert flat["provider"] == "AWS"
        assert flat["region"] == "us-east-1"
        assert flat["instance_type"] == "m5.xlarge"
        assert flat["cluster_uuid"] == "abc-123"
        assert flat["ontap_version"] == "9.14.1"
        assert flat["model"] == "SIMULATED"
        assert "_cached_at" in flat
        assert "_cache_version" in flat

    def test_model_serialization(self) -> None:
        """Test JSON serialization."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            cloud=[CloudMetadata(provider="AWS")],
        )
        json_str = metadata.model_dump_json()
        assert "test" in json_str
        assert "AWS" in json_str

    def test_model_deserialization(self) -> None:
        """Test creating from dict."""
        data = {
            "cluster_name": "test",
            "cached_at": "2024-01-15T10:30:00+00:00",
            "cache_version": "1.0",
            "cloud": [{"provider": "Azure", "region": "eastus"}],
            "cluster": {"ontap_version": "9.13.1"},
            "nodes": [],
            "network": {},
            "storage": {},
            "licenses": {},
            "ha": {},
            "relationships": {},
        }
        metadata = CachedClusterMetadata.model_validate(data)
        assert metadata.cluster_name == "test"
        assert metadata.cloud[0].provider == "Azure"
        assert metadata.cluster.ontap_version == "9.13.1"
