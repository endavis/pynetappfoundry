# ruff: noqa: N815
"""DiiAssetsSharesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsSharesAnnotation(OntapModel):
    """DiiAssetsSharesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
