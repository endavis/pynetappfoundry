"""OntapQuotaRule type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.quota.rules.model import (
    OntapQuotaRule,
    OntapQuotaRuleUser,
)


def _transform_users(record: dict[str, Any]) -> list[OntapQuotaRuleUser]:
    """Transform users into OntapQuotaRuleUser list."""
    return [OntapQuotaRuleUser(**item) for item in record.get("users", [])]


ONTAPQUOTARULE_MAPPING = TypeMapping(
    name="OntapQuotaRule",
    model_class=OntapQuotaRule,
    api_endpoint="/storage/quota/rules?fields=*",
    api_type="ontap",
    identifier_field="uuid",
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
            cache_attr="group.id",
        ),
        FieldMapping(
            cache_attr="group.name",
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
            cache_attr="user_mapping",
            default=False,
        ),
        FieldMapping(
            cache_attr="users",
            transform=_transform_users,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapQuotaRule", ONTAPQUOTARULE_MAPPING)
