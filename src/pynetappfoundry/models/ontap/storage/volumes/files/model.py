"""OntapFileInfo information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFileInfo(OntapModel):
    """OntapFileInfo information."""

    accessed_time: str = ""
    analytics_by_accessed_time_bytes_used_labels: list[str] = Field(default_factory=list)
    analytics_by_accessed_time_bytes_used_newest_label: str = ""
    analytics_by_accessed_time_bytes_used_percentages: list[float] = Field(default_factory=list)
    analytics_by_accessed_time_bytes_used_values: list[int] = Field(default_factory=list)
    analytics_by_modified_time_bytes_used_labels: list[str] = Field(default_factory=list)
    analytics_by_modified_time_bytes_used_newest_label: str = ""
    analytics_by_modified_time_bytes_used_percentages: list[float] = Field(default_factory=list)
    analytics_by_modified_time_bytes_used_values: list[int] = Field(default_factory=list)
    analytics_bytes_used: int = 0
    analytics_file_count: int = 0
    analytics_incomplete_data: bool = False
    analytics_subdir_count: int = 0
    bytes_used: int = 0
    changed_time: str = ""
    constituent_name: str = ""
    constituent_uuid: str = ""
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
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    size: int = 0
    target: str = ""
    type_: str = ""
    unique_bytes: int = 0
    unix_permissions: int = 0
    volume_name: str = ""
    volume_uuid: str = ""
