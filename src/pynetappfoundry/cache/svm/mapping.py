"""SVM type mapping definition for the declarative field mapping framework.

Defines SVM_MAPPING which maps ONTAP REST API SVM data
to SVMInfo cache model attributes. SVM is API-only -- there is no CLI
command for this data.

All fields use simple dot-path extraction; no transform functions are
needed.

Note: ``snapmirror.*`` is an expensive property and must be explicitly
requested via ``?fields=*,snapmirror``.
``anti_ransomware_auto_switch_minimum_incoming_data_percent`` exists
as a filter param (integer, 9.13+) but is not in the OpenAPI
definition body; it will default to 0 on older ONTAP versions.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.svm.model import SVMInfo

SVM_MAPPING = TypeMapping(
    name="SVM",
    model_class=SVMInfo,
    api_endpoint="/svm/svms?fields=*,snapmirror",
    cli_command="",
    fields=(
        # Core (4)
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="language",
            api_path="language",
        ),
        FieldMapping(
            cache_attr="subtype",
            api_path="subtype",
        ),
        # References / Lists (4)
        FieldMapping(
            cache_attr="aggregate_uuids",
            api_path="aggregates[*].uuid",
            default=[],
        ),
        FieldMapping(
            cache_attr="ip_interface_uuids",
            api_path="ip_interfaces[*].uuid",
            default=[],
        ),
        FieldMapping(
            cache_attr="fc_interface_uuids",
            api_path="fc_interfaces[*].uuid",
            default=[],
        ),
        FieldMapping(
            cache_attr="snapshot_policy_uuid",
            api_path="snapshot_policy.uuid",
        ),
        # Name Services (2)
        FieldMapping(
            cache_attr="nis_enabled",
            api_path="nis.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ldap_enabled",
            api_path="ldap.enabled",
            default=False,
        ),
        # Protocol Flags (13)
        FieldMapping(
            cache_attr="nfs_enabled",
            api_path="nfs.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="nfs_allowed",
            api_path="nfs.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="cifs_enabled",
            api_path="cifs.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="cifs_allowed",
            api_path="cifs.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="iscsi_enabled",
            api_path="iscsi.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="iscsi_allowed",
            api_path="iscsi.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="fcp_enabled",
            api_path="fcp.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="fcp_allowed",
            api_path="fcp.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="nvme_enabled",
            api_path="nvme.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="nvme_allowed",
            api_path="nvme.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="ndmp_allowed",
            api_path="ndmp.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="s3_allowed",
            api_path="s3.allowed",
            default=True,
        ),
        FieldMapping(
            cache_attr="s3_enabled",
            api_path="s3.enabled",
            default=False,
        ),
        # SVM Settings (4)
        FieldMapping(
            cache_attr="aggregates_delegated",
            api_path="aggregates_delegated",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_volumes",
            api_path="max_volumes",
        ),
        FieldMapping(
            cache_attr="auto_enable_analytics",
            api_path="auto_enable_analytics",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_enable_activity_tracking",
            api_path="auto_enable_activity_tracking",
            default=False,
        ),
        # Anti-Ransomware (6)
        FieldMapping(
            cache_attr="anti_ransomware_auto_switch_from_learning_to_enabled",
            api_path="anti_ransomware_auto_switch_from_learning_to_enabled",
            default=True,
        ),
        FieldMapping(
            cache_attr="anti_ransomware_auto_switch_minimum_incoming_data_percent",
            api_path="anti_ransomware_auto_switch_minimum_incoming_data_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="anti_ransomware_auto_switch_duration_without_new_file_extension",
            api_path="anti_ransomware_auto_switch_duration_without_new_file_extension",
            default=3,
        ),
        FieldMapping(
            cache_attr="anti_ransomware_auto_switch_minimum_learning_period",
            api_path="anti_ransomware_auto_switch_minimum_learning_period",
            default=10,
        ),
        FieldMapping(
            cache_attr="anti_ransomware_auto_switch_minimum_file_count",
            api_path="anti_ransomware_auto_switch_minimum_file_count",
            default=200,
        ),
        FieldMapping(
            cache_attr="anti_ransomware_auto_switch_minimum_file_extension",
            api_path="anti_ransomware_auto_switch_minimum_file_extension",
            default=10,
        ),
        # SnapMirror (2)
        FieldMapping(
            cache_attr="snapmirror_is_protected",
            api_path="snapmirror.is_protected",
            default=False,
        ),
        FieldMapping(
            cache_attr="snapmirror_protected_volumes_count",
            api_path="snapmirror.protected_volumes_count",
            default=0,
        ),
        # Storage (1)
        FieldMapping(
            cache_attr="storage_limit",
            api_path="storage.limit",
            default=0,
        ),
        # Space Management (2)
        FieldMapping(
            cache_attr="is_space_enforcement_logical",
            api_path="is_space_enforcement_logical",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_space_reporting_logical",
            api_path="is_space_reporting_logical",
            default=False,
        ),
        # QoS References (3)
        FieldMapping(
            cache_attr="qos_adaptive_policy_group_template_uuid",
            api_path="qos_adaptive_policy_group_template.uuid",
        ),
        FieldMapping(
            cache_attr="qos_policy_uuid",
            api_path="qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="qos_policy_group_template_uuid",
            api_path="qos_policy_group_template.uuid",
        ),
        # NSSwitch (5)
        FieldMapping(
            cache_attr="nsswitch_group",
            api_path="nsswitch.group",
            default=[],
        ),
        FieldMapping(
            cache_attr="nsswitch_hosts",
            api_path="nsswitch.hosts",
            default=[],
        ),
        FieldMapping(
            cache_attr="nsswitch_namemap",
            api_path="nsswitch.namemap",
            default=[],
        ),
        FieldMapping(
            cache_attr="nsswitch_netgroup",
            api_path="nsswitch.netgroup",
            default=[],
        ),
        FieldMapping(
            cache_attr="nsswitch_passwd",
            api_path="nsswitch.passwd",
            default=[],
        ),
    ),
)

model_registry.register_mapping("SVM", SVM_MAPPING)
