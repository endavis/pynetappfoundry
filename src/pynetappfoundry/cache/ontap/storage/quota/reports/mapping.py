"""OntapQuotaReport type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.quota.reports.model import (
    OntapQuotaReport,
    OntapQuotaReportUser,
)


def _transform_users(record: dict[str, Any]) -> list[OntapQuotaReportUser]:
    """Transform users into OntapQuotaReportUser list."""
    return [OntapQuotaReportUser(**item) for item in record.get("users", [])]


ONTAPQUOTAREPORT_MAPPING = TypeMapping(
    name="OntapQuotaReport",
    model_class=OntapQuotaReport,
    api_endpoint="/storage/quota/reports?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="files.hard_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.soft_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.used.hard_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.used.soft_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.used.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="group.id",
        ),
        FieldMapping(
            cache_attr="group.name",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="qtree.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="qtree.name",
        ),
        FieldMapping(
            cache_attr="space.hard_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.soft_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used.hard_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used.soft_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="users",
            transform=_transform_users,
            default=[],
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapQuotaReport", ONTAPQUOTAREPORT_MAPPING)
