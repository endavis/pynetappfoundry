"""S3 bucket information — /protocols/s3/buckets."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class S3BucketInfo(CacheModel):
    """S3 bucket information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    type: str = ""  # s3, nas-s3
    size: int = 0  # bytes
    versioning_state: str = ""  # enabled, disabled, suspended
    comment: str = ""
    nas_path: str = ""
