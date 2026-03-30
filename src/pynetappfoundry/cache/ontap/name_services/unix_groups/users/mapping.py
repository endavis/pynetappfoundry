"""OntapUnixGroupUsers type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.unix_groups.users.model import (
    OntapUnixGroupUsers,
    OntapUnixGroupUsersRecord,
)


def _transform_records(record: dict[str, Any]) -> list[OntapUnixGroupUsersRecord]:
    """Transform records into OntapUnixGroupUsersRecord list."""
    return [OntapUnixGroupUsersRecord(**item) for item in record.get("records", [])]


ONTAPUNIXGROUPUSERS_MAPPING = TypeMapping(
    name="OntapUnixGroupUsers",
    model_class=OntapUnixGroupUsers,
    api_endpoint="/name-services/unix-groups/{svm.uuid}/{unix_group.name}/users?fields=*",
    api_type="ontap",
    parent_mapping="OntapUnixGroup",
    parent_id_field="svm_uuid",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="records",
            api_path="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="skip_name_validation",
            api_path="skip_name_validation",
            default=False,
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
            cache_attr="unix_group_name",
            api_path="unix_group.name",
        ),
    ),
)

model_registry.register_mapping("OntapUnixGroupUsers", ONTAPUNIXGROUPUSERS_MAPPING)
