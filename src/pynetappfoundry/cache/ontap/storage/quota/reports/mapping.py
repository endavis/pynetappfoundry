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
            api_path="files.hard_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.soft_limit",
            api_path="files.soft_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.used.hard_limit_percent",
            api_path="files.used.hard_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.used.soft_limit_percent",
            api_path="files.used.soft_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="files.used.total",
            api_path="files.used.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="group.id",
            api_path="group.id",
        ),
        FieldMapping(
            cache_attr="group.name",
            api_path="group.name",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="qtree.id",
            api_path="qtree.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="qtree.name",
            api_path="qtree.name",
        ),
        FieldMapping(
            cache_attr="space.hard_limit",
            api_path="space.hard_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.soft_limit",
            api_path="space.soft_limit",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used.hard_limit_percent",
            api_path="space.used.hard_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used.soft_limit_percent",
            api_path="space.used.soft_limit_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used.total",
            api_path="space.used.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="users",
            api_path="users",
            transform=_transform_users,
            default=[],
        ),
        FieldMapping(
            cache_attr="volume.name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapQuotaReport", ONTAPQUOTAREPORT_MAPPING)
