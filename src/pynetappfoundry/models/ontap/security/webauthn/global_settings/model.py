"""OntapWebauthnGlobal information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapWebauthnGlobal(OntapModel):
    """OntapWebauthnGlobal information."""

    attestation: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    require_rk: bool = False
    resident_key: str = ""
    scope: str = ""
    timeout: int = 0
    user_verification: str = ""
