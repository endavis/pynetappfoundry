"""OntapClusterSpace information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterSpaceMedia(OntapModel):
    """OntapClusterSpaceMedia sub-model for medias."""

    available: int = 0
    efficiency_logical_used: int = 0
    efficiency_ratio: float = 0.0
    efficiency_savings: int = 0
    efficiency_without_snapshots_logical_used: int = 0
    efficiency_without_snapshots_ratio: float = 0.0
    efficiency_without_snapshots_savings: int = 0
    efficiency_without_snapshots_flexclones_logical_used: int = 0
    efficiency_without_snapshots_flexclones_ratio: float = 0.0
    efficiency_without_snapshots_flexclones_savings: int = 0
    physical_used: int = 0
    size: int = 0
    type: str = ""
    used: int = 0


class OntapClusterSpace(OntapModel):
    """OntapClusterSpace information."""

    block_storage_available: int = 0
    block_storage_inactive_data: int = 0
    block_storage_medias: list[OntapClusterSpaceMedia] = Field(default_factory=list)
    block_storage_physical_used: int = 0
    block_storage_size: int = 0
    block_storage_used: int = 0
    cloud_storage_used: int = 0
    efficiency_logical_used: int = 0
    efficiency_ratio: float = 0.0
    efficiency_savings: int = 0
    efficiency_without_snapshots_logical_used: int = 0
    efficiency_without_snapshots_ratio: float = 0.0
    efficiency_without_snapshots_savings: int = 0
    efficiency_without_snapshots_flexclones_logical_used: int = 0
    efficiency_without_snapshots_flexclones_ratio: float = 0.0
    efficiency_without_snapshots_flexclones_savings: int = 0
