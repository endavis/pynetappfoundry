"""OntapExportPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapExportPolicyRuleClient(OntapModel):
    """OntapExportPolicyRuleClient sub-model for clients."""

    match: str = ""


class OntapExportPolicyRule(OntapModel):
    """OntapExportPolicyRule sub-model for rules."""

    allow_device_creation: bool = False
    allow_suid: bool = False
    anonymous_user: str = ""
    chown_mode: str = ""
    clients: list[OntapExportPolicyRuleClient] = Field(default_factory=list)
    index: int = 0
    ntfs_unix_security: str = ""
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)


class OntapExportPolicySvm(OntapModel):
    """OntapExportPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapExportPolicy(OntapModel):
    """OntapExportPolicy information."""

    id: int = 0
    name: str = ""
    rules: list[OntapExportPolicyRule] = Field(default_factory=list)
    svm: OntapExportPolicySvm = Field(default_factory=OntapExportPolicySvm)
