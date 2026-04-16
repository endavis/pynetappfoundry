# ruff: noqa: N815
"""DiiAssetsAnnotationsValue information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsAnnotationsValue(OntapModel):
    """DiiAssetsAnnotationsValue information."""

    values: list[str] = Field(default_factory=list)
    objectType: str = ""
