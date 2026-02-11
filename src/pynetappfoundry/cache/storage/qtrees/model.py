"""Qtree information — /storage/qtrees."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class QtreeInfo(CacheModel):
    """Qtree information."""

    id: int = 0
    name: str = ""
    svm: str = ""
    volume: str = ""
    path: str = ""
    security_style: str = ""  # unix, ntfs, mixed
    unix_permissions: str = ""
    export_policy: str = ""
