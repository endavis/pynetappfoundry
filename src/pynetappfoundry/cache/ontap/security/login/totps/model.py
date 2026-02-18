"""OntapTotp information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapTotp(CacheModel):
    """OntapTotp information."""

    account_name: str = ""
    comment: str = ""
    enabled: bool = False
    owner_name: str = ""
    owner_uuid: str = ""
    scope: str = ""
    sha_fingerprint: str = ""
