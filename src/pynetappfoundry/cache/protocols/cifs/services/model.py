"""CIFS service information — /protocols/cifs/services."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class CIFSServiceInfo(CacheModel):
    """CIFS/SMB service configuration per SVM."""

    svm: str = ""
    name: str = ""  # CIFS server name
    enabled: bool = False
    ad_domain: str = ""
    comment: str = ""
    default_unix_user: str = ""
    netbios_aliases: list[str] = Field(default_factory=list)
