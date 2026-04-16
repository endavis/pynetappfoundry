# ruff: noqa: N815
"""DiiAssetsVirtualmachinesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVirtualmachinesAnnotation(OntapModel):
    """DiiAssetsVirtualmachinesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
