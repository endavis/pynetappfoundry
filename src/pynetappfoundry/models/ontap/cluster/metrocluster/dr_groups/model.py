"""OntapMetroclusterDrGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterDrGroupDrPair(OntapModel):
    """OntapMetroclusterDrGroupDrPair sub-model for dr_pairs."""

    node_name: str = ""
    node_uuid: str = ""
    partner_name: str = ""
    partner_uuid: str = ""


class OntapMetroclusterDrGroupMccipPort(OntapModel):
    """OntapMetroclusterDrGroupMccipPort sub-model for mccip_ports."""

    l3_config_ipv4_interface_address: str = ""
    l3_config_ipv4_interface_gateway: str = ""
    l3_config_ipv4_interface_netmask: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    uuid: str = ""
    vlan_id: int = 0


class OntapMetroclusterDrGroup(OntapModel):
    """OntapMetroclusterDrGroup information."""

    dr_pairs: list[OntapMetroclusterDrGroupDrPair] = Field(default_factory=list)
    id: int = 0
    mccip_ports: list[OntapMetroclusterDrGroupMccipPort] = Field(default_factory=list)
    partner_cluster_name: str = ""
    partner_cluster_uuid: OntapUUID = ""
