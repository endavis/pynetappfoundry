"""OntapS3BucketLifecycleRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapS3BucketLifecycleRule(CacheModel):
    """OntapS3BucketLifecycleRule information."""

    abort_incomplete_multipart_upload_after_initiation_days: int = 0
    bucket_name: str = ""
    enabled: bool = False
    expiration_expired_object_delete_marker: bool = False
    expiration_object_age_days: int = 0
    expiration_object_expiry_date: str = ""
    name: str = ""
    non_current_version_expiration_new_non_current_versions: int = 0
    non_current_version_expiration_non_current_days: int = 0
    object_filter_prefix: str = ""
    object_filter_size_greater_than: int = 0
    object_filter_size_less_than: int = 0
    object_filter_tags: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: OntapUUID = ""
