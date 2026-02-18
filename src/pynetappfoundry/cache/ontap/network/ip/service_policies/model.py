"""OntapIpServicePolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapIpServicePolicy(CacheModel):
    """OntapIpServicePolicy information."""

    ipspace_name: str = ""
    ipspace_uuid: str = ""
    is_built_in: bool = False
    name: str = ""
    scope: str = ""
    services: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
