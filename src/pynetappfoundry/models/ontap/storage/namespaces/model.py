"""OntapNvmeNamespace information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeNamespaceObjectStore(OntapModel):
    """OntapNvmeNamespaceObjectStore sub-model for object_stores."""

    name: str = ""


class OntapNvmeNamespaceHost(OntapModel):
    """OntapNvmeNamespaceHost sub-model for hosts."""

    dh_hmac_chap_controller_secret_key: str = ""
    dh_hmac_chap_group_size: str = ""
    dh_hmac_chap_hash_function: str = ""
    dh_hmac_chap_host_secret_key: str = ""
    dh_hmac_chap_mode: str = ""
    nqn: str = ""
    priority: str = ""
    tls_configured_psk: str = ""
    tls_key_type: str = ""


class OntapNvmeNamespace(OntapModel):
    """OntapNvmeNamespace information."""

    auto_delete: bool = False
    clone_source_name: str = ""
    clone_source_uuid: str = ""
    comment: str = ""
    consistency_group_name: str = ""
    consistency_group_uuid: str = ""
    convert_lun_name: str = ""
    convert_lun_uuid: str = ""
    create_time: str = ""
    enabled: bool = False
    location_namespace: str = ""
    location_node_name: str = ""
    location_node_uuid: str = ""
    location_qtree_id: int = 0
    location_qtree_name: str = ""
    location_volume_name: str = ""
    location_volume_uuid: str = ""
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
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
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
    provisioning_options_tiering_object_stores: list[OntapNvmeNamespaceObjectStore] = Field(
        default_factory=list
    )
    provisioning_options_tiering_policy: str = ""
    provisioning_options_use_mirrored_aggregates: bool = False
    space_block_size: int = 0
    space_efficiency_ratio: float = 0.0
    space_guarantee_requested: bool = False
    space_guarantee_reserved: bool = False
    space_physical_used: int = 0
    space_physical_used_by_snapshots: int = 0
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
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    status_container_state: str = ""
    status_mapped: bool = False
    status_read_only: bool = False
    status_state: str = ""
    subsystem_map_anagrpid: str = ""
    subsystem_map_nsid: str = ""
    subsystem_map_subsystem_comment: str = ""
    subsystem_map_subsystem_hosts: list[OntapNvmeNamespaceHost] = Field(default_factory=list)
    subsystem_map_subsystem_name: str = ""
    subsystem_map_subsystem_os_type: str = ""
    subsystem_map_subsystem_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
