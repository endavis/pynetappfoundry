"""OntapS3Group type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.services.groups.model import (
    OntapS3Group,
    OntapS3GroupPolicy,
    OntapS3GroupUser,
)


def _transform_policies(record: dict[str, Any]) -> list[OntapS3GroupPolicy]:
    """Transform policies into OntapS3GroupPolicy list."""
    return [OntapS3GroupPolicy(**item) for item in record.get("policies", [])]


def _transform_users(record: dict[str, Any]) -> list[OntapS3GroupUser]:
    """Transform users into OntapS3GroupUser list."""
    return [OntapS3GroupUser(**item) for item in record.get("users", [])]


ONTAPS3GROUP_MAPPING = TypeMapping(
    name="OntapS3Group",
    model_class=OntapS3Group,
    api_endpoint="/protocols/s3/services/{svm.uuid}/groups?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="policies",
            transform=_transform_policies,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="users",
            transform=_transform_users,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapS3Group", ONTAPS3GROUP_MAPPING)
