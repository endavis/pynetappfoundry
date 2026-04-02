"""OntapCifsService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsServiceAdDomain(OntapModel):
    """OntapCifsServiceAdDomain sub-model for ad_domain."""

    default_site: str = ""
    fqdn: str = ""
    organizational_unit: str = ""
    password: str = ""
    user: str = ""


class OntapCifsServiceMetricIops(OntapModel):
    """OntapCifsServiceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapCifsServiceMetricLatency(OntapModel):
    """OntapCifsServiceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapCifsServiceMetricThroughput(OntapModel):
    """OntapCifsServiceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapCifsServiceMetric(OntapModel):
    """OntapCifsServiceMetric sub-model for metric."""

    duration: str = ""
    iops: OntapCifsServiceMetricIops = Field(default_factory=OntapCifsServiceMetricIops)
    latency: OntapCifsServiceMetricLatency = Field(default_factory=OntapCifsServiceMetricLatency)
    status: str = ""
    throughput: OntapCifsServiceMetricThroughput = Field(
        default_factory=OntapCifsServiceMetricThroughput
    )
    timestamp: str = ""


class OntapCifsServiceNetbios(OntapModel):
    """OntapCifsServiceNetbios sub-model for netbios."""

    aliases: list[str] = Field(default_factory=list)
    enabled: bool = False
    wins_servers: list[str] = Field(default_factory=list)


class OntapCifsServiceOptions(OntapModel):
    """OntapCifsServiceOptions sub-model for options."""

    admin_to_root_mapping: bool = False
    advanced_sparse_file: bool = False
    backup_symlink_enabled: bool = False
    client_dup_detection_enabled: bool = False
    client_version_reporting_enabled: bool = False
    copy_offload: bool = False
    dac_enabled: bool = False
    export_policy_enabled: bool = False
    fake_open: bool = False
    fsctl_trim: bool = False
    junction_reparse: bool = False
    large_mtu: bool = False
    max_connections_per_session: int = 0
    max_lifs_per_session: int = 0
    max_opens_same_file_per_tree: int = 0
    max_same_tree_connect_per_session: int = 0
    max_same_user_sessions_per_connection: int = 0
    max_watches_set_per_tree: int = 0
    multichannel: bool = False
    null_user_windows_name: str = ""
    path_component_cache: bool = False
    referral: bool = False
    shadowcopy: bool = False
    shadowcopy_dir_depth: int = 0
    smb_credits: int = 0
    trusted_domain_enum_search_enabled: bool = False
    widelink_reparse_versions: list[str] = Field(default_factory=list)


class OntapCifsServiceSecurity(OntapModel):
    """OntapCifsServiceSecurity sub-model for security."""

    advertised_kdc_encryptions: list[str] = Field(default_factory=list)
    aes_netlogon_enabled: bool = False
    encrypt_dc_connection: bool = False
    kdc_encryption: bool = False
    ldap_referral_enabled: bool = False
    lm_compatibility_level: str = ""
    restrict_anonymous: str = ""
    session_security: str = ""
    smb_encryption: bool = False
    smb_signing: bool = False
    try_ldap_channel_binding: bool = False
    use_ldaps: bool = False
    use_start_tls: bool = False


class OntapCifsServiceStatisticsIopsRaw(OntapModel):
    """OntapCifsServiceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapCifsServiceStatisticsLatencyRaw(OntapModel):
    """OntapCifsServiceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapCifsServiceStatisticsThroughputRaw(OntapModel):
    """OntapCifsServiceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapCifsServiceStatistics(OntapModel):
    """OntapCifsServiceStatistics sub-model for statistics."""

    iops_raw: OntapCifsServiceStatisticsIopsRaw = Field(
        default_factory=OntapCifsServiceStatisticsIopsRaw
    )
    latency_raw: OntapCifsServiceStatisticsLatencyRaw = Field(
        default_factory=OntapCifsServiceStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapCifsServiceStatisticsThroughputRaw = Field(
        default_factory=OntapCifsServiceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapCifsServiceSvm(OntapModel):
    """OntapCifsServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsService(OntapModel):
    """OntapCifsService information."""

    ad_domain: OntapCifsServiceAdDomain = Field(default_factory=OntapCifsServiceAdDomain)
    auth_style: str = ""
    auth_user_type: str = ""
    authentication_method: str = ""
    client_certificate: str = ""
    client_id: str = ""
    client_secret: str = ""
    comment: str = ""
    default_unix_user: str = ""
    enabled: bool = False
    group_policy_object_enabled: bool = False
    key_vault_uri: str = ""
    metric: OntapCifsServiceMetric = Field(default_factory=OntapCifsServiceMetric)
    name: str = ""
    netbios: OntapCifsServiceNetbios = Field(default_factory=OntapCifsServiceNetbios)
    oauth_host: str = ""
    options: OntapCifsServiceOptions = Field(default_factory=OntapCifsServiceOptions)
    proxy_host: str = ""
    proxy_password: str = ""
    proxy_port: int = 0
    proxy_type: str = ""
    proxy_username: str = ""
    security: OntapCifsServiceSecurity = Field(default_factory=OntapCifsServiceSecurity)
    statistics: OntapCifsServiceStatistics = Field(default_factory=OntapCifsServiceStatistics)
    svm: OntapCifsServiceSvm = Field(default_factory=OntapCifsServiceSvm)
    tenant_id: str = ""
    timeout: int = 0
    verify_host: bool = False
    workgroup: str = ""
