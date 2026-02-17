"""OntapAudit information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapAudit(CacheModel):
    """OntapAudit information."""

    charge_qos: bool = False
    enabled: bool = False
    events_async_delete: bool = False
    events_audit_policy_change: bool = False
    events_authorization_policy: bool = False
    events_cap_staging: bool = False
    events_cifs_logon_logoff: bool = False
    events_file_operations: bool = False
    events_file_share: bool = False
    events_security_group: bool = False
    events_user_account: bool = False
    guarantee: bool = False
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
