"""FlexCache information — /storage/flexcache/flexcaches."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class FlexCacheInfo(CacheModel):
    """FlexCache volume information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    path: str = ""
    size: int = 0  # bytes
    origins: list[str] = Field(default_factory=list)  # origin volume paths
    global_file_locking_enabled: bool = False
    dr_cache: bool = False
