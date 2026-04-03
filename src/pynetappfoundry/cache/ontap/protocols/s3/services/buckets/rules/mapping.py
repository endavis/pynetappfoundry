"""OntapS3BucketLifecycleRule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.services.buckets.rules.model import (
    OntapS3BucketLifecycleRule,
)

ONTAPS3BUCKETLIFECYCLERULE_MAPPING = TypeMapping(
    name="OntapS3BucketLifecycleRule",
    model_class=OntapS3BucketLifecycleRule,
    api_endpoint="/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/rules?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="abort_incomplete_multipart_upload.after_initiation_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="bucket_name",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="expiration.expired_object_delete_marker",
            default=False,
        ),
        FieldMapping(
            cache_attr="expiration.object_age_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="expiration.object_expiry_date",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="non_current_version_expiration.new_non_current_versions",
            default=0,
        ),
        FieldMapping(
            cache_attr="non_current_version_expiration.non_current_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="object_filter.prefix",
        ),
        FieldMapping(
            cache_attr="object_filter.size_greater_than",
            default=0,
        ),
        FieldMapping(
            cache_attr="object_filter.size_less_than",
            default=0,
        ),
        FieldMapping(
            cache_attr="object_filter.tags",
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3BucketLifecycleRule", ONTAPS3BUCKETLIFECYCLERULE_MAPPING)
