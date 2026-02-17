"""OntapCounterRow information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapCounterRowCounter(CacheModel):
    """OntapCounterRowCounter sub-model for counters."""

    counters_counters: list[dict[str, Any]] = Field(default_factory=list)
    counters_labels: list[str] = Field(default_factory=list)
    counters_name: str = ""
    counters_value: int = 0
    counters_values: list[int] = Field(default_factory=list)


class OntapCounterRowProperty(CacheModel):
    """OntapCounterRowProperty sub-model for properties."""

    properties_name: str = ""
    properties_value: str = ""


class OntapCounterRow(CacheModel):
    """OntapCounterRow information."""

    aggregation_complete: bool = False
    aggregation_count: int = 0
    counter_table_name: str = ""
    counters: list[OntapCounterRowCounter] = Field(default_factory=list)
    id: str = ""
    properties: list[OntapCounterRowProperty] = Field(default_factory=list)
