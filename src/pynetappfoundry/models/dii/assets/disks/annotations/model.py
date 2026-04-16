# ruff: noqa: N815
"""DiiAssetsDisksAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsDisksAnnotation(OntapModel):
    """DiiAssetsDisksAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
