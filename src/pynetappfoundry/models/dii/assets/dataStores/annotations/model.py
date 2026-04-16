# ruff: noqa: N815
"""DiiAssetsDatastoresAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsDatastoresAnnotation(OntapModel):
    """DiiAssetsDatastoresAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
