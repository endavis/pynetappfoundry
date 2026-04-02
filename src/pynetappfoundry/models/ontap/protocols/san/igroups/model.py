# ruff: noqa: E501
"""OntapIgroup information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIgroupConnectivityTrackingRequiredNode(OntapModel):
    """OntapIgroupConnectivityTrackingRequiredNode sub-model for required_nodes."""

    name: str = ""
    uuid: str = ""


class OntapIgroupConnectivityTracking(OntapModel):
    """OntapIgroupConnectivityTracking sub-model for connectivity_tracking."""

    alerts: list[dict[str, Any]] = Field(default_factory=list)
    connection_state: str = ""
    required_nodes: list[OntapIgroupConnectivityTrackingRequiredNode] = Field(default_factory=list)


class OntapIgroupIgroupIgroupIgroupIgroupIgroup(OntapModel):
    """OntapIgroupIgroupIgroupIgroupIgroupIgroup sub-model for igroups."""

    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    name: str = ""
    uuid: str = ""


class OntapIgroupIgroupIgroupIgroupIgroup(OntapModel):
    """OntapIgroupIgroupIgroupIgroupIgroup sub-model for igroups."""

    comment: str = ""
    igroups: list[OntapIgroupIgroupIgroupIgroupIgroupIgroup] = Field(default_factory=list)
    name: str = ""
    uuid: str = ""


class OntapIgroupIgroupIgroupIgroup(OntapModel):
    """OntapIgroupIgroupIgroupIgroup sub-model for igroups."""

    comment: str = ""
    igroups: list[OntapIgroupIgroupIgroupIgroupIgroup] = Field(default_factory=list)
    name: str = ""
    uuid: str = ""


class OntapIgroupIgroupIgroup(OntapModel):
    """OntapIgroupIgroupIgroup sub-model for igroups."""

    comment: str = ""
    igroups: list[OntapIgroupIgroupIgroupIgroup] = Field(default_factory=list)
    name: str = ""
    uuid: str = ""


class OntapIgroupIgroup(OntapModel):
    """OntapIgroupIgroup sub-model for igroups."""

    comment: str = ""
    igroups: list[OntapIgroupIgroupIgroup] = Field(default_factory=list)
    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorConnectivityTracking(OntapModel):
    """OntapIgroupInitiatorConnectivityTracking sub-model for connectivity_tracking."""

    connection_state: str = ""


class OntapIgroupInitiatorIgroup(OntapModel):
    """OntapIgroupInitiatorIgroup sub-model for igroup."""

    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorProximityPeerSvm(OntapModel):
    """OntapIgroupInitiatorProximityPeerSvm sub-model for peer_svms."""

    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorProximity(OntapModel):
    """OntapIgroupInitiatorProximity sub-model for proximity."""

    local_svm: bool = False
    peer_svms: list[OntapIgroupInitiatorProximityPeerSvm] = Field(default_factory=list)


class OntapIgroupInitiator(OntapModel):
    """OntapIgroupInitiator sub-model for initiators."""

    comment: str = ""
    connectivity_tracking: OntapIgroupInitiatorConnectivityTracking = Field(
        default_factory=OntapIgroupInitiatorConnectivityTracking
    )
    igroup: OntapIgroupInitiatorIgroup = Field(default_factory=OntapIgroupInitiatorIgroup)
    name: str = ""
    proximity: OntapIgroupInitiatorProximity = Field(default_factory=OntapIgroupInitiatorProximity)


class OntapIgroupLunMapLunNode(OntapModel):
    """OntapIgroupLunMapLunNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapIgroupLunMapLun(OntapModel):
    """OntapIgroupLunMapLun sub-model for lun."""

    name: str = ""
    node: OntapIgroupLunMapLunNode = Field(default_factory=OntapIgroupLunMapLunNode)
    uuid: str = ""


class OntapIgroupLunMap(OntapModel):
    """OntapIgroupLunMap sub-model for lun_maps."""

    logical_unit_number: int = 0
    lun: OntapIgroupLunMapLun = Field(default_factory=OntapIgroupLunMapLun)


class OntapIgroupParentIgroupParentIgroupParentIgroupParentIgroupParentIgroup(OntapModel):
    """OntapIgroupParentIgroupParentIgroupParentIgroupParentIgroupParentIgroup sub-model for parent_igroups."""

    comment: str = ""
    name: str = ""
    parent_igroups: list[dict[str, Any]] = Field(default_factory=list)
    uuid: str = ""


