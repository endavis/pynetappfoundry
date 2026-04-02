# ruff: noqa: N815
"""OntapNfsService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNfsServiceAccessCacheConfig(OntapModel):
    """OntapNfsServiceAccessCacheConfig sub-model for access_cache_config."""

    harvest_timeout: int = 0
    isDnsTTLEnabled: bool = False
    ttl_failure: int = 0
    ttl_negative: int = 0
    ttl_positive: int = 0


class OntapNfsServiceCredentialCache(OntapModel):
    """OntapNfsServiceCredentialCache sub-model for credential_cache."""

    negative_ttl: int = 0
    positive_ttl: int = 0
    transient_error_ttl: int = 0


class OntapNfsServiceExports(OntapModel):
    """OntapNfsServiceExports sub-model for exports."""

    name_service_lookup_protocol: str = ""
    netgroup_trust_any_nsswitch_no_match: bool = False


class OntapNfsServiceMetricV3Iops(OntapModel):
    """OntapNfsServiceMetricV3Iops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV3Latency(OntapModel):
    """OntapNfsServiceMetricV3Latency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV3Throughput(OntapModel):
    """OntapNfsServiceMetricV3Throughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV3(OntapModel):
    """OntapNfsServiceMetricV3 sub-model for v3."""

    duration: str = ""
    iops: OntapNfsServiceMetricV3Iops = Field(default_factory=OntapNfsServiceMetricV3Iops)
    latency: OntapNfsServiceMetricV3Latency = Field(default_factory=OntapNfsServiceMetricV3Latency)
    status: str = ""
    throughput: OntapNfsServiceMetricV3Throughput = Field(
        default_factory=OntapNfsServiceMetricV3Throughput
    )
    timestamp: str = ""


class OntapNfsServiceMetricV4Iops(OntapModel):
    """OntapNfsServiceMetricV4Iops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV4Latency(OntapModel):
    """OntapNfsServiceMetricV4Latency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV4Throughput(OntapModel):
    """OntapNfsServiceMetricV4Throughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV4(OntapModel):
    """OntapNfsServiceMetricV4 sub-model for v4."""

    duration: str = ""
    iops: OntapNfsServiceMetricV4Iops = Field(default_factory=OntapNfsServiceMetricV4Iops)
    latency: OntapNfsServiceMetricV4Latency = Field(default_factory=OntapNfsServiceMetricV4Latency)
    status: str = ""
    throughput: OntapNfsServiceMetricV4Throughput = Field(
        default_factory=OntapNfsServiceMetricV4Throughput
    )
    timestamp: str = ""


class OntapNfsServiceMetricV41Iops(OntapModel):
    """OntapNfsServiceMetricV41Iops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV41Latency(OntapModel):
    """OntapNfsServiceMetricV41Latency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV41Throughput(OntapModel):
    """OntapNfsServiceMetricV41Throughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceMetricV41(OntapModel):
    """OntapNfsServiceMetricV41 sub-model for v41."""

    duration: str = ""
    iops: OntapNfsServiceMetricV41Iops = Field(default_factory=OntapNfsServiceMetricV41Iops)
    latency: OntapNfsServiceMetricV41Latency = Field(
        default_factory=OntapNfsServiceMetricV41Latency
    )
    status: str = ""
    throughput: OntapNfsServiceMetricV41Throughput = Field(
        default_factory=OntapNfsServiceMetricV41Throughput
    )
    timestamp: str = ""


class OntapNfsServiceMetric(OntapModel):
    """OntapNfsServiceMetric sub-model for metric."""

    v3: OntapNfsServiceMetricV3 = Field(default_factory=OntapNfsServiceMetricV3)
    v4: OntapNfsServiceMetricV4 = Field(default_factory=OntapNfsServiceMetricV4)
    v41: OntapNfsServiceMetricV41 = Field(default_factory=OntapNfsServiceMetricV41)


class OntapNfsServiceProtocolV3Features(OntapModel):
    """OntapNfsServiceProtocolV3Features sub-model for v3_features."""

    connection_drop: bool = False
    ejukebox_enabled: bool = False
    fsid_change: bool = False
    hide_snapshot_enabled: bool = False
    mount_daemon_port: int = 0
    mount_root_only: bool = False
    network_lock_manager_port: int = 0
    network_status_monitor_port: int = 0
    rquota_daemon_port: int = 0


