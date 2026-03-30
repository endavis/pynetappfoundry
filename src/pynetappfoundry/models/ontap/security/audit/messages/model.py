"""OntapSecurityAuditLog information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSecurityAuditLog(OntapModel):
    """OntapSecurityAuditLog information."""

    application: str = ""
    command_id: str = ""
    index: int = 0
    input: str = ""
    location: str = ""
    message: str = ""
    node_name: str = ""
    node_uuid: str = ""
    scope: str = ""
    session_id: str = ""
    state: str = ""
    svm_name: str = ""
    timestamp: str = ""
    user: str = ""
