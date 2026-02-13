"""Tests for cache Pydantic models."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pynetappfoundry.cache import CachedClusterMetadata, HasUUID, MediatorInfo, RelationshipsInfo
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.cloud.targets.model import CloudTargetInfo
from pynetappfoundry.cache.cluster.licensing.model import (
    LicenseInstance,
    LicensePackage,
)
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.cluster.nodes.model import NodeInfo
from pynetappfoundry.cache.cluster.peers.model import ClusterPeer
from pynetappfoundry.cache.cluster.schedules.model import ScheduleInfo
from pynetappfoundry.cache.name_services.dns.model import DNSInfo
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import (
    BroadcastDomain,
)
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF
from pynetappfoundry.cache.network.ip.subnets.model import IPSubnetInfo
from pynetappfoundry.cache.network.model import NetworkInfo
from pynetappfoundry.cache.protocols.cifs.services.model import CIFSServiceInfo
from pynetappfoundry.cache.protocols.cifs.shares.model import CIFSShareInfo
from pynetappfoundry.cache.protocols.model import ProtocolsInfo
from pynetappfoundry.cache.protocols.nfs.export_policies.model import (
    ExportPolicyInfo,
    ExportRuleInfo,
)
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
from pynetappfoundry.cache.storage.snapshot_policies.model import (
    SnapshotPolicyInfo,
    SnapshotScheduleInfo,
)
from pynetappfoundry.cache.storage.volumes.model import VolumeInfo
from pynetappfoundry.cache.svm.model import SVMInfo
from pynetappfoundry.cache.svm.peers.model import SVMPeerInfo


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
            version_generation="SIMULATED",
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
        assert node.membership == ""
        assert node.location == ""

    def test_with_values(self) -> None:
        """Test with node data."""
        node = NodeInfo(
            uuid="node-uuid-1",
            name="node1",
            serial_number="123456789",
            system_id="0123456789",
            model="SIMULATED",
            membership="available",
            location="rack-1",
        )
        assert node.uuid == "node-uuid-1"
        assert node.name == "node1"
        assert node.serial_number == "123456789"
        assert node.membership == "available"
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
        assert bd.ipspace_uuid == ""
        assert bd.port_uuids == []

    def test_with_values(self) -> None:
        """Test with broadcast domain data."""
        bd = BroadcastDomain(
            name="Default",
            ipspace_uuid="ipspace-uuid-1",
            mtu=1500,
            port_uuids=["port-uuid-1", "port-uuid-2"],
        )
        assert bd.name == "Default"
        assert bd.ipspace_uuid == "ipspace-uuid-1"
        assert len(bd.port_uuids) == 2


class TestNetworkInfo:
    """Tests for NetworkInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        network = NetworkInfo()
        assert network.intercluster_lifs == []
        assert network.data_lifs == []
        assert network.ipspaces == []
        assert network.dns == []
        assert network.subnets == []

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
        assert svm.language == ""
        assert svm.subtype == ""
        assert svm.aggregate_uuids == []
        assert svm.nfs_enabled is False
        assert svm.nfs_allowed is True

    def test_with_values(self) -> None:
        """Test with SVM data."""
        svm = SVMInfo(
            uuid="svm-uuid-1",
            name="svm1",
            subtype="default",
            language="c.utf_8",
            nfs_enabled=True,
            cifs_enabled=True,
            aggregate_uuids=["aggr-uuid-1", "aggr-uuid-2"],
        )
        assert svm.uuid == "svm-uuid-1"
        assert svm.name == "svm1"
        assert svm.subtype == "default"
        assert svm.language == "c.utf_8"
        assert svm.nfs_enabled is True
        assert svm.cifs_enabled is True
        assert svm.aggregate_uuids == ["aggr-uuid-1", "aggr-uuid-2"]


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
        assert storage.luns == []
        assert storage.igroups == []
        assert storage.qos_policies == []
        assert storage.flexcaches == []

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


