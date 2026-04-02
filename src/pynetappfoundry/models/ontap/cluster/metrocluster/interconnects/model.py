"""OntapMetroclusterInterconnect information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMetroclusterInterconnectInterface(OntapModel):
    """OntapMetroclusterInterconnectInterface sub-model for interfaces."""

    address: str = ""
    gateway: str = ""
    netmask: str = ""


class OntapMetroclusterInterconnectMirror(OntapModel):
    """OntapMetroclusterInterconnectMirror sub-model for mirror."""

    enabled: bool = False
    state: str = ""


class OntapMetroclusterInterconnectNode(OntapModel):
    """OntapMetroclusterInterconnectNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterInterconnect(OntapModel):
    """OntapMetroclusterInterconnect information."""

    adapter: str = ""
    interfaces: list[OntapMetroclusterInterconnectInterface] = Field(default_factory=list)
    mirror: OntapMetroclusterInterconnectMirror = Field(
        default_factory=OntapMetroclusterInterconnectMirror
    )
    multipath_policy: str = ""
    node: OntapMetroclusterInterconnectNode = Field(
        default_factory=OntapMetroclusterInterconnectNode
    )
    partner_type: str = ""
    state: str = ""
    type_: str = ""
    vlan_id: int = 0
