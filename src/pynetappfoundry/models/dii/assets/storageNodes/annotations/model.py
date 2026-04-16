# ruff: noqa: N815
"""DiiAssetsStoragenodesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragenodesAnnotation(OntapModel):
    """DiiAssetsStoragenodesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
