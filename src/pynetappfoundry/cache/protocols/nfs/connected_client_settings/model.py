"""OntapNfsClientsCache information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNfsClientsCache(CacheModel):
    """OntapNfsClientsCache information."""

    client_retention_interval: str = ""
    enable_nfs_clients_deletion: bool = False
    update_interval: str = ""
