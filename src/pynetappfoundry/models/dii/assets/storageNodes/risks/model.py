# ruff: noqa: N815
"""DiiAssetsStoragenodesRisk information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragenodesRisk(OntapModel):
    """DiiAssetsStoragenodesRisk information."""

    severity: str = ""
    sourceId: int = 0
    parent: str = ""
    resource: str = ""
    impact: str = ""
    link: str = ""
    simpleName: str = ""
    sourceType: str = ""
    mitigationCategory: str = ""
    riskSource: str = ""
    name: str = ""
    details: str = ""
    id: int = 0
    category: str = ""
    statusCode: str = ""
