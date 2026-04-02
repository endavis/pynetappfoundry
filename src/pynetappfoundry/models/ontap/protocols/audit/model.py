"""OntapAudit information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAuditEvents(OntapModel):
    """OntapAuditEvents sub-model for events."""

    async_delete: bool = False
    audit_policy_change: bool = False
    authorization_policy: bool = False
    cap_staging: bool = False
    cifs_logon_logoff: bool = False
    file_operations: bool = False
    file_share: bool = False
    security_group: bool = False
    user_account: bool = False


class OntapAuditLogRetention(OntapModel):
    """OntapAuditLogRetention sub-model for retention."""

    count: int = 0
    duration: str = ""


class OntapAuditLogRotationSchedule(OntapModel):
    """OntapAuditLogRotationSchedule sub-model for schedule."""

    days: list[int] = Field(default_factory=list)
    hours: list[int] = Field(default_factory=list)
    minutes: list[int] = Field(default_factory=list)
    months: list[int] = Field(default_factory=list)
    weekdays: list[int] = Field(default_factory=list)


class OntapAuditLogRotation(OntapModel):
    """OntapAuditLogRotation sub-model for rotation."""

    now: bool = False
    schedule: OntapAuditLogRotationSchedule = Field(default_factory=OntapAuditLogRotationSchedule)
    size: int = 0


class OntapAuditLog(OntapModel):
    """OntapAuditLog sub-model for log."""

    format: str = ""
    retention: OntapAuditLogRetention = Field(default_factory=OntapAuditLogRetention)
    rotation: OntapAuditLogRotation = Field(default_factory=OntapAuditLogRotation)


class OntapAuditSvm(OntapModel):
    """OntapAuditSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapAudit(OntapModel):
    """OntapAudit information."""

    charge_qos: bool = False
    enabled: bool = False
    events: OntapAuditEvents = Field(default_factory=OntapAuditEvents)
    guarantee: bool = False
    log: OntapAuditLog = Field(default_factory=OntapAuditLog)
    log_path: str = ""
    svm: OntapAuditSvm = Field(default_factory=OntapAuditSvm)
