"""OntapIgroupNested information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIgroupNestedIgroup(OntapModel):
    """OntapIgroupNestedIgroup sub-model for igroup."""

    uuid: str = ""


class OntapIgroupNestedRecord(OntapModel):
    """OntapIgroupNestedRecord sub-model for records."""

    name: str = ""
    uuid: str = ""


class OntapIgroupNested(OntapModel):
    """OntapIgroupNested information."""

    igroup: OntapIgroupNestedIgroup = Field(default_factory=OntapIgroupNestedIgroup)
    name: str = ""
    records: list[OntapIgroupNestedRecord] = Field(default_factory=list)
    uuid: str = ""
