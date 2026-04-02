"""OntapSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmAggregate(OntapModel):
    """OntapSvmAggregate sub-model for aggregates."""

    available_size: int = 0
    name: str = ""
    snaplock_type: str = ""
    state: str = ""
    type_: str = ""
    uuid: str = ""


class OntapSvmAntiRansomwareEventLog(OntapModel):
    """OntapSvmAntiRansomwareEventLog sub-model for event_log."""

    is_enabled_on_new_file_extension_seen: bool = False
    is_enabled_on_snapshot_copy_creation: bool = False


class OntapSvmAntiRansomware(OntapModel):
    """OntapSvmAntiRansomware sub-model for anti_ransomware."""

    event_log: OntapSvmAntiRansomwareEventLog = Field(
        default_factory=OntapSvmAntiRansomwareEventLog
    )


class OntapSvmCertificate(OntapModel):
    """OntapSvmCertificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapSvmCifsAdDomain(OntapModel):
    """OntapSvmCifsAdDomain sub-model for ad_domain."""

    default_site: str = ""
    fqdn: str = ""
    organizational_unit: str = ""
    password: str = ""
    user: str = ""


class OntapSvmCifs(OntapModel):
    """OntapSvmCifs sub-model for cifs."""

    ad_domain: OntapSvmCifsAdDomain = Field(default_factory=OntapSvmCifsAdDomain)
    allowed: bool = False
    auth_style: str = ""
    domain_workgroup: str = ""
    enabled: bool = False
    name: str = ""
    workgroup: str = ""


class OntapSvmDns(OntapModel):
    """OntapSvmDns sub-model for dns."""

    domains: list[str] = Field(default_factory=list)
    servers: list[str] = Field(default_factory=list)


class OntapSvmFcInterfaceLocationPortNode(OntapModel):
    """OntapSvmFcInterfaceLocationPortNode sub-model for node."""

    name: str = ""


class OntapSvmFcInterfaceLocationPort(OntapModel):
    """OntapSvmFcInterfaceLocationPort sub-model for port."""

    name: str = ""
    node: OntapSvmFcInterfaceLocationPortNode = Field(
        default_factory=OntapSvmFcInterfaceLocationPortNode
    )
    uuid: str = ""


class OntapSvmFcInterfaceLocation(OntapModel):
    """OntapSvmFcInterfaceLocation sub-model for location."""

    port: OntapSvmFcInterfaceLocationPort = Field(default_factory=OntapSvmFcInterfaceLocationPort)


class OntapSvmFcInterface(OntapModel):
    """OntapSvmFcInterface sub-model for fc_interfaces."""

    data_protocol: str = ""
    location: OntapSvmFcInterfaceLocation = Field(default_factory=OntapSvmFcInterfaceLocation)
    name: str = ""
    uuid: str = ""


class OntapSvmFcp(OntapModel):
    """OntapSvmFcp sub-model for fcp."""

    allowed: bool = False
    enabled: bool = False


class OntapSvmIpInterfaceIp(OntapModel):
    """OntapSvmIpInterfaceIp sub-model for ip."""

    address: str = ""
    netmask: str = ""


class OntapSvmIpInterfaceLocationBroadcastDomain(OntapModel):
    """OntapSvmIpInterfaceLocationBroadcastDomain sub-model for broadcast_domain."""

    name: str = ""
    uuid: str = ""


class OntapSvmIpInterfaceLocationHomeNode(OntapModel):
    """OntapSvmIpInterfaceLocationHomeNode sub-model for home_node."""

    name: str = ""
    uuid: str = ""


class OntapSvmIpInterfaceLocationHomePort(OntapModel):
    """OntapSvmIpInterfaceLocationHomePort sub-model for home_port."""

    name: str = ""
    uuid: str = ""


class OntapSvmIpInterfaceLocation(OntapModel):
    """OntapSvmIpInterfaceLocation sub-model for location."""

    broadcast_domain: OntapSvmIpInterfaceLocationBroadcastDomain = Field(
        default_factory=OntapSvmIpInterfaceLocationBroadcastDomain
    )
    home_node: OntapSvmIpInterfaceLocationHomeNode = Field(
        default_factory=OntapSvmIpInterfaceLocationHomeNode
    )
    home_port: OntapSvmIpInterfaceLocationHomePort = Field(
        default_factory=OntapSvmIpInterfaceLocationHomePort
    )


