"""OntapQuotaRule type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.quota.rules.model import OntapQuotaRule, OntapQuotaRuleUser


def _transform_users(record: dict[str, Any]) -> list[OntapQuotaRuleUser]:
    """Transform users into OntapQuotaRuleUser list."""
    return [OntapQuotaRuleUser(**item) for item in record.get("users", [])]


ONTAPQUOTARULE_MAPPING = TypeMapping(
    name="OntapQuotaRule",
    model_class=OntapQuotaRule,
    api_endpoint="/storage/quota/rules?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="files_hard_limit",
            api_path="files.hard_limit",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="files_soft_limit",
            api_path="files.soft_limit",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="group_id",
            api_path="group.id",
        ),
        FieldMapping(
            cache_attr="group_name",
            api_path="group.name",
        ),
        FieldMapping(
            cache_attr="qtree_id",
            api_path="qtree.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="qtree_name",
            api_path="qtree.name",
        ),
        FieldMapping(
            cache_attr="space_hard_limit",
            api_path="space.hard_limit",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="space_soft_limit",
            api_path="space.soft_limit",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="user_mapping",
            api_path="user_mapping",
            default=False,
        ),
        FieldMapping(
            cache_attr="users",
            api_path="users",
            transform=_transform_users,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapQuotaRule", ONTAPQUOTARULE_MAPPING)
