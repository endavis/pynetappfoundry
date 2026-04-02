"""OntapExportRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapExportRuleClient(OntapModel):
    """OntapExportRuleClient sub-model for clients."""

    match: str = ""


class OntapExportRulePolicy(OntapModel):
    """OntapExportRulePolicy sub-model for policy."""

    id: int = 0
    name: str = ""


class OntapExportRuleSvm(OntapModel):
    """OntapExportRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapExportRule(OntapModel):
    """OntapExportRule information."""

    allow_device_creation: bool = False
    allow_suid: bool = False
    anonymous_user: str = ""
    chown_mode: str = ""
    clients: list[OntapExportRuleClient] = Field(default_factory=list)
    index: int = 0
    ntfs_unix_security: str = ""
    policy: OntapExportRulePolicy = Field(default_factory=OntapExportRulePolicy)
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)
    svm: OntapExportRuleSvm = Field(default_factory=OntapExportRuleSvm)
