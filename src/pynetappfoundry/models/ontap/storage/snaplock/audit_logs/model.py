"""OntapSnaplockLog information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockLogLogArchive(OntapModel):
    """OntapSnaplockLogLogArchive sub-model for log_archive."""

    archive: bool = False
    base_name: str = ""


class OntapSnaplockLogLogFile(OntapModel):
    """OntapSnaplockLogLogFile sub-model for log_files."""

    base_name: str = ""
    expiry_time: str = ""
    path: str = ""
    size: int = 0


class OntapSnaplockLogLogVolumeVolume(OntapModel):
    """OntapSnaplockLogLogVolumeVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockLogLogVolume(OntapModel):
    """OntapSnaplockLogLogVolume sub-model for log_volume."""

    max_log_size: int = 0
    retention_period: str = ""
    volume: OntapSnaplockLogLogVolumeVolume = Field(default_factory=OntapSnaplockLogLogVolumeVolume)


class OntapSnaplockLogSvm(OntapModel):
    """OntapSnaplockLogSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockLog(OntapModel):
    """OntapSnaplockLog information."""

    log_archive: OntapSnaplockLogLogArchive = Field(default_factory=OntapSnaplockLogLogArchive)
    log_files: list[OntapSnaplockLogLogFile] = Field(default_factory=list)
    log_volume: OntapSnaplockLogLogVolume = Field(default_factory=OntapSnaplockLogLogVolume)
    svm: OntapSnaplockLogSvm = Field(default_factory=OntapSnaplockLogSvm)
