"""OntapNetworkRoute information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNetworkRouteDestination(OntapModel):
    """OntapNetworkRouteDestination sub-model for destination."""

    address: str = ""
    family: str = ""
    netmask: str = ""


class OntapNetworkRouteInterfaceIp(OntapModel):
    """OntapNetworkRouteInterfaceIp sub-model for ip."""

    address: str = ""


class OntapNetworkRouteInterface(OntapModel):
    """OntapNetworkRouteInterface sub-model for interfaces."""

    ip: OntapNetworkRouteInterfaceIp = Field(default_factory=OntapNetworkRouteInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapNetworkRouteIpspace(OntapModel):
    """OntapNetworkRouteIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapNetworkRouteSvm(OntapModel):
    """OntapNetworkRouteSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNetworkRoute(OntapModel):
    """OntapNetworkRoute information."""

    destination: OntapNetworkRouteDestination = Field(default_factory=OntapNetworkRouteDestination)
    gateway: str = ""
    interfaces: list[OntapNetworkRouteInterface] = Field(default_factory=list)
    ipspace: OntapNetworkRouteIpspace = Field(default_factory=OntapNetworkRouteIpspace)
    metric: int = 0
    scope: str = ""
    svm: OntapNetworkRouteSvm = Field(default_factory=OntapNetworkRouteSvm)
    uuid: str = ""
