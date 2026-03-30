"""OntapSnaplockFileRetention information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockFileRetention(OntapModel):
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
