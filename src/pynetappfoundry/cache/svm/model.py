"""SVM information — /svm/svms."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class SVMInfo(CacheModel):
    """Storage Virtual Machine information."""

    uuid: str = ""
    name: str = ""
    state: str = ""
    subtype: str = ""  # default, dp_destination, sync_source
    root_volume: str = ""
    root_volume_aggregate: str = ""
    allowed_protocols: list[str] = Field(default_factory=list)
    language: str = ""
