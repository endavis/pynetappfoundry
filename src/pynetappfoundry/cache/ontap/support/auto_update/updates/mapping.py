"""OntapAutoUpdateStatus type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.auto_update.updates.model import (
    OntapAutoUpdateStatus,
    OntapAutoUpdateStatusStatusArgument,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_status_arguments(
    record: dict[str, Any],
) -> list[OntapAutoUpdateStatusStatusArgument]:
    """Transform status.arguments into OntapAutoUpdateStatusStatusArgument list."""
    try:
        items = get_nested_value(record, "status.arguments")
    except Exception:
        items = []
    return [OntapAutoUpdateStatusStatusArgument(**item) for item in items]


ONTAPAUTOUPDATESTATUS_MAPPING = TypeMapping(
    name="OntapAutoUpdateStatus",
    model_class=OntapAutoUpdateStatus,
    api_endpoint="/support/auto-update/updates?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="action",
        ),
        FieldMapping(
            cache_attr="content_category",
        ),
        FieldMapping(
            cache_attr="content_type",
        ),
        FieldMapping(
            cache_attr="creation_time",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="expiry_time",
        ),
        FieldMapping(
            cache_attr="last_state_change_time",
        ),
        FieldMapping(
            cache_attr="package_id",
        ),
        FieldMapping(
            cache_attr="percent_complete",
            default=0,
        ),
        FieldMapping(
            cache_attr="remaining_time",
        ),
        FieldMapping(
            cache_attr="schedule_time",
        ),
        FieldMapping(
            cache_attr="scheduled_time",
        ),
        FieldMapping(
            cache_attr="start_time",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="status.arguments",
            transform=_transform_status_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="status.code",
        ),
        FieldMapping(
            cache_attr="status.message",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapAutoUpdateStatus", ONTAPAUTOUPDATESTATUS_MAPPING)
