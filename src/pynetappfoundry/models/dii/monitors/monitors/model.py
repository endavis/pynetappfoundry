# ruff: noqa: N815
"""DiiMonitorsMonitor information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class DiiMonitorsMonitorFilter(OntapModel):
    """DiiMonitorsMonitorFilter sub-model for filters."""

    displayValue: str = ""
    field: str = ""
    id: OntapUUID = ""
    value: str = ""


class DiiMonitorsMonitorResolutionconditionObjectassociation(OntapModel):
    """DiiMonitorsMonitorResolutionconditionObjectassociation sub-model for objectAssociation."""

    matchType: str = ""
    objectMetadataField: str = ""
    regexValue: str = ""
    objectType: str = ""
    columnName: str = ""


class DiiMonitorsMonitorResolutioncondition(OntapModel):
    """DiiMonitorsMonitorResolutioncondition sub-model for resolutionConditions."""

    ceiling: float = 0.0
    timeAggregation: str = ""
    anomalyCalcWindowSeconds: int = 0
    aggregation: str = ""
    occurrence: str = ""
    metric: str = ""
    qualifier: str = ""
    objectAssociation: DiiMonitorsMonitorResolutionconditionObjectassociation = Field(
        default_factory=DiiMonitorsMonitorResolutionconditionObjectassociation
    )
    metricLabel: str = ""
    falseAlarmRate: str = ""
    windowSeconds: int = 0
    metricCounters: str = ""
    floor: float = 0.0
    levels: str = ""
    direction: str = ""


class DiiMonitorsMonitorResolutionfilter(OntapModel):
    """DiiMonitorsMonitorResolutionfilter sub-model for resolutionFilters."""

    displayValue: str = ""
    field: str = ""
    id: OntapUUID = ""
    value: str = ""


class DiiMonitorsMonitorConditionObjectassociation(OntapModel):
    """DiiMonitorsMonitorConditionObjectassociation sub-model for objectAssociation."""

    matchType: str = ""
    objectMetadataField: str = ""
    regexValue: str = ""
    objectType: str = ""
    columnName: str = ""


class DiiMonitorsMonitorCondition(OntapModel):
    """DiiMonitorsMonitorCondition sub-model for conditions."""

    ceiling: float = 0.0
    timeAggregation: str = ""
    anomalyCalcWindowSeconds: int = 0
    aggregation: str = ""
    occurrence: str = ""
    metric: str = ""
    qualifier: str = ""
    objectAssociation: DiiMonitorsMonitorConditionObjectassociation = Field(
        default_factory=DiiMonitorsMonitorConditionObjectassociation
    )
    metricLabel: str = ""
    falseAlarmRate: str = ""
    windowSeconds: int = 0
    metricCounters: str = ""
    floor: float = 0.0
    levels: str = ""
    direction: str = ""


class DiiMonitorsMonitor(OntapModel):
    """DiiMonitorsMonitor information."""

    metadata_: str = ""
    resolutionType: str = ""
    resolutionExpression: str = ""
    advanced: bool = False
    groupId: str = ""
    correctiveActions: str = ""
    description: str = ""
    groupBy: list[str] = Field(default_factory=list)
    measurement: str = ""
    objectType: str = ""
    baseUnit: str = ""
    monitorType: str = ""
    immutableConfigUpdated: int = 0
    id: OntapUUID = ""
    defaultAlertMetric: str = ""
    expression: str = ""
    resolutionTimeoutSeconds: int = 0
    schemaVersion: int = 0
    created: int = 0
    advancedExpression: str = ""
    filters: list[DiiMonitorsMonitorFilter] = Field(default_factory=list)
    resolutionConditions: list[DiiMonitorsMonitorResolutioncondition] = Field(default_factory=list)
    isSystem: bool = False
    targetUnit: str = ""
    resolutionFilters: list[DiiMonitorsMonitorResolutionfilter] = Field(default_factory=list)
    name: str = ""
    self: str = ""
    category: str = ""
    conditions: list[DiiMonitorsMonitorCondition] = Field(default_factory=list)
    advancedResolutionExpression: str = ""
    updated: int = 0
    status: str = ""
