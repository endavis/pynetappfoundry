"""NFS service information — /protocols/nfs/services."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class NFSServiceInfo(CacheModel):
    """NFS service configuration per SVM."""

    svm: str = ""
    enabled: bool = False
    protocol_v3_enabled: bool = False
    protocol_v4_enabled: bool = False
    protocol_v41_enabled: bool = False
    showmount_enabled: bool = False
    vstorage_enabled: bool = False
