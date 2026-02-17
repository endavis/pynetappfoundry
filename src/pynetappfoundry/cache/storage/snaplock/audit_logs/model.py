"""OntapSnaplockLog information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockLogLogFile(CacheModel):
    """OntapSnaplockLogLogFile sub-model for log_files."""

    log_files_base_name: str = ""
    log_files_expiry_time: str = ""
    log_files_path: str = ""
    log_files_size: int = 0


class OntapSnaplockLog(CacheModel):
    """OntapSnaplockLog information."""

    log_archive_archive: bool = False
    log_archive_base_name: str = ""
    log_files: list[OntapSnaplockLogLogFile] = Field(default_factory=list)
    log_volume_max_log_size: int = 0
    log_volume_retention_period: str = ""
    log_volume_volume_name: str = ""
    log_volume_volume_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
