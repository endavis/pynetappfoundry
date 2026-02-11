"""Job schedule information — /cluster/schedules."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class ScheduleInfo(CacheModel):
    """Job schedule information."""

    uuid: str = ""
    name: str = ""
    type: str = ""  # cron, interval
    scope: str = ""  # cluster, svm
    svm: str = ""
    cron: dict[str, list[int]] = Field(default_factory=dict)
    interval: str = ""
