"""OntapUnixGroupUsers type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.unix_groups.users.model import (
    OntapUnixGroupUsers,
    OntapUnixGroupUsersRecord,
)

ONTAPUNIXGROUPUSERS_MAPPING = TypeMapping(
    name="OntapUnixGroupUsers",
    model_class=OntapUnixGroupUsers,
    api_endpoint="/name-services/unix-groups/{svm.uuid}/{unix_group.name}/users?fields=*",
    api_type="ontap",
    parent_mapping="OntapUnixGroup",
    parent_id_fields=(
        "svm.uuid",
        "name",
    ),
    fields=(
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="records",
            item_model=OntapUnixGroupUsersRecord,
            default=[],
        ),
        FieldMapping(
            cache_attr="skip_name_validation",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="unix_group.name",
        ),
    ),
)

model_registry.register_mapping("OntapUnixGroupUsers", ONTAPUNIXGROUPUSERS_MAPPING)
