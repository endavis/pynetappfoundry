"""OntapEmsFilter information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsFilterMessageCriteria(OntapModel):
    """OntapEmsFilterMessageCriteria sub-model for message_criteria."""

    name_pattern: str = ""
    severities: str = ""
    snmp_trap_types: str = ""


class OntapEmsFilterParameterCriteria(OntapModel):
    """OntapEmsFilterParameterCriteria sub-model for parameter_criteria."""

    name_pattern: str = ""
    value_pattern: str = ""


class OntapEmsFilter(OntapModel):
    """OntapEmsFilter information."""

    index: int = 0
    message_criteria: OntapEmsFilterMessageCriteria = Field(
        default_factory=OntapEmsFilterMessageCriteria
    )
    parameter_criteria: list[OntapEmsFilterParameterCriteria] = Field(default_factory=list)
    type_: str = ""
