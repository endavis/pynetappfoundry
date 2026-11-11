"""OntapLocalCifsGroupMembers type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.local_groups.members.model import (
    OntapLocalCifsGroupMembers,
    OntapLocalCifsGroupMembersRecord,
)

ONTAPLOCALCIFSGROUPMEMBERS_MAPPING = TypeMapping(
    name="OntapLocalCifsGroupMembers",
    model_class=OntapLocalCifsGroupMembers,
    api_endpoint="/protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members?fields=*",
    api_type="ontap",
    parent_mapping="OntapLocalCifsGroup",
    parent_id_fields=(
        "svm.uuid",
        "sid",
    ),
    fields=(
        FieldMapping(
            cache_attr="local_cifs_group.sid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="records",
            item_model=OntapLocalCifsGroupMembersRecord,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLocalCifsGroupMembers", ONTAPLOCALCIFSGROUPMEMBERS_MAPPING)
