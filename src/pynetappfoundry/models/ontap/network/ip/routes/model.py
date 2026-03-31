"""OntapNetworkRoute information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNetworkRouteInterface(OntapModel):
    """OntapNetworkRouteInterface sub-model for interfaces."""

    ip_address: str = ""
    name: str = ""
    uuid: str = ""


class OntapNetworkRoute(OntapModel):
    """OntapNetworkRoute information."""

    destination_address: str = ""
    destination_family: str = ""
    destination_netmask: str = ""
    gateway: str = ""
    interfaces: list[OntapNetworkRouteInterface] = Field(default_factory=list)
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    metric: int = 0
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
