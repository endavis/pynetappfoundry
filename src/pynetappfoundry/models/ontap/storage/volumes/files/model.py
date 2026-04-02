"""OntapFileInfo information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFileInfoAnalyticsByAccessedTimeBytesUsed(OntapModel):
    """OntapFileInfoAnalyticsByAccessedTimeBytesUsed sub-model for bytes_used."""

    labels: list[str] = Field(default_factory=list)
    newest_label: str = ""
    percentages: list[float] = Field(default_factory=list)
    values: list[int] = Field(default_factory=list)


class OntapFileInfoAnalyticsByAccessedTime(OntapModel):
    """OntapFileInfoAnalyticsByAccessedTime sub-model for by_accessed_time."""

    bytes_used: OntapFileInfoAnalyticsByAccessedTimeBytesUsed = Field(
        default_factory=OntapFileInfoAnalyticsByAccessedTimeBytesUsed
    )


class OntapFileInfoAnalyticsByModifiedTimeBytesUsed(OntapModel):
    """OntapFileInfoAnalyticsByModifiedTimeBytesUsed sub-model for bytes_used."""

    labels: list[str] = Field(default_factory=list)
    newest_label: str = ""
    percentages: list[float] = Field(default_factory=list)
    values: list[int] = Field(default_factory=list)


class OntapFileInfoAnalyticsByModifiedTime(OntapModel):
    """OntapFileInfoAnalyticsByModifiedTime sub-model for by_modified_time."""

    bytes_used: OntapFileInfoAnalyticsByModifiedTimeBytesUsed = Field(
        default_factory=OntapFileInfoAnalyticsByModifiedTimeBytesUsed
    )


class OntapFileInfoAnalytics(OntapModel):
    """OntapFileInfoAnalytics sub-model for analytics."""

    by_accessed_time: OntapFileInfoAnalyticsByAccessedTime = Field(
        default_factory=OntapFileInfoAnalyticsByAccessedTime
    )
    by_modified_time: OntapFileInfoAnalyticsByModifiedTime = Field(
        default_factory=OntapFileInfoAnalyticsByModifiedTime
    )
    bytes_used: int = 0
    file_count: int = 0
    incomplete_data: bool = False
    subdir_count: int = 0


class OntapFileInfoConstituent(OntapModel):
    """OntapFileInfoConstituent sub-model for constituent."""

    name: str = ""
    uuid: str = ""


class OntapFileInfoQosPolicy(OntapModel):
    """OntapFileInfoQosPolicy sub-model for qos_policy."""

    name: str = ""
    uuid: str = ""


class OntapFileInfoVolume(OntapModel):
    """OntapFileInfoVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileInfo(OntapModel):
    """OntapFileInfo information."""

    accessed_time: str = ""
    analytics: OntapFileInfoAnalytics = Field(default_factory=OntapFileInfoAnalytics)
    bytes_used: int = 0
    changed_time: str = ""
    constituent: OntapFileInfoConstituent = Field(default_factory=OntapFileInfoConstituent)
    creation_time: str = ""
    fill_enabled: bool = False
    group_id: int = 0
    hard_links_count: int = 0
    inode_generation: int = 0
    inode_number: int = 0
    is_empty: bool = False
    is_junction: bool = False
    is_snapshot: bool = False
    is_vm_aligned: bool = False
    modified_time: str = ""
    name: str = ""
    overwrite_enabled: bool = False
    owner_id: int = 0
    path: str = ""
    qos_policy: OntapFileInfoQosPolicy = Field(default_factory=OntapFileInfoQosPolicy)
    size: int = 0
    target: str = ""
    type_: str = ""
    unique_bytes: int = 0
    unix_permissions: int = 0
    volume: OntapFileInfoVolume = Field(default_factory=OntapFileInfoVolume)
