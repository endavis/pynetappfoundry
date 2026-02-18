"""OntapS3BucketSnapshot type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.s3.services.buckets.snapshots.model import (
    OntapS3BucketSnapshot,
)

ONTAPS3BUCKETSNAPSHOT_MAPPING = TypeMapping(
    name="OntapS3BucketSnapshot",
    model_class=OntapS3BucketSnapshot,
    api_endpoint="/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="bucket_uuid",
            api_path="bucket_uuid",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3BucketSnapshot", ONTAPS3BUCKETSNAPSHOT_MAPPING)
