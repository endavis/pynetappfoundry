"""OntapSecurityAudit information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSecurityAudit(OntapModel):
    """OntapSecurityAudit information."""

    cli: bool = False
    http: bool = False
    ontapi: bool = False
