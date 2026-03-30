# ruff: noqa: E501
"""OntapConsistencyGroupResponse information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupResponseConsistencyGroup(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroup sub-model for consistency_groups."""

    consistency_groups_application_component_type: str = ""
    consistency_groups_application_type: str = ""
    consistency_groups_luns: list[dict[str, Any]] = Field(default_factory=list)
    consistency_groups_name: str = ""
    consistency_groups_namespaces: list[dict[str, Any]] = Field(default_factory=list)
    consistency_groups_parent_consistency_group_name: str = ""
    consistency_groups_parent_consistency_group_uuid: str = ""
    consistency_groups_provisioning_options_action: str = ""
    consistency_groups_provisioning_options_name: str = ""
    consistency_groups_provisioning_options_storage_service_name: str = ""
    consistency_groups_qos_policy_name: str = ""
    consistency_groups_qos_policy_uuid: str = ""
    consistency_groups_restore_to_snapshot_name: str = ""
    consistency_groups_restore_to_snapshot_uuid: str = ""
    consistency_groups_snapshot_policy_name: str = ""
    consistency_groups_snapshot_policy_uuid: str = ""
    consistency_groups_space_available: int = 0
    consistency_groups_space_size: int = 0
    consistency_groups_space_used: int = 0
    consistency_groups_svm_name: str = ""
    consistency_groups_svm_uuid: str = ""
    consistency_groups_tiering_control: str = ""
    consistency_groups_tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    consistency_groups_tiering_policy: str = ""
    consistency_groups_uuid: str = ""
    consistency_groups_volumes: list[dict[str, Any]] = Field(default_factory=list)


class OntapConsistencyGroupResponseLun(OntapModel):
    """OntapConsistencyGroupResponseLun sub-model for luns."""

    luns_clone_source_name: str = ""
    luns_clone_source_uuid: str = ""
    luns_comment: str = ""
    luns_create_time: str = ""
    luns_enabled: bool = False
    luns_lun_maps: list[dict[str, Any]] = Field(default_factory=list)
    luns_name: str = ""
    luns_os_type: str = ""
    luns_provisioning_options_action: str = ""
    luns_provisioning_options_count: int = 0
    luns_qos_policy_max_throughput_iops: int = 0
    luns_qos_policy_max_throughput_mbps: int = 0
    luns_qos_policy_min_throughput_iops: int = 0
    luns_qos_policy_min_throughput_mbps: int = 0
    luns_qos_policy_name: str = ""
    luns_qos_policy_uuid: str = ""
    luns_serial_number: str = ""
    luns_space_guarantee_requested: bool = False
    luns_space_guarantee_reserved: bool = False
    luns_space_size: int = 0
    luns_space_used: int = 0
    luns_uuid: str = ""


class OntapConsistencyGroupResponseNamespace(OntapModel):
    """OntapConsistencyGroupResponseNamespace sub-model for namespaces."""

    namespaces_auto_delete: bool = False
    namespaces_comment: str = ""
    namespaces_create_time: str = ""
    namespaces_enabled: bool = False
    namespaces_name: str = ""
    namespaces_os_type: str = ""
    namespaces_provisioning_options_action: str = ""
    namespaces_provisioning_options_count: int = 0
    namespaces_space_block_size: int = 0
    namespaces_space_guarantee_requested: bool = False
    namespaces_space_guarantee_reserved: bool = False
    namespaces_space_size: int = 0
    namespaces_space_used: int = 0
    namespaces_status_container_state: str = ""
    namespaces_status_mapped: bool = False
    namespaces_status_read_only: bool = False
    namespaces_status_state: str = ""
    namespaces_subsystem_map_anagrpid: str = ""
    namespaces_subsystem_map_nsid: str = ""
    namespaces_subsystem_map_subsystem_comment: str = ""
    namespaces_subsystem_map_subsystem_hosts: list[dict[str, Any]] = Field(default_factory=list)
    namespaces_subsystem_map_subsystem_name: str = ""
    namespaces_subsystem_map_subsystem_os_type: str = ""
    namespaces_subsystem_map_subsystem_uuid: str = ""
    namespaces_uuid: str = ""


