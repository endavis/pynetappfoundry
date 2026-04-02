"""OntapEmsFilterRuleResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsFilterRuleResponseMessageCriteria(OntapModel):
    """OntapEmsFilterRuleResponseMessageCriteria sub-model for message_criteria."""

    name_pattern: str = ""
    severities: str = ""
    snmp_trap_types: str = ""


class OntapEmsFilterRuleResponseParameterCriteria(OntapModel):
    """OntapEmsFilterRuleResponseParameterCriteria sub-model for parameter_criteria."""

    name_pattern: str = ""
    value_pattern: str = ""


class OntapEmsFilterRuleResponse(OntapModel):
    """OntapEmsFilterRuleResponse information."""

    index: int = 0
    message_criteria: OntapEmsFilterRuleResponseMessageCriteria = Field(
        default_factory=OntapEmsFilterRuleResponseMessageCriteria
    )
    parameter_criteria: list[OntapEmsFilterRuleResponseParameterCriteria] = Field(
        default_factory=list
    )
    type_: str = ""
