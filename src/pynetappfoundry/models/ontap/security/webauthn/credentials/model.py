"""OntapWebauthnCredentials information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapWebauthnCredentialsCredential(OntapModel):
    """OntapWebauthnCredentialsCredential sub-model for credential."""

    id_sha: str = ""
    type_: str = ""


class OntapWebauthnCredentialsOwner(OntapModel):
    """OntapWebauthnCredentialsOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapWebauthnCredentialsPublicKey(OntapModel):
    """OntapWebauthnCredentialsPublicKey sub-model for public_key."""

    algorithm: str = ""
    value: str = ""


class OntapWebauthnCredentialsRelyingParty(OntapModel):
    """OntapWebauthnCredentialsRelyingParty sub-model for relying_party."""

    id: str = ""
    name: str = ""


class OntapWebauthnCredentials(OntapModel):
    """OntapWebauthnCredentials information."""

    creation_time: str = ""
    credential: OntapWebauthnCredentialsCredential = Field(
        default_factory=OntapWebauthnCredentialsCredential
    )
    display_name: str = ""
    index: int = 0
    last_used_time: str = ""
    owner: OntapWebauthnCredentialsOwner = Field(default_factory=OntapWebauthnCredentialsOwner)
    public_key: OntapWebauthnCredentialsPublicKey = Field(
        default_factory=OntapWebauthnCredentialsPublicKey
    )
    relying_party: OntapWebauthnCredentialsRelyingParty = Field(
        default_factory=OntapWebauthnCredentialsRelyingParty
    )
    scope: str = ""
    username: str = ""