class OntapConsistencyGroupResponseReplicationRelationship(OntapModel):
    """OntapConsistencyGroupResponseReplicationRelationship sub-model for replication_relationships."""

    replication_relationships_is_protected_by_svm_dr: bool = False
    replication_relationships_is_source: bool = False
    replication_relationships_uuid: str = ""


class OntapConsistencyGroupResponseObjectStore(OntapModel):
    """OntapConsistencyGroupResponseObjectStore sub-model for object_stores."""

    tiering_object_stores_name: str = ""


class OntapConsistencyGroupResponseVolume(OntapModel):
    """OntapConsistencyGroupResponseVolume sub-model for volumes."""

    volumes_comment: str = ""
    volumes_name: str = ""
    volumes_nas_cifs_shares: list[dict[str, Any]] = Field(default_factory=list)
    volumes_nas_export_policy_id: int = 0
    volumes_nas_export_policy_name: str = ""
    volumes_nas_export_policy_rules: list[dict[str, Any]] = Field(default_factory=list)
    volumes_nas_gid: int = 0
    volumes_nas_junction_parent_name: str = ""
    volumes_nas_junction_parent_uuid: str = ""
    volumes_nas_path: str = ""
    volumes_nas_security_style: str = ""
    volumes_nas_uid: int = 0
    volumes_nas_unix_permissions: int = 0
    volumes_provisioning_options_action: str = ""
    volumes_provisioning_options_count: int = 0
    volumes_provisioning_options_storage_service_name: str = ""
    volumes_qos_policy_name: str = ""
    volumes_qos_policy_uuid: str = ""
    volumes_space_available: int = 0
    volumes_space_size: int = 0
    volumes_space_used: int = 0
    volumes_tiering_control: str = ""
    volumes_tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    volumes_tiering_policy: str = ""
    volumes_uuid: str = ""


class OntapConsistencyGroupResponse(OntapModel):
    """OntapConsistencyGroupResponse information."""

    application_component_type: str = ""
    application_type: str = ""
    clone_guarantee_type: str = ""
    clone_is_flexclone: bool = False
    clone_parent_consistency_group_name: str = ""
    clone_parent_consistency_group_uuid: str = ""
    clone_parent_snapshot_name: str = ""
    clone_parent_snapshot_uuid: str = ""
    clone_parent_svm_name: str = ""
    clone_parent_svm_uuid: str = ""
    clone_split_complete_percent: int = 0
    clone_split_estimate: int = 0
    clone_split_initiated: bool = False
    clone_volume_prefix: str = ""
    clone_volume_suffix: str = ""
    consistency_groups: list[OntapConsistencyGroupResponseConsistencyGroup] = Field(
        default_factory=list
    )
    luns: list[OntapConsistencyGroupResponseLun] = Field(default_factory=list)
    metric_available_space: int = 0
    metric_duration: str = ""
    metric_iops_other: int = 0
    metric_iops_read: int = 0
    metric_iops_total: int = 0
    metric_iops_write: int = 0
    metric_latency_other: int = 0
    metric_latency_read: int = 0
    metric_latency_total: int = 0
    metric_latency_write: int = 0
    metric_size: int = 0
    metric_status: str = ""
    metric_throughput_other: int = 0
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    metric_used_space: int = 0
    name: str = ""
    namespaces: list[OntapConsistencyGroupResponseNamespace] = Field(default_factory=list)
    parent_consistency_group_name: str = ""
    parent_consistency_group_uuid: str = ""
    provisioning_options_action: str = ""
    provisioning_options_name: str = ""
    provisioning_options_storage_service_name: str = ""
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    replicated: bool = False
    replication_relationships: list[OntapConsistencyGroupResponseReplicationRelationship] = Field(
        default_factory=list
    )
    replication_source: bool = False
    restore_to_snapshot_name: str = ""
    restore_to_snapshot_uuid: str = ""
    snapshot_policy_name: str = ""
    snapshot_policy_uuid: str = ""
    space_available: int = 0
    space_size: int = 0
    space_used: int = 0
    statistics_available_space: int = 0
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_size: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_other: int = 0
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    statistics_used_space: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    tiering_control: str = ""
    tiering_object_stores: list[OntapConsistencyGroupResponseObjectStore] = Field(
        default_factory=list
    )
    tiering_policy: str = ""
    uuid: str = ""
    volumes: list[OntapConsistencyGroupResponseVolume] = Field(default_factory=list)
