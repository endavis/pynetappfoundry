"""OntapKeyManagerKeys information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKeyManagerKeysNode(OntapModel):
    """OntapKeyManagerKeysNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapKeyManagerKeysSecurityKeyManager(OntapModel):
    """OntapKeyManagerKeysSecurityKeyManager sub-model for security_key_manager."""

    uuid: str = ""


class OntapKeyManagerKeysSvm(OntapModel):
    """OntapKeyManagerKeysSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapKeyManagerKeys(OntapModel):
    """OntapKeyManagerKeys information."""

    crn: str = ""
    encryption_algorithm: str = ""
    key_id: str = ""
    key_manager: str = ""
    key_server: str = ""
    key_store: str = ""
    key_store_type: str = ""
    key_tag: str = ""
    key_type: str = ""
    key_user: str = ""
    node: OntapKeyManagerKeysNode = Field(default_factory=OntapKeyManagerKeysNode)
    policy: str = ""
    restored: bool = False
    scope: str = ""
    security_key_manager: OntapKeyManagerKeysSecurityKeyManager = Field(
        default_factory=OntapKeyManagerKeysSecurityKeyManager
    )
    svm: OntapKeyManagerKeysSvm = Field(default_factory=OntapKeyManagerKeysSvm)
