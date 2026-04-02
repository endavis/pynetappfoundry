"""OntapMetroclusterDrGroup information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterDrGroupMccipPortL3ConfigIpv4Interface(OntapModel):
    """OntapMetroclusterDrGroupMccipPortL3ConfigIpv4Interface sub-model for ipv4_interface."""

    address: str = ""
    gateway: str = ""
    netmask: str = ""


class OntapMetroclusterDrGroupMccipPortL3Config(OntapModel):
    """OntapMetroclusterDrGroupMccipPortL3Config sub-model for l3_config."""

    ipv4_interface: OntapMetroclusterDrGroupMccipPortL3ConfigIpv4Interface = Field(
        default_factory=OntapMetroclusterDrGroupMccipPortL3ConfigIpv4Interface
    )


class OntapMetroclusterDrGroupMccipPortNode(OntapModel):
    """OntapMetroclusterDrGroupMccipPortNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDrGroupMccipPort(OntapModel):
    """OntapMetroclusterDrGroupMccipPort sub-model for mccip_ports."""

    l3_config: OntapMetroclusterDrGroupMccipPortL3Config = Field(
        default_factory=OntapMetroclusterDrGroupMccipPortL3Config
    )
    name: str = ""
    node: OntapMetroclusterDrGroupMccipPortNode = Field(
        default_factory=OntapMetroclusterDrGroupMccipPortNode
    )
    uuid: str = ""
    vlan_id: int = 0


class OntapMetroclusterDrGroupPartnerCluster(OntapModel):
    """OntapMetroclusterDrGroupPartnerCluster sub-model for partner_cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterDrGroup(OntapModel):
    """OntapMetroclusterDrGroup information."""

    dr_pairs: list[dict[str, Any]] = Field(default_factory=list)
    id: int = 0
    mccip_ports: list[OntapMetroclusterDrGroupMccipPort] = Field(default_factory=list)
    partner_cluster: OntapMetroclusterDrGroupPartnerCluster = Field(
        default_factory=OntapMetroclusterDrGroupPartnerCluster
    )
