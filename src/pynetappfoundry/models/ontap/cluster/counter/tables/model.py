"""OntapCounterTable information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCounterTableCounterSchemaDenominator(OntapModel):
    """OntapCounterTableCounterSchemaDenominator sub-model for denominator."""

    name: str = ""


class OntapCounterTableCounterSchema(OntapModel):
    """OntapCounterTableCounterSchema sub-model for counter_schemas."""

    denominator: OntapCounterTableCounterSchemaDenominator = Field(
        default_factory=OntapCounterTableCounterSchemaDenominator
    )
    description: str = ""
    name: str = ""
    type_: str = ""
    unit: str = ""


class OntapCounterTable(OntapModel):
    """OntapCounterTable information."""

    counter_schemas: list[OntapCounterTableCounterSchema] = Field(default_factory=list)
    description: str = ""
    name: str = ""
