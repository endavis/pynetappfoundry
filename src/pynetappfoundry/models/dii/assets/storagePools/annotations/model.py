# ruff: noqa: N815
"""DiiAssetsStoragepoolsAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragepoolsAnnotation(OntapModel):
    """DiiAssetsStoragepoolsAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
