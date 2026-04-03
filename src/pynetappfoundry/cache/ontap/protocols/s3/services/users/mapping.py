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
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="access_key",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="key_expiry_time",
        ),
        FieldMapping(
            cache_attr="key_time_to_live",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="secret_key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3User", ONTAPS3USER_MAPPING)
