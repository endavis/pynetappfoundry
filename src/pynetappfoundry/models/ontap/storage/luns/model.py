"""OntapLun information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLunAttribute(OntapModel):
    """OntapLunAttribute sub-model for attributes."""

    attributes_name: str = ""
    attributes_value: str = ""


class OntapLunDestination(OntapModel):
    """OntapLunDestination sub-model for destinations."""

    copy_destinations_max_throughput: int = 0
    copy_destinations_name: str = ""
    copy_destinations_peer_name: str = ""
    copy_destinations_peer_uuid: str = ""
    copy_destinations_progress_elapsed: int = 0
    copy_destinations_progress_failure_arguments: list[dict[str, Any]] = Field(default_factory=list)
    copy_destinations_progress_failure_code: str = ""
    copy_destinations_progress_failure_message: str = ""
    copy_destinations_progress_percent_complete: int = 0
    copy_destinations_progress_state: str = ""
    copy_destinations_progress_volume_snapshot_blocked: bool = False
    copy_destinations_uuid: str = ""


class OntapLunArgument(OntapModel):
    """OntapLunArgument sub-model for arguments."""

    copy_source_progress_failure_arguments_code: str = ""
    copy_source_progress_failure_arguments_message: str = ""


class OntapLunLunMap(OntapModel):
    """OntapLunLunMap sub-model for lun_maps."""

    lun_maps_igroup_comment: str = ""
    lun_maps_igroup_igroups: list[dict[str, Any]] = Field(default_factory=list)
    lun_maps_igroup_initiators: list[dict[str, Any]] = Field(default_factory=list)
    lun_maps_igroup_name: str = ""
    lun_maps_igroup_os_type: str = ""
    lun_maps_igroup_protocol: str = ""
    lun_maps_igroup_uuid: str = ""
    lun_maps_logical_unit_number: int = 0


class OntapLunArgument2(OntapModel):
    """OntapLunArgument2 sub-model for arguments."""

    movement_progress_failure_arguments_code: str = ""
    movement_progress_failure_arguments_message: str = ""


class OntapLunObjectStore(OntapModel):
    """OntapLunObjectStore sub-model for object_stores."""

    provisioning_options_tiering_object_stores_name: str = ""


class OntapLunBinding(OntapModel):
    """OntapLunBinding sub-model for bindings."""

    vvol_bindings_id: int = 0
    vvol_bindings_partner_name: str = ""
    vvol_bindings_partner_uuid: str = ""
    vvol_bindings_secondary_id: str = ""


class OntapLun(OntapModel):
    """OntapLun information."""

    attributes: list[OntapLunAttribute] = Field(default_factory=list)
    auto_delete: bool = False
    class_: str = ""
    clone_source_name: str = ""
    clone_source_uuid: str = ""
    comment: str = ""
    consistency_group_name: str = ""
    consistency_group_uuid: str = ""
    convert_namespace_name: str = ""
    convert_namespace_uuid: str = ""
    copy_destinations: list[OntapLunDestination] = Field(default_factory=list)
    copy_source_max_throughput: int = 0
    copy_source_name: str = ""
    copy_source_peer_name: str = ""
    copy_source_peer_uuid: str = ""
    copy_source_progress_elapsed: int = 0
    copy_source_progress_failure_arguments: list[OntapLunArgument] = Field(default_factory=list)
    copy_source_progress_failure_code: str = ""
    copy_source_progress_failure_message: str = ""
    copy_source_progress_percent_complete: int = 0
    copy_source_progress_state: str = ""
    copy_source_progress_volume_snapshot_blocked: bool = False
    copy_source_uuid: str = ""
    create_time: str = ""
    enabled: bool = False
    location_logical_unit: str = ""
    location_node_name: str = ""
    location_node_uuid: str = ""
    location_qtree_id: int = 0
    location_qtree_name: str = ""
    location_volume_name: str = ""
    location_volume_uuid: str = ""
    lun_maps: list[OntapLunLunMap] = Field(default_factory=list)
    metric_duration: str = ""
    metric_iops_other: int = 0
    metric_iops_read: int = 0
    metric_iops_total: int = 0
    metric_iops_write: int = 0
    metric_latency_other: int = 0
    metric_latency_read: int = 0
    metric_latency_total: int = 0
    metric_latency_write: int = 0
    metric_status: str = ""
    metric_throughput_other: int = 0
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    movement_max_throughput: int = 0
    movement_paths_destination: str = ""
    movement_paths_source: str = ""
    movement_progress_elapsed: int = 0
    movement_progress_failure_arguments: list[OntapLunArgument2] = Field(default_factory=list)
    movement_progress_failure_code: str = ""
    movement_progress_failure_message: str = ""
    movement_progress_percent_complete: int = 0
    movement_progress_state: str = ""
    movement_progress_volume_snapshot_blocked: bool = False
    name: str = ""
    os_type: str = ""
    provisioning_options_auto: bool = False
    provisioning_options_count: int = 0
    provisioning_options_qos_policy_name: str = ""
    provisioning_options_qos_policy_uuid: str = ""
    provisioning_options_snapshot_policy_name: str = ""
    provisioning_options_snapshot_policy_uuid: str = ""
    provisioning_options_storage_service_name: str = ""
    provisioning_options_tiering_control: str = ""
    provisioning_options_tiering_object_stores: list[OntapLunObjectStore] = Field(
        default_factory=list
    )
    provisioning_options_tiering_policy: str = ""
    provisioning_options_use_mirrored_aggregates: bool = False
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    serial_number: str = ""
    space_efficiency_ratio: float = 0.0
    space_guarantee_requested: bool = False
    space_guarantee_reserved: bool = False
    space_physical_used: int = 0
    space_physical_used_by_snapshots: int = 0
    space_scsi_thin_provisioning_support_enabled: bool = False
    space_size: int = 0
    space_used: int = 0
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_other: int = 0
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    status_container_state: str = ""
    status_mapped: bool = False
    status_read_only: bool = False
    status_state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    vvol_bindings: list[OntapLunBinding] = Field(default_factory=list)
    vvol_is_bound: bool = False
