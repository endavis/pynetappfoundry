"""OntapLocalCifsGroup type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.cifs.local_groups.model import (
    OntapLocalCifsGroup,
    OntapLocalCifsGroupMember,
)


def _transform_members(record: dict[str, Any]) -> list[OntapLocalCifsGroupMember]:
    """Transform members into OntapLocalCifsGroupMember list."""
    return [OntapLocalCifsGroupMember(**item) for item in record.get("members", [])]


ONTAPLOCALCIFSGROUP_MAPPING = TypeMapping(
    name="OntapLocalCifsGroup",
    model_class=OntapLocalCifsGroup,
    api_endpoint="/protocols/cifs/local-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="members",
            transform=_transform_members,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="sid",
            api_path="sid",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLocalCifsGroup", ONTAPLOCALCIFSGROUP_MAPPING)
