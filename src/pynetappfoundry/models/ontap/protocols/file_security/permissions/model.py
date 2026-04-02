"""OntapFileDirectorySecurity information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFileDirectorySecurityAdvancedRights(OntapModel):
    """OntapFileDirectorySecurityAdvancedRights sub-model for advanced_rights."""

    append_data: bool = False
    delete: bool = False
    delete_child: bool = False
    execute_file: bool = False
    full_control: bool = False
    read_attr: bool = False
    read_data: bool = False
    read_ea: bool = False
    read_perm: bool = False
    synchronize: bool = False
    write_attr: bool = False
    write_data: bool = False
    write_ea: bool = False
    write_owner: bool = False
    write_perm: bool = False


class OntapFileDirectorySecurityApplyTo(OntapModel):
    """OntapFileDirectorySecurityApplyTo sub-model for apply_to."""

    files: bool = False
    sub_folders: bool = False
    this_folder: bool = False


class OntapFileDirectorySecurity(OntapModel):
    """OntapFileDirectorySecurity information."""

    access: str = ""
    access_control: str = ""
    advanced_rights: OntapFileDirectorySecurityAdvancedRights = Field(
        default_factory=OntapFileDirectorySecurityAdvancedRights
    )
    apply_to: OntapFileDirectorySecurityApplyTo = Field(
        default_factory=OntapFileDirectorySecurityApplyTo
    )
    inherited: bool = False
    rights: str = ""
    user: str = ""
