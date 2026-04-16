# ruff: noqa: N815
"""DiiAssetsAnnotation information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsAnnotation(OntapModel):
    """DiiAssetsAnnotation information."""

    name: str = ""
    description: str = ""
    isUserDefined: bool = False
    isCostBased: bool = False
    id: int = 0
    label: str = ""
    type_: str = ""
    supportedObjectTypes: list[str] = Field(default_factory=list)
    enumValues: list[str] = Field(default_factory=list)
