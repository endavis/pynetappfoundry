"""OntapS3User information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapS3User(OntapModel):
    """OntapS3User information."""

    access_key: str = ""
    comment: str = ""
    key_expiry_time: str = ""
    key_time_to_live: str = ""
    name: str = ""
    secret_key: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
