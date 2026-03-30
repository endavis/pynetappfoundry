"""OntapUnixUser type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.unix_users.model import OntapUnixUser

ONTAPUNIXUSER_MAPPING = TypeMapping(
    name="OntapUnixUser",
    model_class=OntapUnixUser,
    api_endpoint="/name-services/unix-users?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="full_name",
            api_path="full_name",
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="primary_gid",
            api_path="primary_gid",
            default=0,
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
    ),
)

model_registry.register_mapping("OntapUnixUser", ONTAPUNIXUSER_MAPPING)
