"""Export policy information — /protocols/nfs/export-policies."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class ExportRuleInfo(CacheModel):
    """Export rule within an export policy."""

    index: int = 0
    clients: list[str] = Field(default_factory=list)
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)
    anonymous_user: str = ""


class ExportPolicyInfo(CacheModel):
    """NFS export policy information."""

    id: int = 0
    name: str = ""
    svm: str = ""
    rules: list[ExportRuleInfo] = Field(default_factory=list)
