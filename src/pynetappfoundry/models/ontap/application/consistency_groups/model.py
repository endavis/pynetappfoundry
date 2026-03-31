# ruff: noqa: E501
"""OntapConsistencyGroupResponse information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupResponseConsistencyGroup(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroup sub-model for consistency_groups."""

    application_component_type: str = ""
    application_type: str = ""
    luns: list[dict[str, Any]] = Field(default_factory=list)
    name: str = ""
    namespaces: list[dict[str, Any]] = Field(default_factory=list)
    parent_consistency_group_name: str = ""
    parent_consistency_group_uuid: str = ""
    provisioning_options_action: str = ""
    provisioning_options_name: str = ""
    provisioning_options_storage_service_name: str = ""
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    restore_to_snapshot_name: str = ""
    restore_to_snapshot_uuid: str = ""
    snapshot_policy_name: str = ""
    snapshot_policy_uuid: str = ""
    space_available: int = 0
    space_size: int = 0
    space_used: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    tiering_control: str = ""
    tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    tiering_policy: str = ""
    uuid: str = ""
    volumes: list[dict[str, Any]] = Field(default_factory=list)


class OntapConsistencyGroupResponseLun(OntapModel):
    """OntapConsistencyGroupResponseLun sub-model for luns."""

    clone_source_name: str = ""
    clone_source_uuid: str = ""
    comment: str = ""
    create_time: str = ""
    enabled: bool = False
    lun_maps: list[dict[str, Any]] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    provisioning_options_action: str = ""
    provisioning_options_count: int = 0
    qos_policy_max_throughput_iops: int = 0
    qos_policy_max_throughput_mbps: int = 0
    qos_policy_min_throughput_iops: int = 0
    qos_policy_min_throughput_mbps: int = 0
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    serial_number: str = ""
    space_guarantee_requested: bool = False
    space_guarantee_reserved: bool = False
    space_size: int = 0
    space_used: int = 0
    uuid: str = ""


class OntapConsistencyGroupResponseNamespace(OntapModel):
    """OntapConsistencyGroupResponseNamespace sub-model for namespaces."""

    auto_delete: bool = False
    comment: str = ""
    create_time: str = ""
    enabled: bool = False
    name: str = ""
    os_type: str = ""
    provisioning_options_action: str = ""
    provisioning_options_count: int = 0
    space_block_size: int = 0
    space_guarantee_requested: bool = False
    space_guarantee_reserved: bool = False
    space_size: int = 0
    space_used: int = 0
    status_container_state: str = ""
    status_mapped: bool = False
    status_read_only: bool = False
    status_state: str = ""
    subsystem_map_anagrpid: str = ""
    subsystem_map_nsid: str = ""
    subsystem_map_subsystem_comment: str = ""
    subsystem_map_subsystem_hosts: list[dict[str, Any]] = Field(default_factory=list)
    subsystem_map_subsystem_name: str = ""
    subsystem_map_subsystem_os_type: str = ""
    subsystem_map_subsystem_uuid: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseReplicationRelationship(OntapModel):
    """OntapConsistencyGroupResponseReplicationRelationship sub-model for replication_relationships."""

    is_protected_by_svm_dr: bool = False
    is_source: bool = False
    uuid: str = ""


class OntapConsistencyGroupResponseObjectStore(OntapModel):
    """OntapConsistencyGroupResponseObjectStore sub-model for object_stores."""

    name: str = ""


class OntapConsistencyGroupResponseVolume(OntapModel):
    """OntapConsistencyGroupResponseVolume sub-model for volumes."""

    comment: str = ""
    name: str = ""
    nas_cifs_shares: list[dict[str, Any]] = Field(default_factory=list)
    nas_export_policy_id: int = 0
    nas_export_policy_name: str = ""
    nas_export_policy_rules: list[dict[str, Any]] = Field(default_factory=list)
    nas_gid: int = 0
    nas_junction_parent_name: str = ""
    nas_junction_parent_uuid: str = ""
    nas_path: str = ""
    nas_security_style: str = ""
    nas_uid: int = 0
    nas_unix_permissions: int = 0
    provisioning_options_action: str = ""
    provisioning_options_count: int = 0
    provisioning_options_storage_service_name: str = ""
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    space_available: int = 0
    space_size: int = 0
    space_used: int = 0
    tiering_control: str = ""
    tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    tiering_policy: str = ""
    uuid: str = ""


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
