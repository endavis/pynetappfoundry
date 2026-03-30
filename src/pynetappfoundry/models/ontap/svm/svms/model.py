"""OntapSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmAggregate(OntapModel):
    """OntapSvmAggregate sub-model for aggregates."""

    aggregates_available_size: int = 0
    aggregates_name: str = ""
    aggregates_snaplock_type: str = ""
    aggregates_state: str = ""
    aggregates_type: str = ""
    aggregates_uuid: str = ""


class OntapSvmFcInterface(OntapModel):
    """OntapSvmFcInterface sub-model for fc_interfaces."""

    fc_interfaces_data_protocol: str = ""
    fc_interfaces_location_port_name: str = ""
    fc_interfaces_location_port_node_name: str = ""
    fc_interfaces_location_port_uuid: str = ""
    fc_interfaces_name: str = ""
    fc_interfaces_uuid: str = ""


class OntapSvmIpInterface(OntapModel):
    """OntapSvmIpInterface sub-model for ip_interfaces."""

    ip_interfaces_ip_address: str = ""
    ip_interfaces_ip_netmask: str = ""
    ip_interfaces_location_broadcast_domain_name: str = ""
    ip_interfaces_location_broadcast_domain_uuid: str = ""
    ip_interfaces_location_home_node_name: str = ""
    ip_interfaces_location_home_node_uuid: str = ""
    ip_interfaces_location_home_port_name: str = ""
    ip_interfaces_location_home_port_uuid: str = ""
    ip_interfaces_name: str = ""
    ip_interfaces_service_policy: str = ""
    ip_interfaces_services: list[str] = Field(default_factory=list)
    ip_interfaces_subnet_name: str = ""
    ip_interfaces_subnet_uuid: str = ""
    ip_interfaces_uuid: str = ""


class OntapSvmRoute(OntapModel):
    """OntapSvmRoute sub-model for routes."""

    routes_destination_address: str = ""
    routes_destination_family: str = ""
    routes_destination_netmask: str = ""
    routes_gateway: str = ""


class OntapSvm(OntapModel):
    """OntapSvm information."""

    aggregates: list[OntapSvmAggregate] = Field(default_factory=list)
    aggregates_delegated: bool = False
    anti_ransomware_event_log_is_enabled_on_new_file_extension_seen: bool = False
    anti_ransomware_event_log_is_enabled_on_snapshot_copy_creation: bool = False
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
    certificate_name: str = ""
    certificate_uuid: str = ""
    cifs_ad_domain_default_site: str = ""
    cifs_ad_domain_fqdn: str = ""
    cifs_ad_domain_organizational_unit: str = ""
    cifs_ad_domain_password: str = ""
    cifs_ad_domain_user: str = ""
    cifs_allowed: bool = False
    cifs_auth_style: str = ""
    cifs_domain_workgroup: str = ""
    cifs_enabled: bool = False
    cifs_name: str = ""
    cifs_workgroup: str = ""
    comment: str = ""
    dns_domains: list[str] = Field(default_factory=list)
    dns_servers: list[str] = Field(default_factory=list)
    fc_interfaces: list[OntapSvmFcInterface] = Field(default_factory=list)
    fcp_allowed: bool = False
    fcp_enabled: bool = False
    ip_interfaces: list[OntapSvmIpInterface] = Field(default_factory=list)
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    is_space_enforcement_logical: bool = False
    is_space_reporting_logical: bool = False
    iscsi_allowed: bool = False
    iscsi_enabled: bool = False
    language: str = ""
    ldap_ad_domain: str = ""
    ldap_base_dn: str = ""
    ldap_bind_dn: str = ""
    ldap_enabled: bool = False
    ldap_restrict_discovery_to_site: bool = False
    ldap_servers: list[str] = Field(default_factory=list)
    max_volumes: str = ""
    name: str = ""
    ndmp_allowed: bool = False
    nfs_allowed: bool = False
    nfs_enabled: bool = False
    nis_domain: str = ""
    nis_enabled: bool = False
    nis_servers: list[str] = Field(default_factory=list)
    nsswitch_group: list[str] = Field(default_factory=list)
    nsswitch_hosts: list[str] = Field(default_factory=list)
    nsswitch_namemap: list[str] = Field(default_factory=list)
    nsswitch_netgroup: list[str] = Field(default_factory=list)
    nsswitch_passwd: list[str] = Field(default_factory=list)
    number_of_volumes_in_recovery_queue: int = 0
    nvme_allowed: bool = False
    nvme_enabled: bool = False
    qos_adaptive_policy_group_template_max_throughput_iops: int = 0
    qos_adaptive_policy_group_template_max_throughput_mbps: int = 0
    qos_adaptive_policy_group_template_min_throughput_iops: int = 0
    qos_adaptive_policy_group_template_min_throughput_mbps: int = 0
    qos_adaptive_policy_group_template_name: str = ""
    qos_adaptive_policy_group_template_uuid: str = ""
    qos_policy_max_throughput_iops: int = 0
    qos_policy_max_throughput_mbps: int = 0
    qos_policy_min_throughput_iops: int = 0
    qos_policy_min_throughput_mbps: int = 0
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    qos_policy_group_template_max_throughput_iops: int = 0
    qos_policy_group_template_max_throughput_mbps: int = 0
    qos_policy_group_template_min_throughput_iops: int = 0
    qos_policy_group_template_min_throughput_mbps: int = 0
    qos_policy_group_template_name: str = ""
    qos_policy_group_template_uuid: str = ""
    routes: list[OntapSvmRoute] = Field(default_factory=list)
    s3_allowed: bool = False
    s3_certificate_name: str = ""
    s3_certificate_uuid: str = ""
    s3_default_unix_user: str = ""
    s3_default_win_user: str = ""
    s3_enabled: bool = False
    s3_is_http_enabled: bool = False
    s3_is_https_enabled: bool = False
    s3_name: str = ""
    s3_port: int = 0
    s3_secure_port: int = 0
    snapmirror_is_protected: bool = False
    snapmirror_protected_consistency_group_count: int = 0
    snapmirror_protected_volumes_count: int = 0
    snapshot_policy_name: str = ""
    snapshot_policy_uuid: str = ""
    state: str = ""
    storage_allocated: int = 0
    storage_available: int = 0
    storage_limit: int = 0
    storage_limit_threshold_alert: int = 0
    storage_limit_threshold_exceeded: bool = False
    storage_used_percentage: int = 0
    subtype: str = ""
    total_volume_size_in_recovery_queue: int = 0
    uuid: str = ""
