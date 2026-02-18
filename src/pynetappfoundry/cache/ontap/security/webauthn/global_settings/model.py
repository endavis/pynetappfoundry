"""OntapWebauthnGlobal information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapWebauthnGlobal(CacheModel):
    """OntapWebauthnGlobal information."""

    attestation: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    require_rk: bool = False
    resident_key: str = ""
    scope: str = ""
    timeout: int = 0
    user_verification: str = ""
