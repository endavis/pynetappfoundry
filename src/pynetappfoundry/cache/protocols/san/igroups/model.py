"""Igroup information — /protocols/san/igroups."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class IgroupInfo(CacheModel):
    """Initiator group information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    protocol: str = ""  # fcp, iscsi, mixed
    os_type: str = ""  # linux, windows, vmware, etc.
    initiators: list[str] = Field(default_factory=list)
    comment: str = ""