class TestLunInfo:
    """Tests for LunInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        lun = LunInfo()
        assert lun.uuid == ""
        assert lun.name == ""
        assert lun.svm == ""
        assert lun.volume == ""
        assert lun.size == 0
        assert lun.os_type == ""
        assert lun.enabled is True
        assert lun.qos_policy == ""

    def test_with_values(self) -> None:
        """Test with LUN data."""
        lun = LunInfo(
            uuid="lun-uuid-1",
            name="/vol/vol1/lun1",
            svm="svm1",
            volume="vol1",
            size=10737418240,
            os_type="linux",
            serial_number="ABC123",
            enabled=True,
            comment="Test LUN",
            qos_policy="qos1",
        )
        assert lun.name == "/vol/vol1/lun1"
        assert lun.os_type == "linux"
        assert lun.size == 10737418240


class TestIgroupInfo:
    """Tests for IgroupInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        igroup = IgroupInfo()
        assert igroup.uuid == ""
        assert igroup.name == ""
        assert igroup.svm == ""
        assert igroup.protocol == ""
        assert igroup.os_type == ""
        assert igroup.initiators == []

    def test_with_values(self) -> None:
        """Test with igroup data."""
        igroup = IgroupInfo(
            uuid="ig-uuid-1",
            name="igroup1",
            svm="svm1",
            protocol="iscsi",
            os_type="linux",
            initiators=["iqn.1991-05.com.example:host1", "iqn.1991-05.com.example:host2"],
            comment="Test igroup",
        )
        assert igroup.name == "igroup1"
        assert igroup.protocol == "iscsi"
        assert len(igroup.initiators) == 2


class TestQosPolicyInfo:
    """Tests for QosPolicyInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        qos = QosPolicyInfo()
        assert qos.uuid == ""
        assert qos.name == ""
        assert qos.scope == ""
        assert qos.fixed_max_throughput_iops == 0
        assert qos.adaptive_expected_iops == 0

    def test_with_fixed_values(self) -> None:
        """Test with fixed QoS policy data."""
        qos = QosPolicyInfo(
            uuid="qos-uuid-1",
            name="qos-fixed",
            svm="svm1",
            scope="svm",
            policy_class="user_defined",
            fixed_max_throughput_iops=5000,
            fixed_max_throughput_mbps=200,
        )
        assert qos.name == "qos-fixed"
        assert qos.fixed_max_throughput_iops == 5000

    def test_with_adaptive_values(self) -> None:
        """Test with adaptive QoS policy data."""
        qos = QosPolicyInfo(
            uuid="qos-uuid-2",
            name="qos-adaptive",
            svm="svm1",
            scope="svm",
            policy_class="user_defined",
            adaptive_expected_iops=3000,
            adaptive_peak_iops=6000,
            adaptive_block_size="any",
        )
        assert qos.adaptive_expected_iops == 3000
        assert qos.adaptive_peak_iops == 6000
        assert qos.adaptive_block_size == "any"


class TestNFSServiceInfo:
    """Tests for NFSServiceInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        nfs = NFSServiceInfo()
        assert nfs.svm == ""
        assert nfs.enabled is False
        assert nfs.protocol_v3_enabled is False
        assert nfs.protocol_v4_enabled is False
        assert nfs.protocol_v41_enabled is False
        assert nfs.showmount_enabled is False
        assert nfs.vstorage_enabled is False

    def test_with_values(self) -> None:
        """Test with NFS service data."""
        nfs = NFSServiceInfo(
            svm="svm1",
            enabled=True,
            protocol_v3_enabled=True,
            protocol_v4_enabled=True,
            protocol_v41_enabled=False,
            showmount_enabled=True,
            vstorage_enabled=False,
        )
        assert nfs.svm == "svm1"
        assert nfs.enabled is True
        assert nfs.protocol_v3_enabled is True
        assert nfs.protocol_v41_enabled is False


