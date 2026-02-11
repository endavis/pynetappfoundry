"""Snapshot policy information — /storage/snapshot-policies."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class SnapshotScheduleInfo(CacheModel):
    """Schedule entry within a snapshot policy."""

    schedule: str = ""
    count: int = 0
    prefix: str = ""
    snapmirror_label: str = ""


class SnapshotPolicyInfo(CacheModel):
    """Snapshot policy information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    enabled: bool = True
    scope: str = ""  # cluster, svm
    schedules: list[SnapshotScheduleInfo] = Field(default_factory=list)
