"""Re-export storage aggregate cache models and mappings."""

from __future__ import annotations

from pynetappfoundry.cache.storage.aggregates.mapping import AGGREGATE_MAPPING
from pynetappfoundry.cache.storage.aggregates.model import AggregateInfo

__all__ = [
    "AGGREGATE_MAPPING",
    "AggregateInfo",
]
