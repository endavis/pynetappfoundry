"""OntapMetroclusterNode information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterNodeCluster(OntapModel):
    """OntapMetroclusterNodeCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterNodeDrAuxiliaryCluster(OntapModel):
    """OntapMetroclusterNodeDrAuxiliaryCluster sub-model for dr_auxiliary_cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterNodeDrAuxiliaryPartner(OntapModel):
    """OntapMetroclusterNodeDrAuxiliaryPartner sub-model for dr_auxiliary_partner."""

    name: str = ""
    system_id: str = ""
    uuid: str = ""


class OntapMetroclusterNodeDrPartner(OntapModel):
    """OntapMetroclusterNodeDrPartner sub-model for dr_partner."""

    name: str = ""
    system_id: str = ""
    uuid: str = ""


class OntapMetroclusterNodeDrPartnerCluster(OntapModel):
    """OntapMetroclusterNodeDrPartnerCluster sub-model for dr_partner_cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterNodeHaPartner(OntapModel):
    """OntapMetroclusterNodeHaPartner sub-model for ha_partner."""

    name: str = ""
    system_id: str = ""
    uuid: str = ""


class OntapMetroclusterNodeHaPartnerCluster(OntapModel):
    """OntapMetroclusterNodeHaPartnerCluster sub-model for ha_partner_cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterNodeNode(OntapModel):
    """OntapMetroclusterNodeNode sub-model for node."""

    name: str = ""
    system_id: str = ""
    uuid: str = ""


class OntapMetroclusterNode(OntapModel):
    """OntapMetroclusterNode information."""

    automatic_uso: bool = False
    cluster: OntapMetroclusterNodeCluster = Field(default_factory=OntapMetroclusterNodeCluster)
    configuration_state: str = ""
    dr_auxiliary_cluster: OntapMetroclusterNodeDrAuxiliaryCluster = Field(
        default_factory=OntapMetroclusterNodeDrAuxiliaryCluster
    )
    dr_auxiliary_partner: OntapMetroclusterNodeDrAuxiliaryPartner = Field(
        default_factory=OntapMetroclusterNodeDrAuxiliaryPartner
    )
    dr_group_id: int = 0
    dr_mirroring_state: str = ""
    dr_operation_state: str = ""
    dr_partner: OntapMetroclusterNodeDrPartner = Field(
        default_factory=OntapMetroclusterNodeDrPartner
    )
    dr_partner_cluster: OntapMetroclusterNodeDrPartnerCluster = Field(
        default_factory=OntapMetroclusterNodeDrPartnerCluster
    )
    encryption_enabled: bool = False
    ha_partner: OntapMetroclusterNodeHaPartner = Field(
        default_factory=OntapMetroclusterNodeHaPartner
    )
    ha_partner_cluster: OntapMetroclusterNodeHaPartnerCluster = Field(
        default_factory=OntapMetroclusterNodeHaPartnerCluster
    )
    is_mccip: bool = False
    limit_enforcement: str = ""
    node: OntapMetroclusterNodeNode = Field(default_factory=OntapMetroclusterNodeNode)
