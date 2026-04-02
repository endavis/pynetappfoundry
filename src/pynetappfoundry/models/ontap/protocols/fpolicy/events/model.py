"""OntapFpolicyEvent information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyEventFileOperations(OntapModel):
    """OntapFpolicyEventFileOperations sub-model for file_operations."""

    access: bool = False
    close: bool = False
    create: bool = False
    create_dir: bool = False
    delete: bool = False
    delete_dir: bool = False
    getattr: bool = False
    link: bool = False
    lookup: bool = False
    open: bool = False
    read: bool = False
    rename: bool = False
    rename_dir: bool = False
    setattr: bool = False
    symlink: bool = False
    write: bool = False


class OntapFpolicyEventFilters(OntapModel):
    """OntapFpolicyEventFilters sub-model for filters."""

    close_with_modification: bool = False
    close_with_read: bool = False
    close_without_modification: bool = False
    exclude_directory: bool = False
    first_read: bool = False
    first_write: bool = False
    monitor_ads: bool = False
    offline_bit: bool = False
    open_with_delete_intent: bool = False
    open_with_write_intent: bool = False
    setattr_with_access_time_change: bool = False
    setattr_with_allocation_size_change: bool = False
    setattr_with_creation_time_change: bool = False
    setattr_with_dacl_change: bool = False
    setattr_with_group_change: bool = False
    setattr_with_mode_change: bool = False
    setattr_with_modify_time_change: bool = False
    setattr_with_owner_change: bool = False
    setattr_with_sacl_change: bool = False
    setattr_with_size_change: bool = False
    write_with_size_change: bool = False


class OntapFpolicyEventSvm(OntapModel):
    """OntapFpolicyEventSvm sub-model for svm."""

    uuid: str = ""


class OntapFpolicyEvent(OntapModel):
    """OntapFpolicyEvent information."""

    file_operations: OntapFpolicyEventFileOperations = Field(
        default_factory=OntapFpolicyEventFileOperations
    )
    filters: OntapFpolicyEventFilters = Field(default_factory=OntapFpolicyEventFilters)
    monitor_fileop_failure: bool = False
    name: str = ""
    protocol: str = ""
    svm: OntapFpolicyEventSvm = Field(default_factory=OntapFpolicyEventSvm)
    volume_monitoring: bool = False
