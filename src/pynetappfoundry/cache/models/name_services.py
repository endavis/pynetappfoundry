"""Name services models (/name-services API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DNSInfo(BaseModel):
    """DNS configuration per SVM or cluster."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    svm: str = ""
    scope: str = ""  # cluster, svm
    domains: list[str] = Field(default_factory=list)
    servers: list[str] = Field(default_factory=list)
    timeout: int = 0
    attempts: int = 0
