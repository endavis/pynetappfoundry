"""DiiMonitorsRule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.monitors.rules.model import DiiMonitorsRule, DiiMonitorsRuleFilter

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
            item_model=DiiMonitorsRuleFilter,
            default=[],
        ),
        FieldMapping(
            cache_attr="endTime",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiMonitorsRule", DIIMONITORSRULE_MAPPING)
