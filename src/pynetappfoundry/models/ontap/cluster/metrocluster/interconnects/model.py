"""OntapMetroclusterInterconnect information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMetroclusterInterconnectInterface(OntapModel):
    """OntapMetroclusterInterconnectInterface sub-model for interfaces."""

    address: str = ""
    gateway: str = ""
    netmask: str = ""


class OntapMetroclusterInterconnect(OntapModel):
    """OntapMetroclusterInterconnect information."""

    adapter: str = ""
    interfaces: list[OntapMetroclusterInterconnectInterface] = Field(default_factory=list)
    mirror_enabled: bool = False
    mirror_state: str = ""
    multipath_policy: str = ""
    node_name: str = ""
    node_uuid: str = ""
    partner_type: str = ""
    state: str = ""
    type_: str = ""
    vlan_id: int = 0
