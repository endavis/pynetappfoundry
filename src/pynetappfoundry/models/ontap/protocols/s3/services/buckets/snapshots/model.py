"""OntapS3BucketSnapshot information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3BucketSnapshot(OntapModel):
    """OntapS3BucketSnapshot information."""

    bucket_uuid: OntapUUID = ""
    create_time: str = ""
    name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: OntapUUID = ""
