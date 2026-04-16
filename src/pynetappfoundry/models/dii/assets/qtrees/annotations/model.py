# ruff: noqa: N815
"""DiiAssetsQtreesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsQtreesAnnotation(OntapModel):
    """DiiAssetsQtreesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
