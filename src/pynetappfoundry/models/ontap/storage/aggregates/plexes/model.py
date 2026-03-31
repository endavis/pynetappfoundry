"""OntapPlex information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPlexRaidGroup(OntapModel):
    """OntapPlexRaidGroup sub-model for raid_groups."""

    cache_tier: bool = False
    degraded: bool = False
    disks: list[dict[str, Any]] = Field(default_factory=list)
    name: str = ""
    raid_type: str = ""
    recomputing_parity_active: bool = False
    recomputing_parity_percent: int = 0
    reconstruct_active: bool = False
    reconstruct_percent: int = 0


class OntapPlex(OntapModel):
    """OntapPlex information."""

    aggregate_name: str = ""
    aggregate_uuid: str = ""
    name: str = ""
    online: bool = False
    pool: str = ""
    raid_groups: list[OntapPlexRaidGroup] = Field(default_factory=list)
    resync_active: bool = False
    resync_level: str = ""
    resync_percent: int = 0
    state: str = ""
