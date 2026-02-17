"""Re-export S3 cache models from sub-packages."""

from __future__ import annotations

from pynetappfoundry.cache.protocols.s3.buckets import OntapS3Bucket

__all__ = [
    "OntapS3Bucket",
]
