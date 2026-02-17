"""OntapIgroupNested information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapIgroupNestedRecord(CacheModel):
    """OntapIgroupNestedRecord sub-model for records."""

    records_name: str = ""
    records_uuid: str = ""


class OntapIgroupNested(CacheModel):
    """OntapIgroupNested information."""

    igroup_uuid: str = ""
    name: str = ""
    records: list[OntapIgroupNestedRecord] = Field(default_factory=list)
    uuid: str = ""
