"""OntapSvmMigration information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSvmMigrationDestinationIpspace(OntapModel):
    """OntapSvmMigrationDestinationIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapSvmMigrationDestinationVolumePlacementAggregate(OntapModel):
    """OntapSvmMigrationDestinationVolumePlacementAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapSvmMigrationDestinationVolumePlacement(OntapModel):
    """OntapSvmMigrationDestinationVolumePlacement sub-model for volume_placement."""

    aggregates: list[OntapSvmMigrationDestinationVolumePlacementAggregate] = Field(
        default_factory=list
    )
    volume_aggregate_pairs: list[dict[str, Any]] = Field(default_factory=list)


class OntapSvmMigrationDestination(OntapModel):
    """OntapSvmMigrationDestination sub-model for destination."""

    ipspace: OntapSvmMigrationDestinationIpspace = Field(
        default_factory=OntapSvmMigrationDestinationIpspace
    )
    volume_placement: OntapSvmMigrationDestinationVolumePlacement = Field(
        default_factory=OntapSvmMigrationDestinationVolumePlacement
    )


class OntapSvmMigrationIpInterfacePlacement(OntapModel):
    """OntapSvmMigrationIpInterfacePlacement sub-model for ip_interface_placement."""

    ip_interfaces: list[dict[str, Any]] = Field(default_factory=list)


class OntapSvmMigrationMessage(OntapModel):
    """OntapSvmMigrationMessage sub-model for messages."""

    code: str = ""
    message: str = ""


class OntapSvmMigrationSourceCluster(OntapModel):
    """OntapSvmMigrationSourceCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapSvmMigrationSourceSvm(OntapModel):
    """OntapSvmMigrationSourceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSvmMigrationSource(OntapModel):
    """OntapSvmMigrationSource sub-model for source."""

    cluster: OntapSvmMigrationSourceCluster = Field(default_factory=OntapSvmMigrationSourceCluster)
    svm: OntapSvmMigrationSourceSvm = Field(default_factory=OntapSvmMigrationSourceSvm)


class OntapSvmMigrationTimeMetrics(OntapModel):
    """OntapSvmMigrationTimeMetrics sub-model for time_metrics."""

    cutover_complete_time: str = ""
    cutover_start_time: str = ""
    cutover_trigger_time: str = ""
    end_time: str = ""
    last_pause_time: str = ""
    last_resume_time: str = ""
    start_time: str = ""


class OntapSvmMigration(OntapModel):
    """OntapSvmMigration information."""

    auto_cutover: bool = False
    auto_source_cleanup: bool = False
    check_only: bool = False
    current_operation: str = ""
    destination: OntapSvmMigrationDestination = Field(default_factory=OntapSvmMigrationDestination)
    ip_interface_placement: OntapSvmMigrationIpInterfacePlacement = Field(
        default_factory=OntapSvmMigrationIpInterfacePlacement
    )
    last_failed_state: str = ""
    last_operation: str = ""
    messages: list[OntapSvmMigrationMessage] = Field(default_factory=list)
    point_of_no_return: bool = False
    restart_count: int = 0
    source: OntapSvmMigrationSource = Field(default_factory=OntapSvmMigrationSource)
    throttle: int = 0
    time_metrics: OntapSvmMigrationTimeMetrics = Field(default_factory=OntapSvmMigrationTimeMetrics)
    uuid: OntapUUID = ""
