"""OntapMediatorResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapMediatorResponse(CacheModel):
    """OntapMediatorResponse information."""

    ca_certificate: str = ""
    dr_group_id: int = 0
    ip_address: str = ""
    password: str = ""
    peer_cluster_name: str = ""
    peer_cluster_uuid: str = ""
    peer_mediator_connectivity: str = ""
    port: int = 0
    reachable: bool = False
    user: str = ""
    uuid: str = ""
