"""OntapPublickey information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapPublickey(OntapModel):
    """OntapPublickey information."""

    account_name: str = ""
    certificate: str = ""
    certificate_details: str = ""
    certificate_expired: str = ""
    certificate_revoked: str = ""
    comment: str = ""
    index: int = 0
    obfuscated_fingerprint: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    public_key: str = ""
    scope: str = ""
    sha_fingerprint: str = ""
