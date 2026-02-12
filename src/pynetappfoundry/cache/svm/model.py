"""SVM information -- /svm/svms."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class SVMInfo(CacheModel):
    """Storage Virtual Machine information."""

    # Core (4)
    uuid: str = ""
    name: str = ""
    language: str = ""
    subtype: str = ""  # default, dp_destination, sync_source

    # References / Lists (4)
    aggregate_uuids: list[str] = Field(default_factory=list)
    ip_interface_uuids: list[str] = Field(default_factory=list)
    fc_interface_uuids: list[str] = Field(default_factory=list)
    snapshot_policy_uuid: str = ""

    # Name Services (2)
    nis_enabled: bool = False
    ldap_enabled: bool = False

    # Protocol Flags (13)
    nfs_enabled: bool = False
    nfs_allowed: bool = True
    cifs_enabled: bool = False
    cifs_allowed: bool = True
    iscsi_enabled: bool = False
    iscsi_allowed: bool = True
    fcp_enabled: bool = False
    fcp_allowed: bool = True
    nvme_enabled: bool = False
    nvme_allowed: bool = True
    ndmp_allowed: bool = True
    s3_allowed: bool = True
    s3_enabled: bool = False

    # SVM Settings (4)
    aggregates_delegated: bool = False
    max_volumes: str = ""
    auto_enable_analytics: bool = False
    auto_enable_activity_tracking: bool = False

    # Anti-Ransomware (6)
    anti_ransomware_auto_switch_from_learning_to_enabled: bool = True
    anti_ransomware_auto_switch_minimum_incoming_data_percent: int = 0
    anti_ransomware_auto_switch_duration_without_new_file_extension: int = 3
    anti_ransomware_auto_switch_minimum_learning_period: int = 10
    anti_ransomware_auto_switch_minimum_file_count: int = 200
    anti_ransomware_auto_switch_minimum_file_extension: int = 10

    # SnapMirror (2)
    snapmirror_is_protected: bool = False
    snapmirror_protected_volumes_count: int = 0

    # Storage (1)
    storage_limit: int = 0

    # Space Management (2)
    is_space_enforcement_logical: bool = False
    is_space_reporting_logical: bool = False

    # QoS References (3)
    qos_adaptive_policy_group_template_uuid: str = ""
    qos_policy_uuid: str = ""
    qos_policy_group_template_uuid: str = ""

    # NSSwitch (5)
    nsswitch_group: list[str] = Field(default_factory=list)
    nsswitch_hosts: list[str] = Field(default_factory=list)
    nsswitch_namemap: list[str] = Field(default_factory=list)
    nsswitch_netgroup: list[str] = Field(default_factory=list)
    nsswitch_passwd: list[str] = Field(default_factory=list)
