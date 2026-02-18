"""OntapSchedule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapSchedule(CacheModel):
    """OntapSchedule information."""

    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    cron_days: list[int] = Field(default_factory=list)
    cron_hours: list[int] = Field(default_factory=list)
    cron_minutes: list[int] = Field(default_factory=list)
    cron_months: list[int] = Field(default_factory=list)
    cron_weekdays: list[int] = Field(default_factory=list)
    interval: str = ""
    name: str = ""
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    uuid: OntapUUID = ""
