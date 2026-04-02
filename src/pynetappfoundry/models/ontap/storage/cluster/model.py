# ruff: noqa: E501
"""OntapClusterSpace information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterSpaceBlockStorageMediaEfficiency(OntapModel):
    """OntapClusterSpaceBlockStorageMediaEfficiency sub-model for efficiency."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshots(OntapModel):
    """OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshots sub-model for efficiency_without_snapshots."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshotsFlexclones(OntapModel):
    """OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshotsFlexclones sub-model for efficiency_without_snapshots_flexclones."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapClusterSpaceBlockStorageMedia(OntapModel):
    """OntapClusterSpaceBlockStorageMedia sub-model for medias."""

    available: int = 0
    efficiency: OntapClusterSpaceBlockStorageMediaEfficiency = Field(
        default_factory=OntapClusterSpaceBlockStorageMediaEfficiency
    )
    efficiency_without_snapshots: OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshots = (
        Field(default_factory=OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshots)
    )
    efficiency_without_snapshots_flexclones: OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshotsFlexclones = Field(
        default_factory=OntapClusterSpaceBlockStorageMediaEfficiencyWithoutSnapshotsFlexclones
    )
    physical_used: int = 0
    size: int = 0
    type_: str = ""
    used: int = 0


class OntapClusterSpaceBlockStorage(OntapModel):
    """OntapClusterSpaceBlockStorage sub-model for block_storage."""

    available: int = 0
    inactive_data: int = 0
    medias: list[OntapClusterSpaceBlockStorageMedia] = Field(default_factory=list)
    physical_used: int = 0
    size: int = 0
    used: int = 0


class OntapClusterSpaceCloudStorage(OntapModel):
    """OntapClusterSpaceCloudStorage sub-model for cloud_storage."""

    used: int = 0


class OntapClusterSpaceEfficiency(OntapModel):
    """OntapClusterSpaceEfficiency sub-model for efficiency."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapClusterSpaceEfficiencyWithoutSnapshots(OntapModel):
    """OntapClusterSpaceEfficiencyWithoutSnapshots sub-model for efficiency_without_snapshots."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapClusterSpaceEfficiencyWithoutSnapshotsFlexclones(OntapModel):
    """OntapClusterSpaceEfficiencyWithoutSnapshotsFlexclones sub-model for efficiency_without_snapshots_flexclones."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapClusterSpace(OntapModel):
    """OntapClusterSpace information."""

    block_storage: OntapClusterSpaceBlockStorage = Field(
        default_factory=OntapClusterSpaceBlockStorage
    )
    cloud_storage: OntapClusterSpaceCloudStorage = Field(
        default_factory=OntapClusterSpaceCloudStorage
    )
    efficiency: OntapClusterSpaceEfficiency = Field(default_factory=OntapClusterSpaceEfficiency)
    efficiency_without_snapshots: OntapClusterSpaceEfficiencyWithoutSnapshots = Field(
        default_factory=OntapClusterSpaceEfficiencyWithoutSnapshots
    )
    efficiency_without_snapshots_flexclones: OntapClusterSpaceEfficiencyWithoutSnapshotsFlexclones = Field(
        default_factory=OntapClusterSpaceEfficiencyWithoutSnapshotsFlexclones
    )
