"""OntapMetroclusterDrGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapMetroclusterDrGroupDrPair(CacheModel):
    """OntapMetroclusterDrGroupDrPair sub-model for dr_pairs."""

    dr_pairs_node_name: str = ""
    dr_pairs_node_uuid: str = ""
    dr_pairs_partner_name: str = ""
    dr_pairs_partner_uuid: str = ""


class OntapMetroclusterDrGroupMccipPort(CacheModel):
    """OntapMetroclusterDrGroupMccipPort sub-model for mccip_ports."""

    mccip_ports_l3_config_ipv4_interface_address: str = ""
    mccip_ports_l3_config_ipv4_interface_gateway: str = ""
    mccip_ports_l3_config_ipv4_interface_netmask: str = ""
    mccip_ports_name: str = ""
    mccip_ports_node_name: str = ""
    mccip_ports_node_uuid: str = ""
    mccip_ports_uuid: str = ""
    mccip_ports_vlan_id: int = 0


class OntapMetroclusterDrGroup(CacheModel):
    """OntapMetroclusterDrGroup information."""

    dr_pairs: list[OntapMetroclusterDrGroupDrPair] = Field(default_factory=list)
    id: int = 0
    mccip_ports: list[OntapMetroclusterDrGroupMccipPort] = Field(default_factory=list)
    partner_cluster_name: str = ""
    partner_cluster_uuid: OntapUUID = ""
