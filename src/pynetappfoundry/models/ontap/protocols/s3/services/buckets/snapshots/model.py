"""OntapS3BucketSnapshot information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3BucketSnapshotSvm(OntapModel):
    """OntapS3BucketSnapshotSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketSnapshot(OntapModel):
    """OntapS3BucketSnapshot information."""

    bucket_uuid: OntapUUID = ""
    create_time: str = ""
    name: str = ""
    svm: OntapS3BucketSnapshotSvm = Field(default_factory=OntapS3BucketSnapshotSvm)
    uuid: OntapUUID = ""
