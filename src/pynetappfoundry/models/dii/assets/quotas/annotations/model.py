# ruff: noqa: N815
"""DiiAssetsQuotasAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsQuotasAnnotation(OntapModel):
    """DiiAssetsQuotasAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
