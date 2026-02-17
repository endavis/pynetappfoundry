"""OntapFileDirectorySecurity information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapFileDirectorySecurity(CacheModel):
    """OntapFileDirectorySecurity information."""

    access: str = ""
    access_control: str = ""
    advanced_rights_append_data: bool = False
    advanced_rights_delete: bool = False
    advanced_rights_delete_child: bool = False
    advanced_rights_execute_file: bool = False
    advanced_rights_full_control: bool = False
    advanced_rights_read_attr: bool = False
    advanced_rights_read_data: bool = False
    advanced_rights_read_ea: bool = False
    advanced_rights_read_perm: bool = False
    advanced_rights_synchronize: bool = False
    advanced_rights_write_attr: bool = False
    advanced_rights_write_data: bool = False
    advanced_rights_write_ea: bool = False
    advanced_rights_write_owner: bool = False
    advanced_rights_write_perm: bool = False
    apply_to_files: bool = False
    apply_to_sub_folders: bool = False
    apply_to_this_folder: bool = False
    inherited: bool = False
    rights: str = ""
    user: str = ""
