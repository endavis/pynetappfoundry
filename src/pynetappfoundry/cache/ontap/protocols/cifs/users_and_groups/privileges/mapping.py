"""OntapUserGroupPrivileges type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.users_and_groups.privileges.model import (
    OntapUserGroupPrivileges,
)

ONTAPUSERGROUPPRIVILEGES_MAPPING = TypeMapping(
    name="OntapUserGroupPrivileges",
    model_class=OntapUserGroupPrivileges,
    api_endpoint="/protocols/cifs/users-and-groups/privileges?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="privileges",
            api_path="privileges",
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

model_registry.register_mapping("OntapUserGroupPrivileges", ONTAPUSERGROUPPRIVILEGES_MAPPING)
