"""OntapSvmMigration information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSvmMigrationAggregate(OntapModel):
    """OntapSvmMigrationAggregate sub-model for aggregates."""

    destination_volume_placement_aggregates_name: str = ""
    destination_volume_placement_aggregates_uuid: str = ""


class OntapSvmMigrationVolumeAggregatePair(OntapModel):
    """OntapSvmMigrationVolumeAggregatePair sub-model for volume_aggregate_pairs."""

    destination_volume_placement_volume_aggregate_pairs_aggregate_name: str = ""
    destination_volume_placement_volume_aggregate_pairs_aggregate_uuid: str = ""
    destination_volume_placement_volume_aggregate_pairs_volume_name: str = ""
    destination_volume_placement_volume_aggregate_pairs_volume_uuid: str = ""


class OntapSvmMigrationIpInterface(OntapModel):
    """OntapSvmMigrationIpInterface sub-model for ip_interfaces."""

    ip_interface_placement_ip_interfaces_interface_ip_address: str = ""
    ip_interface_placement_ip_interfaces_interface_name: str = ""
    ip_interface_placement_ip_interfaces_interface_uuid: str = ""
    ip_interface_placement_ip_interfaces_port_name: str = ""
    ip_interface_placement_ip_interfaces_port_node_name: str = ""
    ip_interface_placement_ip_interfaces_port_uuid: str = ""


class OntapSvmMigrationMessage(OntapModel):
    """OntapSvmMigrationMessage sub-model for messages."""

    messages_code: str = ""
    messages_message: str = ""


class OntapSvmMigration(OntapModel):
    """OntapSvmMigration information."""

    auto_cutover: bool = False
    auto_source_cleanup: bool = False
    check_only: bool = False
    current_operation: str = ""
    destination_ipspace_name: str = ""
    destination_ipspace_uuid: str = ""
    destination_volume_placement_aggregates: list[OntapSvmMigrationAggregate] = Field(
        default_factory=list
    )
    destination_volume_placement_volume_aggregate_pairs: list[
        OntapSvmMigrationVolumeAggregatePair
    ] = Field(default_factory=list)
    ip_interface_placement_ip_interfaces: list[OntapSvmMigrationIpInterface] = Field(
        default_factory=list
    )
    last_failed_state: str = ""
    last_operation: str = ""
    messages: list[OntapSvmMigrationMessage] = Field(default_factory=list)
    point_of_no_return: bool = False
    restart_count: int = 0
    source_cluster_name: str = ""
    source_cluster_uuid: OntapUUID = ""
    source_svm_name: str = ""
    source_svm_uuid: str = ""
    throttle: int = 0
    time_metrics_cutover_complete_time: str = ""
    time_metrics_cutover_start_time: str = ""
    time_metrics_cutover_trigger_time: str = ""
    time_metrics_end_time: str = ""
    time_metrics_last_pause_time: str = ""
    time_metrics_last_resume_time: str = ""
    time_metrics_start_time: str = ""
    uuid: OntapUUID = ""
