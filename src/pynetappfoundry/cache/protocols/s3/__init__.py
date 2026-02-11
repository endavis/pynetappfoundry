"""Re-export S3 cache models from sub-packages."""

from __future__ import annotations

from pynetappfoundry.cache.protocols.s3.buckets import S3BucketInfo

__all__ = [
    "S3BucketInfo",
]
