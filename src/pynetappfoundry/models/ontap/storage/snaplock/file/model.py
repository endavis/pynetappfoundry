"""OntapSnaplockFileRetention information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockFileRetentionSvm(OntapModel):
    """OntapSnaplockFileRetentionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockFileRetentionVolume(OntapModel):
    """OntapSnaplockFileRetentionVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockFileRetention(OntapModel):
    """OntapSnaplockFileRetention information."""

    expiry_time: str = ""
    file_path: str = ""
    is_expired: bool = False
    retention_period: str = ""
    seconds_until_expiry: int = 0
    svm: OntapSnaplockFileRetentionSvm = Field(default_factory=OntapSnaplockFileRetentionSvm)
    volume: OntapSnaplockFileRetentionVolume = Field(
        default_factory=OntapSnaplockFileRetentionVolume
    )
