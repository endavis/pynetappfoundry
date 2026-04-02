"""OntapSecurityAuditLogForward information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityAuditLogForwardIpspace(OntapModel):
    """OntapSecurityAuditLogForwardIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapSecurityAuditLogForward(OntapModel):
    """OntapSecurityAuditLogForward information."""

    address: str = ""
    facility: str = ""
    hostname_format_override: str = ""
    ipspace: OntapSecurityAuditLogForwardIpspace = Field(
        default_factory=OntapSecurityAuditLogForwardIpspace
    )
    message_format: str = ""
    port: int = 0
    protocol: str = ""
    timestamp_format_override: str = ""
    verify_server: bool = False
