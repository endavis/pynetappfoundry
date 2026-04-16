# ruff: noqa: N815
"""DiiQuery information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiQuery(OntapModel):
    """DiiQuery information."""

    owner: str = ""
    objectMeasurement: str = ""
    expression: str = ""
    schemaVersion: int = 0
    offset: int = 0
    sort: str = ""
    groupBy: list[str] = Field(default_factory=list)
    creationDate: str = ""
    ownerid: str = ""
    objectType: str = ""
    otherProps: str = ""
    stickyPaneWidth: int = 0
    groupByFieldWidths: list[str] = Field(default_factory=list)
    name: str = ""
    limit: int = 0
    fromTime: int = 0
    id: int = 0
    fields: list[str] = Field(default_factory=list)
    toTime: int = 0
    objectCategory: str = ""
    timeRange: str = ""