class OntapSvmIpInterfaceSubnet(OntapModel):
    """OntapSvmIpInterfaceSubnet sub-model for subnet."""

    name: str = ""
    uuid: str = ""


class OntapSvmIpInterface(OntapModel):
    """OntapSvmIpInterface sub-model for ip_interfaces."""

    ip: OntapSvmIpInterfaceIp = Field(default_factory=OntapSvmIpInterfaceIp)
    location: OntapSvmIpInterfaceLocation = Field(default_factory=OntapSvmIpInterfaceLocation)
    name: str = ""
    service_policy: str = ""
    services: list[str] = Field(default_factory=list)
    subnet: OntapSvmIpInterfaceSubnet = Field(default_factory=OntapSvmIpInterfaceSubnet)
    uuid: str = ""


class OntapSvmIpspace(OntapModel):
    """OntapSvmIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapSvmIscsi(OntapModel):
    """OntapSvmIscsi sub-model for iscsi."""

    allowed: bool = False
    enabled: bool = False


class OntapSvmLdap(OntapModel):
    """OntapSvmLdap sub-model for ldap."""

    ad_domain: str = ""
    base_dn: str = ""
    bind_dn: str = ""
    enabled: bool = False
    restrict_discovery_to_site: bool = False
    servers: list[str] = Field(default_factory=list)


class OntapSvmNdmp(OntapModel):
    """OntapSvmNdmp sub-model for ndmp."""

    allowed: bool = False


class OntapSvmNfs(OntapModel):
    """OntapSvmNfs sub-model for nfs."""

    allowed: bool = False
    enabled: bool = False


class OntapSvmNis(OntapModel):
    """OntapSvmNis sub-model for nis."""

    domain: str = ""
    enabled: bool = False
    servers: list[str] = Field(default_factory=list)


class OntapSvmNsswitch(OntapModel):
    """OntapSvmNsswitch sub-model for nsswitch."""

    group: list[str] = Field(default_factory=list)
    hosts: list[str] = Field(default_factory=list)
    namemap: list[str] = Field(default_factory=list)
    netgroup: list[str] = Field(default_factory=list)
    passwd: list[str] = Field(default_factory=list)


class OntapSvmNvme(OntapModel):
    """OntapSvmNvme sub-model for nvme."""

    allowed: bool = False
    enabled: bool = False


class OntapSvmQosAdaptivePolicyGroupTemplate(OntapModel):
    """OntapSvmQosAdaptivePolicyGroupTemplate sub-model for qos_adaptive_policy_group_template."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapSvmQosPolicy(OntapModel):
    """OntapSvmQosPolicy sub-model for qos_policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapSvmQosPolicyGroupTemplate(OntapModel):
    """OntapSvmQosPolicyGroupTemplate sub-model for qos_policy_group_template."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapSvmRouteDestination(OntapModel):
    """OntapSvmRouteDestination sub-model for destination."""

    address: str = ""
    family: str = ""
    netmask: str = ""


class OntapSvmRoute(OntapModel):
    """OntapSvmRoute sub-model for routes."""

    destination: OntapSvmRouteDestination = Field(default_factory=OntapSvmRouteDestination)
    gateway: str = ""


class OntapSvmS3Certificate(OntapModel):
    """OntapSvmS3Certificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapSvmS3(OntapModel):
    """OntapSvmS3 sub-model for s3."""

    allowed: bool = False
    certificate: OntapSvmS3Certificate = Field(default_factory=OntapSvmS3Certificate)
    default_unix_user: str = ""
    default_win_user: str = ""
    enabled: bool = False
    is_http_enabled: bool = False
    is_https_enabled: bool = False
    name: str = ""
    port: int = 0
    secure_port: int = 0


class OntapSvmSnapmirror(OntapModel):
    """OntapSvmSnapmirror sub-model for snapmirror."""

    is_protected: bool = False
    protected_consistency_group_count: int = 0
    protected_volumes_count: int = 0


class OntapSvmSnapshotPolicy(OntapModel):
    """OntapSvmSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapSvmStorage(OntapModel):
    """OntapSvmStorage sub-model for storage."""

    allocated: int = 0
    available: int = 0
    limit: int = 0
    limit_threshold_alert: int = 0
    limit_threshold_exceeded: bool = False
    used_percentage: int = 0


