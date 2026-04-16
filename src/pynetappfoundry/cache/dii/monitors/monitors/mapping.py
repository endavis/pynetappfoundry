# ruff: noqa: N802
"""DiiMonitorsMonitor type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.monitors.monitors.model import (
    DiiMonitorsMonitor,
    DiiMonitorsMonitorCondition,
    DiiMonitorsMonitorFilter,
    DiiMonitorsMonitorResolutioncondition,
    DiiMonitorsMonitorResolutionfilter,
)


def _transform_filters(record: dict[str, Any]) -> list[DiiMonitorsMonitorFilter]:
    """Transform filters into DiiMonitorsMonitorFilter list."""
    return [DiiMonitorsMonitorFilter(**item) for item in record.get("filters", [])]


def _transform_resolutionConditions(
    record: dict[str, Any],
) -> list[DiiMonitorsMonitorResolutioncondition]:
    """Transform resolutionConditions into DiiMonitorsMonitorResolutioncondition list."""
    return [
        DiiMonitorsMonitorResolutioncondition(**item)
        for item in record.get("resolutionConditions", [])
    ]


def _transform_resolutionFilters(
    record: dict[str, Any],
) -> list[DiiMonitorsMonitorResolutionfilter]:
    """Transform resolutionFilters into DiiMonitorsMonitorResolutionfilter list."""
    return [
        DiiMonitorsMonitorResolutionfilter(**item) for item in record.get("resolutionFilters", [])
    ]


def _transform_conditions(record: dict[str, Any]) -> list[DiiMonitorsMonitorCondition]:
    """Transform conditions into DiiMonitorsMonitorCondition list."""
    return [DiiMonitorsMonitorCondition(**item) for item in record.get("conditions", [])]


DIIMONITORSMONITOR_MAPPING = TypeMapping(
    name="DiiMonitorsMonitor",
    model_class=DiiMonitorsMonitor,
    api_endpoint="/monitors/monitors",
    api_type="dii",
    identifier_field="id",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="metadata_",
            api_path="metadata",
        ),
        FieldMapping(
            cache_attr="resolutionType",
        ),
        FieldMapping(
            cache_attr="resolutionExpression",
        ),
        FieldMapping(
            cache_attr="advanced",
            default=False,
        ),
        FieldMapping(
            cache_attr="groupId",
        ),
        FieldMapping(
            cache_attr="correctiveActions",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="groupBy",
            default=[],
        ),
        FieldMapping(
            cache_attr="measurement",
        ),
        FieldMapping(
            cache_attr="objectType",
        ),
        FieldMapping(
            cache_attr="baseUnit",
        ),
        FieldMapping(
            cache_attr="monitorType",
        ),
        FieldMapping(
            cache_attr="immutableConfigUpdated",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="defaultAlertMetric",
        ),
        FieldMapping(
            cache_attr="expression",
        ),
        FieldMapping(
            cache_attr="resolutionTimeoutSeconds",
            default=0,
        ),
        FieldMapping(
            cache_attr="schemaVersion",
            default=0,
        ),
        FieldMapping(
            cache_attr="created",
            default=0,
        ),
        FieldMapping(
            cache_attr="advancedExpression",
        ),
        FieldMapping(
            cache_attr="filters",
            transform=_transform_filters,
            default=[],
        ),
        FieldMapping(
            cache_attr="resolutionConditions",
            transform=_transform_resolutionConditions,
            default=[],
        ),
        FieldMapping(
            cache_attr="isSystem",
            default=False,
        ),
        FieldMapping(
            cache_attr="targetUnit",
        ),
        FieldMapping(
            cache_attr="resolutionFilters",
            transform=_transform_resolutionFilters,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="category",
        ),
        FieldMapping(
            cache_attr="conditions",
            transform=_transform_conditions,
            default=[],
        ),
        FieldMapping(
            cache_attr="advancedResolutionExpression",
        ),
        FieldMapping(
            cache_attr="updated",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("DiiMonitorsMonitor", DIIMONITORSMONITOR_MAPPING)
