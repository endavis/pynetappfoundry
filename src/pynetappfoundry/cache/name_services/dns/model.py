"""DNS configuration — /name-services/dns."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class DNSInfo(CacheModel):
    """DNS configuration per SVM or cluster."""

    uuid: str = ""
    svm: str = ""
    scope: str = ""  # cluster, svm
    domains: list[str] = Field(default_factory=list)
    servers: list[str] = Field(default_factory=list)
    timeout: int = 0
    attempts: int = 0
