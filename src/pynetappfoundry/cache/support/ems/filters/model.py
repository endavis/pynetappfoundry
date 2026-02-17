"""OntapEmsFilter information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapEmsFilterParameterCriteria(CacheModel):
    """OntapEmsFilterParameterCriteria sub-model for parameter_criteria."""

    parameter_criteria_name_pattern: str = ""
    parameter_criteria_value_pattern: str = ""


class OntapEmsFilter(CacheModel):
    """OntapEmsFilter information."""

    index: int = 0
    message_criteria_name_pattern: str = ""
    message_criteria_severities: str = ""
    message_criteria_snmp_trap_types: str = ""
    parameter_criteria: list[OntapEmsFilterParameterCriteria] = Field(default_factory=list)
    type_: str = ""
