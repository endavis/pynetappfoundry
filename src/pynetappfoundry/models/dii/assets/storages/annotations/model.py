# ruff: noqa: N815
"""DiiAssetsStoragesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragesAnnotation(OntapModel):
    """DiiAssetsStoragesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
