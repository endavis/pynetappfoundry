"""OntapS3User type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.services.users.model import OntapS3User

ONTAPS3USER_MAPPING = TypeMapping(
    name="OntapS3User",
    model_class=OntapS3User,
    api_endpoint="/protocols/s3/services/{svm.uuid}/users?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="svm_uuid",
    fields=(
        FieldMapping(
            cache_attr="access_key",
            api_path="access_key",
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="key_expiry_time",
            api_path="key_expiry_time",
        ),
        FieldMapping(
            cache_attr="key_time_to_live",
            api_path="key_time_to_live",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="secret_key",
            api_path="secret_key",
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

model_registry.register_mapping("OntapS3User", ONTAPS3USER_MAPPING)
