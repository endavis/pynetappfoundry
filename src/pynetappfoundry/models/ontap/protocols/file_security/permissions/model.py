"""OntapFileDirectorySecurity information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFileDirectorySecurityAclAdvancedRights(OntapModel):
    """OntapFileDirectorySecurityAclAdvancedRights sub-model for advanced_rights."""

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


class OntapFileDirectorySecurityAclApplyTo(OntapModel):
    """OntapFileDirectorySecurityAclApplyTo sub-model for apply_to."""

    files: bool = False
    sub_folders: bool = False
    this_folder: bool = False


class OntapFileDirectorySecurityAcl(OntapModel):
    """OntapFileDirectorySecurityAcl sub-model for acls."""

    access: str = ""
    access_control: str = ""
    advanced_rights: OntapFileDirectorySecurityAclAdvancedRights = Field(
        default_factory=OntapFileDirectorySecurityAclAdvancedRights
    )
    apply_to: OntapFileDirectorySecurityAclApplyTo = Field(
        default_factory=OntapFileDirectorySecurityAclApplyTo
    )
    inherited: bool = False
    rights: str = ""
    user: str = ""


class OntapFileDirectorySecurity(OntapModel):
    """OntapFileDirectorySecurity information."""

    access_control: str = ""
    acls: list[OntapFileDirectorySecurityAcl] = Field(default_factory=list)
    control_flags: str = ""
    dos_attributes: str = ""
    effective_style: str = ""
    group: str = ""
    group_id: str = ""
    ignore_paths: list[str] = Field(default_factory=list)
    inode: int = 0
    mode_bits: int = 0
    owner: str = ""
    propagation_mode: str = ""
    security_style: str = ""
    text_dos_attr: str = ""
    text_mode_bits: str = ""
    user_id: str = ""
