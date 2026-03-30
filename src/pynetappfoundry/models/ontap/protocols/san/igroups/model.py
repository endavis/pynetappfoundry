"""OntapIgroup information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIgroupAlert(OntapModel):
    """OntapIgroupAlert sub-model for alerts."""

    connectivity_tracking_alerts_summary_arguments: list[dict[str, Any]] = Field(
        default_factory=list
    )
    connectivity_tracking_alerts_summary_code: str = ""
    connectivity_tracking_alerts_summary_message: str = ""


class OntapIgroupRequiredNode(OntapModel):
    """OntapIgroupRequiredNode sub-model for required_nodes."""

    connectivity_tracking_required_nodes_name: str = ""
    connectivity_tracking_required_nodes_uuid: str = ""


class OntapIgroupIgroup(OntapModel):
    """OntapIgroupIgroup sub-model for igroups."""

    igroups_comment: str = ""
    igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    igroups_name: str = ""
    igroups_uuid: str = ""


class OntapIgroupInitiator(OntapModel):
    """OntapIgroupInitiator sub-model for initiators."""

    initiators_comment: str = ""
    initiators_connectivity_tracking_connection_state: str = ""
    initiators_igroup_name: str = ""
    initiators_igroup_uuid: str = ""
    initiators_name: str = ""
    initiators_proximity_local_svm: bool = False
    initiators_proximity_peer_svms: list[dict[str, Any]] = Field(default_factory=list)


class OntapIgroupLunMap(OntapModel):
    """OntapIgroupLunMap sub-model for lun_maps."""

    lun_maps_logical_unit_number: int = 0
    lun_maps_lun_name: str = ""
    lun_maps_lun_node_name: str = ""
    lun_maps_lun_node_uuid: str = ""
    lun_maps_lun_uuid: str = ""


class OntapIgroupParentIgroup(OntapModel):
    """OntapIgroupParentIgroup sub-model for parent_igroups."""

    parent_igroups_comment: str = ""
    parent_igroups_name: str = ""
    parent_igroups_parent_igroups: list[dict[str, Any]] = Field(default_factory=list)
    parent_igroups_uuid: str = ""


class OntapIgroupArgument(OntapModel):
    """OntapIgroupArgument sub-model for arguments."""

    replication_error_summary_arguments_code: str = ""
    replication_error_summary_arguments_message: str = ""


class OntapIgroup(OntapModel):
    """OntapIgroup information."""

    comment: str = ""
    connectivity_tracking_alerts: list[OntapIgroupAlert] = Field(default_factory=list)
    connectivity_tracking_connection_state: str = ""
    connectivity_tracking_required_nodes: list[OntapIgroupRequiredNode] = Field(
        default_factory=list
    )
    delete_on_unmap: bool = False
    igroups: list[OntapIgroupIgroup] = Field(default_factory=list)
    initiators: list[OntapIgroupInitiator] = Field(default_factory=list)
    lun_maps: list[OntapIgroupLunMap] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    parent_igroups: list[OntapIgroupParentIgroup] = Field(default_factory=list)
    portset_name: str = ""
    portset_uuid: str = ""
    protocol: str = ""
    replication_error_igroup_local_svm: bool = False
    replication_error_igroup_name: str = ""
    replication_error_igroup_uuid: str = ""
    replication_error_summary_arguments: list[OntapIgroupArgument] = Field(default_factory=list)
    replication_error_summary_code: str = ""
    replication_error_summary_message: str = ""
    replication_peer_svm_name: str = ""
    replication_peer_svm_uuid: str = ""
    replication_state: str = ""
    supports_igroups: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    target_firmware_revision: str = ""
    target_product_id: str = ""
    target_vendor_id: str = ""
    uuid: str = ""
