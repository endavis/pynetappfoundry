"""OntapWebauthnGlobal information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapWebauthnGlobalOwner(OntapModel):
    """OntapWebauthnGlobalOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapWebauthnGlobal(OntapModel):
    """OntapWebauthnGlobal information."""

    attestation: str = ""
    owner: OntapWebauthnGlobalOwner = Field(default_factory=OntapWebauthnGlobalOwner)
    require_rk: bool = False
    resident_key: str = ""
    scope: str = ""
    timeout: int = 0
    user_verification: str = ""
