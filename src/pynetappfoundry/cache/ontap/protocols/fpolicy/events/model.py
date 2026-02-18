"""OntapFpolicyEvent information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapFpolicyEvent(CacheModel):
    """OntapFpolicyEvent information."""

    file_operations_access: bool = False
    file_operations_close: bool = False
    file_operations_create: bool = False
    file_operations_create_dir: bool = False
    file_operations_delete: bool = False
    file_operations_delete_dir: bool = False
    file_operations_getattr: bool = False
    file_operations_link: bool = False
    file_operations_lookup: bool = False
    file_operations_open: bool = False
    file_operations_read: bool = False
    file_operations_rename: bool = False
    file_operations_rename_dir: bool = False
    file_operations_setattr: bool = False
    file_operations_symlink: bool = False
    file_operations_write: bool = False
    filters_close_with_modification: bool = False
    filters_close_with_read: bool = False
    filters_close_without_modification: bool = False
    filters_exclude_directory: bool = False
    filters_first_read: bool = False
    filters_first_write: bool = False
    filters_monitor_ads: bool = False
    filters_offline_bit: bool = False
    filters_open_with_delete_intent: bool = False
    filters_open_with_write_intent: bool = False
    filters_setattr_with_access_time_change: bool = False
    filters_setattr_with_allocation_size_change: bool = False
    filters_setattr_with_creation_time_change: bool = False
    filters_setattr_with_dacl_change: bool = False
    filters_setattr_with_group_change: bool = False
    filters_setattr_with_mode_change: bool = False
    filters_setattr_with_modify_time_change: bool = False
    filters_setattr_with_owner_change: bool = False
    filters_setattr_with_sacl_change: bool = False
    filters_setattr_with_size_change: bool = False
    filters_write_with_size_change: bool = False
    monitor_fileop_failure: bool = False
    name: str = ""
    protocol: str = ""
    svm_uuid: str = ""
    volume_monitoring: bool = False
