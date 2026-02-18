"""OntapS3User information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapS3User(CacheModel):
    """OntapS3User information."""

    access_key: str = ""
    comment: str = ""
    key_expiry_time: str = ""
    key_time_to_live: str = ""
    name: str = ""
    secret_key: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
