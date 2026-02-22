"""OntapLocalCifsGroupMembers type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.cifs.local_groups.members.model import (
    OntapLocalCifsGroupMembers,
    OntapLocalCifsGroupMembersRecord,
)


def _transform_records(record: dict[str, Any]) -> list[OntapLocalCifsGroupMembersRecord]:
    """Transform records into OntapLocalCifsGroupMembersRecord list."""
    return [OntapLocalCifsGroupMembersRecord(**item) for item in record.get("records", [])]


ONTAPLOCALCIFSGROUPMEMBERS_MAPPING = TypeMapping(
    name="OntapLocalCifsGroupMembers",
    model_class=OntapLocalCifsGroupMembers,
    api_endpoint="/protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members?fields=*",
    api_type="ontap",
    parent_mapping="OntapLocalCifsGroup",
    parent_id_field="svm_uuid",
    fields=(
        FieldMapping(
            cache_attr="local_cifs_group_sid",
            api_path="local_cifs_group.sid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
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

model_registry.register_mapping("OntapLocalCifsGroupMembers", ONTAPLOCALCIFSGROUPMEMBERS_MAPPING)
