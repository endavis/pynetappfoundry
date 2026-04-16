# ruff: noqa: N815
"""DiiAssetsFabricsAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsFabricsAnnotation(OntapModel):
    """DiiAssetsFabricsAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
