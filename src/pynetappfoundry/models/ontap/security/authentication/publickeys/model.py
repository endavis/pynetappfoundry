"""OntapPublickey information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPublickeyAccount(OntapModel):
    """OntapPublickeyAccount sub-model for account."""

    name: str = ""


class OntapPublickeyOwner(OntapModel):
    """OntapPublickeyOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapPublickey(OntapModel):
    """OntapPublickey information."""

    account: OntapPublickeyAccount = Field(default_factory=OntapPublickeyAccount)
    certificate: str = ""
    certificate_details: str = ""
    certificate_expired: str = ""
    certificate_revoked: str = ""
    comment: str = ""
    index: int = 0
    obfuscated_fingerprint: str = ""
    owner: OntapPublickeyOwner = Field(default_factory=OntapPublickeyOwner)
    public_key: str = ""
    scope: str = ""
    sha_fingerprint: str = ""
