"""OntapFabric information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFabricConnection(OntapModel):
    """OntapFabricConnection sub-model for connections."""

    cluster_port_name: str = ""
    cluster_port_node_name: str = ""
    cluster_port_uuid: str = ""
    cluster_port_wwpn: str = ""
    switch_port_wwpn: str = ""
    switch_wwn: str = ""


class OntapFabric(OntapModel):
    """OntapFabric information."""

    cache_age: str = ""
    cache_is_current: bool = False
    cache_update_time: str = ""
    connections: list[OntapFabricConnection] = Field(default_factory=list)
    name: str = ""
    zoneset_name: str = ""
