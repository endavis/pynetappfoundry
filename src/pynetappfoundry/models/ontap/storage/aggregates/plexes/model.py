"""OntapPlex information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPlexAggregate(OntapModel):
    """OntapPlexAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapPlexRaidGroupDiskDisk(OntapModel):
    """OntapPlexRaidGroupDiskDisk sub-model for disk."""

    name: str = ""


class OntapPlexRaidGroupDisk(OntapModel):
    """OntapPlexRaidGroupDisk sub-model for disks."""

    disk: OntapPlexRaidGroupDiskDisk = Field(default_factory=OntapPlexRaidGroupDiskDisk)
    position: str = ""
    state: str = ""
    type_: str = ""
    usable_size: int = 0


class OntapPlexRaidGroupRecomputingParity(OntapModel):
    """OntapPlexRaidGroupRecomputingParity sub-model for recomputing_parity."""

    active: bool = False
    percent: int = 0


class OntapPlexRaidGroupReconstruct(OntapModel):
    """OntapPlexRaidGroupReconstruct sub-model for reconstruct."""

    active: bool = False
    percent: int = 0


class OntapPlexRaidGroup(OntapModel):
    """OntapPlexRaidGroup sub-model for raid_groups."""

    cache_tier: bool = False
    degraded: bool = False
    disks: list[OntapPlexRaidGroupDisk] = Field(default_factory=list)
    name: str = ""
    raid_type: str = ""
    recomputing_parity: OntapPlexRaidGroupRecomputingParity = Field(
        default_factory=OntapPlexRaidGroupRecomputingParity
    )
    reconstruct: OntapPlexRaidGroupReconstruct = Field(
        default_factory=OntapPlexRaidGroupReconstruct
    )


class OntapPlexResync(OntapModel):
    """OntapPlexResync sub-model for resync."""

    active: bool = False
    level: str = ""
    percent: int = 0


class OntapPlex(OntapModel):
    """OntapPlex information."""

    aggregate: OntapPlexAggregate = Field(default_factory=OntapPlexAggregate)
    name: str = ""
    online: bool = False
    pool: str = ""
    raid_groups: list[OntapPlexRaidGroup] = Field(default_factory=list)
    resync: OntapPlexResync = Field(default_factory=OntapPlexResync)
    state: str = ""
