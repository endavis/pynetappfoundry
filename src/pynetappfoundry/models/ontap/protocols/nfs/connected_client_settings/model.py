"""OntapNfsClientsCache information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNfsClientsCache(OntapModel):
    """OntapNfsClientsCache information."""

    client_retention_interval: str = ""
    enable_nfs_clients_deletion: bool = False
    update_interval: str = ""
