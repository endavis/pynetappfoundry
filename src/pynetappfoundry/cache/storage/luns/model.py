"""LUN information — /storage/luns."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class LunInfo(CacheModel):
    """LUN (Logical Unit Number) information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    volume: str = ""
    size: int = 0  # bytes
    os_type: str = ""  # linux, windows, vmware, etc.
    serial_number: str = ""
    enabled: bool = True
    comment: str = ""
    qos_policy: str = ""
    create_time: str = ""
