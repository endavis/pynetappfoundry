"""OntapCounterRow information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCounterRowAggregation(OntapModel):
    """OntapCounterRowAggregation sub-model for aggregation."""

    complete: bool = False
    count: int = 0


class OntapCounterRowCounterTable(OntapModel):
    """OntapCounterRowCounterTable sub-model for counter_table."""

    name: str = ""


class OntapCounterRowCounterCounter(OntapModel):
    """OntapCounterRowCounterCounter sub-model for counters."""

    label: str = ""
    values: list[int] = Field(default_factory=list)


class OntapCounterRowCounter(OntapModel):
    """OntapCounterRowCounter sub-model for counters."""

    counters: list[OntapCounterRowCounterCounter] = Field(default_factory=list)
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

    aggregation: OntapCounterRowAggregation = Field(default_factory=OntapCounterRowAggregation)
    counter_table: OntapCounterRowCounterTable = Field(default_factory=OntapCounterRowCounterTable)
    counters: list[OntapCounterRowCounter] = Field(default_factory=list)
    id: str = ""
    properties: list[OntapCounterRowProperty] = Field(default_factory=list)
