"""OntapMetroclusterInterconnect information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapMetroclusterInterconnectInterface(CacheModel):
    """OntapMetroclusterInterconnectInterface sub-model for interfaces."""

    interfaces_address: str = ""
    interfaces_gateway: str = ""
    interfaces_netmask: str = ""


class OntapMetroclusterInterconnect(CacheModel):
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