class TestCIFSServiceInfo:
    """Tests for CIFSServiceInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        cifs = CIFSServiceInfo()
        assert cifs.svm == ""
        assert cifs.name == ""
        assert cifs.enabled is False
        assert cifs.ad_domain == ""
        assert cifs.netbios_aliases == []

    def test_with_values(self) -> None:
        """Test with CIFS service data."""
        cifs = CIFSServiceInfo(
            svm="svm1",
            name="CIFSSERVER",
            enabled=True,
            ad_domain="example.com",
            comment="Production CIFS",
            default_unix_user="pcuser",
            netbios_aliases=["ALIAS1", "ALIAS2"],
        )
        assert cifs.svm == "svm1"
        assert cifs.name == "CIFSSERVER"
        assert cifs.enabled is True
        assert cifs.ad_domain == "example.com"
        assert len(cifs.netbios_aliases) == 2


class TestDNSInfo:
    """Tests for DNSInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        dns = DNSInfo()
        assert dns.uuid == ""
        assert dns.svm_uuid == ""
        assert dns.scope == ""
        assert dns.domains == []
        assert dns.servers == []
        assert dns.timeout == 0
        assert dns.attempts == 0
        assert dns.dynamic_dns_enabled is False
        assert dns.dynamic_dns_fqdn == ""
        assert dns.dynamic_dns_time_to_live == ""
        assert dns.dynamic_dns_use_secure is False
        assert dns.packet_query_match is True
        assert dns.source_address_match is True
        assert dns.tld_query_enabled is True
        assert dns.service_ips == []

    def test_with_values(self) -> None:
        """Test with DNS data."""
        dns = DNSInfo(
            uuid="dns-uuid-1",
            svm_uuid="svm-uuid-1",
            scope="svm",
            domains=["example.com", "corp.example.com"],
            servers=["10.0.0.1", "10.0.0.2"],
            timeout=2,
            attempts=1,
        )
        assert dns.svm_uuid == "svm-uuid-1"
        assert dns.scope == "svm"
        assert len(dns.domains) == 2
        assert len(dns.servers) == 2
        assert dns.timeout == 2


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
        assert protocols.nfs_services == []
        assert protocols.cifs_services == []
        assert protocols.s3_buckets == []

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

    def test_with_nfs_services(self) -> None:
        """Test with NFS service data."""
        nfs = NFSServiceInfo(svm="svm1", enabled=True)
        protocols = ProtocolsInfo(nfs_services=[nfs])
        assert len(protocols.nfs_services) == 1
        assert protocols.nfs_services[0].svm == "svm1"

    def test_with_cifs_services(self) -> None:
        """Test with CIFS service data."""
        cifs = CIFSServiceInfo(svm="svm1", name="CIFSSERVER", enabled=True)
        protocols = ProtocolsInfo(cifs_services=[cifs])
        assert len(protocols.cifs_services) == 1
        assert protocols.cifs_services[0].name == "CIFSSERVER"

    def test_with_s3_buckets(self) -> None:
        """Test with S3 bucket data."""
        bucket = S3BucketInfo(name="mybucket", svm="svm1")
        protocols = ProtocolsInfo(s3_buckets=[bucket])
        assert len(protocols.s3_buckets) == 1
        assert protocols.s3_buckets[0].name == "mybucket"


class TestFlexCacheInfo:
    """Tests for FlexCacheInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        fc = FlexCacheInfo()
        assert fc.uuid == ""
        assert fc.name == ""
        assert fc.svm == ""
        assert fc.path == ""
        assert fc.size == 0
        assert fc.origins == []
        assert fc.global_file_locking_enabled is False
        assert fc.dr_cache is False

    def test_with_values(self) -> None:
        """Test with FlexCache data."""
        fc = FlexCacheInfo(
            uuid="fc-uuid-1",
            name="fc_vol1",
            svm="svm1",
            path="/fc_vol1",
            size=1073741824,
            origins=["svm1:origin_vol1"],
            global_file_locking_enabled=True,
            dr_cache=False,
        )
        assert fc.uuid == "fc-uuid-1"
        assert fc.name == "fc_vol1"
        assert fc.svm == "svm1"
        assert fc.size == 1073741824
        assert fc.origins == ["svm1:origin_vol1"]
        assert fc.global_file_locking_enabled is True


class TestSVMPeerInfo:
    """Tests for SVMPeerInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        peer = SVMPeerInfo()
        assert peer.uuid == ""
        assert peer.name == ""
        assert peer.svm == ""
        assert peer.peer_svm == ""
        assert peer.peer_cluster == ""
        assert peer.state == ""
        assert peer.applications == []

    def test_with_values(self) -> None:
        """Test with SVM peer data."""
        peer = SVMPeerInfo(
            uuid="svmpeer-uuid-1",
            name="svm1_to_svm2",
            svm="svm1",
            peer_svm="svm2",
            peer_cluster="remote-cluster",
            state="peered",
            applications=["snapmirror"],
        )
        assert peer.uuid == "svmpeer-uuid-1"
        assert peer.name == "svm1_to_svm2"
        assert peer.svm == "svm1"
        assert peer.peer_svm == "svm2"
        assert peer.peer_cluster == "remote-cluster"
        assert peer.state == "peered"
        assert peer.applications == ["snapmirror"]


