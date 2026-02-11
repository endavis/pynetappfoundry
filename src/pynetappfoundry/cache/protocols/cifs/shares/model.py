"""CIFS share information — /protocols/cifs/shares."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class CIFSShareInfo(CacheModel):
    """CIFS/SMB share information."""

    name: str = ""
    path: str = ""
    svm: str = ""
    comment: str = ""
    home_directory: bool = False
    oplocks: bool = True
    access_based_enumeration: bool = False
    change_notify: bool = True
    encryption: bool = False
    unix_symlink: str = ""  # local, widelink, disable
