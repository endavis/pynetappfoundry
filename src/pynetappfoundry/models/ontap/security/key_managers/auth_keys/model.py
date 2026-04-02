"""OntapKeyManagerAuthKey information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKeyManagerAuthKeySecurityKeyManager(OntapModel):
    """OntapKeyManagerAuthKeySecurityKeyManager sub-model for security_key_manager."""

    uuid: str = ""


class OntapKeyManagerAuthKey(OntapModel):
    """OntapKeyManagerAuthKey information."""

    key_id: str = ""
    key_tag: str = ""
    passphrase: str = ""
    security_key_manager: OntapKeyManagerAuthKeySecurityKeyManager = Field(
        default_factory=OntapKeyManagerAuthKeySecurityKeyManager
    )
