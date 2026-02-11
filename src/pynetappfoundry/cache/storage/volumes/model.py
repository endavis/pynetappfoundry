"""Volume information — /storage/volumes."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class VolumeInfo(CacheModel):
    """Volume information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    state: str = ""  # online, offline, restricted
    type: str = ""  # rw, dp, ls
    style: str = ""  # flexvol, flexgroup
    size: int = 0  # bytes
    autosize_mode: str = ""  # off, grow, grow_shrink
    autosize_grow_threshold: int = 0  # percentage
    autosize_shrink_threshold: int = 0  # percentage
    autosize_maximum: int = 0  # bytes
    autosize_minimum: int = 0  # bytes
    files_maximum: int = 0
    tiering_policy: str = ""  # none, snapshot-only, auto, all
    tiering_minimum_cooling_days: int = 0
    aggregate: str = ""  # FlexVol aggregate name
    aggregates: list[str] = Field(default_factory=list)  # FlexGroup aggregates
    snapshot_policy: str = ""
    export_policy: str = ""
    junction_path: str = ""
    nas_security_style: str = ""  # unix, ntfs, mixed
