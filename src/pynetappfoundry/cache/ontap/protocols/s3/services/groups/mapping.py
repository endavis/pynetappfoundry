"""OntapS3Group type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.services.groups.model import (
    OntapS3Group,
    OntapS3GroupPolicy,
    OntapS3GroupUser,
)

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
            item_model=OntapS3GroupPolicy,
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
            item_model=OntapS3GroupUser,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapS3Group", ONTAPS3GROUP_MAPPING)
