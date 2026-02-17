"""OntapS3BucketLifecycleRule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.s3.services.buckets.rules.model import (
    OntapS3BucketLifecycleRule,
)

ONTAPS3BUCKETLIFECYCLERULE_MAPPING = TypeMapping(
    name="OntapS3BucketLifecycleRule",
    model_class=OntapS3BucketLifecycleRule,
    api_endpoint="/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/rules?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="abort_incomplete_multipart_upload_after_initiation_days",
            api_path="abort_incomplete_multipart_upload.after_initiation_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="bucket_name",
            api_path="bucket_name",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="expiration_expired_object_delete_marker",
            api_path="expiration.expired_object_delete_marker",
            default=False,
        ),
        FieldMapping(
            cache_attr="expiration_object_age_days",
            api_path="expiration.object_age_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="expiration_object_expiry_date",
            api_path="expiration.object_expiry_date",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="non_current_version_expiration_new_non_current_versions",
            api_path="non_current_version_expiration.new_non_current_versions",
            default=0,
        ),
        FieldMapping(
            cache_attr="non_current_version_expiration_non_current_days",
            api_path="non_current_version_expiration.non_current_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="object_filter_prefix",
            api_path="object_filter.prefix",
        ),
        FieldMapping(
            cache_attr="object_filter_size_greater_than",
            api_path="object_filter.size_greater_than",
            default=0,
        ),
        FieldMapping(
            cache_attr="object_filter_size_less_than",
            api_path="object_filter.size_less_than",
            default=0,
        ),
        FieldMapping(
            cache_attr="object_filter_tags",
            api_path="object_filter.tags",
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
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3BucketLifecycleRule", ONTAPS3BUCKETLIFECYCLERULE_MAPPING)
