"""OntapEmsFilterRuleResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapEmsFilterRuleResponseParameterCriteria(CacheModel):
    """OntapEmsFilterRuleResponseParameterCriteria sub-model for parameter_criteria."""

    parameter_criteria_name_pattern: str = ""
    parameter_criteria_value_pattern: str = ""


class OntapEmsFilterRuleResponse(CacheModel):
    """OntapEmsFilterRuleResponse information."""

    index: int = 0
    message_criteria_name_pattern: str = ""
    message_criteria_severities: str = ""
    message_criteria_snmp_trap_types: str = ""
    parameter_criteria: list[OntapEmsFilterRuleResponseParameterCriteria] = Field(
        default_factory=list
    )
    type_: str = ""
