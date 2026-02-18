"""OntapExportRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapExportRuleClient(CacheModel):
    """OntapExportRuleClient sub-model for clients."""

    clients_match: str = ""


class OntapExportRule(CacheModel):
    """OntapExportRule information."""

    allow_device_creation: bool = False
    allow_suid: bool = False
    anonymous_user: str = ""
    chown_mode: str = ""
    clients: list[OntapExportRuleClient] = Field(default_factory=list)
    index: int = 0
    ntfs_unix_security: str = ""
    policy_id: int = 0
    policy_name: str = ""
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
