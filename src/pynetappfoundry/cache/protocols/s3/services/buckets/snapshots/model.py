"""OntapS3BucketSnapshot information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapS3BucketSnapshot(CacheModel):
    """OntapS3BucketSnapshot information."""

    bucket_uuid: OntapUUID = ""
    create_time: str = ""
    name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: OntapUUID = ""
