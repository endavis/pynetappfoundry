# ruff: noqa: E501
"""OntapS3BucketLifecycleRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3BucketLifecycleRuleAbortIncompleteMultipartUpload(OntapModel):
    """OntapS3BucketLifecycleRuleAbortIncompleteMultipartUpload sub-model for abort_incomplete_multipart_upload."""

    after_initiation_days: int = 0


class OntapS3BucketLifecycleRuleExpiration(OntapModel):
    """OntapS3BucketLifecycleRuleExpiration sub-model for expiration."""

    expired_object_delete_marker: bool = False
    object_age_days: int = 0
    object_expiry_date: str = ""


class OntapS3BucketLifecycleRuleNonCurrentVersionExpiration(OntapModel):
    """OntapS3BucketLifecycleRuleNonCurrentVersionExpiration sub-model for non_current_version_expiration."""

    new_non_current_versions: int = 0
    non_current_days: int = 0


class OntapS3BucketLifecycleRuleObjectFilter(OntapModel):
    """OntapS3BucketLifecycleRuleObjectFilter sub-model for object_filter."""

    prefix: str = ""
    size_greater_than: int = 0
    size_less_than: int = 0
    tags: list[str] = Field(default_factory=list)


class OntapS3BucketLifecycleRuleSvm(OntapModel):
    """OntapS3BucketLifecycleRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketLifecycleRule(OntapModel):
    """OntapS3BucketLifecycleRule information."""

    abort_incomplete_multipart_upload: OntapS3BucketLifecycleRuleAbortIncompleteMultipartUpload = (
        Field(default_factory=OntapS3BucketLifecycleRuleAbortIncompleteMultipartUpload)
    )
    bucket_name: str = ""
    enabled: bool = False
    expiration: OntapS3BucketLifecycleRuleExpiration = Field(
        default_factory=OntapS3BucketLifecycleRuleExpiration
    )
    name: str = ""
    non_current_version_expiration: OntapS3BucketLifecycleRuleNonCurrentVersionExpiration = Field(
        default_factory=OntapS3BucketLifecycleRuleNonCurrentVersionExpiration
    )
    object_filter: OntapS3BucketLifecycleRuleObjectFilter = Field(
        default_factory=OntapS3BucketLifecycleRuleObjectFilter
    )
    svm: OntapS3BucketLifecycleRuleSvm = Field(default_factory=OntapS3BucketLifecycleRuleSvm)
    uuid: OntapUUID = ""
