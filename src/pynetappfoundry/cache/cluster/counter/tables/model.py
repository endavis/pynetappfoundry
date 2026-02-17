"""OntapCounterTable information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapCounterTable(CacheModel):
    """OntapCounterTable information."""

    denominator_name: str = ""
    description: str = ""
    name: str = ""
    type_: str = ""
    unit: str = ""
