# ruff: noqa: N815
"""DiiAssetsVmdksAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVmdksAnnotation(OntapModel):
    """DiiAssetsVmdksAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