class TestS3BucketInfo:
    """Tests for S3BucketInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        bucket = S3BucketInfo()
        assert bucket.uuid == ""
        assert bucket.name == ""
        assert bucket.svm == ""
        assert bucket.type == ""
        assert bucket.size == 0
        assert bucket.versioning_state == ""
        assert bucket.comment == ""
        assert bucket.nas_path == ""

    def test_with_values(self) -> None:
        """Test with S3 bucket data."""
        bucket = S3BucketInfo(
            uuid="bucket-uuid-1",
            name="mybucket",
            svm="svm1",
            type="s3",
            size=1073741824,
            versioning_state="enabled",
            comment="Test bucket",
            nas_path="/vol1",
        )
        assert bucket.uuid == "bucket-uuid-1"
        assert bucket.name == "mybucket"
        assert bucket.svm == "svm1"
        assert bucket.type == "s3"
        assert bucket.size == 1073741824
        assert bucket.versioning_state == "enabled"
        assert bucket.nas_path == "/vol1"


class TestIPSubnetInfo:
    """Tests for IPSubnetInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        subnet = IPSubnetInfo()
        assert subnet.uuid == ""
        assert subnet.name == ""
        assert subnet.ipspace == ""
        assert subnet.broadcast_domain == ""
        assert subnet.subnet == ""
        assert subnet.gateway == ""
        assert subnet.ip_ranges == []

    def test_with_values(self) -> None:
        """Test with IP subnet data."""
        subnet = IPSubnetInfo(
            uuid="subnet-uuid-1",
            name="data-subnet",
            ipspace="Default",
            broadcast_domain="Default",
            subnet="10.0.0.0/24",
            gateway="10.0.0.1",
            ip_ranges=["10.0.0.10-10.0.0.50"],
        )
        assert subnet.uuid == "subnet-uuid-1"
        assert subnet.name == "data-subnet"
        assert subnet.ipspace == "Default"
        assert subnet.broadcast_domain == "Default"
        assert subnet.subnet == "10.0.0.0/24"
        assert subnet.gateway == "10.0.0.1"
        assert subnet.ip_ranges == ["10.0.0.10-10.0.0.50"]


class TestLicenseInstance:
    """Tests for LicenseInstance model."""

    def test_default_values(self) -> None:
        """Test default values."""
        inst = LicenseInstance()
        assert inst.active is False
        assert inst.capacity_max == 0
        assert inst.compliance_state == ""
        assert inst.evaluation is False
        assert inst.expiry_time == ""
        assert inst.host_id == ""
        assert inst.installed_license == ""
        assert inst.owner == ""
        assert inst.serial_number == ""
        assert inst.shutdown_imminent is False
        assert inst.start_time == ""

    def test_with_values(self) -> None:
        """Test with license instance data."""
        inst = LicenseInstance(
            active=True,
            capacity_max=109951162777600,
            compliance_state="compliant",
            evaluation=False,
            host_id="4082368507",
            installed_license="Enterprise",
            owner="node1",
            serial_number="123456789",
            shutdown_imminent=False,
        )
        assert inst.active is True
        assert inst.capacity_max == 109951162777600
        assert inst.compliance_state == "compliant"
        assert inst.host_id == "4082368507"
        assert inst.serial_number == "123456789"


class TestLicensePackage:
    """Tests for LicensePackage model."""

    def test_default_values(self) -> None:
        """Test default values."""
        pkg = LicensePackage()
        assert pkg.name == ""
        assert pkg.scope == ""
        assert pkg.state == ""
        assert pkg.description == ""
        assert pkg.entitlement_action == ""
        assert pkg.entitlement_risk == ""
        assert pkg.instances == []

    def test_with_nested_instances(self) -> None:
        """Test with nested license instances."""
        inst = LicenseInstance(
            active=True,
            compliance_state="compliant",
            owner="node1",
            serial_number="123456789",
        )
        pkg = LicensePackage(
            name="NFS",
            scope="cluster",
            state="compliant",
            description="NFS License",
            entitlement_action="none",
            entitlement_risk="low",
            instances=[inst],
        )
        assert pkg.name == "NFS"
        assert pkg.scope == "cluster"
        assert pkg.state == "compliant"
        assert len(pkg.instances) == 1
        assert pkg.instances[0].owner == "node1"