class OntapNfsServiceProtocolV40Features(OntapModel):
    """OntapNfsServiceProtocolV40Features sub-model for v40_features."""

    acl_enabled: bool = False
    acl_max_aces: int = 0
    acl_preserve: bool = False
    read_delegation_enabled: bool = False
    referrals_enabled: bool = False
    write_delegation_enabled: bool = False


class OntapNfsServiceProtocolV41Features(OntapModel):
    """OntapNfsServiceProtocolV41Features sub-model for v41_features."""

    acl_enabled: bool = False
    implementation_domain: str = ""
    implementation_name: str = ""
    pnfs_enabled: bool = False
    read_delegation_enabled: bool = False
    referrals_enabled: bool = False
    trunking_enabled: bool = False
    write_delegation_enabled: bool = False


class OntapNfsServiceProtocolV42Features(OntapModel):
    """OntapNfsServiceProtocolV42Features sub-model for v42_features."""

    seclabel_enabled: bool = False
    sparsefile_ops_enabled: bool = False
    xattrs_enabled: bool = False


class OntapNfsServiceProtocol(OntapModel):
    """OntapNfsServiceProtocol sub-model for protocol."""

    v3_64bit_identifiers_enabled: bool = False
    v3_enabled: bool = False
    v3_features: OntapNfsServiceProtocolV3Features = Field(
        default_factory=OntapNfsServiceProtocolV3Features
    )
    v40_enabled: bool = False
    v40_features: OntapNfsServiceProtocolV40Features = Field(
        default_factory=OntapNfsServiceProtocolV40Features
    )
    v41_enabled: bool = False
    v41_features: OntapNfsServiceProtocolV41Features = Field(
        default_factory=OntapNfsServiceProtocolV41Features
    )
    v42_features: OntapNfsServiceProtocolV42Features = Field(
        default_factory=OntapNfsServiceProtocolV42Features
    )
    v4_64bit_identifiers_enabled: bool = False
    v4_fsid_change: bool = False
    v4_grace_seconds: int = 0
    v4_id_domain: str = ""
    v4_lease_seconds: int = 0
    v4_session_slot_reply_cache_size: int = 0
    v4_session_slots: int = 0


class OntapNfsServiceProtocolAccessRules(OntapModel):
    """OntapNfsServiceProtocolAccessRules sub-model for protocol_access_rules."""

    cifs_access_type: str = ""
    nfs3_access_type: str = ""
    nfs4_access_type: str = ""


class OntapNfsServiceQtree(OntapModel):
    """OntapNfsServiceQtree sub-model for qtree."""

    export_enabled: bool = False
    validate_export: bool = False


class OntapNfsServiceRoot(OntapModel):
    """OntapNfsServiceRoot sub-model for root."""

    ignore_nt_acl: bool = False
    skip_write_permission_check: bool = False


class OntapNfsServiceSecurity(OntapModel):
    """OntapNfsServiceSecurity sub-model for security."""

    chown_mode: str = ""
    nt_acl_display_permission: bool = False
    ntfs_unix_security: str = ""
    permitted_encryption_types: list[str] = Field(default_factory=list)
    rpcsec_context_idle: int = 0


class OntapNfsServiceStatisticsV3IopsRaw(OntapModel):
    """OntapNfsServiceStatisticsV3IopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV3LatencyRaw(OntapModel):
    """OntapNfsServiceStatisticsV3LatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV3ThroughputRaw(OntapModel):
    """OntapNfsServiceStatisticsV3ThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV3(OntapModel):
    """OntapNfsServiceStatisticsV3 sub-model for v3."""

    iops_raw: OntapNfsServiceStatisticsV3IopsRaw = Field(
        default_factory=OntapNfsServiceStatisticsV3IopsRaw
    )
    latency_raw: OntapNfsServiceStatisticsV3LatencyRaw = Field(
        default_factory=OntapNfsServiceStatisticsV3LatencyRaw
    )
    status: str = ""
    throughput_raw: OntapNfsServiceStatisticsV3ThroughputRaw = Field(
        default_factory=OntapNfsServiceStatisticsV3ThroughputRaw
    )
    timestamp: str = ""


class OntapNfsServiceStatisticsV4IopsRaw(OntapModel):
    """OntapNfsServiceStatisticsV4IopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV4LatencyRaw(OntapModel):
    """OntapNfsServiceStatisticsV4LatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV4ThroughputRaw(OntapModel):
    """OntapNfsServiceStatisticsV4ThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV4(OntapModel):
    """OntapNfsServiceStatisticsV4 sub-model for v4."""

    iops_raw: OntapNfsServiceStatisticsV4IopsRaw = Field(
        default_factory=OntapNfsServiceStatisticsV4IopsRaw
    )
    latency_raw: OntapNfsServiceStatisticsV4LatencyRaw = Field(
        default_factory=OntapNfsServiceStatisticsV4LatencyRaw
    )
    status: str = ""
    throughput_raw: OntapNfsServiceStatisticsV4ThroughputRaw = Field(
        default_factory=OntapNfsServiceStatisticsV4ThroughputRaw
    )
    timestamp: str = ""


