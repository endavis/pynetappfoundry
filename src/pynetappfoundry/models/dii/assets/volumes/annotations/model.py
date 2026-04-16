# ruff: noqa: N815
"""DiiAssetsVolumesAnnotation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVolumesAnnotation(OntapModel):
    """DiiAssetsVolumesAnnotation information."""

    displayValue: str = ""
    rawValue: str = ""
    definition: str = ""
    label: str = ""
    annotationAssignment: str = ""
