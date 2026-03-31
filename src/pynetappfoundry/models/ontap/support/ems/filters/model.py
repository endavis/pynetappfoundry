"""OntapEmsFilter information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsFilterParameterCriteria(OntapModel):
    """OntapEmsFilterParameterCriteria sub-model for parameter_criteria."""

    name_pattern: str = ""
    value_pattern: str = ""


class OntapEmsFilter(OntapModel):
    """OntapEmsFilter information."""

    index: int = 0
    message_criteria_name_pattern: str = ""
    message_criteria_severities: str = ""
    message_criteria_snmp_trap_types: str = ""
    parameter_criteria: list[OntapEmsFilterParameterCriteria] = Field(default_factory=list)
    type_: str = ""
