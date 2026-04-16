# ruff: noqa: N815
"""DiiAssetsHostsAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsHostsAnnotation(OntapModel):
    """DiiAssetsHostsAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
