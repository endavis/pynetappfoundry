"""OntapSecurityAuditLog information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityAuditLogNode(OntapModel):
    """OntapSecurityAuditLogNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSecurityAuditLogSvm(OntapModel):
    """OntapSecurityAuditLogSvm sub-model for svm."""

    name: str = ""


class OntapSecurityAuditLog(OntapModel):
    """OntapSecurityAuditLog information."""

    application: str = ""
    command_id: str = ""
    index: int = 0
    input: str = ""
    location: str = ""
    message: str = ""
    node: OntapSecurityAuditLogNode = Field(default_factory=OntapSecurityAuditLogNode)
    scope: str = ""
    session_id: str = ""
    state: str = ""
    svm: OntapSecurityAuditLogSvm = Field(default_factory=OntapSecurityAuditLogSvm)
    timestamp: str = ""
    user: str = ""
