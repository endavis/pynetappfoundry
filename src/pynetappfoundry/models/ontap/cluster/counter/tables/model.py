"""OntapCounterTable information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapCounterTable(OntapModel):
    """OntapCounterTable information."""

    denominator_name: str = ""
    description: str = ""
    name: str = ""
    type_: str = ""
    unit: str = ""