class OntapNfsServiceStatisticsV41IopsRaw(OntapModel):
    """OntapNfsServiceStatisticsV41IopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV41LatencyRaw(OntapModel):
    """OntapNfsServiceStatisticsV41LatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV41ThroughputRaw(OntapModel):
    """OntapNfsServiceStatisticsV41ThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNfsServiceStatisticsV41(OntapModel):
    """OntapNfsServiceStatisticsV41 sub-model for v41."""

    iops_raw: OntapNfsServiceStatisticsV41IopsRaw = Field(
        default_factory=OntapNfsServiceStatisticsV41IopsRaw
    )
    latency_raw: OntapNfsServiceStatisticsV41LatencyRaw = Field(
        default_factory=OntapNfsServiceStatisticsV41LatencyRaw
    )
    status: str = ""
    throughput_raw: OntapNfsServiceStatisticsV41ThroughputRaw = Field(
        default_factory=OntapNfsServiceStatisticsV41ThroughputRaw
    )
    timestamp: str = ""


class OntapNfsServiceStatistics(OntapModel):
    """OntapNfsServiceStatistics sub-model for statistics."""

    v3: OntapNfsServiceStatisticsV3 = Field(default_factory=OntapNfsServiceStatisticsV3)
    v4: OntapNfsServiceStatisticsV4 = Field(default_factory=OntapNfsServiceStatisticsV4)
    v41: OntapNfsServiceStatisticsV41 = Field(default_factory=OntapNfsServiceStatisticsV41)


class OntapNfsServiceSvm(OntapModel):
    """OntapNfsServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNfsServiceTransport(OntapModel):
    """OntapNfsServiceTransport sub-model for transport."""

    rdma_enabled: bool = False
    tcp_enabled: bool = False
    tcp_max_transfer_size: int = 0
    udp_enabled: bool = False


class OntapNfsServiceWindows(OntapModel):
    """OntapNfsServiceWindows sub-model for windows."""

    default_user: str = ""
    map_unknown_uid_to_default_user: bool = False
    v3_ms_dos_client_enabled: bool = False


class OntapNfsService(OntapModel):
    """OntapNfsService information."""

    access_cache_config: OntapNfsServiceAccessCacheConfig = Field(
        default_factory=OntapNfsServiceAccessCacheConfig
    )
    auth_sys_extended_groups_enabled: bool = False
    credential_cache: OntapNfsServiceCredentialCache = Field(
        default_factory=OntapNfsServiceCredentialCache
    )
    enabled: bool = False
    exports: OntapNfsServiceExports = Field(default_factory=OntapNfsServiceExports)
    extended_groups_limit: int = 0
    file_session_io_grouping_count: int = 0
    file_session_io_grouping_duration: int = 0
    metric: OntapNfsServiceMetric = Field(default_factory=OntapNfsServiceMetric)
    protocol: OntapNfsServiceProtocol = Field(default_factory=OntapNfsServiceProtocol)
    protocol_access_rules: OntapNfsServiceProtocolAccessRules = Field(
        default_factory=OntapNfsServiceProtocolAccessRules
    )
    qtree: OntapNfsServiceQtree = Field(default_factory=OntapNfsServiceQtree)
    root: OntapNfsServiceRoot = Field(default_factory=OntapNfsServiceRoot)
    rquota_enabled: bool = False
    security: OntapNfsServiceSecurity = Field(default_factory=OntapNfsServiceSecurity)
    showmount_enabled: bool = False
    state: str = ""
    statistics: OntapNfsServiceStatistics = Field(default_factory=OntapNfsServiceStatistics)
    svm: OntapNfsServiceSvm = Field(default_factory=OntapNfsServiceSvm)
    transport: OntapNfsServiceTransport = Field(default_factory=OntapNfsServiceTransport)
    vstorage_enabled: bool = False
    windows: OntapNfsServiceWindows = Field(default_factory=OntapNfsServiceWindows)
