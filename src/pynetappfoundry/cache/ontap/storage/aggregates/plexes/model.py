"""OntapPlex information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapPlexRaidGroup(CacheModel):
    """OntapPlexRaidGroup sub-model for raid_groups."""

    raid_groups_cache_tier: bool = False
    raid_groups_degraded: bool = False
    raid_groups_disks: list[dict[str, Any]] = Field(default_factory=list)
    raid_groups_name: str = ""
    raid_groups_raid_type: str = ""
    raid_groups_recomputing_parity_active: bool = False
    raid_groups_recomputing_parity_percent: int = 0
    raid_groups_reconstruct_active: bool = False
    raid_groups_reconstruct_percent: int = 0


class OntapPlex(CacheModel):
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
