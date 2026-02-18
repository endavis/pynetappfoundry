"""OntapMetroclusterNode information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapMetroclusterNode(CacheModel):
    """OntapMetroclusterNode information."""

    automatic_uso: bool = False
    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    configuration_state: str = ""
    dr_auxiliary_cluster_name: str = ""
    dr_auxiliary_cluster_uuid: OntapUUID = ""
    dr_auxiliary_partner_name: str = ""
    dr_auxiliary_partner_system_id: str = ""
    dr_auxiliary_partner_uuid: str = ""
    dr_group_id: int = 0
    dr_mirroring_state: str = ""
    dr_operation_state: str = ""
    dr_partner_name: str = ""
    dr_partner_system_id: str = ""
    dr_partner_uuid: str = ""
    dr_partner_cluster_name: str = ""
    dr_partner_cluster_uuid: OntapUUID = ""
    encryption_enabled: bool = False
    ha_partner_name: str = ""
    ha_partner_system_id: str = ""
    ha_partner_uuid: str = ""
    ha_partner_cluster_name: str = ""
    ha_partner_cluster_uuid: OntapUUID = ""
    is_mccip: bool = False
    limit_enforcement: str = ""
    node_name: str = ""
    node_system_id: str = ""
    node_uuid: str = ""