class OntapIgroupParentIgroupParentIgroupParentIgroupParentIgroup(OntapModel):
    """OntapIgroupParentIgroupParentIgroupParentIgroupParentIgroup sub-model for parent_igroups."""

    comment: str = ""
    name: str = ""
    parent_igroups: list[
        OntapIgroupParentIgroupParentIgroupParentIgroupParentIgroupParentIgroup
    ] = Field(default_factory=list)
    uuid: str = ""


class OntapIgroupParentIgroupParentIgroupParentIgroup(OntapModel):
    """OntapIgroupParentIgroupParentIgroupParentIgroup sub-model for parent_igroups."""

    comment: str = ""
    name: str = ""
    parent_igroups: list[OntapIgroupParentIgroupParentIgroupParentIgroupParentIgroup] = Field(
        default_factory=list
    )
    uuid: str = ""


class OntapIgroupParentIgroupParentIgroup(OntapModel):
    """OntapIgroupParentIgroupParentIgroup sub-model for parent_igroups."""

    comment: str = ""
    name: str = ""
    parent_igroups: list[OntapIgroupParentIgroupParentIgroupParentIgroup] = Field(
        default_factory=list
    )
    uuid: str = ""


class OntapIgroupParentIgroup(OntapModel):
    """OntapIgroupParentIgroup sub-model for parent_igroups."""

    comment: str = ""
    name: str = ""
    parent_igroups: list[OntapIgroupParentIgroupParentIgroup] = Field(default_factory=list)
    uuid: str = ""


class OntapIgroupPortset(OntapModel):
    """OntapIgroupPortset sub-model for portset."""

    name: str = ""
    uuid: str = ""


class OntapIgroupReplicationErrorIgroup(OntapModel):
    """OntapIgroupReplicationErrorIgroup sub-model for igroup."""

    local_svm: bool = False
    name: str = ""
    uuid: str = ""


class OntapIgroupReplicationErrorSummaryArgument(OntapModel):
    """OntapIgroupReplicationErrorSummaryArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapIgroupReplicationErrorSummary(OntapModel):
    """OntapIgroupReplicationErrorSummary sub-model for summary."""

    arguments: list[OntapIgroupReplicationErrorSummaryArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapIgroupReplicationError(OntapModel):
    """OntapIgroupReplicationError sub-model for error."""

    igroup: OntapIgroupReplicationErrorIgroup = Field(
        default_factory=OntapIgroupReplicationErrorIgroup
    )
    summary: OntapIgroupReplicationErrorSummary = Field(
        default_factory=OntapIgroupReplicationErrorSummary
    )


class OntapIgroupReplicationPeerSvm(OntapModel):
    """OntapIgroupReplicationPeerSvm sub-model for peer_svm."""

    name: str = ""
    uuid: str = ""


class OntapIgroupReplication(OntapModel):
    """OntapIgroupReplication sub-model for replication."""

    error: OntapIgroupReplicationError = Field(default_factory=OntapIgroupReplicationError)
    peer_svm: OntapIgroupReplicationPeerSvm = Field(default_factory=OntapIgroupReplicationPeerSvm)
    state: str = ""


class OntapIgroupSvm(OntapModel):
    """OntapIgroupSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIgroupTarget(OntapModel):
    """OntapIgroupTarget sub-model for target."""

    firmware_revision: str = ""
    product_id: str = ""
    vendor_id: str = ""


class OntapIgroup(OntapModel):
    """OntapIgroup information."""

    comment: str = ""
    connectivity_tracking: OntapIgroupConnectivityTracking = Field(
        default_factory=OntapIgroupConnectivityTracking
    )
    delete_on_unmap: bool = False
    igroups: list[OntapIgroupIgroup] = Field(default_factory=list)
    initiators: list[OntapIgroupInitiator] = Field(default_factory=list)
    lun_maps: list[OntapIgroupLunMap] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    parent_igroups: list[OntapIgroupParentIgroup] = Field(default_factory=list)
    portset: OntapIgroupPortset = Field(default_factory=OntapIgroupPortset)
    protocol: str = ""
    replication: OntapIgroupReplication = Field(default_factory=OntapIgroupReplication)
    supports_igroups: bool = False
    svm: OntapIgroupSvm = Field(default_factory=OntapIgroupSvm)
    target: OntapIgroupTarget = Field(default_factory=OntapIgroupTarget)
    uuid: str = ""
