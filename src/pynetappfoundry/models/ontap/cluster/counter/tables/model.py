"""OntapCounterTable information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCounterTableDenominator(OntapModel):
    """OntapCounterTableDenominator sub-model for denominator."""

    name: str = ""


class OntapCounterTable(OntapModel):
    """OntapCounterTable information."""

    denominator: OntapCounterTableDenominator = Field(default_factory=OntapCounterTableDenominator)
    description: str = ""
    name: str = ""
    type_: str = ""
    unit: str = ""
