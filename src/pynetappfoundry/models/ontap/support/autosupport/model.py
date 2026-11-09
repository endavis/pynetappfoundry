"""OntapAutosupport information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutosupportIssueCorrectiveAction(OntapModel):
    """OntapAutosupportIssueCorrectiveAction sub-model for corrective_action."""

    code: str = ""
    message: str = ""


class OntapAutosupportIssueIssue(OntapModel):
    """OntapAutosupportIssueIssue sub-model for issue."""

    code: str = ""
    message: str = ""


class OntapAutosupportIssueNode(OntapModel):
    """OntapAutosupportIssueNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapAutosupportIssue(OntapModel):
    """OntapAutosupportIssue sub-model for issues."""

    component: str = ""
    corrective_action: OntapAutosupportIssueCorrectiveAction = Field(
        default_factory=OntapAutosupportIssueCorrectiveAction
    )
    destination: str = ""
    issue: OntapAutosupportIssueIssue = Field(default_factory=OntapAutosupportIssueIssue)
    node: OntapAutosupportIssueNode = Field(default_factory=OntapAutosupportIssueNode)


class OntapAutosupport(OntapModel):
    """OntapAutosupport information."""

    contact_support: bool = False
    enabled: bool = False
    from_: str = ""
    is_minimal: bool = False
    issues: list[OntapAutosupportIssue] = Field(default_factory=list)
    mail_hosts: list[str] = Field(default_factory=list)
    ondemand_enabled: bool = False
    partner_addresses: list[str] = Field(default_factory=list)
    proxy_url: str = ""
    smtp_encryption: str = ""
    to: list[str] = Field(default_factory=list)
    transport: str = ""
