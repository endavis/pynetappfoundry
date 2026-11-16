"""AiqumAlert type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.management_server.alerts.model import (
    AiqumAlert,
    AiqumAlertResource,
)

AIQUMALERT_MAPPING = TypeMapping(
    name="AiqumAlert",
    model_class=AiqumAlert,
    api_endpoint="/management-server/alerts",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="action.notification.duration",
        ),
        FieldMapping(
            cache_attr="action.notification.emails",
            default=[],
        ),
        FieldMapping(
            cache_attr="action.notification.from_",
            api_path="action.notification.from",
        ),
        FieldMapping(
            cache_attr="action.notification.send_snmp_trap",
            default=False,
        ),
        FieldMapping(
            cache_attr="action.notification.to",
        ),
        FieldMapping(
            cache_attr="action.script.key",
        ),
        FieldMapping(
            cache_attr="action.script.name",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="event.severities",
            default=[],
        ),
        FieldMapping(
            cache_attr="event.types",
            default=[],
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="resource",
            item_model=AiqumAlertResource,
            default=[],
        ),
    ),
)

model_registry.register_mapping("AiqumAlert", AIQUMALERT_MAPPING)
