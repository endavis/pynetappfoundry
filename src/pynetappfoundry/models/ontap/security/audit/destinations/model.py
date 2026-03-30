"""OntapSecurityAuditLogForward information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSecurityAuditLogForward(OntapModel):
    """OntapSecurityAuditLogForward information."""

    address: str = ""
    facility: str = ""
    hostname_format_override: str = ""
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    message_format: str = ""
    port: int = 0
    protocol: str = ""
    timestamp_format_override: str = ""
    verify_server: bool = False