class TestMediatorInfo:
    """Tests for MediatorInfo model."""

    def test_default_values(self) -> None:
        """Test default values."""
        mediator = MediatorInfo()
        assert mediator.mediator_address == ""
        assert mediator.mediator_uuid == ""
        assert mediator.mediator_port == 0

    def test_populated(self) -> None:
        """Test populated mediator configuration."""
        mediator = MediatorInfo(
            mediator_address="10.0.0.100",
            mediator_uuid="med-uuid-1",
            mediator_port=31784,
        )
        assert mediator.mediator_address == "10.0.0.100"
        assert mediator.mediator_uuid == "med-uuid-1"
        assert mediator.mediator_port == 31784


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
        assert rel.svm_peers == []


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
                version_generation="SIMULATED",
            ),
        )
        flat = metadata.to_flat_dict()

        assert flat["instance_id"] == "i-123"
        assert flat["provider"] == "AWS"
        assert flat["region"] == "us-east-1"
        assert flat["instance_type"] == "m5.xlarge"
        assert flat["cluster_uuid"] == "abc-123"
        assert flat["ontap_version"] == "9.14.1"
        assert flat["version_generation"] == "SIMULATED"
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
            "license_packages": [],
            "ha": {},
            "relationships": {},
        }
        metadata = CachedClusterMetadata.model_validate(data)
        assert metadata.cluster_name == "test"
        assert metadata.cloud[0].provider == "Azure"
        assert metadata.cluster.ontap_version == "9.13.1"


