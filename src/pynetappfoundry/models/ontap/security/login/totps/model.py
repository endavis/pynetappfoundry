"""OntapTotp information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTotpAccount(OntapModel):
    """OntapTotpAccount sub-model for account."""

    name: str = ""


class OntapTotpOwner(OntapModel):
    """OntapTotpOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapTotp(OntapModel):
    """OntapTotp information."""

    account: OntapTotpAccount = Field(default_factory=OntapTotpAccount)
    comment: str = ""
    enabled: bool = False
    owner: OntapTotpOwner = Field(default_factory=OntapTotpOwner)
    scope: str = ""
    sha_fingerprint: str = ""
