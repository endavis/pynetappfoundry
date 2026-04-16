"""DiiMonitorsRule type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.monitors.rules.model import DiiMonitorsRule, DiiMonitorsRuleFilter


def _transform_filters(record: dict[str, Any]) -> list[DiiMonitorsRuleFilter]:
    """Transform filters into DiiMonitorsRuleFilter list."""
    return [DiiMonitorsRuleFilter(**item) for item in record.get("filters", [])]


DIIMONITORSRULE_MAPPING = TypeMapping(
    name="DiiMonitorsRule",
    model_class=DiiMonitorsRule,
    api_endpoint="/monitors/rules",
    api_type="dii",
    identifier_field="id",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="expression",
        ),
        FieldMapping(
            cache_attr="tenantId",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="active",
            default=False,
        ),
        FieldMapping(
            cache_attr="startTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="filters",
            transform=_transform_filters,
            default=[],
        ),
        FieldMapping(
            cache_attr="endTime",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiMonitorsRule", DIIMONITORSRULE_MAPPING)
