"""OntapWebauthnCredentials information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapWebauthnCredentials(OntapModel):
    """OntapWebauthnCredentials information."""

    creation_time: str = ""
    credential_id_sha: str = ""
    credential_type: str = ""
    display_name: str = ""
    index: int = 0
    last_used_time: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    public_key_algorithm: str = ""
    public_key_value: str = ""
    relying_party_id: str = ""
    relying_party_name: str = ""
    scope: str = ""
    username: str = ""
