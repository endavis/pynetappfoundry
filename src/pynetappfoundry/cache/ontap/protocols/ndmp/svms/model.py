"""OntapNdmpSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNdmpSvm(CacheModel):
    """OntapNdmpSvm information."""

    authentication_types: list[str] = Field(default_factory=list)
    enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
