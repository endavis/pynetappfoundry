"""OntapMediatorResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMediatorResponseDrGroup(OntapModel):
    """OntapMediatorResponseDrGroup sub-model for dr_group."""

    id: int = 0


class OntapMediatorResponsePeerCluster(OntapModel):
    """OntapMediatorResponsePeerCluster sub-model for peer_cluster."""

    name: str = ""
    uuid: str = ""


class OntapMediatorResponse(OntapModel):
    """OntapMediatorResponse information."""

    ca_certificate: str = ""
    dr_group: OntapMediatorResponseDrGroup = Field(default_factory=OntapMediatorResponseDrGroup)
    ip_address: str = ""
    password: str = ""
    peer_cluster: OntapMediatorResponsePeerCluster = Field(
        default_factory=OntapMediatorResponsePeerCluster
    )
    peer_mediator_connectivity: str = ""
    port: int = 0
    reachable: bool = False
    user: str = ""
    uuid: str = ""
