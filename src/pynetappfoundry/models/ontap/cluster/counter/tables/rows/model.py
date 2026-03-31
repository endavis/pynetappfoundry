"""OntapCounterRow information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCounterRowCounter(OntapModel):
    """OntapCounterRowCounter sub-model for counters."""

    counters: list[dict[str, Any]] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)
    name: str = ""
    value: int = 0
    values: list[int] = Field(default_factory=list)


class OntapCounterRowProperty(OntapModel):
    """OntapCounterRowProperty sub-model for properties."""

    name: str = ""
    value: str = ""


class OntapCounterRow(OntapModel):
    """OntapCounterRow information."""

    aggregation_complete: bool = False
    aggregation_count: int = 0
    counter_table_name: str = ""
    counters: list[OntapCounterRowCounter] = Field(default_factory=list)
    id: str = ""
    properties: list[OntapCounterRowProperty] = Field(default_factory=list)
