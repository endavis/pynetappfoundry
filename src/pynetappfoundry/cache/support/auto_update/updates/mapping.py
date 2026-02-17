"""OntapAutoUpdateStatus type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.support.auto_update.updates.model import (
    OntapAutoUpdateStatus,
    OntapAutoUpdateStatusArgument,
)


def _transform_status_arguments(record: dict[str, Any]) -> list[OntapAutoUpdateStatusArgument]:
    """Transform status.arguments into OntapAutoUpdateStatusArgument list."""
    return [OntapAutoUpdateStatusArgument(**item) for item in record.get("status.arguments", [])]


ONTAPAUTOUPDATESTATUS_MAPPING = TypeMapping(
    name="OntapAutoUpdateStatus",
    model_class=OntapAutoUpdateStatus,
    api_endpoint="/support/auto-update/updates?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="action",
            api_path="action",
        ),
        FieldMapping(
            cache_attr="content_category",
            api_path="content_category",
        ),
        FieldMapping(
            cache_attr="content_type",
            api_path="content_type",
        ),
        FieldMapping(
            cache_attr="creation_time",
            api_path="creation_time",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="end_time",
            api_path="end_time",
        ),
        FieldMapping(
            cache_attr="expiry_time",
            api_path="expiry_time",
        ),
        FieldMapping(
            cache_attr="last_state_change_time",
            api_path="last_state_change_time",
        ),
        FieldMapping(
            cache_attr="package_id",
            api_path="package_id",
        ),
        FieldMapping(
            cache_attr="percent_complete",
            api_path="percent_complete",
            default=0,
        ),
        FieldMapping(
            cache_attr="remaining_time",
            api_path="remaining_time",
        ),
        FieldMapping(
            cache_attr="schedule_time",
            api_path="schedule_time",
        ),
        FieldMapping(
            cache_attr="scheduled_time",
            api_path="scheduled_time",
        ),
        FieldMapping(
            cache_attr="start_time",
            api_path="start_time",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="status_arguments",
            transform=_transform_status_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="status_code",
            api_path="status.code",
        ),
        FieldMapping(
            cache_attr="status_message",
            api_path="status.message",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapAutoUpdateStatus", ONTAPAUTOUPDATESTATUS_MAPPING)
