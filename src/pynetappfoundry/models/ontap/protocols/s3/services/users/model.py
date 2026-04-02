"""OntapS3User information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapS3UserSvm(OntapModel):
    """OntapS3UserSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3User(OntapModel):
    """OntapS3User information."""

    access_key: str = ""
    comment: str = ""
    key_expiry_time: str = ""
    key_time_to_live: str = ""
    name: str = ""
    secret_key: str = ""
    svm: OntapS3UserSvm = Field(default_factory=OntapS3UserSvm)
