"""OntapAutoUpdateInfo information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapAutoUpdateInfo(CacheModel):
    """OntapAutoUpdateInfo information."""

    enabled: bool = False
    eula_accepted: bool = False
    eula_accepted_ip_address: str = ""
    eula_accepted_timestamp: str = ""
    eula_user_id_accepted: str = ""
