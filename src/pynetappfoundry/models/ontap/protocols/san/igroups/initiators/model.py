"""OntapIgroupInitiator information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceFc(OntapModel):
    """OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceFc sub-model for fc."""

    name: str = ""
    uuid: str = ""
    wwpn: str = ""


class OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceIp(OntapModel):
    """OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceIp sub-model for ip."""

    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterface(OntapModel):
    """OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterface sub-model for interface."""

    fc: OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceFc = Field(
        default_factory=OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceFc
    )
    ip: OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceIp = Field(
        default_factory=OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterfaceIp
    )


class OntapIgroupInitiatorConnectivityTrackingConnectionLogin(OntapModel):
    """OntapIgroupInitiatorConnectivityTrackingConnectionLogin sub-model for logins."""

    connected: bool = False
    interface: OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterface = Field(
        default_factory=OntapIgroupInitiatorConnectivityTrackingConnectionLoginInterface
    )
    last_seen_time: str = ""


class OntapIgroupInitiatorConnectivityTrackingConnectionNode(OntapModel):
    """OntapIgroupInitiatorConnectivityTrackingConnectionNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorConnectivityTrackingConnection(OntapModel):
    """OntapIgroupInitiatorConnectivityTrackingConnection sub-model for connections."""

    logins: list[OntapIgroupInitiatorConnectivityTrackingConnectionLogin] = Field(
        default_factory=list
    )
    node: OntapIgroupInitiatorConnectivityTrackingConnectionNode = Field(
        default_factory=OntapIgroupInitiatorConnectivityTrackingConnectionNode
    )


class OntapIgroupInitiatorConnectivityTracking(OntapModel):
    """OntapIgroupInitiatorConnectivityTracking sub-model for connectivity_tracking."""

    alerts: list[dict[str, Any]] = Field(default_factory=list)
    connection_state: str = ""
    connections: list[OntapIgroupInitiatorConnectivityTrackingConnection] = Field(
        default_factory=list
    )


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


class OntapIgroupInitiatorRecordProximityPeerSvm(OntapModel):
    """OntapIgroupInitiatorRecordProximityPeerSvm sub-model for peer_svms."""

    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorRecordProximity(OntapModel):
    """OntapIgroupInitiatorRecordProximity sub-model for proximity."""

    local_svm: bool = False
    peer_svms: list[OntapIgroupInitiatorRecordProximityPeerSvm] = Field(default_factory=list)


class OntapIgroupInitiatorRecord(OntapModel):
    """OntapIgroupInitiatorRecord sub-model for records."""

    comment: str = ""
    name: str = ""
    proximity: OntapIgroupInitiatorRecordProximity = Field(
        default_factory=OntapIgroupInitiatorRecordProximity
    )


class OntapIgroupInitiator(OntapModel):
    """OntapIgroupInitiator information."""

    comment: str = ""
    connectivity_tracking: OntapIgroupInitiatorConnectivityTracking = Field(
        default_factory=OntapIgroupInitiatorConnectivityTracking
    )
    igroup: OntapIgroupInitiatorIgroup = Field(default_factory=OntapIgroupInitiatorIgroup)
    name: str = ""
    proximity: OntapIgroupInitiatorProximity = Field(default_factory=OntapIgroupInitiatorProximity)
    records: list[OntapIgroupInitiatorRecord] = Field(default_factory=list)
