# ruff: noqa: N815
"""DiiMonitorsRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class DiiMonitorsRuleFilter(OntapModel):
    """DiiMonitorsRuleFilter sub-model for filters."""

    displayValue: str = ""
    field: str = ""
    id: OntapUUID = ""
    value: str = ""


class DiiMonitorsRule(OntapModel):
    """DiiMonitorsRule information."""

    expression: str = ""
    tenantId: str = ""
    name: str = ""
    active: bool = False
    startTime: int = 0
    id: str = ""
    filters: list[DiiMonitorsRuleFilter] = Field(default_factory=list)
    endTime: int = 0
