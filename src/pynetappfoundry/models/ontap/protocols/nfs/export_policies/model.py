"""OntapExportPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapExportPolicyClient(OntapModel):
    """OntapExportPolicyClient sub-model for clients."""

    clients_match: str = ""


class OntapExportPolicy(OntapModel):
    """OntapExportPolicy information."""

    allow_device_creation: bool = False
    allow_suid: bool = False
    anonymous_user: str = ""
    chown_mode: str = ""
    clients: list[OntapExportPolicyClient] = Field(default_factory=list)
    index: int = 0
    ntfs_unix_security: str = ""
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)
