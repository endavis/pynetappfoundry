"""OntapSecurityAudit information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSecurityAudit(CacheModel):
    """OntapSecurityAudit information."""

    cli: bool = False
    http: bool = False
    ontapi: bool = False