class TestUuidIndex:
    """Tests for CachedClusterMetadata.uuid_index cached property."""

    def test_empty_cache(self) -> None:
        """Test uuid_index is empty when all lists are defaults."""
        metadata = CachedClusterMetadata(cluster_name="test")
        assert metadata.uuid_index == {}

    def test_single_type(self) -> None:
        """Test uuid_index with two NodeInfo objects."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[
                NodeInfo(uuid="node-1", name="node1"),
                NodeInfo(uuid="node-2", name="node2"),
            ],
        )
        assert len(metadata.uuid_index) == 2
        assert metadata.uuid_index["node-1"].uuid == "node-1"
        assert metadata.uuid_index["node-2"].uuid == "node-2"

    def test_multiple_types(self) -> None:
        """Test uuid_index spans multiple categories."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[NodeInfo(uuid="uuid-node", name="node1")],
            storage=StorageInfo(
                volumes=[VolumeInfo(uuid="uuid-vol", name="vol1")],
            ),
            relationships=RelationshipsInfo(
                cluster_peers=[ClusterPeer(uuid="uuid-peer", name="peer1")],
            ),
            protocols=ProtocolsInfo(
                s3_buckets=[S3BucketInfo(uuid="uuid-bucket", name="bucket1")],
            ),
        )
        index = metadata.uuid_index
        assert len(index) == 4
        assert isinstance(index["uuid-node"], NodeInfo)
        assert isinstance(index["uuid-vol"], VolumeInfo)
        assert isinstance(index["uuid-peer"], ClusterPeer)
        assert isinstance(index["uuid-bucket"], S3BucketInfo)

    def test_skips_empty_uuid(self) -> None:
        """Test that objects with empty uuid are excluded from the index."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[
                NodeInfo(uuid="", name="no-uuid-node"),
                NodeInfo(uuid="real-uuid", name="has-uuid-node"),
            ],
        )
        assert len(metadata.uuid_index) == 1
        assert "real-uuid" in metadata.uuid_index
        assert "" not in metadata.uuid_index

    def test_missing_uuid_returns_none(self) -> None:
        """Test that looking up a nonexistent UUID returns None via .get()."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[NodeInfo(uuid="exists", name="node1")],
        )
        assert metadata.uuid_index.get("nonexistent") is None

    def test_is_cached(self) -> None:
        """Test that uuid_index is the same object on repeated access."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[NodeInfo(uuid="node-1", name="node1")],
        )
        first = metadata.uuid_index
        second = metadata.uuid_index
        assert first is second

    def test_all_18_types(self) -> None:
        """Test that all 18 UUID-bearing types are included in the index."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[NodeInfo(uuid="uuid-01")],
            network=NetworkInfo(
                broadcast_domains=[BroadcastDomain(uuid="uuid-02")],
                subnets=[IPSubnetInfo(uuid="uuid-03")],
                dns=[DNSInfo(uuid="uuid-04")],
            ),
            storage=StorageInfo(
                aggregates=[AggregateInfo(uuid="uuid-05")],
                svms=[SVMInfo(uuid="uuid-06")],
                cloud_targets=[CloudTargetInfo(uuid="uuid-07")],
                volumes=[VolumeInfo(uuid="uuid-08")],
                snapshot_policies=[SnapshotPolicyInfo(uuid="uuid-09")],
                schedules=[ScheduleInfo(uuid="uuid-10")],
                luns=[LunInfo(uuid="uuid-11")],
                igroups=[IgroupInfo(uuid="uuid-12")],
                qos_policies=[QosPolicyInfo(uuid="uuid-13")],
                flexcaches=[FlexCacheInfo(uuid="uuid-14")],
            ),
            relationships=RelationshipsInfo(
                snapmirror_destinations=[SnapMirrorRelationship(uuid="uuid-15")],
                cluster_peers=[ClusterPeer(uuid="uuid-16")],
                svm_peers=[SVMPeerInfo(uuid="uuid-17")],
            ),
            protocols=ProtocolsInfo(
                s3_buckets=[S3BucketInfo(uuid="uuid-18")],
            ),
        )
        index = metadata.uuid_index
        assert len(index) == 18
        assert isinstance(index["uuid-01"], NodeInfo)
        assert isinstance(index["uuid-02"], BroadcastDomain)
        assert isinstance(index["uuid-03"], IPSubnetInfo)
        assert isinstance(index["uuid-04"], DNSInfo)
        assert isinstance(index["uuid-05"], AggregateInfo)
        assert isinstance(index["uuid-06"], SVMInfo)
        assert isinstance(index["uuid-07"], CloudTargetInfo)
        assert isinstance(index["uuid-08"], VolumeInfo)
        assert isinstance(index["uuid-09"], SnapshotPolicyInfo)
        assert isinstance(index["uuid-10"], ScheduleInfo)
        assert isinstance(index["uuid-11"], LunInfo)
        assert isinstance(index["uuid-12"], IgroupInfo)
        assert isinstance(index["uuid-13"], QosPolicyInfo)
        assert isinstance(index["uuid-14"], FlexCacheInfo)
        assert isinstance(index["uuid-15"], SnapMirrorRelationship)
        assert isinstance(index["uuid-16"], ClusterPeer)
        assert isinstance(index["uuid-17"], SVMPeerInfo)
        assert isinstance(index["uuid-18"], S3BucketInfo)

    def test_excludes_non_uuid_models(self) -> None:
        """Test that models without uuid fields don't appear in the index."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            cloud=[CloudMetadata(instance_id="i-123", provider="AWS")],
            cluster=ClusterInfo(cluster_uuid="cluster-uuid-1"),
            protocols=ProtocolsInfo(
                export_policies=[ExportPolicyInfo(id=1, name="default")],
            ),
            storage=StorageInfo(
                qtrees=[QtreeInfo(id=1, name="qt1")],
            ),
        )
        assert metadata.uuid_index == {}

    def test_cross_reference_use_case(self) -> None:
        """Test resolving a SnapMirror transfer_schedule_uuid to its ScheduleInfo."""
        schedule_uuid = "sched-uuid-abc"
        metadata = CachedClusterMetadata(
            cluster_name="test",
            storage=StorageInfo(
                schedules=[
                    ScheduleInfo(uuid=schedule_uuid, name="hourly"),
                ],
            ),
            relationships=RelationshipsInfo(
                snapmirror_destinations=[
                    SnapMirrorRelationship(
                        uuid="sm-uuid-1",
                        source_path="svm1:vol1",
                        destination_path="svm2:vol1_dp",
                        transfer_schedule_uuid=schedule_uuid,
                    ),
                ],
            ),
        )
        rel = metadata.relationships.snapmirror_destinations[0]
        schedule = metadata.uuid_index.get(rel.transfer_schedule_uuid)
        assert schedule is not None
        assert isinstance(schedule, ScheduleInfo)
        assert schedule.name == "hourly"

    def test_not_in_model_dump(self) -> None:
        """Test that uuid_index does not appear in model_dump() output."""
        metadata = CachedClusterMetadata(
            cluster_name="test",
            nodes=[NodeInfo(uuid="node-1", name="node1")],
        )
        # Access uuid_index to ensure it's been computed
        _ = metadata.uuid_index
        dump = metadata.model_dump()
        assert "uuid_index" not in dump

    def test_has_uuid_protocol(self) -> None:
        """Test that HasUUID protocol works as runtime checkable."""
        node = NodeInfo(uuid="test-uuid")
        assert isinstance(node, HasUUID)

        # Models without uuid field should not satisfy the protocol
        lif = NetworkLIF(name="lif1")
        assert not isinstance(lif, HasUUID)
