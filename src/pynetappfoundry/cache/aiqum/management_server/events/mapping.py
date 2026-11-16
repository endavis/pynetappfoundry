"""AiqumEvent type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.management_server.events.model import AiqumEvent

AIQUMEVENT_MAPPING = TypeMapping(
    name="AiqumEvent",
    model_class=AiqumEvent,
    api_endpoint="/management-server/events",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="acknowledged_username",
        ),
        FieldMapping(
            cache_attr="annotation",
        ),
        FieldMapping(
            cache_attr="assigned",
        ),
        FieldMapping(
            cache_attr="cause",
        ),
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="config_advisor_rule_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="current_state",
        ),
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="group",
        ),
        FieldMapping(
            cache_attr="history",
            default=[],
        ),
        FieldMapping(
            cache_attr="impact",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.key",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="origin",
        ),
        FieldMapping(
            cache_attr="resolved_username",
        ),
        FieldMapping(
            cache_attr="severity",
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumEvent", AIQUMEVENT_MAPPING)
