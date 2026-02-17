"""OntapNetworkRoute information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNetworkRouteInterface(CacheModel):
    """OntapNetworkRouteInterface sub-model for interfaces."""

    interfaces_ip_address: str = ""
    interfaces_name: str = ""
    interfaces_uuid: str = ""


class OntapNetworkRoute(CacheModel):
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
