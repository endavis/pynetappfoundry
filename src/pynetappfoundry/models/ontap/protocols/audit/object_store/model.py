"""OntapS3Audit information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapS3Audit(OntapModel):
    """OntapS3Audit information."""

    enabled: bool = False
    events_data: bool = False
    events_management: bool = False
    log_format: str = ""
    log_retention_count: int = 0
    log_retention_duration: str = ""
    log_rotation_now: bool = False
    log_rotation_schedule_days: list[int] = Field(default_factory=list)
    log_rotation_schedule_hours: list[int] = Field(default_factory=list)
    log_rotation_schedule_minutes: list[int] = Field(default_factory=list)
    log_rotation_schedule_months: list[int] = Field(default_factory=list)
    log_rotation_schedule_weekdays: list[int] = Field(default_factory=list)
    log_rotation_size: int = 0
    log_path: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
