# ruff: noqa: N815
"""DiiAssetsInternalvolumesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsInternalvolumesAnnotation(OntapModel):
    """DiiAssetsInternalvolumesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
