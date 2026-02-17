"""OntapSnaplockFileRetention information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockFileRetention(CacheModel):
    """OntapSnaplockFileRetention information."""

    expiry_time: str = ""
    file_path: str = ""
    is_expired: bool = False
    retention_period: str = ""
    seconds_until_expiry: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
