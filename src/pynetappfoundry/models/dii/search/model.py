# ruff: noqa: N815
"""DiiSearchresultsummary information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiSearchresultsummary(OntapModel):
    """DiiSearchresultsummary information."""

    searchString: str = ""
    foundResults: bool = False
    topHit: str = ""
    resultsByCategory: str = ""