class OntapSvm(OntapModel):
    """OntapSvm information."""

    aggregates: list[OntapSvmAggregate] = Field(default_factory=list)
    aggregates_delegated: bool = False
    anti_ransomware: OntapSvmAntiRansomware = Field(default_factory=OntapSvmAntiRansomware)
    anti_ransomware_auto_switch_duration_without_new_file_extension: int = 0
    anti_ransomware_auto_switch_from_learning_to_enabled: bool = False
    anti_ransomware_auto_switch_minimum_file_count: int = 0
    anti_ransomware_auto_switch_minimum_file_extension: int = 0
    anti_ransomware_auto_switch_minimum_incoming_data: str = ""
    anti_ransomware_auto_switch_minimum_learning_period: int = 0
    anti_ransomware_default_volume_state: str = ""
    anti_ransomware_incoming_write_threshold: str = ""
    anti_ransomware_incoming_write_threshold_percent: str = ""
    auto_enable_activity_tracking: bool = False
    auto_enable_analytics: bool = False
    certificate: OntapSvmCertificate = Field(default_factory=OntapSvmCertificate)
    cifs: OntapSvmCifs = Field(default_factory=OntapSvmCifs)
    comment: str = ""
    dns: OntapSvmDns = Field(default_factory=OntapSvmDns)
    fc_interfaces: list[OntapSvmFcInterface] = Field(default_factory=list)
    fcp: OntapSvmFcp = Field(default_factory=OntapSvmFcp)
    ip_interfaces: list[OntapSvmIpInterface] = Field(default_factory=list)
    ipspace: OntapSvmIpspace = Field(default_factory=OntapSvmIpspace)
    is_space_enforcement_logical: bool = False
    is_space_reporting_logical: bool = False
    iscsi: OntapSvmIscsi = Field(default_factory=OntapSvmIscsi)
    language: str = ""
    ldap: OntapSvmLdap = Field(default_factory=OntapSvmLdap)
    max_volumes: str = ""
    name: str = ""
    ndmp: OntapSvmNdmp = Field(default_factory=OntapSvmNdmp)
    nfs: OntapSvmNfs = Field(default_factory=OntapSvmNfs)
    nis: OntapSvmNis = Field(default_factory=OntapSvmNis)
    nsswitch: OntapSvmNsswitch = Field(default_factory=OntapSvmNsswitch)
    number_of_volumes_in_recovery_queue: int = 0
    nvme: OntapSvmNvme = Field(default_factory=OntapSvmNvme)
    qos_adaptive_policy_group_template: OntapSvmQosAdaptivePolicyGroupTemplate = Field(
        default_factory=OntapSvmQosAdaptivePolicyGroupTemplate
    )
    qos_policy: OntapSvmQosPolicy = Field(default_factory=OntapSvmQosPolicy)
    qos_policy_group_template: OntapSvmQosPolicyGroupTemplate = Field(
        default_factory=OntapSvmQosPolicyGroupTemplate
    )
    routes: list[OntapSvmRoute] = Field(default_factory=list)
    s3: OntapSvmS3 = Field(default_factory=OntapSvmS3)
    snapmirror: OntapSvmSnapmirror = Field(default_factory=OntapSvmSnapmirror)
    snapshot_policy: OntapSvmSnapshotPolicy = Field(default_factory=OntapSvmSnapshotPolicy)
    state: str = ""
    storage: OntapSvmStorage = Field(default_factory=OntapSvmStorage)
    subtype: str = ""
    total_volume_size_in_recovery_queue: int = 0
    uuid: str = ""
