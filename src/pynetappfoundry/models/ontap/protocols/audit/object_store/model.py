"""OntapS3Audit information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapS3AuditEvents(OntapModel):
    """OntapS3AuditEvents sub-model for events."""

    data: bool = False
    management: bool = False


class OntapS3AuditLogRetention(OntapModel):
    """OntapS3AuditLogRetention sub-model for retention."""

    count: int = 0
    duration: str = ""


class OntapS3AuditLogRotationSchedule(OntapModel):
    """OntapS3AuditLogRotationSchedule sub-model for schedule."""

    days: list[int] = Field(default_factory=list)
    hours: list[int] = Field(default_factory=list)
    minutes: list[int] = Field(default_factory=list)
    months: list[int] = Field(default_factory=list)
    weekdays: list[int] = Field(default_factory=list)


class OntapS3AuditLogRotation(OntapModel):
    """OntapS3AuditLogRotation sub-model for rotation."""

    now: bool = False
    schedule: OntapS3AuditLogRotationSchedule = Field(
        default_factory=OntapS3AuditLogRotationSchedule
    )
    size: int = 0


class OntapS3AuditLog(OntapModel):
    """OntapS3AuditLog sub-model for log."""

    format: str = ""
    retention: OntapS3AuditLogRetention = Field(default_factory=OntapS3AuditLogRetention)
    rotation: OntapS3AuditLogRotation = Field(default_factory=OntapS3AuditLogRotation)


class OntapS3AuditSvm(OntapModel):
    """OntapS3AuditSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3Audit(OntapModel):
    """OntapS3Audit information."""

    enabled: bool = False
    events: OntapS3AuditEvents = Field(default_factory=OntapS3AuditEvents)
    log: OntapS3AuditLog = Field(default_factory=OntapS3AuditLog)
    log_path: str = ""
    svm: OntapS3AuditSvm = Field(default_factory=OntapS3AuditSvm)
