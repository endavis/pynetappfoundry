# ruff: noqa: N815
"""DiiAssetsSwitchesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsSwitchesAnnotation(OntapModel):
    """DiiAssetsSwitchesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
